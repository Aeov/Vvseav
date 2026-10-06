"""Minimal 2D CAD kit: model-space views rendered to SVG sheets (paper mm) + DXF at 1:1.

Model coordinates are millimetres, y-up. Paper coordinates are millimetres, y-down.
"""
import math
from xml.sax.saxutils import escape

FONT = "Liberation Sans, Arial, Helvetica, sans-serif"

PROJECT = {
    "name": "COURTYARD CANOPY & GARDEN TERRACE",
    "site": "Private residence — rear courtyard (site address to be inserted)",
    "client": "Owner / Client",
    "by": "Design & drawings: Claude Code",
    "date": "06.10.2026",
    "rev": "C01",
    "status": "CONSTRUCTION ISSUE — subject to site survey & local engineer sign-off",
}

# ---------------------------------------------------------------- hatches
HATCH_DEFS = """
<pattern id="h-conc" patternUnits="userSpaceOnUse" width="4" height="4">
  <circle cx="0.6" cy="0.8" r="0.12" fill="#555"/><circle cx="2.7" cy="2.9" r="0.1" fill="#555"/>
  <circle cx="3.4" cy="0.6" r="0.08" fill="#555"/>
  <path d="M1.6 2.2 l0.45 -0.6 l0.3 0.7 z" fill="none" stroke="#555" stroke-width="0.07"/>
</pattern>
<pattern id="h-rc" patternUnits="userSpaceOnUse" width="3" height="3" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="3" stroke="#666" stroke-width="0.08"/>
</pattern>
<pattern id="h-masonry" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="1.6" stroke="#444" stroke-width="0.09"/>
</pattern>
<pattern id="h-earth" patternUnits="userSpaceOnUse" width="5" height="5">
  <path d="M0 5 L5 0 M-1 1 L1 -1 M4 6 L6 4" stroke="#6b4b2a" stroke-width="0.12"/>
  <path d="M0.5 2 h1.2 M3 4.3 h1" stroke="#6b4b2a" stroke-width="0.1"/>
</pattern>
<pattern id="h-soil" patternUnits="userSpaceOnUse" width="3" height="3">
  <circle cx="0.7" cy="0.7" r="0.18" fill="#5a3d1e"/><circle cx="2.2" cy="1.9" r="0.14" fill="#5a3d1e"/>
  <circle cx="1.3" cy="2.6" r="0.1" fill="#5a3d1e"/>
</pattern>
<pattern id="h-gravel" patternUnits="userSpaceOnUse" width="3" height="3">
  <circle cx="0.8" cy="0.8" r="0.5" fill="none" stroke="#555" stroke-width="0.08"/>
  <circle cx="2.3" cy="2.1" r="0.45" fill="none" stroke="#555" stroke-width="0.08"/>
  <circle cx="2.4" cy="0.5" r="0.25" fill="none" stroke="#555" stroke-width="0.08"/>
</pattern>
<pattern id="h-subbase" patternUnits="userSpaceOnUse" width="4" height="4">
  <path d="M0.3 1 l0.8 -0.5 l0.6 0.6 l-0.7 0.5 z M2.3 3 l0.9 -0.4 l0.4 0.7 l-0.9 0.3 z" fill="none" stroke="#444" stroke-width="0.08"/>
  <circle cx="3.2" cy="1.1" r="0.15" fill="#444"/><circle cx="1.1" cy="3.2" r="0.12" fill="#444"/>
</pattern>
<pattern id="h-sand" patternUnits="userSpaceOnUse" width="2" height="2">
  <circle cx="0.5" cy="0.5" r="0.08" fill="#777"/><circle cx="1.5" cy="1.4" r="0.08" fill="#777"/>
</pattern>
<pattern id="h-timber" patternUnits="userSpaceOnUse" width="2" height="2" patternTransform="rotate(30)">
  <line x1="0" y1="0" x2="0" y2="2" stroke="#8a5a2b" stroke-width="0.07"/>
</pattern>
<pattern id="h-insul" patternUnits="userSpaceOnUse" width="2" height="2">
  <path d="M0 1 Q0.5 0 1 1 T2 1" fill="none" stroke="#888" stroke-width="0.08"/>
</pattern>
<pattern id="h-render" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
  <circle cx="0.3" cy="0.3" r="0.07" fill="#888"/>
</pattern>
<pattern id="h-glass" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(-45)">
  <line x1="0" y1="0" x2="0" y2="1.4" stroke="#7aa5c0" stroke-width="0.12"/>
</pattern>
<pattern id="h-slats" patternUnits="userSpaceOnUse" width="1.5" height="1.5">
  <line x1="0" y1="0.75" x2="1.5" y2="0.75" stroke="#3b2a1d" stroke-width="0.12"/>
</pattern>
<pattern id="h-grass" patternUnits="userSpaceOnUse" width="4" height="4">
  <path d="M0.5 3 l0.3 -1 l0.3 1 M2.5 1.6 l0.3 -1 l0.3 1" fill="none" stroke="#4d7a3a" stroke-width="0.1"/>
</pattern>
"""

