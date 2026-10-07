/* Courtyard roof — visual render built from the Rev C09 drawings (all dimensions in metres).
   Model axes as the drawings: x along the annex (annex 0..8, end facade with the door at x = 8),
   y across (low white wall inner face y = -0.75, annex y 0..2.54, passage to 3.44, tall wall face 3.44),
   z up.  three.js mapping: (x, y, z) -> (x, z, -y).
   URL params: v = V1 | V2 | V1T | V2T,  view = eye | aerial | under,  w, h = image size. */
(function () {
  const Q = new URLSearchParams(location.search);
  const VER = Q.get('v') || 'V1';
  const VIEW = Q.get('view') || 'eye';
  const W = +(Q.get('w') || 1800), H = +(Q.get('h') || 1200);

  // ------------------------------------------------------------------ geometry (from the drawings, m)
  const HOUSE_L = 8.0, HOUSE_W = 2.54, HOUSE_TOP = 2.92, STRIP = 0.9, WALL_Y0 = HOUSE_W + STRIP;  // 3.44
  const TW_T = 0.25, TW_H = 5.6;
  const ENTR = [0.25, 2.29], HEAD = 2.2, SLIDES = [[1.23, 2.29, 0], [1.17, 2.23, 1]];
  const LATTICE = [HOUSE_W + 0.05, WALL_Y0 - 0.05];
  const KERB = [0.10, 0.25], KERB_H = 0.25, WI = -0.75, LW = [-0.95, -0.75], LW_H = 1.40;
  const GX0 = HOUSE_L + 1.00;                                   // planter starts after the 1.00 paved entry space ...
  const ROOF_L = 3.22, TRI = 1.26, RX0 = HOUSE_L, RX1 = HOUSE_L + ROOF_L, TIP = RX1 + TRI;
  const SOFFIT = 2.36, FASCIA = 0.43, FTOP = SOFFIT + FASCIA, COL_TOP = FTOP + 0.13;
  const XE_ALL = TIP;
  const EDGE = WI;                                              // roof plants edge at the low wall
  const GX1 = XE_ALL + 7;                                       // ... and CONTINUES along the low wall (client)
  const tri = VER.endsWith('T');
  const RD = VER.startsWith('V1') ? WALL_Y0 : HOUSE_W;          // roof back edge
  const rods = VER.startsWith('V2');
  const XE = tri ? TIP : RX1;
  const CY = WI + 0.10;
  const COLS = tri ? [RX0 + (ROOF_L + TRI) / 2, TIP - 0.60] : [RX0 + ROOF_L / 2, RX1 - 0.10];
  const roofPoly = [[RX0, EDGE], [XE, EDGE], [RX1, RD], [RX0, RD]];

  // ------------------------------------------------------------------ renderer / scene
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(W, H);
  renderer.setPixelRatio(1);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  document.body.appendChild(renderer.domElement);
  const scene = new THREE.Scene();

  // sky dome (vertex gradient)
  {
    const g = new THREE.SphereGeometry(400, 32, 16);
    const cols = [];
    const top = new THREE.Color('#5d8fd6'), hor = new THREE.Color('#dbe8f3');
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const t = Math.max(0, Math.min(1, p.getY(i) / 400));
      const c = hor.clone().lerp(top, Math.pow(t, 0.55));
      cols.push(c.r, c.g, c.b);
    }
    g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    scene.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false })));
  }
  scene.fog = new THREE.Fog('#dfe9f2', 45, 160);

  // lights: Athens afternoon sun from the south-west, soft sky
  scene.add(new THREE.HemisphereLight('#dcebff', '#b9a68c', 0.45));
  const sun = new THREE.DirectionalLight('#fff1d6', 2.9);
  sun.position.set(22, 17, -10);
  sun.target.position.set(9, 0, -1);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  Object.assign(sun.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16, near: 1, far: 80 });
  sun.shadow.bias = -0.0006;
  sun.shadow.normalBias = 0.035;
  scene.add(sun, sun.target);
  scene.add(new THREE.AmbientLight('#ffffff', 0.12));

  // ------------------------------------------------------------------ textures (procedural canvases)
  function rnd(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
  function canvasTex(w, h, draw, rep) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    draw(c.getContext('2d'), w, h);
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.encoding = THREE.sRGBEncoding;
    t.anisotropy = 8;
    if (rep) t.repeat.set(rep[0], rep[1]);
    return t;
  }
  const paveTex = canvasTex(1024, 1024, (g, w, h) => {
    const r = rnd(7), cols = ['#d9cdb8', '#cbb79a', '#bfb2a2', '#a99f95', '#d8c3ad', '#c7a98c', '#b9a58f', '#9d958e'];
    g.fillStyle = '#8f8576'; g.fillRect(0, 0, w, h);
    const n = 8, s = w / n;
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      g.fillStyle = cols[Math.floor(r() * cols.length)];
      g.fillRect(i * s + 3, j * s + 3, s - 6, s - 6);
      for (let k = 0; k < 30; k++) {           // stone speckle
        g.fillStyle = `rgba(${80 + r() * 60},${70 + r() * 50},${60 + r() * 40},${0.08 + r() * 0.1})`;
        g.fillRect(i * s + r() * s, j * s + r() * s, 4 + r() * 10, 2 + r() * 6);
      }
    }
  });
  const brickTex = canvasTex(512, 512, (g, w, h) => {
    const r = rnd(3);
    g.fillStyle = '#d8cbbd'; g.fillRect(0, 0, w, h);
    const bh = 16, bw = 48;
    for (let y = 0, row = 0; y < h; y += bh, row++) for (let x = -(row % 2) * bw / 2; x < w; x += bw) {
      const v = 0.8 + r() * 0.35;
      g.fillStyle = `rgb(${Math.min(255, 168 * v)},${Math.min(255, 78 * v)},${Math.min(255, 58 * v)})`;
      g.fillRect(x + 2, y + 2, bw - 4, bh - 4);
    }
  });
  const woodTex = canvasTex(256, 512, (g, w, h) => {
    const r = rnd(11);
    g.fillStyle = '#a8743f'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 90; i++) {
      g.strokeStyle = `rgba(${90 + r() * 40},${50 + r() * 25},${20 + r() * 15},${0.25 + r() * 0.3})`;
      g.lineWidth = 1 + r() * 2.5; const x = r() * w;
      g.beginPath(); g.moveTo(x, 0); g.bezierCurveTo(x + r() * 10 - 5, h / 3, x + r() * 10 - 5, 2 * h / 3, x + r() * 6 - 3, h); g.stroke();
    }
  });
  const renderTex = canvasTex(256, 256, (g, w, h) => {
    const r = rnd(5);
    g.fillStyle = '#f1eee8'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 2500; i++) { g.fillStyle = `rgba(0,0,0,${r() * 0.05})`; g.fillRect(r() * w, r() * h, 2, 2); }
  });
  const soilTex = canvasTex(256, 256, (g, w, h) => {
    const r = rnd(9);
    g.fillStyle = '#5e4632'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 1800; i++) { g.fillStyle = `rgba(${40 + r() * 70},${30 + r() * 50},${20 + r() * 30},0.6)`; g.fillRect(r() * w, r() * h, 2 + r() * 4, 2 + r() * 3); }
  });

  // ------------------------------------------------------------------ materials
  const M = {
    white: new THREE.MeshStandardMaterial({ color: '#f3f0ea', map: renderTex, roughness: 0.92 }),
    whiteSmooth: new THREE.MeshStandardMaterial({ color: '#fbfbfa', roughness: 0.35, metalness: 0.05 }),
    kerb: new THREE.MeshStandardMaterial({ color: '#ebe6dc', roughness: 0.8 }),
    pave: new THREE.MeshStandardMaterial({ map: paveTex, roughness: 0.85 }),
    brick: new THREE.MeshStandardMaterial({ map: brickTex, roughness: 0.9 }),
    wood: new THREE.MeshStandardMaterial({ map: woodTex, roughness: 0.7 }),
    woodDark: new THREE.MeshStandardMaterial({ color: '#8c5a2e', map: woodTex, roughness: 0.7 }),
    soffit: new THREE.MeshStandardMaterial({ color: '#c99766', map: woodTex, roughness: 0.65 }),
    slider: new THREE.MeshStandardMaterial({ color: '#5b4231', roughness: 0.55, metalness: 0.2 }),
    sliderDark: new THREE.MeshStandardMaterial({ color: '#3f2e22', roughness: 0.6, metalness: 0.2 }),
    frame: new THREE.MeshStandardMaterial({ color: '#d9dadb', roughness: 0.4, metalness: 0.6 }),
    glass: new THREE.MeshStandardMaterial({ color: '#6f8794', roughness: 0.05, metalness: 0.6, transparent: true, opacity: 0.55 }),
    dark: new THREE.MeshStandardMaterial({ color: '#1d2125', roughness: 0.9 }),
    soil: new THREE.MeshStandardMaterial({ map: soilTex, roughness: 1 }),
    roofTop: new THREE.MeshStandardMaterial({ color: '#c9cdd0', roughness: 0.8 }),
    steel: new THREE.MeshStandardMaterial({ color: '#f2f2f0', roughness: 0.35, metalness: 0.3 }),
    ss: new THREE.MeshStandardMaterial({ color: '#c7ccd1', roughness: 0.25, metalness: 0.9 }),
    ac: new THREE.MeshStandardMaterial({ color: '#f4f4f2', roughness: 0.5 }),
    solar: new THREE.MeshStandardMaterial({ color: '#1f3346', roughness: 0.25, metalness: 0.5 }),
    tank: new THREE.MeshStandardMaterial({ color: '#d7dadc', roughness: 0.25, metalness: 0.85 }),
    ground: new THREE.MeshStandardMaterial({ color: '#5f6b3e', roughness: 1 }),
  };

  // ------------------------------------------------------------------ helpers
  function add(mesh, cast = true, recv = true) { mesh.castShadow = cast; mesh.receiveShadow = recv; scene.add(mesh); return mesh; }
  function box(x0, x1, y0, y1, z0, z1, mat, uvScale) {
    const g = new THREE.BoxGeometry(x1 - x0, z1 - z0, y1 - y0);
    if (uvScale) {                                  // world-scaled UVs for tiled textures
      const uv = g.attributes.uv, n = g.attributes.normal, p = g.attributes.position;
      for (let i = 0; i < uv.count; i++) {
        const nx = Math.abs(n.getX(i)), ny = Math.abs(n.getY(i));
        const X = p.getX(i) + (x0 + x1) / 2, Y = p.getY(i) + (z0 + z1) / 2, Z = p.getZ(i) - (y0 + y1) / 2;
        if (ny > 0.5) uv.setXY(i, X / uvScale, Z / uvScale);
        else if (nx > 0.5) uv.setXY(i, Z / uvScale, Y / uvScale);
        else uv.setXY(i, X / uvScale, Y / uvScale);
      }
    }
    const m = new THREE.Mesh(g, mat);
    m.position.set((x0 + x1) / 2, (z0 + z1) / 2, -(y0 + y1) / 2);
    return add(m);
  }
  function prism(pts, z0, z1, mat) {               // horizontal polygon (model x,y) extruded z0..z1
    const sh = new THREE.Shape(pts.map(([x, y]) => new THREE.Vector2(x, y)));
    const g = new THREE.ExtrudeGeometry(sh, { depth: z1 - z0, bevelEnabled: false });
    const m = new THREE.Mesh(g, mat);
    m.rotation.x = -Math.PI / 2; m.position.y = z0;
    return add(m);
  }
  function plate(a, b, z0, z1, t, mat) {          // vertical plate along segment a->b (model plan), thickness t
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy);
    const g = new THREE.BoxGeometry(L, z1 - z0, t);
    const m = new THREE.Mesh(g, mat);
    m.position.set((a[0] + b[0]) / 2, (z0 + z1) / 2, -(a[1] + b[1]) / 2);
    m.rotation.y = Math.atan2(dy, dx);
    return add(m);
  }
  function cyl(a, b, r, mat) {                    // cylinder between model points a, b
    const A = new THREE.Vector3(a[0], a[2], -a[1]), B = new THREE.Vector3(b[0], b[2], -b[1]);
    const L = A.distanceTo(B);
    const g = new THREE.CylinderGeometry(r, r, L, 12);
    const m = new THREE.Mesh(g, mat);
    m.position.copy(A.clone().add(B).multiplyScalar(0.5));
    m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize());
    return add(m);
  }
  function bracket(xf, y, sgn, r = 0.2) {         // curved steel bracket under the column/roof junction
    const sh = new THREE.Shape();
    sh.moveTo(0, 0); sh.lineTo(sgn * r, 0);
    for (let k = 0; k <= 12; k++) {
      const a = Math.PI / 2 * k / 12;
      sh.lineTo(sgn * (r - r * Math.sin(a)), -r + r * Math.cos(a));
    }
    sh.lineTo(0, 0);
    const g = new THREE.ExtrudeGeometry(sh, { depth: 0.012, bevelEnabled: false });
    const m = new THREE.Mesh(g, M.steel);
    m.position.set(xf, SOFFIT, -(y + 0.006));
    return add(m);
  }
  function foliage(x, y, z, r, seed, cols, flowers, squash = 1) {
    const R = rnd(Math.floor(seed * 7919) + 13), grp = new THREE.Group();
    const core = new THREE.Mesh(new THREE.SphereGeometry(r * 0.72, 16, 12),
      new THREE.MeshStandardMaterial({ color: new THREE.Color(cols[0]).multiplyScalar(0.38), roughness: 1 }));
    core.scale.set(1, squash, 1); core.position.set(x, z, -y); core.castShadow = true; core.receiveShadow = true;
    grp.add(core);
    const n = Math.max(160, Math.min(3600, Math.round(r * r * 900)));
    const lr = Math.max(0.03, Math.min(0.26, r * 0.075));
    const geo = new THREE.IcosahedronGeometry(lr, 0);
    const mat = new THREE.MeshStandardMaterial({ roughness: 0.85, flatShading: true });
    const im = new THREE.InstancedMesh(geo, mat, n);
    const d = new THREE.Object3D(), c = new THREE.Color();
    for (let i = 0; i < n; i++) {
      const th = R() * Math.PI * 2, u = 2 * R() - 1, s2 = Math.sqrt(1 - u * u);
      const rr = r * (0.62 + 0.42 * Math.sqrt(R()));
      const dz = u * rr * squash;
      d.position.set(x + rr * s2 * Math.cos(th), z + dz, -(y + rr * s2 * Math.sin(th)));
      d.rotation.set(R() * 6, R() * 6, R() * 6);
      const sc = 0.7 + R() * 0.7; d.scale.set(sc, sc * (0.6 + R() * 0.5), sc);
      d.updateMatrix(); im.setMatrixAt(i, d.matrix);
      c.set(cols[Math.floor(R() * cols.length)]);
      const lit = 0.85 + 0.35 * ((u + 1) / 2) + (R() - 0.5) * 0.15;          // lighter on top
      c.multiplyScalar(lit); im.setColorAt(i, c);
    }
    im.castShadow = true; im.receiveShadow = true;
    grp.add(im);
    if (flowers) {
      const fg = new THREE.SphereGeometry(0.032, 6, 5);
      const fm = new THREE.MeshStandardMaterial({ roughness: 0.6 });
      const fi = new THREE.InstancedMesh(fg, fm, flowers);
      for (let i = 0; i < flowers; i++) {
        const th = R() * Math.PI * 2, u = 0.2 + 0.8 * R(), s2 = Math.sqrt(1 - u * u), rr = r * (0.98 + R() * 0.1);
        d.position.set(x + rr * s2 * Math.cos(th), z + u * rr * squash, -(y + rr * s2 * Math.sin(th)));
        d.rotation.set(0, 0, 0); const sc = 0.8 + R() * 0.8; d.scale.set(sc, sc, sc);
        d.updateMatrix(); fi.setMatrixAt(i, d.matrix);
        c.set(['#ff8a3d', '#f25c8a', '#ffd23f', '#ff6f61', '#fbe7ef', '#e8508a'][Math.floor(R() * 6)]);
        fi.setColorAt(i, c);
      }
      grp.add(fi);
    }
    scene.add(grp);
    return grp;
  }
  function trunk(x, y, z0, z1, r) { cyl([x, y, z0], [x, y, z1], r, new THREE.MeshStandardMaterial({ color: '#7a6a58', roughness: 1 })); }
  function pine(x, y, h, seed) {
    trunk(x, y, -0.5, h * 0.55, 0.18);
    foliage(x, y, h * 0.72, h * 0.32, seed, ['#3e6b3a', '#4f7d45', '#365f33', '#5c8a4c'], 0, 0.75);
  }
  function eucalyptus(x, y, h, seed) {
    trunk(x, y, -0.5, h * 0.7, 0.22);
    foliage(x, y, h * 0.78, h * 0.3, seed, ['#8fa978', '#a3b98c', '#7f9a6c', '#b4c59c'], 0, 0.8);
  }
  function cypress(x, y, h, seed) {
    trunk(x, y, -0.5, h * 0.3, 0.12);
    const R = rnd(seed);
    for (let i = 0; i < 9; i++) foliage(x, y, h * (0.2 + 0.09 * i), h * 0.09 * (1.25 - i * 0.09), seed + i, ['#2f5a33', '#3a6a3c', '#27502c'], 0, 1.4);
  }

  // ------------------------------------------------------------------ site
  // ground outside (lower, beyond the low wall) + courtyard paving
  box(-30, 40, -40, 40, -0.62, -0.5, M.ground);
  box(HOUSE_L - 6, GX1, KERB[1], WALL_Y0, -0.12, 0.0, M.pave, 3.2);                   // courtyard paving
  box(HOUSE_L, GX0, WI, KERB[1], -0.12, 0.0, M.pave, 3.2);                           // paved entry space
  box(HOUSE_L - 6, HOUSE_L, -0.95, 0, -0.5, 0.0, M.ground);
  // tall house wall (brick) + AC units
  box(HOUSE_L - 9, GX1, WALL_Y0, WALL_Y0 + TW_T, -0.5, TW_H, M.brick, 1.6);
  box(HOUSE_L - 9, GX1, WALL_Y0 - 0.02, WALL_Y0 + TW_T + 0.02, TW_H, TW_H + 0.08, M.white);
  box(HOUSE_L - 0.9, HOUSE_L - 0.1, WALL_Y0 - 0.30, WALL_Y0, 3.25, 3.85, M.ac);
  box(HOUSE_L + 0.4, HOUSE_L + 1.2, WALL_Y0 - 0.30, WALL_Y0, 3.55, 4.15, M.ac);
  // annex (white render) + parapet + entrance
  box(0, HOUSE_L, 0, HOUSE_W, -0.12, HOUSE_TOP, M.white, 1.5);
  box(-0.03, HOUSE_L + 0.03, -0.03, HOUSE_W + 0.03, HOUSE_TOP, HOUSE_TOP + 0.06, M.kerb);
  box(HOUSE_L, HOUSE_L + 0.004, ENTR[0], ENTR[1], 0, HEAD, M.dark);                    // opening (interior dark)
  box(HOUSE_L + 0.004, HOUSE_L + 0.03, ENTR[0] + 0.04, ENTR[0] + 0.94, 0.02, HEAD - 0.04, M.glass);   // glass door (left, open part)
  box(HOUSE_L + 0.004, HOUSE_L + 0.04, ENTR[0], ENTR[0] + 0.04, 0, HEAD, M.frame);
  box(HOUSE_L + 0.004, HOUSE_L + 0.04, ENTR[0] + 0.92, ENTR[0] + 0.96, 0, HEAD, M.frame);
  box(HOUSE_L - 0.02, HOUSE_L + 0.12, ENTR[0] - 0.04, ENTR[1] + 0.04, HEAD, HEAD + 0.05, M.frame);   // top track
  for (const [a, b, tr] of SLIDES) {                                                  // brown louvred sliders
    const x0 = HOUSE_L + 0.01 + tr * 0.045;
    box(x0, x0 + 0.035, a, b, 0.01, HEAD - 0.005, tr ? M.slider : M.sliderDark);
    if (tr) for (let z = 0.12; z < HEAD - 0.06; z += 0.065) box(x0 + 0.035, x0 + 0.05, a + 0.04, b - 0.04, z, z + 0.035, M.sliderDark);
  }
  // annex roof: AC unit + solar water heater (as photo)
  box(HOUSE_L - 1.2, HOUSE_L - 0.4, 0.25, 0.55, HOUSE_TOP + 0.06, HOUSE_TOP + 0.66, M.ac);
  {
    const p = box(HOUSE_L - 2.4, HOUSE_L - 1.0, 1.1, 2.3, 0, 0.04, M.solar);
    p.position.set(HOUSE_L - 1.7, HOUSE_TOP + 0.75, -1.7); p.rotation.x = 0; p.rotation.z = -0.9;
    cyl([HOUSE_L - 2.4, 1.1, HOUSE_TOP + 1.55], [HOUSE_L - 2.4, 2.3, HOUSE_TOP + 1.55], 0.25, M.tank);
  }
  // passage + lattice door
  box(HOUSE_L - 0.12, HOUSE_L - 0.06, LATTICE[0], LATTICE[1], 0, HEAD, M.woodDark);

  // ------------------------------------------------------------------ garden: kerb -> 1.00 planter -> low white wall
  box(RX0 - 0.2, GX1, LW[0], LW[1], -0.5, LW_H, M.white, 1.2);                        // low white wall
  box(HOUSE_L - 0.2, HOUSE_L, LW[0], 0, -0.5, LW_H, M.white, 1.2);                     // return to the annex corner
  cyl([RX0 - 0.2, -0.85, LW_H], [GX1, -0.85, LW_H], 0.1, M.white);                     // rounded coping
  box(GX0, GX1, WI, KERB[0], -0.12, KERB_H - 0.03, M.soil);
  box(GX0, GX1, KERB[0], KERB[1], -0.12, KERB_H, M.kerb);
  box(GX0, GX0 + 0.15, WI, KERB[1], -0.12, KERB_H, M.kerb);
  {
    const R = rnd(21);
    for (let x = GX0 + 0.35; x < GX1 - 0.25; x += 0.45 + R() * 0.25) {
      const kind = R();
      if (kind < 0.45) foliage(x, -0.35 + R() * 0.25, KERB_H + 0.45 + R() * 0.3, 0.42 + R() * 0.2, 100 + x * 10, ['#4c7a3a', '#5d8b43', '#3f6b32', '#6e9a4e'], 28, 0.9);   // lantana
      else if (kind < 0.75) foliage(x, -0.45 + R() * 0.2, KERB_H + 0.9 + R() * 0.6, 0.5 + R() * 0.2, 200 + x * 10, ['#4a7b3f', '#3b6a35', '#5b8c47'], 0, 1.1);          // shrub
      else foliage(x, -0.3, KERB_H + 0.6 + R() * 0.3, 0.38, 300 + x * 10, ['#8fb55a', '#a3c464', '#7aa64d'], 0, 1.2);                                               // ficus
    }
    foliage(GX0 + 0.5, -0.5, 2.0, 0.75, 77, ['#4f8240', '#3e6e35', '#5f9149'], 6, 1.0);         // bougainvillea by the door
  }

  // ------------------------------------------------------------------ the new roof
  prism(roofPoly, SOFFIT + 0.02, FTOP - 0.04, M.roofTop);
  // fascia 0.43 on the free edges (white aluminium)
  plate([RX0, EDGE], [XE, EDGE], SOFFIT, FTOP, 0.03, M.whiteSmooth);
  plate([XE, EDGE], [RX1, RD], SOFFIT, FTOP, 0.03, M.whiteSmooth);
  if (rods) plate([RX0, RD], [RX1, RD], SOFFIT, FTOP, 0.03, M.whiteSmooth);
  // thermo-ash soffit slats (along x), clipped to the outline
  for (let y = EDGE + 0.06; y < RD - 0.05; y += 0.09) {
    const xEnd = tri ? TIP - TRI * (y - EDGE) / (RD - EDGE) : RX1;
    box(RX0 + 0.01, xEnd - 0.04, y, y + 0.068, SOFFIT, SOFFIT + 0.02, M.soffit);
  }
  // columns (SHS clad in thermo-ash 200x200, 0.13 above roof) against the low wall + brackets
  for (const x of COLS) {
    box(x - 0.1, x + 0.1, CY - 0.1, CY + 0.1, 0, COL_TOP, M.wood);
    box(x - 0.115, x + 0.115, CY - 0.115, CY + 0.115, COL_TOP, COL_TOP + 0.012, M.steel);
    for (const s of [-1, 1]) {
      const xf = x + s * 0.1;
      if ((s > 0 && xf > XE - 0.3) || (s < 0 && xf < RX0 + 0.3)) continue;
      bracket(xf, CY, s);
    }
    for (const z of [0.45, 1.15]) box(x - 0.06, x + 0.06, WI - 0.01, CY - 0.1, z - 0.04, z + 0.04, M.ss);   // fixings to the wall
  }
  // V2 / V2T: 2 slim stainless rods across the 0.90 void to the tall wall
  if (rods) for (const xr of [RX0 + ROOF_L / 2, RX1 - 0.15]) {
    cyl([xr, RD, SOFFIT + 0.15], [xr, WALL_Y0, 3.05], 0.008, M.ss);
    box(xr - 0.1, xr + 0.1, WALL_Y0 - 0.012, WALL_Y0, 2.95, 3.15, M.ss);
  }
  // V1 / V1T: ledger flashing line at the tall wall
  if (!rods) box(RX0, RX1, WALL_Y0 - 0.04, WALL_Y0, FTOP - 0.05, FTOP + 0.12, M.frame);

  // ------------------------------------------------------------------ background trees (existing, behind)
  pine(5.5, -5.0, 12, 1); pine(10.5, -6.5, 11, 2); pine(12.5, -9.0, 10, 3); pine(1.5, -3.5, 9, 4);
  eucalyptus(3.0, 7.0, 15, 5); eucalyptus(9.0, 8.5, 16, 6); eucalyptus(-2.0, 3.0, 14, 7);
  cypress(-3.0, -9.0, 11, 8); cypress(-1.5, -10.5, 12, 9); cypress(0.5, -11.0, 10, 10);
  foliage(13.5, -2.4, 1.2, 1.3, 55, ['#4c7a3a', '#5d8b43', '#3f6b32'], 40, 0.8);            // lantana outside the wall
  foliage(16.0, -1.9, 1.0, 1.0, 56, ['#4c7a3a', '#5d8b43', '#6e9a4e'], 30, 0.8);

  // ------------------------------------------------------------------ camera
  const cam = new THREE.PerspectiveCamera(VIEW === 'aerial' ? 38 : 58, W / H, 0.05, 600);
  const P = (x, y, z) => new THREE.Vector3(x, z, -y);
  if (VIEW === 'aerial') { cam.position.copy(P(21.5, -3.0, 8.0)); cam.lookAt(P(9.9, 1.2, 1.1)); }
  else if (VIEW === 'under') { cam.position.copy(P(12.6, 2.6, 1.55)); cam.lookAt(P(8.6, -0.2, 1.7)); }
  else { cam.position.copy(P(15.6, 1.9, 1.55)); cam.lookAt(P(8.2, 0.15, 1.45)); }   // as the site photo

  renderer.render(scene, cam);
  window.__done = true;
})();
