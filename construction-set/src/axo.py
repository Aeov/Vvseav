"""Simple axonometric renderer (painter's algorithm) for presentation views."""
import math
import random


class Axo:
    def __init__(self, beta=28, elev=32):
        b = math.radians(beta)
        e = math.radians(elev)
        self.cb, self.sb, self.ce, self.se = math.cos(b), math.sin(b), math.cos(e), math.sin(e)
        self.items = []  # (depth, svg_fn)

    def proj(self, X, Y, Z):
        x1 = X * self.cb + Y * self.sb
        y1 = -X * self.sb + Y * self.cb
        return x1, Z * self.ce + y1 * self.se, y1 * self.ce - Z * self.se

    def box(self, x, y, z, dx, dy, dz, top="#ddd", south="#bbb", east="#ccc", stroke="#333", w=0.15,
            layer=0, bias=0.0, west=None, north=None):
        X0, X1, Y0, Y1, Z0, Z1 = x, x + dx, y, y + dy, z, z + dz
        faces = []
        faces.append(([(X0, Y0, Z1), (X1, Y0, Z1), (X1, Y1, Z1), (X0, Y1, Z1)], top))
        faces.append(([(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y0, Z1), (X0, Y0, Z1)], south))
        faces.append(([(X1, Y0, Z0), (X1, Y1, Z0), (X1, Y1, Z1), (X1, Y0, Z1)], east))
        cx, cy, cz = (X0 + X1) / 2, (Y0 + Y1) / 2, (Z0 + Z1) / 2
        d = self.proj(cx, cy, cz)[2]
        # bias: nearer corner dominates for long items
        dn = self.proj(X1, Y0, Z1)[2]
        self.items.append((layer, -(0.5 * d + 0.5 * dn) + bias, ("faces", faces, stroke, w)))

    def poly3(self, pts, fill, stroke="#333", w=0.12, layer=0, bias=0.0):
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        cz = sum(p[2] for p in pts) / len(pts)
        d = self.proj(cx, cy, cz)[2]
        self.items.append((layer, -d + bias, ("faces", [(pts, fill)], stroke, w)))

    def blob(self, x, y, z, r, fill="#7fa86a", stroke="#4f7a3d", layer=0, bias=0.0, flowers=0, seed=1, squash=0.85):
        d = self.proj(x, y, z)[2]
        self.items.append((layer, -d + bias, ("blob", (x, y, z, r, fill, stroke, flowers, seed, squash))))

    def render(self, sheet, ox, oy, scale):
        """ox, oy: paper position of world origin; scale: mm world per mm paper."""
        k = 1.0 / scale
        out = []
        for layer, key, it in sorted(self.items, key=lambda t: (t[0], t[1])):
            if it[0] == "faces":
                _, faces, stroke, w = it
                for pts, fill in faces:
                    if fill is None:
                        continue
                    pp = []
                    for (X, Y, Z) in pts:
                        sx, sy, _ = self.proj(X, Y, Z)
                        pp.append((ox + sx * k, oy - sy * k))
                    sheet.poly(pp, w=w, color=stroke, fill=fill)
            else:
                x, y, z, r, fill, stroke, flowers, seed, squash = it[1]
                sx, sy, _ = self.proj(x, y, z)
                cx, cy = ox + sx * k, oy - sy * k
                rr = r * k
                rnd = random.Random(seed)
                n = 16
                pts = []
                for i in range(n):
                    a = 2 * math.pi * i / n
                    f = 1 + rnd.uniform(-0.12, 0.12)
                    pts.append((cx + math.cos(a) * rr * f, cy + math.sin(a) * rr * f * squash))
                sheet.poly(pts, w=0.12, color=stroke, fill=fill)
                sheet.circle(cx - rr * 0.3, cy - rr * 0.3, rr * 0.35, w=0, fill="#ffffff", )
                sheet.add(f'<circle cx="{cx - rr * 0.3:.2f}" cy="{cy - rr * 0.3:.2f}" r="{rr * 0.4:.2f}" '
                          f'fill="#ffffff" fill-opacity="0.18"/>')
                for i in range(flowers):
                    a = rnd.uniform(0, 2 * math.pi)
                    q = rnd.uniform(0, 0.8)
                    sheet.circle(cx + math.cos(a) * rr * q, cy + math.sin(a) * rr * q * squash, max(0.25, rr * 0.07),
                                 w=0, fill="#ffffff")


def shade(hexc, f):
    hexc = hexc.lstrip("#")
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    r, g, b = [max(0, min(255, int(c * f))) for c in (r, g, b)]
    return f"#{r:02x}{g:02x}{b:02x}"


def mbox(a, x, y, z, dx, dy, dz, col, **kw):
    a.box(x, y, z, dx, dy, dz, top=shade(col, 1.08), south=shade(col, 0.9), east=shade(col, 0.78), **kw)
