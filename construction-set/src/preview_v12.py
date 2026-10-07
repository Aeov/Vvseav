"""Rev C04 PREVIEW — two versions (client 07.10.2026), aligned with the site photo:
House (annex) 8.00 m long, 2.54 m wide; its end façade (glass door + brown roller shutter) faces the courtyard.
Planter strip 0.90 m beside it along the low boundary wall (house 2.54 + strip 0.90 = 3.44 sketch).
Roof 3.22 m long from the annex end façade. Underside +2.36, fascia 0.43 (top +2.79), columns 200x200, top +2.92.

V1  ROOF TO THE WALL : roof 3.22 x 3.44 over the planter strip up to the boundary wall;
                       2 columns on the plants side (middle + corner, standing in the planter) + front-right column.
V2  0.90 m VOID      : roof 3.22 x 2.54 (edge on the marked line, in line with the annex side);
                       2 columns on the plants-side edge + front-right column;
                       roof tied across the 0.90 m void to the wall with 2 slim stainless rods.
Axes: X along house/roof (house 0..8000, roof 8000..11220); Y across (front Y = 0, wall face Y = 3440).
"""
import math
import random
from cad import Sheet, View, break_line, PROJECT
from common import shrub, vine, ground, GREEN
from sheets_b import ladder, paving_cut, rhs, upn200, cchan

HOUSE_L, HOUSE_W, WALL = 8000, 2540, 200
STRIP = 900                          # passage to lattice door (top strip in client sketch)
WALL_Y0 = HOUSE_W + STRIP            # 3440 face of TALL wall (main house, AC units) — top side
TW_T, TW_H = 250, 5000               # tall house wall (2 storeys, assumed — verify)
PL = (-1000, -100)                   # planter (photo left = plants side = bottom edge), Y range
LW = (-1200, -1000)                  # low boundary wall behind planter
LW_H = 1400
ROOF_L = 3220
RX0, RX1 = HOUSE_L, HOUSE_L + ROOF_L
XM = RX0 + ROOF_L / 2
SOFFIT, FASCIA = 2360, 430
FTOP = SOFFIT + FASCIA
COL_TOP = FTOP + 130
HOUSE_TOP = 2920
BOS, TOS = SOFFIT + 50, SOFFIT + 250
POST, CLAD = 150, 200
ENTR = (250, 2290)                   # ENTRANCE (site photo): one opening 2.04 m wide x 2.20 high
SLIDE_W = 1060                       # 2 brown louvred SLIDING shutter panels (shown slid to photo-right)
SLIDES = [(ENTR[1] - SLIDE_W, ENTR[1], 0), (ENTR[1] - SLIDE_W - 60, ENTR[1] - 60, 1)]   # (y0, y1, track)
LATTICE = (HOUSE_W + 50, WALL_Y0 - 50)   # lattice door closing the 0.90 passage
HEAD = 2200
ROD_Z = BOS + 100                    # rod at roof top-edge beam
ROD_WALL_Z = 3050                    # rod anchor on tall wall: rises 0.5 m over 0.9 m (≈ 30°, almost horizontal)
COLS = [("C1", XM, 100), ("C2", RX1 - 100, 100)]
RODS_X = [XM, RX1 - 150]

VAR = {
    "V1": dict(name="VERSION 1 — ROOF TO THE WALL", roof_d=WALL_Y0, rods=False, cols=COLS,
               short="roof 3.22 x 3.44 up to the tall wall (bears on wall ledger + curved brackets); 2 columns on the plants side"),
    "V2": dict(name="VERSION 2 — 0.90 m VOID + 2 STEEL RODS", roof_d=HOUSE_W, rods=True, cols=COLS,
               short="roof 3.22 x 2.54; 0.90 m void left open; void edge tied to the tall wall with 2 slim "
                     "Ø16 stainless rods (rising ≈ 30°, almost horizontal); 2 columns on the plants side"),
}


def project(v):
    p = dict(PROJECT)
    p["rev"] = "C04"
    p["date"] = "07.10.2026"
    p["name"] = "COURTYARD ROOF — " + ("V1" if v == "V1" else "V2")
    p["site"] = VAR[v]["name"] + ": " + VAR[v]["short"]
    p["status"] = "PREVIEW FOR CLIENT REVIEW — per client sketch, mark-up & site photo; not for construction"
    return p


def plants(v, x0, x1, y0, y1, seed=1, rmin=170, rmax=260):
    r = random.Random(seed)
    x = x0 + 250
    while x < x1 - 150:
        v.circle(x, (y0 + y1) / 2 + r.uniform(-80, 80), r.uniform(rmin, rmax), w=0.15, color=GREEN, fill="#cfe3c0")
        x += r.uniform(400, 560)