# line hatches: id -> (angle deg, spacing mm, colour, stroke width, dash)
LINE_HATCH = {
    "h-rc": (45, 2.1, "#666", 0.08, None),
    "h-masonry": (45, 1.15, "#444", 0.09, None),
    "h-timber": (30, 1.0, "#8a5a2b", 0.07, None),
    "h-glass": (-45, 4.2, "#7aa5c0", 0.12, "1.4,3"),
    "h-slats": (0, 1.5, "#3b2a1d", 0.12, None),
}
TILE_SIZE = {"h-conc": (4, 4), "h-earth": (5, 5), "h-soil": (3, 3), "h-gravel": (3, 3), "h-subbase": (4, 4),
             "h-sand": (2, 2), "h-insul": (2, 2), "h-render": (1.2, 1.2), "h-grass": (4, 4)}


def _tile_defs():
    import re
    out = []
    for m in re.finditer(r'<pattern id="(h-[a-z]+)"[^>]*>(.*?)</pattern>', HATCH_DEFS, re.S):
        hid, body = m.group(1), m.group(2)
        if hid in TILE_SIZE:
            out.append(f'<g id="t-{hid}">{body.strip()}</g>')
    return "".join(out)


# material -> (tint fill, hatch id or None)
MAT = {
    "conc": ("#e9e9e6", "h-conc"),
    "rc": ("#e2e2df", "h-rc"),
    "masonry": ("#f1ece4", "h-masonry"),
    "earth": ("#efe4d4", "h-earth"),
    "soil": ("#d9c3a3", "h-soil"),
    "gravel": ("#ece8df", "h-gravel"),
    "subbase": ("#ebe7de", "h-subbase"),
    "sand": ("#f3ead2", "h-sand"),
    "timber": ("#e7c79a", "h-timber"),
    "steel": ("#5c6670", None),
    "alu": ("#c9d0d6", None),
    "alu_white": ("#ffffff", None),
    "paver": ("#d8cbb5", None),
    "insul": ("#f5f0c8", "h-insul"),
    "render": ("#f7f3ea", "h-render"),
    "glass": ("#dcecf5", "h-glass"),
    "membrane": ("#222222", None),
    "grout": ("#cfcfcf", "h-sand"),
    "void": ("#ffffff", None),
    "plant": ("#cfe3c0", None),
    "pvc": ("#9aa3ab", None),
    "rubber": ("#333333", None),
    "grass": ("#dfeccf", "h-grass"),
}

DXF_LAYERS = {
    "A-WALL": 7, "A-HIDDEN": 8, "A-DIMS": 3, "A-TEXT": 2, "A-HATCH": 9, "S-STEEL": 1,
    "A-TIMBER": 30, "L-PLANT": 94, "A-DOOR": 5, "E-LIGHT": 6, "C-DRAIN": 4, "A-PAVING": 251,
    "A-GRID": 8, "A-ANNO": 7,
}