def col(v, x, y, lab=None):
    v.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.25, fill="#e7c79a")
    v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
    if lab:
        v.tag(x, y - 380, lab, shape="circle", r=2.0, size=1.4)


def bracket(v, xface, zs, sgn, r=200):
    pts = [(xface, zs), (xface + sgn * r, zs)]
    for k in range(7):
        a = math.radians(90 * k / 6)
        pts.append((xface + sgn * (r - r * math.sin(a)), zs - r + r * math.cos(a)))
    v.pl(pts, w=0.25, fill="#c9d0d6")


def site_plan(v, RD, rods, labels=True):
    """Plan context in model coords: planter (bottom), annex, passage + lattice door, tall wall (top)."""
    # planter, low wall, trees (plants side = bottom)
    v.rect(-300, PL[0], RX1 + 1500, PL[1] - PL[0], w=0.15, fill="#efe4d0", color="#bba")
    v.rect(-300, PL[1], RX1 + 1500, 100, w=0.25, fill="#efe9dd")
    plants(v, -200, RX1 + 1300, PL[0], PL[1], seed=3)
    v.rect(-300, LW[0], RX1 + 1500, LW[1] - LW[0], mat="masonry", w=0.35)
    # tall wall (top)
    v.rect(-300, WALL_Y0, RX1 + 1500, TW_T, mat="masonry", w=0.45)
    # paving
    v.rect(RX0, 0, ROOF_L + 1200, WALL_Y0, w=0, fill="#f3eee4")
    # annex
    v.rect(0, 0, HOUSE_L, HOUSE_W, mat="masonry", w=0.45)
    v.rect(WALL, WALL, HOUSE_L - 2 * WALL, HOUSE_W - 2 * WALL, w=0.3, fill="#fbfaf7")
    v.rect(HOUSE_L - WALL, ENTR[0], WALL, ENTR[1] - ENTR[0], w=0.15, fill="#fff")
    mid = (ENTR[0] + ENTR[1]) / 2
    v.rect(HOUSE_L - 140, ENTR[0], 25, mid - ENTR[0] + 40, w=0.15, fill="#cfe3ef")      # glass sliding door
    v.rect(HOUSE_L - 110, mid - 40, 25, ENTR[1] - mid + 40, w=0.15, fill="#cfe3ef")
    for (a, b, tr) in SLIDES:                                                          # brown louvred slides
        v.rect(HOUSE_L + 10 + tr * 45, a, 35, b - a, w=0.25, fill="#6e5544")
    v.line(HOUSE_L + 5, ENTR[0] - 150, HOUSE_L + 5, ENTR[1] + 150, w=0.15, dash="1.5,0.8")
    # passage + lattice door
    v.rect(0, HOUSE_W, HOUSE_L, STRIP, w=0.1, fill="#f6f3ec", color="#bbb")
    v.rect(HOUSE_L - 120, LATTICE[0], 60, LATTICE[1] - LATTICE[0], w=0.25, fill="#b07a45")
    if labels:
        v.text(HOUSE_L / 2, 1350, "EXISTING ANNEX", size=2.3, anchor="middle", weight="bold", color="#555")
        v.text(HOUSE_L / 2, 950, "8.00 m long", size=1.8, anchor="middle", color="#777")
        v.text(HOUSE_L / 2, HOUSE_W + STRIP / 2 - 80, "PASSAGE 0.90 (lattice door at end)", size=1.5,
               anchor="middle", color="#555")
        v.text(HOUSE_L / 2, WALL_Y0 + TW_T + 150, "TALL HOUSE WALL (exist., AC units) — top side", size=1.5,
               anchor="middle", color="#555")
        v.text(3500, (PL[0] + PL[1]) / 2 - 80, "PLANTER + TREES (plants side)", size=1.5, color="#4f7a3d",
               weight="bold")
        v.text(3500, LW[0] - 300, "LOW BOUNDARY WALL (exist.)", size=1.4, color="#555")
    # roof
    v.rect(RX0, 0, ROOF_L, RD, w=0, fill="#dfe5ea", opacity=0.9)
    v.rect(RX0, 0, ROOF_L, RD, w=0.5, dash="4,1.5")
    for (lab, x, y) in COLS:
        col(v, x, y, lab if labels else None)
    if rods:
        for x in RODS_X:
            v.line(x, HOUSE_W - 60, x, WALL_Y0, w=0.4, color="#c0392b")
            v.rect(x - 60, WALL_Y0, 120, 30, w=0.2, fill="#c0392b")


# ===================================================================== SHEET 1: PLANS
def sheet_plans(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    s = Sheet(f"{vk}-01", f"{c['name']} — top view & roof plan", "1:50 / 1:25", project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color="#c0392b")
    v = View(s, 40, 84, 50)
    site_plan(v, RD, c["rods"])
    v.text(RX0 + ROOF_L / 2, RD / 2 + 200, "ROOF", size=2.4, anchor="middle", weight="bold")
    v.text(RX0 + ROOF_L / 2, RD / 2 - 250, f"3.22 x {RD / 1000:.2f} m", size=1.9, anchor="middle")
    if c["rods"]:
        v.text(RX1 + 150, HOUSE_W + 350, "2 Ø16 SS rods to wall", size=1.5, color="#c0392b", weight="bold")
    v.chain([0, HOUSE_L, RX1], "x", LW[0], -5, size=1.6)
    v.chain([RX0, XM, RX1], "x", LW[0], -15, size=1.5, overall=False)
    v.chain([0, HOUSE_W, WALL_Y0], "y", RX1 + 1200, -6, size=1.7)
    v.chain([0, RD], "y", RX1, -2, size=1.4, overall=False)
    v.title(206, 116, f"1/{vk}-01", "TOP VIEW — ANNEX, ROOF & PLANTER", "1:50 @ A3",
            sub="trees behind low wall & annex (background)")
    # ---- framing plan 1:25 (roof zone only)
    w = View(s, -265, 288, 25)
    w.rect(RX0 - 1000, 0, 1000, HOUSE_W, mat="masonry", w=0.4)
    w.text(RX0 - 500, HOUSE_W / 2, "ANNEX", size=1.8, anchor="middle", rot=90, color="#555")
    w.rect(RX0 - 1000, HOUSE_W, 1000, STRIP, w=0.1, fill="#f6f3ec", color="#bbb")
    w.rect(RX0 - 120, LATTICE[0], 60, LATTICE[1] - LATTICE[0], w=0.25, fill="#b07a45")
    w.rect(RX0 - 1000, WALL_Y0, ROOF_L + 1300, 90, mat="masonry", w=0.35)
    w.rect(RX0, 0, ROOF_L, RD, w=0.4, fill="#eef0f2")
    w.rect(RX0, 150, 75, HOUSE_W - 300, w=0.3, fill="#5c6670")              # ledger on annex
    if RD > HOUSE_W:
        w.rect(RX0 + 75, WALL_Y0 - 75, ROOF_L - 75, 75, w=0.3, fill="#5c6670")  # ledger on tall wall
    w.rect(RX0 + 75, 50, ROOF_L - 275, 100, w=0.35, fill="#7d8790")         # front (plants) edge beam
    w.rect(RX0 + 75, RD - 150 - (75 if RD > HOUSE_W else 0), ROOF_L - 175, 100, w=0.35, fill="#7d8790")
    w.rect(RX1 - 150, 200, 100, RD - 350, w=0.35, fill="#7d8790")           # end beam
    nj = 3 if RD < 3000 else 4
    for i in range(1, nj + 1):
        y = 150 + (RD - 300) * i / (nj + 1)
        w.rect(RX0 + 75, y - 32, ROOF_L - 225, 65, w=0.2, fill="#c9d0d6")
    for (lab, x, y) in COLS:
        w.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.3, fill="#e7c79a")
        w.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
        w.text(x, y - 330, lab, size=1.4, anchor="middle", weight="bold")
    if c["rods"]:
        for x in RODS_X:
            w.line(x, RD - 100, x, WALL_Y0, w=0.5, color="#c0392b")
            w.rect(x - 60, WALL_Y0, 120, 40, w=0.2, fill="#c0392b")
    w.chain([RX0, XM, RX1], "x", 0, -9, size=1.5)
    w.chain([0, RD, WALL_Y0], "y", RX1, -8, size=1.5, overall=False)
    s.text(16, 140, f"2/{vk}-01  ROOF FRAMING PLAN — 1:25", size=2.1, weight="bold")
    items = [("B", "THIS VERSION"), c["short"] + "."]
    if vk == "V1":
        items += ["Roof fixed to the annex end façade AND to the tall house wall (steel ledgers, resin anchors); "
                  "covers the passage in front of the lattice door.",
                  "Plants side: 2 columns (C1 middle, C2 corner) at the planter edge."]
    else:
        items += ["Roof fixed to the annex end façade (ledger). The 0.90 m passage to the lattice door stays open.",
                  "Top edge hung from the tall house wall on 2 Ø16 stainless rods (≈ 50°, turnbuckles, wall plates) — "
                  "slim, almost invisible.",
                  "Plants side: 2 columns (C1 middle, C2 corner) at the planter edge."]
    items += [("B", "COMMON"),
              "Roof 3.22 m from the annex façade. Underside +2.36, fascia 0.43 (top +2.79); columns 200x200, "
              "0.13 above roof, bracket under junction (client section).",
              "Falls 1:70 to concealed gutter at free end; rainwater down C2.",
              "Triangular extension (+1.26) — next step."]
    s.textblock(206, 140, 130, items, size=1.5, gap=0.3)
    s.north_arrow(320, 30, 5)
    s.scale_bar(240, 268, 50)
    return s