def _f(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


class Sheet:
    W, H = 420.0, 297.0
    TB_X = 343.0  # title block column left edge

    def __init__(self, number, title, scale_note="AS SHOWN", series="ARCHITECTURAL", project=None):
        self.number = number
        self.title = title
        self.scale_note = scale_note
        self.series = series
        self.project = project or PROJECT
        self.els = []
        self.dxf_doc = None

    # -------- paper-space primitives (y down)
    def add(self, s):
        self.els.append(s)

    def line(self, x1, y1, x2, y2, w=0.25, color="#000", dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="{color}" '
                 f'stroke-width="{w}" stroke-linecap="{cap}"{d}/>')

    _clip_n = [0]

    def _hatch(self, pts, hid):
        """Vector hatch: clipPath + generated lines/tiles (avoids rasterised SVG patterns in PDF)."""
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x1 - x0 < 0.05 or y1 - y0 < 0.05:
            return
        Sheet._clip_n[0] += 1
        cid = f"c{Sheet._clip_n[0]}"
        p = " ".join(f"{_f(x)},{_f(y)}" for x, y in pts)
        g = [f'<defs><clipPath id="{cid}"><polygon points="{p}"/></clipPath></defs><g clip-path="url(#{cid})">']
        spec = LINE_HATCH.get(hid)
        if spec:
            ang, sp, col, sw, dash = spec
            a = math.radians(ang)
            dx, dy = math.cos(a), math.sin(a)
            nx, ny = -dy, dx
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            R = math.hypot(x1 - x0, y1 - y0) / 2 + sp
            n = int(R / sp) + 1
            dd = f' stroke-dasharray="{dash}"' if dash else ""
            segs = []
            for i in range(-n, n + 1):
                ox, oy = cx + nx * i * sp, cy + ny * i * sp
                segs.append(f"M{_f(ox - dx * R)} {_f(oy - dy * R)}L{_f(ox + dx * R)} {_f(oy + dy * R)}")
            g.append(f'<path d="{"".join(segs)}" stroke="{col}" stroke-width="{sw}" fill="none"{dd}/>')
        else:
            tw, th = TILE_SIZE[hid]
            yy = y0 - (y0 % th)
            while yy < y1:
                xx = x0 - (x0 % tw)
                while xx < x1:
                    g.append(f'<use href="#t-{hid}" x="{_f(xx)}" y="{_f(yy)}"/>')
                    xx += tw
                yy += th
        g.append("</g>")
        self.add("".join(g))

    def poly(self, pts, w=0.25, color="#000", fill="none", closed=True, dash=None, opacity=None, join="miter"):
        if isinstance(fill, str) and fill.startswith("url(#h-"):
            self._hatch(pts, fill[5:-1])
            if w > 0:
                self.poly(pts, w=w, color=color, fill="none", closed=closed, dash=dash)
            return
        tag = "polygon" if closed else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{opacity}"' if opacity is not None else ""
        p = " ".join(f"{_f(x)},{_f(y)}" for x, y in pts)
        sc = color if w > 0 else "none"
        self.add(f'<{tag} points="{p}" fill="{fill}" stroke="{sc}" stroke-width="{w}" '
                 f'stroke-linejoin="{join}"{d}{o}/>')

    def rect(self, x, y, w, h, lw=0.25, color="#000", fill="none", dash=None, rx=0):
        if isinstance(fill, str) and fill.startswith("url(#h-"):
            self._hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill[5:-1])
            if lw > 0:
                self.rect(x, y, w, h, lw=lw, color=color, fill="none", dash=dash)
            return
        d = f' stroke-dasharray="{dash}"' if dash else ""
        sc = color if lw > 0 else "none"
        self.add(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{rx}" fill="{fill}" '
                 f'stroke="{sc}" stroke-width="{lw}"{d}/>')

    def circle(self, cx, cy, r, w=0.25, color="#000", fill="none", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        sc = color if w > 0 else "none"
        self.add(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" fill="{fill}" stroke="{sc}" stroke-width="{w}"{d}/>')

    def path(self, d, w=0.25, color="#000", fill="none", dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}"{dd}/>')

    def text(self, x, y, s, size=2.5, anchor="start", weight="normal", rot=0, color="#000", italic=False,
             family=FONT):
        tr = f' transform="rotate({_f(rot)} {_f(x)} {_f(y)})"' if rot else ""
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{_f(x)}" y="{_f(y)}" font-family="{family}" font-size="{size}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" fill="{color}"{st}{tr}>{escape(str(s))}</text>')

    # -------- helpers
    @staticmethod
    def wrap(s, width_mm, size):
        cw = size * 0.5
        maxc = max(8, int(width_mm / cw))
        out = []
        for para in str(s).split("\n"):
            words = para.split(" ")
            cur = ""
            for wd in words:
                if len(cur) + len(wd) + 1 > maxc and cur:
                    out.append(cur)
                    cur = wd
                else:
                    cur = (cur + " " + wd) if cur else wd
            out.append(cur)
        return out

    def textblock(self, x, y, width, items, size=2.0, lead=1.35, gap=0.6, heading_size=None):
        """items: list of str | ('H', str) heading | ('B', str) bold line. Returns end y."""
        cy = y
        for it in items:
            if isinstance(it, tuple):
                kind, s = it
                if kind == "H":
                    hs = heading_size or size * 1.25
                    cy += hs * 0.4
                    self.text(x, cy + hs, s, size=hs, weight="bold")
                    cy += hs * lead + 0.6
                    self.line(x, cy - hs * 0.25, x + width, cy - hs * 0.25, w=0.15)
                    cy += 0.4
                    continue
                if kind == "B":
                    for ln in self.wrap(s, width, size):
                        self.text(x, cy + size, ln, size=size, weight="bold")
                        cy += size * lead
                    cy += gap * 0.5
                    continue
            lines = self.wrap(it, width - 3, size)
            for i, ln in enumerate(lines):
                if i == 0 and it[:1] not in ("•",) and it[:2].strip() and not it[0].isdigit():
                    pass
                self.text(x + (0 if i == 0 else 3 if it[:1] in "•–-0123456789" else 0), cy + size, ln, size=size)
                cy += size * lead
            cy += gap
        return cy

    def table(self, x, y, cols, rows, size=1.9, header=True, row_h=None, fills=None, wrap=True):
        """cols: list of (title, width). rows: list of lists. Returns end y."""
        rh = row_h or size * 1.9
        cy = y
        widths = [c[1] for c in cols]
        tw = sum(widths)
        if header:
            self.rect(x, cy, tw, rh * 1.15, lw=0.25, fill="#e8e6e1")
            cx = x
            for (t, w) in cols:
                self.text(cx + 0.8, cy + rh * 0.8, t, size=size, weight="bold")
                cx += w
            cy += rh * 1.15
        for ri, r in enumerate(rows):
            # wrap cells
            cells = []
            nl = 1
            for (t, w), v in zip(cols, r):
                ls = self.wrap(v, w - 1.2, size) if wrap else [str(v)]
                cells.append(ls)
                nl = max(nl, len(ls))
            h = rh + (nl - 1) * size * 1.2
            if fills and ri in fills:
                self.rect(x, cy, tw, h, lw=0, fill=fills[ri])
            cx = x
            for (t, w), ls in zip(cols, cells):
                for li, ln in enumerate(ls):
                    self.text(cx + 0.8, cy + rh * 0.72 + li * size * 1.2, ln, size=size)
                cx += w
            self.line(x, cy + h, x + tw, cy + h, w=0.1, color="#777")
            cy += h
        # verticals + border
        cx = x
        for w in widths:
            self.line(cx, y, cx, cy, w=0.1, color="#777")
            cx += w
        self.rect(x, y, tw, cy - y, lw=0.3)
        return cy

    def north_arrow(self, cx, cy, r=6, rot=0):
        g = f'<g transform="rotate({rot} {cx} {cy})">'
        g += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#000" stroke-width="0.25"/>'
        g += f'<polygon points="{cx},{cy - r * 1.15} {cx + r * 0.38},{cy + r * 0.55} {cx},{cy + r * 0.25}" fill="#000"/>'
        g += f'<polygon points="{cx},{cy - r * 1.15} {cx - r * 0.38},{cy + r * 0.55} {cx},{cy + r * 0.25}" fill="#fff" stroke="#000" stroke-width="0.2"/>'
        g += '</g>'
        self.add(g)
        self.text(cx, cy - r * 1.35, "N", size=3, anchor="middle", weight="bold")

    def scale_bar(self, x, y, scale, length_m=None):
        if length_m is None:
            length_m = 5 if scale >= 50 else 2 if scale >= 20 else 1 if scale >= 10 else 0.5
        seg = 5 if length_m >= 5 else 4
        L = length_m * 1000 / scale
        for i in range(seg):
            self.rect(x + i * L / seg, y, L / seg, 1.2, lw=0.15, fill="#000" if i % 2 == 0 else "#fff")
        self.text(x, y + 3.6, "0", size=1.8, anchor="middle")
        self.text(x + L, y + 3.6, f"{_f(length_m)} m", size=1.8, anchor="middle")
        self.text(x + L / 2, y + 3.6, f"{_f(length_m / 2)}", size=1.8, anchor="middle")

    def frame(self):
        W, H = self.W, self.H
        self.rect(0, 0, W, H, lw=0, fill="#ffffff")
        self.rect(10, 5, W - 15, H - 10, lw=0.6)
        X = self.TB_X
        self.line(X, 5, X, H - 5, w=0.6)
        p = self.project
        x0 = X + 3
        w = W - 5 - X - 6
        y = 10
        self.text(x0, y + 1, p["name"], size=3.2, weight="bold")
        y += 5
        for ln in self.wrap(p["site"], w, 1.9):
            self.text(x0, y, ln, size=1.9)
            y += 2.6
        self.text(x0, y, "Client: " + p["client"], size=1.9)
        y += 2.6
        self.text(x0, y, p["by"], size=1.9)
        y += 3.4
        self.line(X, y, W - 5, y, w=0.3)
        # notes area
        y += 3
        notes = [
            ("B", "DRAWING NOTES"),
            "1. Do not scale from this drawing. Use figured dimensions only.",
            "2. All dimensions in millimetres; levels in metres relative to internal FFL ±0.000 (datum to be tied to site survey).",
            "3. Contractor to verify all dimensions, levels & existing structure on site before fabrication or ordering.",
            "4. Read with all other architectural, structural & services drawings and the specification notes (A-001).",
            "5. Structural members are preliminary: final design, connections & calculations by a licensed structural engineer to local code before construction.",
            "6. Report any discrepancy to the designer before proceeding.",
        ]
        y = self.textblock(x0, y, w, notes, size=1.65, gap=0.35)
        self.notes_end = y
        # revisions
        ry = 192
        self.line(X, ry - 4, W - 5, ry - 4, w=0.3)
        self.text(x0, ry, "REVISIONS", size=1.9, weight="bold")
        self.table(x0, ry + 1.5, [("Rev", 8), ("Date", 15), ("Description", w - 23)],
                   [["C01", p["date"], "Issued for construction / tender"],
                    ["P01", "05.10.2026", "Concept (client renders)"]], size=1.6)
        # status
        sy = 213
        self.rect(X, sy, W - 5 - X, 11, lw=0.3, fill="#111")
        for i, ln in enumerate(self.wrap(p["status"], w, 1.8)[:3]):
            self.text(x0, sy + 3.6 + i * 2.5, ln, size=1.8, weight="bold", color="#fff")
        # title fields
        ty = sy + 14
        self.text(x0, ty, "DRAWING TITLE", size=1.5, color="#555")
        tl = self.wrap(self.title, w, 3.0)
        for i, ln in enumerate(tl[:3]):
            self.text(x0, ty + 4.5 + i * 3.8, ln, size=3.0, weight="bold")
        fy = ty + 4.5 + 3 * 3.8 + 1
        self.line(X, fy, W - 5, fy, w=0.3)
        cw = (W - 5 - X) / 2
        fields = [("SCALE @ A3", self.scale_note), ("DATE", p["date"]),
                  ("DRAWN / CHECKED", "CC / —"), ("SERIES", self.series)]
        for i, (k, v) in enumerate(fields):
            cx = X + (i % 2) * cw
            cy = fy + (i // 2) * 8
            self.rect(cx, cy, cw, 8, lw=0.2)
            self.text(cx + 1.5, cy + 2.6, k, size=1.4, color="#555")
            self.text(cx + 1.5, cy + 6.5, v, size=2.2, weight="bold")
        ny = fy + 16
        self.rect(X, ny, W - 5 - X, H - 5 - ny, lw=0.3)
        self.text(x0, ny + 3, "DRAWING No.", size=1.4, color="#555")
        self.text(x0, ny + 13, self.number, size=7.5, weight="bold")
        self.text(W - 8, ny + 3, "REV", size=1.4, color="#555", anchor="end")
        self.text(W - 8, ny + 13, p["rev"], size=7.5, weight="bold", anchor="end")

    def svg(self):
        body = "\n".join(self.els)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}mm" height="{self.H}mm" '
                f'viewBox="0 0 {self.W} {self.H}"><defs>{_tile_defs()}</defs>\n{body}\n</svg>')


class View:
    """Model-space view placed on a sheet. Model mm, y-up. Paper = (x0,y0) + (m - origin)/scale."""

    def __init__(self, sheet, x0, y0, scale, origin=(0, 0), dxf=None, dxf_offset=(0, 0)):
        self.s = sheet
        self.x0, self.y0 = x0, y0
        self.k = 1.0 / scale
        self.scale = scale
        self.ox, self.oy = origin
        self.dxf = dxf  # ezdxf modelspace or None
        self.dxo = dxf_offset

    def P(self, x, y):
        return (self.x0 + (x - self.ox) * self.k, self.y0 - (y - self.oy) * self.k)

    def D(self, x, y):
        return (x + self.dxo[0], y + self.dxo[1])

    # ---------------------------------------------------------- drawing
    def line(self, x1, y1, x2, y2, w=0.25, color="#000", dash=None, layer="A-WALL"):
        a, b = self.P(x1, y1), self.P(x2, y2)
        self.s.line(a[0], a[1], b[0], b[1], w=w, color=color, dash=dash)
        if self.dxf is not None:
            self.dxf.add_line(self.D(x1, y1), self.D(x2, y2),
                              dxfattribs={"layer": layer, **({"linetype": "DASHED"} if dash else {})})

    def pl(self, pts, w=0.25, color="#000", fill="none", closed=True, dash=None, mat=None, layer="A-WALL",
           opacity=None):
        pp = [self.P(x, y) for x, y in pts]
        if mat:
            tint, hid = MAT[mat]
            self.s.poly(pp, w=0, fill=tint, closed=True, opacity=opacity)
            if hid:
                self.s.poly(pp, w=0, fill=f"url(#{hid})", closed=True)
            self.s.poly(pp, w=w, color=color, fill="none", closed=closed, dash=dash)
            if self.dxf is not None:
                try:
                    h = self.dxf.add_hatch(color=253 if not hid else 8, dxfattribs={"layer": "A-HATCH"})
                    if hid in ("h-conc", "h-rc", "h-masonry", "h-earth", "h-timber"):
                        pat = {"h-conc": "AR-CONC", "h-rc": "ANSI31", "h-masonry": "ANSI31",
                               "h-earth": "EARTH", "h-timber": "ANSI36"}[hid]
                        h.set_pattern_fill(pat, scale=max(1, self.scale / 10))
                    h.paths.add_polyline_path([self.D(x, y) for x, y in pts], is_closed=True)
                except Exception:
                    pass
        else:
            self.s.poly(pp, w=w, color=color, fill=fill, closed=closed, dash=dash, opacity=opacity)
        if self.dxf is not None:
            self.dxf.add_lwpolyline([self.D(x, y) for x, y in pts], close=closed,
                                    dxfattribs={"layer": layer, **({"linetype": "DASHED"} if dash else {})})

    def rect(self, x, y, dx, dy, **kw):
        self.pl([(x, y), (x + dx, y), (x + dx, y + dy), (x, y + dy)], **kw)

    def circle(self, cx, cy, r, w=0.25, color="#000", fill="none", dash=None, layer="A-WALL", mat=None):
        p = self.P(cx, cy)
        if mat:
            fill = MAT[mat][0]
        self.s.circle(p[0], p[1], r * self.k, w=w, color=color, fill=fill, dash=dash)
        if self.dxf is not None:
            self.dxf.add_circle(self.D(cx, cy), r, dxfattribs={"layer": layer})

    def arc(self, cx, cy, r, a0, a1, w=0.2, color="#000", dash=None, layer="A-DOOR"):
        n = max(8, int(abs(a1 - a0) / 5))
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.pl(pts, w=w, color=color, closed=False, dash=dash, layer=layer)

    def text(self, x, y, s, size=2.2, anchor="start", weight="normal", rot=0, color="#000", italic=False,
             layer="A-TEXT"):
        p = self.P(x, y)
        self.s.text(p[0], p[1], s, size=size, anchor=anchor, weight=weight, rot=-rot if rot else 0,
                    color=color, italic=italic)
        if self.dxf is not None:
            al = {"start": "LEFT", "middle": "CENTER", "end": "RIGHT"}[anchor]
            from ezdxf.enums import TextEntityAlignment
            t = self.dxf.add_text(str(s), height=size * self.scale * 0.72,
                                  dxfattribs={"layer": layer, "rotation": rot})
            t.set_placement(self.D(x, y), align=getattr(TextEntityAlignment, "BOTTOM_" + al
                            if al != "CENTER" else "BOTTOM_CENTER"))

    # ---------------------------------------------------------- annotation
    def dim(self, p1, p2, off, text=None, size=1.8, ext=True, color="#000", layer="A-DIMS", tick=True):
        """Linear dimension (horizontal if |dx|>=|dy| else vertical). off in paper mm (+ = up/left)."""
        (x1, y1), (x2, y2) = p1, p2
        horiz = abs(x2 - x1) >= abs(y2 - y1)
        o = off / self.k
        if horiz:
            yl = max(y1, y2) + o if off > 0 else min(y1, y2) + o
            a, b = (x1, yl), (x2, yl)
            if ext:
                g = 1.0 / self.k * (1 if off > 0 else -1)
                self.line(x1, y1 + g * 0.8, x1, yl + g * 0.9, w=0.12, color=color, layer=layer)
                self.line(x2, y2 + g * 0.8, x2, yl + g * 0.9, w=0.12, color=color, layer=layer)
        else:
            xl = min(x1, x2) - o if off > 0 else max(x1, x2) - o
            a, b = (xl, y1), (xl, y2)
            if ext:
                g = -1.0 / self.k * (1 if off > 0 else -1)
                self.line(x1 + g * 0.8, y1, xl + g * 0.9, y1, w=0.12, color=color, layer=layer)
                self.line(x2 + g * 0.8, y2, xl + g * 0.9, y2, w=0.12, color=color, layer=layer)
        self.line(a[0], a[1], b[0], b[1], w=0.13, color=color, layer=layer)
        L = math.hypot(x2 - x1, y2 - y1)
        if tick:
            for (tx, ty) in (a, b):
                pp = self.P(tx, ty)
                self.s.line(pp[0] - 0.9, pp[1] + 0.9, pp[0] + 0.9, pp[1] - 0.9, w=0.35, color=color)
        t = text if text is not None else f"{L:.0f}"
        pa, pb = self.P(*a), self.P(*b)
        mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        span = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
        tw = len(t) * size * 0.52
        if horiz:
            if tw + 1 > span:
                mx = max(pa[0], pb[0]) + tw / 2 + 1.2
            self.s.text(mx, my - 0.7, t, size=size, anchor="middle", color=color)
        else:
            if tw + 1 > span:
                my = min(pa[1], pb[1]) - tw / 2 - 1.2
            self.s.text(mx - 0.7, my, t, size=size, anchor="middle", rot=-90, color=color)
        if self.dxf is not None:
            from ezdxf.enums import TextEntityAlignment
            ang = 0 if horiz else 90
            tx = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            e = self.dxf.add_text(t, height=size * self.scale * 0.72, dxfattribs={"layer": layer, "rotation": ang})
            e.set_placement(self.D(*tx), align=TextEntityAlignment.BOTTOM_CENTER)

    def chain(self, coords, axis, at, off, size=1.8, overall=True, texts=None):
        """Chain of dims. axis 'x': coords are x values measured at y=at. axis 'y': y values at x=at."""
        cs = list(coords)
        for i in range(len(cs) - 1):
            t = texts[i] if texts else None
            if axis == "x":
                self.dim((cs[i], at), (cs[i + 1], at), off, text=t, size=size)
            else:
                self.dim((at, cs[i]), (at, cs[i + 1]), off, text=t, size=size)
        if overall and len(cs) > 2:
            o2 = off + (5 if off > 0 else -5)
            if axis == "x":
                self.dim((cs[0], at), (cs[-1], at), o2, size=size)
            else:
                self.dim((at, cs[0]), (at, cs[-1]), o2, size=size)

    def level(self, x, y, label, side="right", length=14, size=1.8, plan=False):
        """Elevation level marker at model (x,y). length in paper mm."""
        p = self.P(x, y)
        d = 1 if side == "right" else -1
        if plan:
            self.s.rect(p[0] - 0.9, p[1] - 0.9, 1.8, 1.8, lw=0.15, fill="#fff")
            self.s.line(p[0] - 0.9, p[1] - 0.9, p[0] + 0.9, p[1] + 0.9, w=0.15)
            self.s.line(p[0] - 0.9, p[1] + 0.9, p[0] + 0.9, p[1] - 0.9, w=0.15)
            self.s.text(p[0] + 1.4, p[1] - 0.8, label, size=size, weight="bold")
            return
        self.s.line(p[0], p[1], p[0] + d * length, p[1], w=0.15)
        tx = p[0] + d * length
        self.s.poly([(tx, p[1]), (tx - 1.1, p[1] - 1.8), (tx + 1.1, p[1] - 1.8)], w=0.15, fill="#fff")
        self.s.poly([(tx, p[1]), (tx - 1.1, p[1] - 1.8), (tx, p[1] - 1.8)], w=0, fill="#000")
        self.s.text(tx + d * 1.8, p[1] - 0.4, label, size=size, anchor="start" if d > 0 else "end")

    def leader(self, pts, lines, size=1.8, anchor=None, dot=False, w=0.13, maxw=None):
        """pts: model points, first = target, last = text anchor point."""
        pp = [self.P(*q) for q in pts]
        self.s.poly(pp, w=w, closed=False)
        tx, ty = pp[0]
        if dot:
            self.s.circle(tx, ty, 0.45, w=0, fill="#000")
        else:
            ang = math.atan2(pp[1][1] - ty, pp[1][0] - tx)
            a1 = ang + 0.3
            a2 = ang - 0.3
            self.s.poly([(tx, ty), (tx + 1.8 * math.cos(a1), ty + 1.8 * math.sin(a1)),
                         (tx + 1.8 * math.cos(a2), ty + 1.8 * math.sin(a2))], w=0, fill="#000")
        ex, ey = pp[-1]
        if anchor is None:
            anchor = "start" if pp[-1][0] >= pp[-2][0] else "end"
        dx = 0.8 if anchor == "start" else -0.8
        if isinstance(lines, str):
            lines = [lines]
        if maxw:
            ll = []
            for l in lines:
                ll += Sheet.wrap(l, maxw, size)
            lines = ll
        n = len(lines)
        y0 = ey - (n - 1) * size * 1.18 / 2 + size * 0.35
        for i, l in enumerate(lines):
            self.s.text(ex + dx, y0 + i * size * 1.18, l, size=size, anchor=anchor)

    def tag(self, x, y, label, shape="circle", r=2.2, size=1.9, fill="#fff", tcolor="#000"):
        p = self.P(x, y)
        if shape == "circle":
            self.s.circle(p[0], p[1], r, w=0.2, fill=fill)
        elif shape == "hex":
            pts = [(p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a))) for a in range(0, 360, 60)]
            self.s.poly(pts, w=0.2, fill=fill)
        elif shape == "diamond":
            self.s.poly([(p[0], p[1] - r), (p[0] + r, p[1]), (p[0], p[1] + r), (p[0] - r, p[1])], w=0.2, fill=fill)
        else:
            self.s.rect(p[0] - r * 1.3, p[1] - r * 0.8, r * 2.6, r * 1.6, lw=0.2, fill=fill)
        self.s.text(p[0], p[1] + size * 0.36, label, size=size, anchor="middle", weight="bold", color=tcolor)

    def section_mark(self, x1, y1, x2, y2, label, sheet_ref, flip=False):
        """Section cut line with heads. arrows point to the viewing direction (left of p1->p2 unless flip)."""
        a, b = self.P(x1, y1), self.P(x2, y2)
        self.s.line(a[0], a[1], b[0], b[1], w=0.35, dash="6,1.5,1,1.5")
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = (uy, -ux) if not flip else (-uy, ux)
        for (px, py) in (a, b):
            cx, cy = px - ux * 4 if (px, py) == a else px + ux * 4, py - uy * 4 if (px, py) == a else py + uy * 4
            self.s.circle(cx, cy, 3.2, w=0.25, fill="#fff")
            self.s.line(cx - 3.2, cy, cx + 3.2, cy, w=0.15)
            self.s.text(cx, cy - 0.6, label, size=2.2, anchor="middle", weight="bold")
            self.s.text(cx, cy + 2.3, sheet_ref, size=1.4, anchor="middle")
            self.s.poly([(cx + nx * 3.2 + ux * 2, cy + ny * 3.2 + uy * 2),
                         (cx + nx * 6.0, cy + ny * 6.0),
                         (cx + nx * 3.2 - ux * 2, cy + ny * 3.2 - uy * 2)], w=0, fill="#000")

    def grid(self, x1, y1, x2, y2, label, end="start", r=3.0):
        self.line(x1, y1, x2, y2, w=0.13, color="#666", dash="8,1.5,1.5,1.5", layer="A-GRID")
        px, py = (x1, y1) if end == "start" else (x2, y2)
        ox, oy = (x1 - x2, y1 - y2) if end == "start" else (x2 - x1, y2 - y1)
        L = math.hypot(ox, oy)
        p = self.P(px, py)
        ux, uy = ox / L, -oy / L
        cx, cy = p[0] + ux * r, p[1] + uy * r
        self.s.circle(cx, cy, r, w=0.25, fill="#fff")
        self.s.text(cx, cy + 1.0, label, size=2.8, anchor="middle", weight="bold")

    def title(self, x, y, num, name, scale_txt, sub=None):
        """View title at paper coords (x,y) top-left of title."""
        s = self.s
        s.circle(x + 4.5, y + 4, 4.2, w=0.35, fill="#fff")
        s.line(x + 0.3, y + 4, x + 8.7, y + 4, w=0.2)
        num_a, num_b = (num.split("/") + [""])[:2]
        s.text(x + 4.5, y + 3.2, num_a, size=2.6, anchor="middle", weight="bold")
        s.text(x + 4.5, y + 6.7, num_b, size=1.4, anchor="middle")
        s.text(x + 11, y + 3.4, name, size=3.0, weight="bold")
        s.line(x + 11, y + 4.5, x + 11 + max(60, len(name) * 1.7), y + 4.5, w=0.45)
        s.text(x + 11, y + 7.6, scale_txt + (("   " + sub) if sub else ""), size=1.8)


def break_line(view, x1, y1, x2, y2, w=0.18):
    """Zig-zag break line between model points."""
    a, b = view.P(x1, y1), view.P(x2, y2)
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    m = (a[0] + dx / 2, a[1] + dy / 2)
    pts = [a, (m[0] - ux * 1.5, m[1] - uy * 1.5), (m[0] - ux * 0.5 + nx * 2, m[1] - uy * 0.5 + ny * 2),
           (m[0] + ux * 0.5 - nx * 2, m[1] + uy * 0.5 - ny * 2), (m[0] + ux * 1.5, m[1] + uy * 1.5), b]
    view.s.poly(pts, w=w, closed=False)