# ===================================================================== SHEET 2: VIEWS
def sheet_views(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    s = Sheet(f"{vk}-02", f"{c['name']} — view as photo, plants-side elevation & section", "1:50 / 1:25",
              project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color="#c0392b")
    # ---- 1: view towards annex façade, same direction as the site photo (plants LEFT). u = Y
    e = View(s, 40 + 1300 / 50, 128, 50)
    ground(e, LW[0] - 100, WALL_Y0 + TW_T + 200, 0, depth=200)
    e.rect(LW[0], 0, LW[1] - LW[0], LW_H, mat="masonry", w=0.35)
    e.rect(PL[1], 0, 100, 380, w=0.3, fill="#efe9dd")
    for i in range(3):
        shrub(e, PL[0] + 150 + i * 300, 380, 420, 900 + i * 200, seed=90 + i, flowers=5)
    e.rect(WALL_Y0, 0, TW_T, 4300, w=0.4, fill="#c98b6b")
    break_line(e, WALL_Y0, 4300, WALL_Y0 + TW_T, 4300)
    e.rect(WALL_Y0 - 30, 3000, 0.1, 0.1, w=0)
    e.rect(HOUSE_W + 50, 2900, 800, 600, w=0.2, fill="#f2f2f2")
    e.text(HOUSE_W + 450, 3200, "AC", size=1.3, anchor="middle")
    e.rect(LATTICE[0], 0, LATTICE[1] - LATTICE[0], HEAD, w=0.3, fill="#b07a45")
    e.rect(0, 0, HOUSE_W, HOUSE_TOP, w=0.4, fill="#f7f3ea")
    e.rect(ENTR[0], 0, ENTR[1] - ENTR[0], HEAD, w=0.35, fill="#2b2f33")                # opening
    e.rect(ENTR[0] + 40, 0, (ENTR[1] - ENTR[0]) / 2, HEAD - 40, w=0.2, fill="#cfe3ef")  # glass slider behind
    e.rect(ENTR[0] - 40, HEAD, ENTR[1] - ENTR[0] + 80, 40, w=0.2, fill="#888")          # top track
    for (a, b, tr) in sorted(SLIDES, key=lambda q: -q[2]):
        e.rect(a, 10, b - a, HEAD - 10, w=0.3, fill="#6e5544" if tr == 0 else "#5b4636")
    z = 80
    while z < HEAD - 20:
        e.line(SLIDES[1][0], z, SLIDES[0][1], z, w=0.06, color="#2e2219")
        z += 60
    e.line(SLIDES[0][0], 10, SLIDES[0][0], HEAD, w=0.25, color="#2e2219")
    e.leader([(ENTR[1] - 500, 1100), (ENTR[1] - 300, -900)], ["Entrance: brown aluminium louvred SLIDING shutters",
             "(2 panels on top track) + glass sliding door behind — as site photo"], size=1.3, anchor="start")
    e.rect(400, HOUSE_TOP, 1600, 1000, w=0.15, dash="2,1", color="#888")
    e.text(1200, HOUSE_TOP + 1150, "solar heater / AC (exist.)", size=1.3, anchor="middle", color="#888")
    e.rect(0, SOFFIT, RD, FASCIA, w=0.45, fill="#ffffff")
    e.rect(0, 0, CLAD, COL_TOP, w=0.35, mat="timber")
    e.text(100, COL_TOP + 100, "C2", size=1.4, anchor="middle", weight="bold")
    if c["rods"]:
        e.line(HOUSE_W - 60, ROD_Z, WALL_Y0, ROD_WALL_Z, w=0.5, color="#c0392b")
        e.rect(WALL_Y0 - 20, ROD_WALL_Z - 70, 20, 140, w=0.2, fill="#c0392b")
    e.chain([LW[1], 0, HOUSE_W, WALL_Y0], "x", 0, -6, size=1.4)
    ladder(e, WALL_Y0 + TW_T, [(0, "±0.000"), (HEAD, "+2.200"), (SOFFIT, "+2.360"), (FTOP, "+2.790"),
                               (COL_TOP, "+2.920")], 152, size=1.3, inside=False)
    s.text(16, 26, f"1/{vk}-02  VIEW TO ANNEX FAÇADE (as site photo / render) — 1:50", size=1.9,
           weight="bold")
    for k, tx in enumerate((-900, 400, 1700, 2900)):
        e.circle(tx, HOUSE_TOP + 1300 + (k % 2) * 300, 900, w=0.15, color="#7fa86a", fill="#e9f2e1")
    e.text(1000, HOUSE_TOP + 2400, "existing trees (background)", size=1.3, anchor="middle", color="#6b8f5a")

    # ---- 2: plants-side elevation along X (viewer in the planter looking at the roof), X to the right
    p = View(s, 22, 212, 50, origin=(4000, 0))
    ground(p, 4000, RX1 + 500, 0, depth=200)
    p.rect(4000, 0, HOUSE_L - 4000, HOUSE_TOP, w=0.4, fill="#f7f3ea")
    break_line(p, 4000, 0, 4000, HOUSE_TOP)
    p.rect(4000, 0, RX1 + 500 - 4000, 0.1, w=0)
    p.rect(RX0, SOFFIT, ROOF_L, FASCIA, w=0.45, fill="#ffffff")
    for (lab, x, y) in COLS:
        p.rect(x - CLAD / 2, 0, CLAD, COL_TOP, w=0.35, mat="timber")
        p.text(x, COL_TOP + 100, lab, size=1.4, anchor="middle", weight="bold")
        for sg in (-1, 1):
            if x + sg * CLAD / 2 < RX1 - 10:
                bracket(p, x + sg * CLAD / 2, SOFFIT, sg)
    p.chain([RX0, XM, RX1], "x", 0, -6, size=1.4)
    p.dim((RX1, 0), (RX1, SOFFIT), -4, size=1.3)
    p.dim((RX1, SOFFIT), (RX1, FTOP), -4, size=1.3)
    s.text(16, 140, f"2/{vk}-02  PLANTS-SIDE ELEVATION — C1 + C2 (as client sketch) — 1:50", size=1.9,
           weight="bold")

    # ---- 3: section across at C1 (1:50 overview — refined at 1:25 on sheet -03)
    def u(y):
        return WALL_Y0 + TW_T - y
    w = View(s, 198, 128, 50)
    paving_cut(w, [(u(WALL_Y0), -15), (u(0), -15)], z_bottom_extra=150, joints=False)
    w.rect(u(WALL_Y0 + TW_T), -300, TW_T, 4300, w=0.35, mat="masonry")
    w.rect(u(0), -200, 100, 580, w=0.3, mat="rc")
    w.rect(u(PL[1]), -200, PL[1] - PL[0], 500, w=0.15, mat="soil")
    w.rect(u(LW[1]), -200, LW[1] - LW[0], LW_H + 200, w=0.3, mat="masonry")
    shrub(w, u(PL[1]) + 450, 300, 600, 900, seed=131, flowers=4)
    w.rect(u(RD), SOFFIT, RD, FASCIA, w=0.35, fill="#e6eaee")
    w.rect(u(CLAD), 0, CLAD, COL_TOP, w=0.3, mat="timber")
    if c["rods"]:
        w.line(u(RD - 100), ROD_Z, u(WALL_Y0), ROD_WALL_Z, w=0.45, color="#c0392b")
    ladder(w, u(WALL_Y0 + TW_T), [(0, "±0.000"), (SOFFIT, "+2.360"), (FTOP, "+2.790")], 190, size=1.3,
           inside=False)
    w.chain([u(WALL_Y0), u(RD), u(0)], "x", -200, -4, size=1.3, overall=False)
    s.text(198, 26, f"3/{vk}-02  SECTION ACROSS AT C1 — 1:50 (see {vk}-03)", size=1.9, weight="bold")
    s.text(198, 30, "tall wall left — plants right (as client sketch)", size=1.4)
    s.textblock(198, 196, 140, [("B", "NOTES"), VAR[vk]["short"] + ".",
                                "Underside +2.36, fascia 0.43 (top +2.79); columns 0.13 above roof.",
                                "Trees are existing, behind the low boundary wall and the annex (background).",
                                "Refined roof section & details: sheet " + vk + "-03."], size=1.5, gap=0.3)
    s.scale_bar(240, 270, 50)
    return s


# ===================================================================== SHEET 3: ROOF SECTION & DETAILS
def roof_layers_y(v, ua, ub, z_top=TOS):
    """Deck + membrane + soffit between paper-model u positions ua<ub (section across roof)."""
    v.rect(ua, z_top + 38, ub - ua, 18, w=0.15, fill="#d9b98a")
    v.line(ua, z_top + 58, ub, z_top + 58, w=0.45, color="#111")
    v.rect(ua, SOFFIT, ub - ua, 20, w=0.12, mat="timber")
    v.rect(ua, SOFFIT + 20, ub - ua, 30, w=0.08, fill="#c9a77c")


def fin(v, x, z, h=120, b=12):
    v.rect(x - b / 2, z - h / 2, b, h, w=0.2, fill="#444")


def sheet_details(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    s = Sheet(f"{vk}-03", f"{c['name']} — roof section & construction details", "1:25 / 1:10",
              project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color="#c0392b")

    def u(y):
        return WALL_Y0 + TW_T - y

    # ---------------- S1 section across at C1, 1:25 (tall wall LEFT, plants RIGHT — client sketches)
    v = View(s, 20, 190, 25)
    paving_cut(v, [(u(WALL_Y0), -15), (u(0), -15)], z_bottom_extra=200)
    v.rect(u(WALL_Y0 + TW_T), -600, TW_T, 4200, w=0.45, mat="masonry")
    break_line(v, u(WALL_Y0 + TW_T), 3600, u(WALL_Y0), 3600)
    v.rect(u(0), -500, 100, 880, w=0.3, mat="rc")
    v.rect(u(PL[1]), -400, PL[1] - PL[0], 700, w=0.15, mat="soil")
    v.rect(u(LW[1]), -600, LW[1] - LW[0], LW_H + 600, w=0.35, mat="masonry")
    for i in range(2):
        shrub(v, u(PL[1]) + 250 + i * 380, 300, 420, 900, seed=140 + i, flowers=4)
    # column C1 + base
    v.rect(u(CLAD), 0, CLAD, COL_TOP, w=0.35, mat="timber")
    v.rect(u(100 + POST / 2), -60, POST, COL_TOP - 10 + 60, w=0.3, fill="#5c6670")
    v.rect(u(CLAD) - 30, COL_TOP - 10, CLAD + 60, 10, w=0.25, fill="#888")
    v.rect(u(100 + 400), -900, 800, 700, w=0.3, mat="rc")
    v.rect(u(100 + 150), -200, 300, 140, w=0.3, mat="rc")
    # roof structure
    rhs(v, u(150), BOS, 100, 200, 6.3)                          # plants edge beam (beyond, frames into C1)
    nj = 3 if RD < 3000 else 4
    for i in range(1, nj + 1):
        y = 150 + (RD - 300) * i / (nj + 1)
        cchan(v, u(y), BOS, facing=-1)
    roof_layers_y(v, u(RD - 50), u(CLAD))
    bracket(v, u(CLAD), SOFFIT, -1)
    v.rect(u(0), SOFFIT, 3, FASCIA, w=0.35, fill="#222") if False else None
    if vk == "V1":
        upn200(v, u(WALL_Y0), BOS, facing=1)
        bracket(v, u(WALL_Y0), SOFFIT + 50, 1, r=180)
        v.pl([(u(WALL_Y0) + 6, TOS + 58), (u(WALL_Y0) + 6, TOS + 220)], w=0.45, closed=False, color="#111")
        v.pl([(u(WALL_Y0), TOS + 240), (u(WALL_Y0) + 40, TOS + 225), (u(WALL_Y0) + 40, TOS + 150)], w=0.35,
             closed=False, color="#7f8c8d")
    else:
        rhs(v, u(RD - 50), BOS, 100, 200, 6.3)                   # void edge beam
        v.pl([(u(RD) + 3, SOFFIT), (u(RD), SOFFIT), (u(RD), FTOP), (u(RD) + 45, FTOP - 6)], w=0.5, closed=False,
             color="#111")
        v.line(u(RD - 60), ROD_Z, u(WALL_Y0), ROD_WALL_Z, w=0.5, color="#c0392b")
        v.rect(u(WALL_Y0), ROD_WALL_Z - 100, 15, 200, w=0.25, fill="#c0392b")
        mx = (u(RD - 60) + u(WALL_Y0)) / 2
        v.rect(mx - 60, (ROD_Z + ROD_WALL_Z) / 2 - 15, 120, 30, w=0.2, fill="#bbb")
        v.text(u(HOUSE_W + STRIP / 2), 900, "0.90 VOID", size=1.6, anchor="middle", rot=90, color="#555")
    ladder(v, u(WALL_Y0 + TW_T), [(0, "±0.000"), (SOFFIT, "+2.360 u/s"), (TOS, "+2.610 TOS"),
                                  (FTOP, "+2.790"), (COL_TOP, "+2.920 col.")]
           + ([(ROD_WALL_Z, "+3.050 rod anchor")] if vk == "V2" else []), 17, size=1.3, inside=True)
    v.chain([u(WALL_Y0), u(RD), u(CLAD), u(0)], "x", -900, -4, size=1.35, overall=True)
    tl = [((u(100), 1300), (u(800), 1100), ["C1 SHS 150x150x8 + 25 thermo-ash = 200x200"]),
          ((u(CLAD) - 80, SOFFIT - 90), (u(800), 1700), ["Steel bracket R200 (10 mm), welded/bolted"]),
          ((u(1000), TOS + 50), (u(1200), 3350), ["1.5 TPO / 18 ply / firrings / C200 joists"]),
          ((u(1500), SOFFIT + 10), (u(1600), 2050), ["68x20 thermo-ash slats on battens, LED in edge profile"]),
          ((u(300), -500), (u(-300), -700), ["Pad 800x800x700 in planter"])]
    if vk == "V1":
        tl.append(((u(WALL_Y0) + 40, BOS + 100), (u(WALL_Y0) + 300, 3150),
                   ["UPN 200 ledger + curved brackets on wall"]))
    else:
        tl.append(((mx, (ROD_Z + ROD_WALL_Z) / 2), (u(WALL_Y0) + 300, 3300),
                   ["Ø16 SS rod + turnbuckle (2 no.)"]))
    for tgt, txt, lines in tl:
        v.leader([tgt, txt], lines, size=1.3, anchor="start")
    s.text(16, 26, f"1/{vk}-03  ROOF SECTION ACROSS AT C1 — 1:25", size=2.0, weight="bold")
    s.text(16, 30, "(as client sketch " + ("A: roof runs to the wall" if vk == "V1" else
                                           "B: roof stops, rods to the wall") + ")", size=1.4)

    # ---------------- D1 wall junction / rod hanger 1:10
    d = View(s, 236, 120, 15, origin=(0, 2300))
    if vk == "V1":
        # local coords: d-x = distance from wall face into roof (0..900)
        d.rect(-200, 2150, 200, 1250, w=0.45, mat="masonry")
        d.pl([(0, BOS), (75, BOS), (75, BOS + 11), (8.5, BOS + 11), (8.5, TOS - 11), (75, TOS - 11), (75, TOS),
              (0, TOS)], w=0.25, mat="steel")
        for z in (BOS + 60, BOS + 140):
            d.rect(-130, z - 6, 140, 12, w=0.12, fill="#888")
        bracket(d, 0, BOS, 1, r=180)
        d.rect(75, BOS, 600, 200, w=0.12, fill="#e6eaee", color="#777")
        roof_layers_y(d, 20, 680)
        d.pl([(8, TOS + 58), (8, TOS + 220)], w=0.5, closed=False, color="#111")
        d.pl([(0, TOS + 240), (40, TOS + 225), (40, TOS + 150)], w=0.4, closed=False, color="#7f8c8d")
        for tgt, txt, lines in (((40, BOS + 100), (300, 2280), ["UPN 200 HDG, M12 resin anchors @ 400"]),
                                ((90, BOS - 90), (300, 2200), ["Curved bracket R180, 10 mm, @ 1.0 m"]),
                                ((40, TOS + 200), (300, 3050), ["Membrane up 150 + alu counter-flashing"]),
                                ((400, TOS + 50), (300, 2980), ["Deck & membrane"])):
            d.leader([tgt, txt], lines, size=1.25, anchor="start")
        s.text(222, 26, "D1  ROOF TO WALL (client sketch A) — 1:15", size=1.8, weight="bold")
    else:
        # d-x = distance from wall face (0) towards roof edge (900)
        d.rect(-200, 2150, 200, 1250, w=0.45, mat="masonry")
        d.rect(0, ROD_WALL_Z - 100, 12, 200, w=0.25, fill="#c0392b")
        for z in (ROD_WALL_Z - 60, ROD_WALL_Z + 60):
            d.rect(-110, z - 6, 122, 12, w=0.12, fill="#888")
        d.rect(12, ROD_WALL_Z - 6, 40, 12, w=0.2, fill="#777")
        rx, rz = STRIP + 40, ROD_Z
        d.line(50, ROD_WALL_Z, rx, rz, w=0.6, color="#c0392b")
        mxl, mzl = (50 + rx) / 2, (ROD_WALL_Z + rz) / 2
        d.rect(mxl - 55, mzl - 14, 110, 28, w=0.2, fill="#bbb")
        rhs(d, STRIP + 50, BOS, 100, 200, 6.3)
        d.rect(STRIP + 30, ROD_Z - 40, 20, 80, w=0.2, fill="#444")
        d.circle(rx, rz, 9, w=0.2, fill="#fff")
        d.pl([(STRIP + 3, SOFFIT), (STRIP, SOFFIT), (STRIP, FTOP), (STRIP + 45, FTOP - 6)], w=0.55, closed=False,
             color="#111")
        roof_layers_y(d, STRIP + 20, STRIP + 300)
        d.text(STRIP / 2, 2450, "0.90 VOID", size=1.4, anchor="middle", color="#555")
        for tgt, txt, lines in (((6, ROD_WALL_Z + 80), (-180, 3330), ["Wall plate 200x150x12 SS, 4 M12 resin"]),
                                ((mxl, mzl), (150, 3200), ["Ø16 SS 316 rod, turnbuckle"]),
                                ((STRIP + 40, ROD_Z), (420, 2250), ["Fork end on 10 mm lug welded to edge beam"]),
                                ((STRIP, 2600), (420, 2150), ["Fascia 0.43 at void edge"])):
            d.leader([tgt, txt], lines, size=1.25, anchor="start")
        s.text(222, 26, "D1  ROD TO WALL (client sketch B) — 1:15", size=1.8, weight="bold")

    # ---------------- D2 column C1 junction 1:10 (plants side), d-x = distance from plants edge (0) into roof
    q = View(s, 249, 217 + 15, 10, origin=(0, 2300 + 150))
    q.rect(-200, 2150, 200, COL_TOP - 2150, w=0.35, mat="timber")
    q.rect(-175, 2150, POST, COL_TOP - 2160, w=0.3, fill="#5c6670")
    q.rect(-230, COL_TOP - 10, 260, 10, w=0.25, fill="#888")
    break_line(q, -220, 2150, 20, 2150)
    q.rect(0, BOS, 500, 200, w=0.25, fill="#7d8790")
    q.rect(6, BOS + 6, 494, 188, w=0.1, fill="#fff")
    fin(q, 6, BOS + 100)
    for z in (BOS + 70, BOS + 130):
        q.circle(50, z, 9, w=0.2, fill="#999")
    bracket(q, 0, SOFFIT, 1, r=200)
    roof_layers_y(q, 0, 500)
    q.pl([(0, TOS + 58), (0, TOS + 210)], w=0.5, closed=False, color="#111")
    q.rect(-230, TOS + 190, 30, 30, w=0.2, fill="#7f8c8d")
    for tgt, txt, lines in (((-100, 2600), (-220, 3150), ["Column SHS 150 + cladding"]),
                            ((50, BOS + 100), (150, 3100), ["FP 12 + 2 M16, edge beam"]),
                            ((60, SOFFIT - 80), (150, 2200), ["Bracket R200"]),
                            ((-100, COL_TOP - 5), (150, 3020), ["Cap plate, +0.13 above roof"])):
        q.leader([tgt, txt], lines, size=1.2, anchor="start")
    s.text(222, 140, "D2  COLUMN / ROOF JUNCTION (plants side) — 1:10", size=1.8, weight="bold")

    s.textblock(222, 240, 116, [
        ("B", "SPECIFICATION"),
        "Steel S355, hot-dip galvanised; columns & brackets powder-coated RAL 9010 or timber-clad (thermo-ash).",
        "Roof: TPO 1.5 on 18 mm marine ply on tapered firrings (fall 1:70 to free-end gutter).",
        "Soffit: thermo-ash 68x20 slats, LED 2700 K in perimeter profile. Fascia 3 mm aluminium RAL 9010, 0.43 m.",
        ("Rods: Ø16 stainless 316, fork ends, turnbuckle, ≈ 30° rise; engineer to confirm wall anchors."
         if vk == "V2" else "Wall ledger & brackets into sound masonry/RC — engineer to confirm anchors."),
    ], size=1.4, gap=0.25)
    s.scale_bar(240, 272, 25, 2)
    return s


def sheets():
    out = []
    for vk in ("V1", "V2"):
        out += [sheet_plans(vk), sheet_views(vk), sheet_details(vk)]
    return out


if __name__ == "__main__":
    import build
    ss = sheets()
    for s in ss:
        build.preview(s, "../preview/" + s.number + ".png", scale=1.2)
    print(build.to_pdf(ss, "Rev-C04_V1-V2_Preview"))
