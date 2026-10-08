"""Rev C17 — OPTION C revised (client 08.10.2026): roof to the tall wall (no void), the TIP on the plants edge now ends
in line with the end of the AC box (it ran past it); the edge at the tall wall keeps its position (1.75); the raked angle
moves and the plants-edge beam carrying the columns is shorter. Loaded by build_c17.py (env C16_VK / C16_L / C16_TRI).

Agreed shape (one-sheet rounds C07..C11):
  * annex side wall and the low white garden wall are ONE line (y = 0); the roof's plants edge is on that line, so the
    roof is exactly the sketch: plants edge 3.22 + 1.26 = 4.48, void edge 3.22, raked edge 2.84, 0.90 m void kept open,
    void edge hung from the tall wall on 2 slim stainless hangers (rods);
  * existing planter 0.70 m wide inside the low wall (soil + white kerb, NO bushes), CONTINUING along the wall;
  * paved entry space 1.00 m between the facade and the planter's near-end kerb (walk in to the left glass door);
  * entrance opening runs to the side wall (no pier): glass door left, brown louvred slider right;
  * timber-clad columns C1 / C2 stand in the planter AGAINST the low wall and are fixed to it.
Axes: X along house/roof (house 0..8000, roof from 8000); Y across (annex side / garden wall line Y = 0,
tall wall face Y = 3440).
"""
import math
import os
import random
from cad import Sheet, View, break_line, PROJECT
from common import shrub, ground, vine, GREEN
from sheets_b import ladder, paving_cut, rhs, upn200, cchan
from axo import Axo, mbox

HOUSE_L, HOUSE_W, WALL = 8000, 2540, 200
STRIP = 900                          # passage to the lattice door (top strip in client sketch)
WALL_Y0 = HOUSE_W + STRIP            # 3440 face of TALL wall (main house, AC units) — top side
TW_T, TW_H = 250, 5000
LW = (0, 200)                        # low white garden wall, IN LINE with the annex side wall, h 1.40, round coping
LW_H = 1400
PL = (200, 750)                      # planter soil (inside the wall) — 0.55 soil, no bushes
KERB = (750, 900)                    # white stone kerb -> planter 0.70 wide from the wall's inner face
KERB_H = 250                         # kerb / soil level above paving
RET = (HOUSE_L - WALL, HOUSE_L)      # (no return wall any more: LW[1] > 0)
ENTRY = 1000                         # paved entry space between the facade and the planter's near-end kerb
GARDEN_X0 = HOUSE_L + ENTRY          # planter starts after the entry space ...
GARDEN_X1 = HOUSE_L + 9000           # ... and CONTINUES along the wall (drawn to the sheet edges)
GARDEN_OPEN_END = True               # no end kerb
CY = LW[1] + 100                     # columns: centre line against the wall's inner face (300)
ROOF_L = int(os.environ.get("C16_L", "2200"))   # roof length at the tall wall (max 2.20, before the AC box)
TRI = int(os.environ.get("C16_TRI", "1260"))   # triangular extension along the plants edge (same raked line)
AC_X = 8000 + 2260                   # existing AC box on the tall wall (verify) — the roof stops before it
RX0, RX1 = HOUSE_L, HOUSE_L + ROOF_L
TIP = RX1 + TRI                      # 12480
XM = RX0 + ROOF_L / 2
SOFFIT, FASCIA = 2360, 430
FTOP = SOFFIT + FASCIA
COL_TOP = FTOP + 130
HOUSE_TOP = 2920
BOS, TOS = SOFFIT + 50, SOFFIT + 250
POST, CLAD = 150, 200
ENTR = (LW[1], 2290)                 # ENTRANCE: opening runs to the side wall (no pier), 2.20 high
SLIDE_W = 1060                       # 2 brown louvred SLIDING shutter panels
SLIDES = [(ENTR[1] - SLIDE_W, ENTR[1], 0), (ENTR[1] - SLIDE_W - 60, ENTR[1] - 60, 1)]   # (y0, y1, track)
LATTICE = (HOUSE_W + 50, WALL_Y0 - 50)
HEAD = 2200
ROD_Z = BOS + 100
ROD_WALL_Z = 3050
RODS_X = [XM, RX1 - 150]
RED = "#c0392b"

COLS_R = [("C1", max(XM, GARDEN_X0 + 300), CY), ("C2", RX1 - 100, CY)]   # C1 clear of the near-end kerb
COLS_T = [("C1", RX0 + (ROOF_L + TRI) / 2, CY), ("C2", TIP - 600, CY)]       # C1 mid plants edge, C2 0.60 from tip

VAR = {
    "V1": dict(name="VERSION 1 — ROOF TO THE WALL", tag="V1 ROOF TO WALL", roof_d=WALL_Y0, rods=False,
               tri=False, cols=COLS_R,
               short="roof 3.22 x 3.44 up to the tall wall (bears on wall ledger + curved brackets); "
                     "2 columns on the plants side"),
    "V2": dict(name="VERSION 2 — 0.90 m VOID + 2 STEEL RODS", tag="V2 VOID + RODS", roof_d=HOUSE_W, rods=True,
               tri=False, cols=COLS_R,
               short=f"rectangular roof {ROOF_L / 1000:.2f} x 2.54 (max length {ROOF_L / 1000:.2f}, stops before the AC box); 0.90 m void left open; void edge tied to the tall wall with 2 slim "
                     "Ø16 stainless rods (rising ≈ 30°); 2 columns on the plants side"),
    "V1T": dict(name="VERSION 1T — TRIANGLE, ROOF TO THE WALL", tag="V1T TRIANGLE TO WALL", roof_d=WALL_Y0,
                rods=False, tri=True, cols=COLS_T,
                short="triangular roof: plants edge 3.22 + 1.26 = 4.48, wall edge 3.22, raked edge 3.66; "
                      "runs to the tall wall (ledger + brackets); 2 columns on the plants side"),
    "V2T": dict(name="VERSION 2T — TRIANGLE, 0.90 m VOID + 2 RODS", tag="V2T TRIANGLE + RODS", roof_d=HOUSE_W,
                rods=True, tri=True, cols=COLS_T,
                short=f"triangular roof, same angle: plants edge {ROOF_L / 1000:.2f} + 1.26 = {(ROOF_L + TRI) / 1000:.2f}, void edge {ROOF_L / 1000:.2f} (max, stops before the AC box), raked edge 2.84; 0.90 m "
                      "void open, 2 slim Ø16 stainless hangers to the tall wall; 2 columns against the garden wall"),
}
ORDER = ("V2T",)
REVS = [["C17", "08.10.2026", "Option C2: tip at the AC line, wall edge kept, angle + edge beam adjusted"],
        ["C16", "08.10.2026", "Roof supported by the tall wall, no void: C triangle / D rectangle 2.20"],
        ["C15", "08.10.2026", "Void edge max 2.20 (before the AC box): A triangle same angle / B rectangle 2.20"]]


# ===================================================================== geometry helpers
def xend(c):
    return TIP if c["tri"] else RX1


EDGE_Y = 0          # plants-side roof edge (Y); 0 = in line with the annex side (C02..C06)


def roof_poly(c):
    RD = c["roof_d"]
    return [(RX0, EDGE_Y), (xend(c), EDGE_Y), (RX1, RD), (RX0, RD)]


def rake_len(c):
    return math.hypot(TRI, c["roof_d"])


def tip_angle(c):
    return math.degrees(math.atan2(c["roof_d"], TRI))


def edge_x(c, y):
    """x of the free end edge (end edge or raked edge) at height y."""
    return TIP - TRI * y / c["roof_d"] if c["tri"] else RX1


def inset_x(c, y, k):
    """x of the line parallel to the free end edge, k mm inside it (normal distance), at height y."""
    if not c["tri"]:
        return RX1 - k
    return edge_x(c, y) - k * rake_len(c) / c["roof_d"]


def band(c, y0, y1, k0, k1, x_from=None):
    """Polygon between the inset lines k0 < k1 (from the free edge), y0..y1; or from x_from to inset k1."""
    if x_from is not None:
        return [(x_from, y0), (inset_x(c, y0, k1), y0), (inset_x(c, y1, k1), y1), (x_from, y1)]
    return [(inset_x(c, y0, k1), y0), (inset_x(c, y0, k0), y0), (inset_x(c, y1, k0), y1), (inset_x(c, y1, k1), y1)]


def project(vk):
    p = dict(PROJECT)
    p["rev"] = "C17"
    p["date"] = "08.10.2026"
    p["name"] = "COURTYARD ROOF — " + vk
    p["site"] = VAR[vk]["name"] + ": " + VAR[vk]["short"]
    p["status"] = "FOR CLIENT CHECK — option C revised: roof tip ends at the AC line; edge at the tall wall unchanged"
    p["revs"] = REVS
    return p


def M(v, px, py):
    """paper -> model for view v"""
    return (v.ox + (px - v.x0) * v.scale, v.oy - (py - v.y0) * v.scale)


def lab(v, tgt, px, py, lines, size=1.35):
    tp = v.P(*tgt)
    v.leader([tgt, M(v, px, py)], lines, size=size, anchor="start" if px >= tp[0] else "end")


def adim(v, p1, p2, off, text, size=1.5):
    """Aligned dimension between model points; off = paper mm, + to the left of p1->p2 (paper)."""
    a, b = v.P(*p1), v.P(*p2)
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = uy, -ux
    A = (a[0] + nx * off, a[1] + ny * off)
    B = (b[0] + nx * off, b[1] + ny * off)
    s = v.s
    sg = 1 if off > 0 else -1
    for (p, q) in ((a, A), (b, B)):
        s.line(p[0] + nx * 0.8 * sg, p[1] + ny * 0.8 * sg, q[0] + nx * 0.9 * sg, q[1] + ny * 0.9 * sg, w=0.12)
    s.line(A[0], A[1], B[0], B[1], w=0.13)
    for (tx, ty) in (A, B):
        s.line(tx - 0.9, ty + 0.9, tx + 0.9, ty - 0.9, w=0.35)
    ang = math.degrees(math.atan2(dy, dx))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    mx, my = (A[0] + B[0]) / 2 + nx * 0.8 * sg, (A[1] + B[1]) / 2 + ny * 0.8 * sg
    s.text(mx, my, text, size=size, anchor="middle", rot=ang)


def plants(v, x0, x1, y0, y1, seed=1, rmin=170, rmax=260):
    r = random.Random(seed)
    x = x0 + 250
    while x < x1 - 150:
        v.circle(x, (y0 + y1) / 2 + r.uniform(-80, 80), r.uniform(rmin, rmax), w=0.15, color=GREEN, fill="#cfe3c0")
        x += r.uniform(400, 560)


def col(v, x, y, lab_=None, lab_dy=-380):
    v.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.25, fill="#e7c79a")
    v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
    if lab_:
        v.tag(x, y + lab_dy, lab_, shape="circle", r=2.0, size=1.4)


def bracket(v, xface, zs, sgn, r=200):
    pts = [(xface, zs), (xface + sgn * r, zs)]
    for k in range(7):
        a = math.radians(90 * k / 6)
        pts.append((xface + sgn * (r - r * math.sin(a)), zs - r + r * math.cos(a)))
    v.pl(pts, w=0.25, fill="#c9d0d6")


def star(v, x, y, r=110, color="#2f6b2a"):
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    v.pl(pts, w=0.12, color=color, fill="#ffffff")


def planting_plan(v, x0, x1, cols=COLS_T):
    """P1 star jasmine (posts + wall @ 1.00), P2 pittosporum @ 0.60, P3 lavender/gaura @ 0.40, P4 erigeron @ 0.30, L1."""
    near = lambda x: any(abs(x - cx) < 280 for (_, cx, _) in cols)
    x = x0 + 450
    while x < x1 - 200:
        if not near(x):
            v.circle(x, 450, 230, w=0.15, color="#3f6b2e", fill="#d4e6c6")
        x += 600
    x = x0 + 300
    while x < x1 - 150:
        v.circle(x, 640, 80, w=0.12, color="#6d7f68", fill="#ffffff")
        x += 400
    x = x0 + 200
    while x < x1 - 100:
        v.circle(x, KERB[0] - 40, 45, w=0.1, color="#b07a90", fill="#fbe3ea")
        x += 300
    x = x0 + 500
    while x < x1 - 200:
        star(v, x, LW[1] + 70)
        x += 1000
    for (_, cx, cy) in cols:
        star(v, cx + 160, cy + 120, r=120)
        v.circle(cx, cy + 230, 55, w=0.15, color="#c27c0e", fill="#ffd27a")
    x = x0 + 600
    while x < x1 - 200:
        if not near(x):
            v.circle(x, LW[1] + 120, 45, w=0.15, color="#c27c0e", fill="#ffd27a")
        x += 1200


# ===================================================================== plan context
def site_plan(v, c, labels=True):
    """Plan in model coords: annex + low garden wall in one line (y = 0), planter inside the wall (continues),
    paved entry space at the door, passage + tall wall (top), roof."""
    RD = c["roof_d"]
    XR = xend(c) + 1500
    # outside (beyond the annex side / garden wall line)
    v.rect(-300, -650, XR + 300, 650, w=0, fill="#e9f0e1")
    # courtyard paving in front of the annex (incl. under the roof and the entry space)
    v.rect(RX0, LW[1], XR - RX0, WALL_Y0 - LW[1], w=0, fill="#f3eee4")
    for x in range(RX0 + 600, XR, 600):
        v.line(x, LW[1], x, WALL_Y0, w=0.05, color="#d9d1c2")
    for y in range(LW[1] + 600, WALL_Y0, 600):
        v.line(RX0, y, XR, y, w=0.05, color="#d9d1c2")
    # GARDEN: planter 0.70 inside the low wall, starts after the 1.00 entry space, continues
    gx1 = min(GARDEN_X1, XR)
    v.rect(GARDEN_X0, PL[0], gx1 - GARDEN_X0, PL[1] - PL[0], w=0.15, fill="#efe4d0", color="#bba")
    v.rect(GARDEN_X0, KERB[0], gx1 - GARDEN_X0, KERB[1] - KERB[0], w=0.3, fill="#f7f4ee")
    v.rect(GARDEN_X0, PL[0], 150, KERB[1] - PL[0], w=0.3, fill="#f7f4ee")                 # near-end kerb
    planting_plan(v, GARDEN_X0, gx1, c["cols"])
    v.rect(HOUSE_L, LW[1], ENTRY, KERB[1] - LW[1], w=0.3, dash="2,1", color=RED)           # paved entry space
    # low white garden wall: continues the annex side wall line
    v.rect(HOUSE_L, LW[0], XR - HOUSE_L, LW[1] - LW[0], mat="masonry", w=0.4)
    # tall wall (top)
    v.rect(-300, WALL_Y0, XR + 300, TW_T, mat="masonry", w=0.45)
    # annex
    v.rect(0, 0, HOUSE_L, HOUSE_W, mat="masonry", w=0.45)
    v.rect(WALL, WALL, HOUSE_L - 2 * WALL, HOUSE_W - 2 * WALL, w=0.3, fill="#fbfaf7")
    v.rect(HOUSE_L - WALL, ENTR[0], WALL, ENTR[1] - ENTR[0], w=0.15, fill="#fff")
    v.rect(HOUSE_L - 140, ENTR[0], 25, SLIDES[1][0] - ENTR[0] + 40, w=0.15, fill="#cfe3ef")   # glass door (left)
    v.rect(HOUSE_L - 110, SLIDES[1][0] - 40, 25, ENTR[1] - SLIDES[1][0] + 40, w=0.15, fill="#cfe3ef")
    # passage + lattice door
    v.rect(0, HOUSE_W, HOUSE_L, STRIP, w=0.1, fill="#f6f3ec", color="#bbb")
    v.rect(HOUSE_L - 120, LATTICE[0], 60, LATTICE[1] - LATTICE[0], w=0.25, fill="#b07a45")
    if labels:
        v.text(HOUSE_L / 2, 1350, "EXISTING ANNEX", size=2.3, anchor="middle", weight="bold", color="#555")
        v.text(HOUSE_L / 2, 950, "8.00 m long", size=1.8, anchor="middle", color="#777")
        v.text(HOUSE_L / 2, HOUSE_W + STRIP / 2 - 80, "PASSAGE 0.90 (lattice door at end)", size=1.5,
               anchor="middle", color="#555")
        v.text(6000, WALL_Y0 + TW_T + 120, "TALL HOUSE WALL (exist., AC units)", size=1.5, anchor="middle",
               weight="bold", color="#333")
        v.text(GARDEN_X0 + 100, -260, "▲ LOW WHITE GARDEN WALL — in line with the annex side wall", size=1.3,
               color="#333", weight="bold")
        v.text(GARDEN_X0 + 100, -520, "▲ PLANTER 0.70 inside the wall — P1 star jasmine on posts + wall wires, P2 / P3 / P4 low planting, L1 uplights — continues", size=1.3,
               color="#3f6b2e", weight="bold")
        v.text(2000, -400, "outside (exist.)", size=1.3, color="#6b8f5a")
    # roof
    poly = roof_poly(c)
    v.pl(poly, w=0, fill="#dfe5ea", opacity=0.7)
    for (a, b, tr) in SLIDES:                                                          # brown louvred slides
        v.rect(HOUSE_L + 10 + tr * 45, a, 35, b - a, w=0.25, fill="#6e5544")
    v.line(HOUSE_L + 5, ENTR[0] - 150, HOUSE_L + 5, ENTR[1] + 150, w=0.15, dash="1.5,0.8")
    v.pl(poly, w=0.5, dash="4,1.5")
    if labels:
        v.text(HOUSE_L + ENTRY / 2, (LW[1] + KERB[1]) / 2 + 40, "ENTRY 1.00", size=1.15, anchor="middle", color=RED,
               weight="bold")
        break_line(v, XR, LW[0] - 120, XR, KERB[1] + 120)
        v.text(XR - 100, KERB[1] + 180, "wall + planter continue →", size=1.15, anchor="end", color="#3f6b2e",
               weight="bold")
    if labels:
        v.text(HOUSE_L + 260, (SLIDES[1][0] + ENTR[1]) / 2, "brown slider", size=1.2, anchor="middle",
               rot=90, color="#5f4838", weight="bold")
    for (lb, x, y) in c["cols"]:
        col(v, x, y, lb if labels else None, lab_dy=1150)
    v.rect(AC_X, WALL_Y0 - 300, 800, 300, w=0.3, fill="#ffffff", dash="1.5,0.8")         # AC box (exist.)
    v.line(AC_X + 800, WALL_Y0 - 300, AC_X + 800, -420, w=0.2, dash="5,1,1,1", color=RED)    # AC end line = roof tip
    if labels:
        v.text(AC_X + 860, WALL_Y0 - 420, "◄ AC end = roof tip line", size=1.15, color=RED, weight="bold")
    if labels:
        v.text(AC_X + 400, WALL_Y0 - 200, "AC box", size=1.2, anchor="middle", weight="bold")
        v.text(AC_X, WALL_Y0 - 560, "◄ roof stops before the AC box", size=1.2, color=RED,
               weight="bold")
    if c["rods"]:
        for x in RODS_X:
            v.line(x, HOUSE_W - 60, x, WALL_Y0, w=0.4, color=RED)
            v.rect(x - 60, WALL_Y0, 120, 30, w=0.2, fill=RED)


# ===================================================================== SHEET 1: PLANS
def sheet_plans(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    XE = xend(c)
    s = Sheet(c.get("num", f"{vk}-01"), f"{c['tag']}\ntop view & roof framing", "1:50 / 1:30", project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color=RED)
    v = View(s, 40, 90, 50)
    site_plan(v, c)
    cx = RX0 + (ROOF_L if not c["tri"] else ROOF_L + TRI * 0.35) / 2
    v.text(cx, RD / 2 + 880, "ROOF", size=2.4, anchor="middle", weight="bold")
    v.text(cx, RD / 2 + 530, (f"{ROOF_L / 1000:.2f} x {RD / 1000:.2f} m" if not c["tri"] else
                              f"{ROOF_L / 1000:.2f} / {(ROOF_L + TRI) / 1000:.2f} x {RD / 1000:.2f} m"), size=1.9, anchor="middle")
    if c["rods"]:
        v.text(RX0 + 120, HOUSE_W + STRIP / 2 - 60, "0.90 VOID — 2 Ø16 SS rods to wall", size=1.4, color=RED,
               weight="bold")
    xs = [0, HOUSE_L, RX1] + ([TIP] if c["tri"] else [])
    v.chain(xs, "x", -650, -12, size=1.6)
    cs = [RX0] + [x for (_, x, _) in c["cols"]] + [XE]
    v.chain(cs, "x", -650, -5, size=1.4, overall=False)
    v.chain([LW[0], LW[1], KERB[1], HOUSE_W, WALL_Y0], "y", XE + 1200, -6, size=1.4, overall=False)
    v.chain([0, HOUSE_W, WALL_Y0], "y", XE + 1200, -12, size=1.6)
    if c["tri"]:
        adim(v, (TIP, 0), (RX1, RD), -4, f"{rake_len(c):.0f}", size=1.4)
        v.text(TIP + 150, 120, f"{tip_angle(c):.1f}°", size=1.4)
    v.title(40, 135, f"1/{vk}-01", "TOP VIEW — ANNEX, GARDEN & ROOF", "1:50 @ A3",
            sub="— annex + garden wall in one line; planter 0.70 continues; entry 1.00 at the door")
    # ---- framing plan 1:30
    w = View(s, 15 - (RX0 - 1000) / 30, 268, 30)
    w.rect(RX0 - 1000, 0, 1000, HOUSE_W, mat="masonry", w=0.4)
    w.text(RX0 - 500, HOUSE_W / 2, "ANNEX", size=1.8, anchor="middle", rot=90, color="#555")
    w.rect(RX0 - 1000, HOUSE_W, 1000, STRIP, w=0.1, fill="#f6f3ec", color="#bbb")
    w.rect(RX0 - 120, LATTICE[0], 60, LATTICE[1] - LATTICE[0], w=0.25, fill="#b07a45")
    w.rect(RX0 - 1000, WALL_Y0, XE - RX0 + 1300, 90, mat="masonry", w=0.35)
    w.pl(roof_poly(c), w=0.45, fill="#eef0f2")
    gx1 = min(GARDEN_X1, inset_x(c, KERB[1], 0))
    for yk in KERB:
        w.line(GARDEN_X0, yk, gx1, yk, w=0.25, dash="2,1", color="#3f6b2e")
    w.text(GARDEN_X0 + 100, KERB[1] + 60, "planter kerb below", size=1.2, color="#3f6b2e")
    w.line(RX0, LW[1], XE, LW[1], w=0.25, dash="2,1", color="#555")
    w.text(RX0 + 200, LW[1] - 150, "low garden wall below (roof edge on the wall line)", size=1.15, color="#555")
    beam = dict(w=0.35, fill="#7d8790")
    w.rect(RX0, 150, 75, HOUSE_W - 300, w=0.3, fill="#5c6670")                     # ledger on annex
    if RD > HOUSE_W:                                                               # trimmer over the passage
        w.rect(RX0, HOUSE_W - 150, 100, WALL_Y0 - 75 - (HOUSE_W - 150), w=0.3, fill="#7d8790")
        w.leader([(RX0 + 50, HOUSE_W + 450), (RX0 - 600, HOUSE_W + 250)], ["RHS trimmer over passage", "annex → wall ledger"],
                 size=1.2, anchor="end")
    if not c["tri"]:
        if RD > HOUSE_W:
            w.rect(RX0 + 75, WALL_Y0 - 75, ROOF_L - 75, 75, w=0.3, fill="#5c6670")  # ledger on tall wall
        w.rect(RX0 + 75, CY - 50, ROOF_L - 175, 100, **beam)                         # plants edge beam on C1/C2
        if RD == HOUSE_W:
            w.rect(RX0 + 75, RD - 150, ROOF_L - 175, 100, **beam)                    # void edge beam
        w.rect(RX1 - 150, 200, 100, RD - 350, **beam)                                # end beam
    else:
        w.pl(band(c, CY - 50, CY + 50, 0, 150, x_from=RX0 + 75), **beam)            # plants edge beam on C1/C2
        if RD > HOUSE_W:
            w.pl(band(c, WALL_Y0 - 75, WALL_Y0, 0, 150, x_from=RX0 + 75), w=0.3, fill="#5c6670")
            ytop = WALL_Y0 - 75
        else:
            w.pl(band(c, RD - 150, RD - 50, 0, 150, x_from=RX0 + 75), **beam)        # void edge beam
            ytop = RD - 50
        w.pl(band(c, 50, ytop, 50, 150), **beam)                                     # raked edge beam
    nj = 3 if RD < 3000 else 4
    for i in range(1, nj + 1):
        y = CY + 50 + (RD - CY - 200) * i / (nj + 1)
        if not c["tri"]:
            w.rect(RX0 + 75, y - 32, ROOF_L - 225, 65, w=0.2, fill="#c9d0d6")
        else:
            w.pl(band(c, y - 32, y + 32, 0, 150, x_from=RX0 + 75), w=0.2, fill="#c9d0d6")
    for (lb, x, y) in c["cols"]:
        w.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.3, fill="#e7c79a")
        w.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
        w.text(x - 130, y + 200, lb, size=1.5, anchor="end", weight="bold")
    if c["rods"]:
        for x in RODS_X:
            w.line(x, RD - 100, x, WALL_Y0, w=0.5, color=RED)
            w.rect(x - 60, WALL_Y0, 120, 40, w=0.2, fill=RED)
    w.chain(cs, "x", 0, -7, size=1.4, overall=not c["tri"])
    if c["tri"]:
        w.chain([RX0, RX1, TIP], "x", 0, -13, size=1.5)
        adim(w, (TIP, 0), (RX1, RD), -4, f"{rake_len(c):.0f}", size=1.4)
        w.chain([RX0, RX1], "x", RD, 4, size=1.4)
    yc = [0, LW[1], CY, HOUSE_W, WALL_Y0]
    w.chain(yc, "y", XE, -8, size=1.2, overall=False)
    s.text(160 if (c["tri"] and RD > HOUSE_W) else 16, 145.5, f"2/{vk}-01  ROOF FRAMING PLAN — 1:30", size=2.1,
           weight="bold")
    items = [("B", "THIS VERSION"), c["short"] + "."]
    if RD > HOUSE_W:
        items += ["Roof fixed to the annex end façade AND to the tall house wall (steel ledgers, resin anchors); "
                  "covers the passage in front of the lattice door (RHS trimmer over the passage, annex → wall ledger)."]
    else:
        items += ["Roof fixed to the annex end façade (ledger). The 0.90 m passage to the lattice door stays open.",
                  "Void edge hung from the tall house wall on 2 Ø16 stainless rods (turnbuckles, wall plates) — "
                  "slim, almost invisible."]
    if c["tri"]:
        cl = c["cols"]
        items += [f"Triangle to the tall wall: plants edge {(ROOF_L + TRI) / 1000:.2f} m — tip in line with the end of the AC box; edge at the tall wall {ROOF_L / 1000:.2f} m (unchanged); edge at the annex line {(edge_x(c, HOUSE_W) - RX0) / 1000:.2f} m; raked edge {rake_len(c) / 1000:.2f} m at "
                  f"{tip_angle(c):.1f}° to the plants edge.",
                  f"C1 in the middle of the {(ROOF_L + TRI) / 1000:.2f} edge ({(cl[0][1] - RX0) / 1000:.2f} from the façade); "
                  f"C2 0.60 m in from the tip (the tip cantilevers 0.60).",
                  "Joists run from the annex ledger to the raked edge beam (max. span ≈ 3.2 m); over the passage they bear on the RHS trimmer + wall ledger."]
    else:
        items += ["C1 just inside the planter (clear of the near-end kerb), C2 at the corner; roof 2.20 long along the tall wall — stops before the AC box."]
    items += [("B", "COMMON"),
              "Annex side wall and low white garden wall are ONE line; the roof's plants edge (fascia) is on it.",
              "Planter 0.70 inside the wall (soil + white kerb), continues along the wall; paved entry space 1.00 "
              "between the façade and the planter (walk in to the left glass door). Entrance opening runs to the "
              "side wall (no pier).",
              "C1 / C2: SHS 150 clad 200x200 thermo-ash, against the garden wall, 2 SS brackets each into the wall; "
              "edge beam on the column line, roof cantilevers 0.30 to the fascia over the wall.",
              "Underside +2.36, fascia 0.43 (top +2.79); columns 0.13 above roof. Falls 1:70 to the box gutter "
              "on the raked edge; rainwater down C2."]
    s.textblock(214, 146, 126, items, size=1.45, gap=0.25)
    s.text(214, 197, f"3/{vk}-01  3D — BIRD'S EYE (from outside, over the low garden wall)", size=1.8,
           weight="bold")
    axo_view(s, c, 214, 200, 338, 272, beta=44, elev=40)
    s.north_arrow(334, 140, 4.5)
    s.scale_bar(236, 280, 50)
    s.text(236, 278, "SCALE BAR 1:50 (top view)", size=1.3)
    return s


# ===================================================================== 3D VIEW
def render_axo(a, sheet, ox, oy, scale, mirror=False):
    """Axo painter render; foliage drawn as soft irregular blobs. mirror: screen x flipped (model built with -Y)."""
    k = 1.0 / scale
    sg = -1 if mirror else 1
    for layer, key, it in sorted(a.items, key=lambda t: (t[0], t[1])):
        if it[0] == "faces":
            _, faces, stroke, w = it
            for pts, fill in faces:
                if fill is None:
                    continue
                pp = []
                for (X, Y, Z) in pts:
                    sx, sy, _ = a.proj(X, Y, Z)
                    pp.append((ox + sg * sx * k, oy - sy * k))
                sheet.poly(pp, w=w, color=stroke, fill=fill)
        else:
            x, y, z, r, fill, stroke, flowers, seed, squash = it[1]
            sx, sy, _ = a.proj(x, y, z)
            cx, cy, rr = ox + sg * sx * k, oy - sy * k, r * k
            rnd = random.Random(seed)
            n = 18
            pts = []
            for i in range(n):
                t = 2 * math.pi * i / n
                f = 1 + rnd.uniform(-0.13, 0.13)
                pts.append((cx + math.cos(t) * rr * f, cy + math.sin(t) * rr * f * squash))
            sheet.poly(pts, w=0.15, color=stroke, fill=fill)
            sheet.poly([(cx - rr * 0.25 + (px - cx) * 0.55, cy - rr * 0.2 + (py - cy) * 0.55) for px, py in pts],
                       w=0, fill="#ffffff", opacity=0.22)
            for i in range(flowers):
                t = rnd.uniform(0, 2 * math.pi)
                q = rnd.uniform(0, 0.75)
                sheet.circle(cx + math.cos(t) * rr * q, cy + math.sin(t) * rr * q * squash, max(0.25, rr * 0.06),
                             w=0, fill="#f4f1e8")


def axo_view(s, c, bx0, by0, bx1, by1, beta=60, elev=36, eye=False):
    """3D. eye=True: from the courtyard paving at low angle, same direction as the site photo (built mirrored
    Y -> -Y so the +Y/+X faces show). eye=False: bird's eye from the plants side, over the low boundary wall."""
    RD = c["roof_d"]
    XE = xend(c)
    mir = eye
    XA, XR = (4200 if eye else 4600), max(XE, GARDEN_X1) + 900
    a = Axo(beta=beta, elev=elev)
    sy_ = -1 if mir else 1

    def B(x, y, z, dx, dy, dz, col, **kw):
        mbox(a, x, -(y + dy) if mir else y, z, dx, dy, dz, col, **kw)

    def P3(pts, fill, **kw):
        a.poly3([(x, sy_ * y, z) for (x, y, z) in pts], fill, **kw)

    def BL(x, y, z, r, **kw):
        a.blob(x, sy_ * y, z, r, **kw)

    # ground + paving joints
    P3([(XA - 800, LW[0], 0), (XR, LW[0], 0), (XR, WALL_Y0, 0), (XA - 800, WALL_Y0, 0)], "#efe9de", layer=0, w=0.1)
    for x in range(RX0 + 600, XR, 600):
        P3([(x, KERB[1], 1), (x + 10, KERB[1], 1), (x + 10, WALL_Y0, 1), (x, WALL_Y0, 1)], "#dcd3c2",
           stroke="#dcd3c2", w=0.02, layer=0.5)
    for y in range(KERB[1] + 600, WALL_Y0, 600):
        P3([(RX0, y, 1), (XR, y, 1), (XR, y + 10, 1), (RX0, y + 10, 1)], "#dcd3c2", stroke="#dcd3c2", w=0.02,
           layer=0.5)
    # existing trees — background only
    if mir:
        for i, x in enumerate(range(XA + 300, XR - 600, 1700)):
            BL(x, LW[0] - 1800, 3300 + (i % 2) * 500, 1150, fill="#b7d1a3", stroke="#6b8f5a", layer=0.2, seed=i)
        for i, y in enumerate((300, 1900)):
            BL(XA - 1600, y, 3900 + i * 300, 1200, fill="#b7d1a3", stroke="#6b8f5a", layer=0.2, seed=7 + i)
    else:
        for i, x in enumerate(range(XA + 700, XR, 1900)):
            BL(x, WALL_Y0 + 1300, 4300 + (i % 2) * 350, 950, fill="#b7d1a3", stroke="#6b8f5a", layer=1, seed=i)
        for i, y in enumerate((-200, 1400)):
            BL(XA - 1300, y, 3500 + i * 250, 950, fill="#b7d1a3", stroke="#6b8f5a", layer=1, seed=7 + i)
    # tall house wall (+ AC unit)
    if mir:      # courtyard face as backdrop
        P3([(XA - 800, WALL_Y0, 0), (XR, WALL_Y0, 0), (XR, WALL_Y0, 4300), (XA - 800, WALL_Y0, 4300)], "#cf9d80",
           layer=0.3, w=0.15)
        P3([(XA - 800, WALL_Y0, 4300), (XR, WALL_Y0, 4300), (XR, WALL_Y0 + TW_T, 4300),
            (XA - 800, WALL_Y0 + TW_T, 4300)], "#e2b9a0", layer=0.31, w=0.15)
        P3([(6200, WALL_Y0 - 1, 2900), (7000, WALL_Y0 - 1, 2900), (7000, WALL_Y0 - 1, 3500), (6200, WALL_Y0 - 1, 3500)],
           "#f2f2f2", layer=0.32, w=0.15)
    else:
        B(XA - 800, WALL_Y0, 0, XR - XA + 800, TW_T, 4300, "#d9ab8f", layer=1.5, w=0.15)
        B(6200, WALL_Y0 - 300, 2900, 800, 300, 600, "#f2f2f2", layer=1.6)
    # annex + lattice door + entrance (brown louvred sliders + glass behind)
    B(XA, 0, 0, HOUSE_L - XA, HOUSE_W, HOUSE_TOP, "#f3efe8", layer=2, w=0.2)
    B(HOUSE_L - 120, LATTICE[0], 0, 60, LATTICE[1] - LATTICE[0], HEAD, "#b07a45", layer=2.5 if mir else 1.7)
    X = HOUSE_L + 1
    P3([(X, ENTR[0], 0), (X, ENTR[1], 0), (X, ENTR[1], HEAD), (X, ENTR[0], HEAD)], "#2b2f33", layer=3)
    mid = (ENTR[0] + ENTR[1]) / 2
    P3([(X + 1, ENTR[0] + 40, 0), (X + 1, mid, 0), (X + 1, mid, HEAD - 40), (X + 1, ENTR[0] + 40, HEAD - 40)],
       "#cfe3ef", layer=3.1)
    B(HOUSE_L, ENTR[0] - 40, HEAD, 100, ENTR[1] - ENTR[0] + 80, 40, "#8a8a8a", layer=3.2)
    for (y0, y1, tr) in sorted(SLIDES, key=lambda q: q[2]):
        x0 = HOUSE_L + 10 + tr * 45
        B(x0, y0, 10, 35, y1 - y0, HEAD - 10, "#6e5544" if tr == 0 else "#5f4838", layer=3.3 + tr * 0.1)
        for z in range(120, HEAD - 60, 110):
            P3([(x0 + 36, y0 + 30, z), (x0 + 36, y1 - 30, z), (x0 + 36, y1 - 30, z + 18), (x0 + 36, y0 + 30, z + 18)],
               "#3b2c22", stroke="#3b2c22", w=0.03, layer=3.35 + tr * 0.1)
    # GARDEN: planter in front of the facade, left of the door; kerb in line with the door jamb (under the roof)
    wl = 1 if mir else 4.6                                  # boundary + return wall: far side / near side
    wx0 = RET[0] if LW[1] < 0 else HOUSE_L                 # wall in line with the annex side: no return
    B(wx0, LW[0], 0, XR - wx0, LW[1] - LW[0], LW_H, "#f1ede6", layer=wl, w=0.2)
    if LW[1] < 0:
        B(RET[0], LW[1], 0, RET[1] - RET[0], 0 - LW[1], LW_H, "#f1ede6", layer=wl - 0.05, w=0.2)
    B(GARDEN_X0, PL[0], 0, GARDEN_X1 - GARDEN_X0, PL[1] - PL[0], KERB_H - 30, "#7d5f42", layer=4)
    B(GARDEN_X0, KERB[0], 0, GARDEN_X1 - GARDEN_X0, KERB[1] - KERB[0], KERB_H, "#f4f1ea", layer=4.1 if mir else 4.05,
      w=0.2)
    if not GARDEN_OPEN_END:
        B(GARDEN_X1 - 150, PL[0], 0, 150, KERB[1] - PL[0], KERB_H, "#f4f1ea", layer=4.2, w=0.2)
    if GARDEN_X0 > HOUSE_L:                                 # near-end kerb: paved entry space at the door
        B(GARDEN_X0, PL[0], 0, 150, KERB[1] - PL[0], KERB_H, "#f4f1ea", layer=4.15, w=0.2)
    # roof: side fascias first (back-facing ones end up under the top), then the top
    poly = roof_poly(c)
    ey = EDGE_Y
    P3([(RX0, ey, SOFFIT), (XE, ey, SOFFIT), (XE, ey, FTOP), (RX0, ey, FTOP)], "#ffffff", w=0.3, layer=5.95)
    P3([(XE, ey, SOFFIT), (RX1, RD, SOFFIT), (RX1, RD, FTOP), (XE, ey, FTOP)], "#f2f3f4", w=0.3, layer=5.96)
    if RD < WALL_Y0:
        P3([(RX0, RD, SOFFIT), (RX1, RD, SOFFIT), (RX1, RD, FTOP), (RX0, RD, FTOP)], "#ffffff", w=0.3, layer=5.94)
    P3([(x_, y_, FTOP) for (x_, y_) in poly], "#e3e8ec", w=0.3, layer=6)
    for (lb, xc, yc) in c["cols"]:
        for sgn in (-1, 1):
            xf = xc + sgn * CLAD / 2
            if (sgn > 0 and xf > XE - 250) or (sgn < 0 and xf < RX0 + 250):
                continue
            arc = [(xf + sgn * (200 - 200 * math.sin(math.radians(90 * k_ / 8))), yc,
                    SOFFIT - 200 + 200 * math.cos(math.radians(90 * k_ / 8))) for k_ in range(9)]
            P3([(xf, yc, SOFFIT), (xf + sgn * 200, yc, SOFFIT)] + arc, "#c9d0d6", w=0.15, layer=6.5)
        B(xc - CLAD / 2, yc - CLAD / 2, 0, CLAD, CLAD, COL_TOP, "#c99a62", layer=6.6, w=0.2)
    if c["rods"]:
        rl = 7 if mir else 5.5                              # near side (courtyard view) / behind the roof edge
        for xr in RODS_X:
            P3([(xr, RD, ROD_Z), (xr, WALL_Y0, ROD_WALL_Z), (xr, WALL_Y0, ROD_WALL_Z + 50), (xr, RD, ROD_Z + 50)],
               RED, stroke=RED, w=0.25, layer=rl)
            P3([(xr - 100, WALL_Y0 - 15, ROD_WALL_Z - 100), (xr + 100, WALL_Y0 - 15, ROD_WALL_Z - 100),
                (xr + 100, WALL_Y0 - 15, ROD_WALL_Z + 100), (xr - 100, WALL_Y0 - 15, ROD_WALL_Z + 100)],
               "#b03a2e", layer=rl + 0.1)

    # fit into the box
    sg = -1 if mir else 1
    pts = []
    for _, _, it in a.items:
        if it[0] == "faces":
            for fp, _ in it[1]:
                pts += [(sg * a.proj(*q)[0], a.proj(*q)[1]) for q in fp]
        else:
            x_, y_, z_, r = it[1][:4]
            sx, sy, _ = a.proj(x_, y_, z_)
            pts += [(sg * sx - r, sy - r), (sg * sx + r, sy + r)]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    scale = max((maxx - minx) / (bx1 - bx0), (maxy - miny) / (by1 - by0))
    k = 1 / scale
    ox = bx0 + ((bx1 - bx0) - (maxx - minx) * k) / 2 - minx * k
    oy = by1 - ((by1 - by0) - (maxy - miny) * k) / 2 + miny * k
    render_axo(a, s, ox, oy, scale, mirror=mir)

    def tp(X_, Y_, Z_):
        sx, sy, _ = a.proj(X_, sy_ * Y_, Z_)
        return ox + sg * sx * k, oy - sy * k

    def note(pt, txt, size=1.45, anchor="middle", color="#1f4e79", weight="bold"):
        s.text(pt[0], pt[1], txt, size=size, anchor=anchor, color=color, weight=weight)

    for (lb, xc, yc) in c["cols"]:
        note(tp(xc, yc, COL_TOP + 220), lb, size=1.5, color="#000")
    if eye:
        p0 = tp(GARDEN_X1 - 900, KERB[1], KERB_H)
        p1 = (p0[0] - 6, p0[1] + 9)
        s.line(p0[0], p0[1], p1[0], p1[1], w=0.15, color="#3f6b2e")
        s.circle(p0[0], p0[1], 0.5, w=0, fill="#3f6b2e")
        note((p1[0], p1[1] + 2.4), "garden kerb — runs UNDER the roof edge", anchor="middle", color="#3f6b2e")
        note(tp(HOUSE_L + 60, (ENTR[0] + ENTR[1]) / 2 + 300, HEAD + 450), "door + brown sliders", size=1.3,
             color="#5f4838")
    else:
        note(tp((RX0 + RX1) / 2, RD, FTOP + 150), f"{ROOF_L / 1000:.2f}")
        note(tp((RX0 + XE) / 2, -1500, 0), "plants edge " + (f"{(ROOF_L + TRI) / 1000:.2f}" if c["tri"] else f"{ROOF_L / 1000:.2f}"),
             size=1.4)
        if c["tri"]:
            note(tp(TIP + 250, -250, SOFFIT - 300), "tip at the AC line", size=1.4, anchor="start")
        if RD < WALL_Y0:
            note(tp(RX1 + 900, WALL_Y0, ROD_WALL_Z + 750), "0.90 void + 2 rods", size=1.35, anchor="start",
                 color="#222")
        p0 = tp(GARDEN_X0 + 400, LW[0], LW_H)
        note((p0[0] - 3, p0[1] + 4), "garden (planter) under the roof edge ►", size=1.35, anchor="end",
             color="#3f6b2e")


# ===================================================================== SHEET 2: VIEWS + 3D
def sheet_views(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    XE = xend(c)
    s = Sheet(f"{vk}-02", f"{c['tag']}\nviews, section & 3D view", "1:50", project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color=RED)
    # ---- 1: view towards annex façade, same direction as the site photo (plants LEFT). u = Y
    e = View(s, 66, 134, 50)
    for k_, tx in enumerate((-700, 600, 1800)):                    # background trees: beyond the annex only
        e.circle(tx, HOUSE_TOP + 1450 + (k_ % 2) * 200, 650, w=0.15, color="#7fa86a", fill="#e9f2e1")
    e.text(600, HOUSE_TOP + 2350, "existing trees (background)", size=1.3, anchor="middle", color="#6b8f5a")
    ground(e, -600, WALL_Y0 + TW_T + 200, 0, depth=200)
    e.rect(WALL_Y0, 0, TW_T, 4300, w=0.4, fill="#c98b6b")
    break_line(e, WALL_Y0, 4300, WALL_Y0 + TW_T, 4300)
    e.rect(WALL_Y0 - 300, 2900, 300, 600, w=0.2, fill="#f2f2f2")
    e.text(WALL_Y0 - 150, 3150, "AC", size=1.2, anchor="middle")
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
    e.rect(400, HOUSE_TOP, 1600, 1000, w=0.15, dash="2,1", color="#888")
    e.text(1500, HOUSE_TOP + 150, "solar heater / AC (exist.)", size=1.2, anchor="middle", color="#888")
    e.rect(0, SOFFIT, RD, FASCIA, w=0.45, fill="#ffffff")
    # garden (planter) in FRONT of the facade, left of the door, partly under the roof
    e.rect(CY - CLAD / 2, 0, CLAD, COL_TOP, w=0.35, mat="timber")
    bracket(e, CY + CLAD / 2, SOFFIT, 1)
    e.text(CY + 120, COL_TOP + 100, "C2 (C1 behind)", size=1.3, anchor="start", weight="bold")
    e.rect(PL[0], 0, KERB[1] - PL[0], KERB_H, w=0.3, fill="#f4f1ea")                # planter (continues, cut)
    shrub(e, 470, KERB_H, 420, 480, seed=91)
    shrub(e, 660, KERB_H, 160, 420, seed=92, flowers=6)
    vine(e, CY + CLAD / 2 + 25, KERB_H, SOFFIT - 20, seed=93, amp=35)
    e.rect(LW[0], 0, LW[1] - LW[0], LW_H, mat="masonry", w=0.35)                    # low garden wall (cut)
    lab(e, (KERB[1] - 20, KERB_H - 40), 82, 152, ["planter 0.70 inside the low wall (continues) —",
                                                  "1.00 paved entry space at the door, C1 / C2 against the wall"],
        size=1.3)
    if c["rods"]:
        e.line(HOUSE_W - 60, ROD_Z, WALL_Y0, ROD_WALL_Z, w=0.5, color=RED)
        e.rect(WALL_Y0 - 20, ROD_WALL_Z - 70, 20, 140, w=0.2, fill=RED)
    e.chain([LW[0], LW[1], KERB[1], HOUSE_W, WALL_Y0], "x", 0, -7, size=1.3)
    ladder(e, WALL_Y0 + TW_T, [(0, "±0.000"), (HEAD, "+2.200"), (SOFFIT, "+2.360"), (FTOP, "+2.790"),
                               (COL_TOP, "+2.920")], 152, size=1.3, inside=False)
    lab(e, (ENTR[1] - 400, 900), 158, 112,
        ["Entrance (as site photo):", "brown louvred SLIDING", "shutters, 2 panels on top", "track + glass slider behind"],
        size=1.3)
    s.text(16, 26, f"1/{vk}-02  VIEW TO ANNEX FAÇADE (as site photo) — 1:50", size=1.9, weight="bold")

    # ---- 2: plants-side elevation along X (viewer on the plants side), X to the right
    xo = 4000 if not c["tri"] else 5200
    p = View(s, 22, 234, 50, origin=(xo, 0))
    p.rect(xo, 0, XE + 500 - xo, 3400, w=0.2, fill="#efdfd4")                      # tall wall beyond (background)
    break_line(p, xo, 3400, XE + 500, 3400)
    p.text(XE + 450, 3150, "tall house wall beyond", size=1.2, anchor="end", color="#8a6a5a")
    ground(p, xo, XE + 500, 0, depth=200)
    p.rect(xo, 0, HOUSE_L - xo, HOUSE_TOP, w=0.4, fill="#f7f3ea")
    break_line(p, xo, 0, xo, HOUSE_TOP)
    p.rect(GARDEN_X0, 0, XE + 500 - GARDEN_X0, KERB_H, w=0.25, fill="#cdb79a")       # planter (soil), continues
    p.rect(GARDEN_X0, 0, 150, KERB_H, w=0.3, fill="#f4f1ea")
    for i, x in enumerate(range(GARDEN_X0 + 450, XE + 300, 600)):
        if all(abs(x - cx) > 280 for (_, cx, _) in c["cols"]):
            shrub(p, x, KERB_H, 460, 420 + (i % 2) * 80, seed=150 + i, flowers=3)
    for (lb, x, y) in c["cols"]:
        vine(p, x - 70, KERB_H, SOFFIT - 20, seed=int(x) % 17, amp=45)
        vine(p, x + 70, KERB_H, SOFFIT - 20, seed=int(x) % 13 + 3, amp=45)
    p.rect(RX0, SOFFIT, XE - RX0, FASCIA, w=0.45, fill="#ffffff")
    for (lb, x, y) in c["cols"]:
        p.rect(x - CLAD / 2, 0, CLAD, COL_TOP, w=0.35, mat="timber")
        p.text(x, COL_TOP + 100, lb, size=1.4, anchor="middle", weight="bold")
        for sg in (-1, 1):
            if x + sg * CLAD / 2 < XE - 10:
                bracket(p, x + sg * CLAD / 2, SOFFIT, sg)
    p.chain([RX0] + [x for (_, x, _) in c["cols"]] + [XE] if c["tri"] else [RX0, XM, RX1], "x", 0, -7, size=1.35)
    p.dim((XE, 0), (XE, SOFFIT), -4, size=1.3)
    p.dim((XE, SOFFIT), (XE, FTOP), -4, size=1.3)
    p.rect(HOUSE_L, 0, XE + 500 - HOUSE_L, LW_H, w=0.25, dash="2.5,1.2", color="#555")   # garden wall in front
    p.text(HOUSE_L + 120, LW_H + 80, "low garden wall in front (dashed) — in line with the annex side", size=1.2,
           color="#555")
    lab(p, (GARDEN_X0 + 500, KERB_H + 300), 84, 163, ["planter 0.70 (continues) behind the wall; 1.00 entry "
                                                      "space at the door; C1 + C2 against the wall"], size=1.3)
    s.text(16, 158, f"2/{vk}-02  PLANTS-SIDE ELEVATION — C1 + C2 — 1:50" +
           (f"   (plants edge {ROOF_L / 1000:.2f} + 1.26 = {(ROOF_L + TRI) / 1000:.2f})" if c["tri"] else ""), size=1.9, weight="bold")

    # ---- 3: section across at C1 (1:50 overview — refined at 1:25 on sheet -03)
    def u(y):
        return WALL_Y0 + TW_T - y
    w = View(s, 214, 124, 50)
    paving_cut(w, [(u(WALL_Y0), -15), (u(KERB[1]), -15)], z_bottom_extra=150, joints=False)
    w.rect(u(WALL_Y0 + TW_T), -300, TW_T, 4300, w=0.35, mat="masonry")
    w.rect(u(PL[1]), -300, PL[1] - PL[0], KERB_H - 30 + 300, w=0.15, mat="soil")       # planter (cut)
    w.rect(u(KERB[1]), -150, KERB[1] - KERB[0], KERB_H + 150, w=0.3, fill="#f4f1ea")  # kerb (cut)
    shrub(w, u(500), KERB_H, 380, 480, seed=131)
    vine(w, u(CY + CLAD / 2 + 25), KERB_H, SOFFIT - 20, seed=132, amp=30)
    w.rect(u(LW[1]), -300, LW[1] - LW[0], LW_H + 300, w=0.3, mat="masonry")         # boundary wall (cut)
    w.rect(u(RD), SOFFIT, RD, FASCIA, w=0.35, fill="#e6eaee")
    w.rect(u(CY + CLAD / 2), 0, CLAD, COL_TOP, w=0.3, mat="timber")
    bracket(w, u(CY + CLAD / 2), SOFFIT, -1)
    w.rect(u(0), -300, 500, 300, w=0.1, mat="earth")
    if RD > HOUSE_W:
        bracket(w, u(WALL_Y0), SOFFIT + 50, 1, r=180)
    if c["rods"]:
        w.line(u(RD - 100), ROD_Z, u(WALL_Y0), ROD_WALL_Z, w=0.45, color=RED)
    ladder(w, u(WALL_Y0 + TW_T), [(0, "±0.000"), (SOFFIT, "+2.360"), (FTOP, "+2.790")], 210, size=1.3,
           inside=False)
    cc = [u(WALL_Y0)] + ([u(RD)] if RD < WALL_Y0 else []) + [u(KERB[1]), u(LW[1]), u(LW[0])]
    w.chain(cc, "x", -300, -4, size=1.2, overall=False)
    lab(w, (u(650), KERB_H - 60), 300, 112, ["planter 0.70 inside the wall:", "P1 jasmine on C1, P2/P3", "low planting, L1 uplights"],
        size=1.25)
    s.text(200, 26, f"3/{vk}-02  SECTION ACROSS AT C1 — 1:50 (refined: {vk}-03)", size=1.9, weight="bold")
    s.text(200, 30, "tall wall left — garden wall right", size=1.4)

    # ---- 4: 3D
    s.text(200, 150, f"4/{vk}-02  3D — EYE LEVEL, SAME DIRECTION AS THE SITE PHOTO", size=1.9, weight="bold")
    axo_view(s, c, 200, 156, 338, 284, beta=70, elev=12, eye=True)

    s.textblock(16, 255, 178, [("B", "NOTES"), VAR[vk]["short"] + ".",
                               "Underside +2.36, fascia 0.43 (top +2.79); columns 0.13 above roof.",
                               "Annex side wall + low garden wall in one line (roof edge on it). Planter 0.70 inside "
                               "the wall, continues; 1.00 paved entry space at the door; C1 + C2 against the wall. "
                               "Trees are existing, in the background.",
                               "Refined roof section & details: sheet " + vk + "-03."], size=1.45, gap=0.3)
    return s


# ===================================================================== SHEET 3: ROOF SECTION & DETAILS
def roof_layers_y(v, ua, ub, z_top=TOS):
    v.rect(ua, z_top + 38, ub - ua, 18, w=0.15, fill="#d9b98a")
    v.line(ua, z_top + 58, ub, z_top + 58, w=0.45, color="#111")
    v.rect(ua, SOFFIT, ub - ua, 20, w=0.12, mat="timber")
    v.rect(ua, SOFFIT + 20, ub - ua, 30, w=0.08, fill="#c9a77c")


def fin(v, x, z, h=120, b=12):
    v.rect(x - b / 2, z - h / 2, b, h, w=0.2, fill="#444")


def corner_plan(s, c, vk):
    """D3: plan of the free corner at C2 (rect: square corner; tri: acute tip) — 1:15."""
    RD = c["roof_d"]
    XE = xend(c)
    x_l = XE - 980
    q = View(s, 222, 280, 15, origin=(x_l, 0))
    ytop = 1080
    # roof edge + fascia
    q.pl([(x_l, 0), (XE, 0), (edge_x(c, ytop), ytop), (x_l, ytop)], w=0, fill="#f1f3f5")
    q.pl([(x_l, 0), (XE, 0), (edge_x(c, ytop), ytop)], w=0.55, closed=False)
    q.pl([(x_l, 25), (inset_x(c, 25, 25), 25), (inset_x(c, ytop, 25), ytop)], w=0.18, closed=False)
    break_line(q, x_l, -60, x_l, ytop + 40)
    gx1 = min(GARDEN_X1, inset_x(c, KERB[1], 0))
    if gx1 > x_l:
        for yk in KERB:
            q.line(x_l, yk, gx1, yk, w=0.25, dash="2,1", color="#3f6b2e")
        q.text(x_l + 40, KERB[1] + 25, "planter kerb below", size=1.1, color="#3f6b2e")
    q.rect(x_l, LW[0], XE + 60 - x_l, LW[1] - LW[0], w=0.2, dash="2,1", color="#555", fill="none")
    q.text(x_l + 40, LW[1] + 30, "low garden wall below", size=1.1, color="#555")
    # beams (RHS 200x100 in plan = 100 wide)
    q.pl(band(c, CY - 50, CY + 50, 0, 150, x_from=x_l), w=0.3, fill="#9aa3ab")
    yb = 50 if c["tri"] else CLAD
    q.pl(band(c, yb, ytop, 50, 150), w=0.3, fill="#9aa3ab")
    q.pl(band(c, CY - 44, CY + 44, 0, 156, x_from=x_l + 6), w=0.1, fill="#e9ecef")
    q.pl(band(c, yb + 6, ytop, 56, 144), w=0.1, fill="#e9ecef")
    nj = 3 if RD < 3000 else 4
    y1 = CY + 50 + (RD - CY - 200) / (nj + 1)
    q.pl(band(c, y1 - 32, y1 + 32, 0, 150, x_from=x_l), w=0.2, fill="#c9d0d6")
    # concealed box gutter (above the beams) along the free edge; side outlet into C2 (post runs on above roof)
    cx2 = c["cols"][-1][1]
    if c["tri"]:
        g = [(cx2 - 40, 25), (inset_x(c, 25, 25), 25), (inset_x(c, ytop, 25), ytop),
             (inset_x(c, ytop, 145), ytop), (inset_x(c, 145, 145), 145), (cx2 - 40, 145)]
    else:
        g = [(inset_x(c, CLAD, 25), CLAD), (inset_x(c, ytop, 25), ytop), (inset_x(c, ytop, 145), ytop),
             (inset_x(c, CLAD, 145), CLAD)]
    q.pl(g, w=0.3, dash="2,0.8", color="#1f6fb2", closed=True)
    for yy in (ytop - 250, ytop - 650):
        xa = inset_x(c, yy, 85)
        xb = inset_x(c, yy - 220, 85)
        q.line(xa, yy, xb, yy - 220, w=0.25, color="#1f6fb2")
        q.pl([(xb, yy - 220), (xb - 15, yy - 170), (xb + 15, yy - 170)], w=0, fill="#1f6fb2")
    # C2: cladding + SHS + downpipe inside + side spigot from the gutter through the SHS wall
    q.rect(cx2 - CLAD / 2, CY - CLAD / 2, CLAD, CLAD, w=0.3, mat="timber")
    q.rect(cx2 - POST / 2, CY - POST / 2, POST, POST, w=0.3, fill="#5c6670")
    q.rect(cx2 - POST / 2 + 8, CY - POST / 2 + 8, POST - 16, POST - 16, w=0.15, fill="#fff")
    q.circle(cx2, CY, 37, w=0.3, color="#1f6fb2", fill="#dbe9f6")
    if c["tri"]:
        q.rect(cx2 - 38, 110, 76, CY - 110 - 30, w=0.3, color="#1f6fb2", fill="#dbe9f6")
    else:
        q.rect(inset_x(c, 0, 85) - 38, 110, 76, CLAD - 110 + 20, w=0.3, color="#1f6fb2", fill="#dbe9f6")
    # dims
    if c["tri"]:
        q.dim((cx2, 0), (TIP, 0), -5, text="600", size=1.3)
        q.text(TIP - 330, 60, f"{tip_angle(c):.1f}°", size=1.3)
        nx_, ny_ = -RD / rake_len(c), -TRI / rake_len(c)
    else:
        nx_, ny_ = -1.0, 0.0
    yd = ytop - 170
    p25 = (inset_x(c, yd, 25), yd)
    p145 = (p25[0] + 120 * nx_, p25[1] + 120 * ny_)
    adim(q, p145, p25, 3, "120", size=1.2)
    fasc = ["Fascia 3 mm alu RAL 9010, 0.43 high" + (", mitred at the tip" if c["tri"] else "")]
    rows = [((inset_x(c, ytop - 120, 85), ytop - 120), ["Box gutter 120 w, 1.2 SS, falls to C2"]),
            ((inset_x(c, y1, 150) - 120, y1), ["C200 joist, cleat to edge beam"]),
            ((inset_x(c, ytop - 560, 140), ytop - 560),
             ["RHS 200x100x6.3 " + ("raked" if c["tri"] else "end") + " edge beam"])]
    if c["tri"]:
        rows += [((cx2 - 90, CY + 80), ["C2 SHS 150 + thermo-ash, against the wall"]),
                 ((cx2 - 300, CY), ["RHS 200x100x6.3 plants edge beam (column line)"]),
                 ((cx2, 150), ["Outlet Ø75 from the gutter into C2 → downpipe"]),
                 ((cx2 + 300, 0), fasc + [" (on the wall line)"])]
    else:
        rows += [((XE, 450), fasc),
                 ((cx2 - 90, 180), ["C2 SHS 150x150x8 + 25 thermo-ash"]),
                 ((cx2 - 300, 100), ["RHS 200x100x6.3 plants edge beam"]),
                 ((inset_x(c, 0, 85), 150), ["Outlet Ø75 through SHS wall → downpipe in C2"])]
    for i, (tgt, lines) in enumerate(rows):
        lab(q, tgt, 292, 207 + 8 * i, lines, size=1.25)
    if c["tri"]:
        s.text(292, 263, "Tip cantilevers 0.60 beyond C2;", size=1.25)
        s.text(292, 265.5, "edge beams mitred + 12 mm end plate.", size=1.25)


def sheet_details(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    s = Sheet(f"{vk}-03", f"{c['tag']}\nroof section & details", "1:25 / 1:15 / 1:20", project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color=RED)

    def u(y):
        return WALL_Y0 + TW_T - y

    # ---------------- S1 section across at C1, 1:25 (tall wall LEFT, plants side RIGHT — client sketches)
    v = View(s, 36, 194, 25)
    paving_cut(v, [(u(WALL_Y0), -15), (u(KERB[1]), -15)], z_bottom_extra=200)
    v.rect(u(LW[0]), -500, 500, 500, w=0.15, mat="earth")
    v.line(u(LW[0]), 0, u(-500), 0, w=0.4)
    break_line(v, u(-500), -500, u(-500), 300)
    v.rect(u(WALL_Y0 + TW_T), -600, TW_T, 4200, w=0.45, mat="masonry")
    break_line(v, u(WALL_Y0 + TW_T), 3600, u(WALL_Y0), 3600)
    # existing planter (garden) under the roof edge: soil, white kerb, low boundary wall, shrubs
    v.rect(u(PL[1]), -400, PL[1] - PL[0], KERB_H - 30 + 400, w=0.15, mat="soil")
    v.rect(u(KERB[1]), -200, KERB[1] - KERB[0], KERB_H + 200, w=0.35, fill="#f4f1ea")
    v.rect(u(PL[1]), -400, PL[1] - PL[0], 100, w=0.12, mat="gravel")                       # drainage layer
    v.line(u(PL[1]), -300, u(PL[0]), -300, w=0.25, dash="2,0.6", color="#7a5c3a")            # geotextile
    v.rect(u(PL[1]), KERB_H - 80, PL[1] - PL[0], 50, w=0.1, fill="#8a6a4a")                 # bark mulch
    shrub(v, u(500), KERB_H - 30, 400, 520, seed=140)
    shrub(v, u(660), KERB_H - 30, 150, 430, seed=141, flowers=7)
    vine(v, u(CY + CLAD / 2 + 30), KERB_H, SOFFIT - 30, seed=142, amp=35)
    v.circle(u(560), KERB_H - 130, 16, w=0.2, fill="#333")                                   # drip line
    v.rect(u(610) - 20, KERB_H - 40, 40, 110, w=0.2, fill="#333")                            # L1 uplight
    v.rect(u(LW[1]), -600, LW[1] - LW[0], LW_H + 600, w=0.35, mat="masonry")
    # column C1 against the garden wall, fixed to it + eccentric pad toward the courtyard
    v.rect(u(CY + CLAD / 2), 0, CLAD, COL_TOP, w=0.35, mat="timber")
    v.rect(u(CY + POST / 2), -60, POST, COL_TOP - 10 + 60, w=0.3, fill="#5c6670")
    v.rect(u(CY + CLAD / 2) - 30, COL_TOP - 10, CLAD + 60, 10, w=0.25, fill="#888")
    for z in (450, 1150):
        v.rect(u(CY - POST / 2), z - 40, (CLAD - POST) / 2 + 60, 80, w=0.25, fill="#9aa3ab")    # SS angle
        v.rect(u(LW[1]) - 5, z - 8, 130, 16, w=0.15, fill="#666")                             # resin anchor
    v.rect(u(CY + 650), -900, 900, 700, w=0.3, mat="rc")
    v.rect(u(CY + 150), -200, 300, 140, w=0.3, mat="rc")
    # roof structure
    nj = 3 if RD < 3000 else 4
    for i in range(1, nj + 1):
        y = CY + 50 + (RD - CY - 200) * i / (nj + 1)
        cchan(v, u(y), BOS, facing=-1)
    rhs(v, u(CY + 50), BOS, 100, 200, 6.3)
    roof_layers_y(v, u(RD - 50), u(0) - 5)
    bracket(v, u(CY + CLAD / 2), SOFFIT, -1)
    if RD > HOUSE_W:
        upn200(v, u(WALL_Y0), BOS, facing=1)
        bracket(v, u(WALL_Y0), SOFFIT + 50, 1, r=180)
        v.pl([(u(WALL_Y0) + 6, TOS + 58), (u(WALL_Y0) + 6, TOS + 220)], w=0.45, closed=False, color="#111")
        v.pl([(u(WALL_Y0), TOS + 240), (u(WALL_Y0) + 40, TOS + 225), (u(WALL_Y0) + 40, TOS + 150)], w=0.35,
             closed=False, color="#7f8c8d")
    else:
        rhs(v, u(RD - 50), BOS, 100, 200, 6.3)
        v.pl([(u(RD) + 3, SOFFIT), (u(RD), SOFFIT), (u(RD), FTOP), (u(RD) + 45, FTOP - 6)], w=0.5, closed=False,
             color="#111")
        v.line(u(RD - 60), ROD_Z, u(WALL_Y0), ROD_WALL_Z, w=0.5, color=RED)
        v.rect(u(WALL_Y0), ROD_WALL_Z - 100, 15, 200, w=0.25, fill=RED)
        mx = (u(RD - 60) + u(WALL_Y0)) / 2
        v.rect(mx - 60, (ROD_Z + ROD_WALL_Z) / 2 - 15, 120, 30, w=0.2, fill="#bbb")
        v.text(u(HOUSE_W + STRIP / 2), 900, "0.90 VOID", size=1.6, anchor="middle", rot=90, color="#555")
    # front fascia (plants side) beyond the column
    v.pl([(u(0) - 3, SOFFIT), (u(0), SOFFIT), (u(0), FTOP), (u(0) - 45, FTOP - 6)], w=0.4, closed=False,
         color="#111")
    ladder(v, u(WALL_Y0 + TW_T), [(0, "±0.000"), (SOFFIT, "+2.360 u/s"), (TOS, "+2.610 TOS"),
                                  (FTOP, "+2.790"), (COL_TOP, "+2.920 col.")]
           + ([(ROD_WALL_Z, "+3.050 rod anchor")] if c["rods"] else []), 33, size=1.3, inside=False)
    cc = [u(WALL_Y0)] + ([u(RD)] if RD < WALL_Y0 else []) + [u(KERB[1]), u(LW[1]), u(LW[0])]
    v.chain(cc, "x", -900, -4, size=1.3, overall=True)
    v.dim((u(RD), FTOP), (u(0), FTOP), 6, text=f"{RD:.0f} roof (edge on the garden-wall line)", size=1.3)
    labels = [((u(RD * 0.45), TOS + 50), (130, 112), ["1.5 TPO / 18 ply / firrings / C200 joists"]),
              ((u(RD * 0.25), SOFFIT + 10), (130, 119), ["68x20 thermo-ash slats on battens, LED in edge profile"]),
              ((u(CY), BOS + 100), (130, 126), ["RHS 200x100x6.3 edge beam on the column line (D2)"]),
              ((u(CY + CLAD / 2) - 80, SOFFIT - 90), (130, 133), ["Steel bracket R200 (10 mm), welded / bolted"]),
              ((u(CY), 1700), (130, 148), ["C1 SHS 150x150x8 + 25 thermo-ash, AGAINST the wall"]),
              ((u(LW[1]) + 2, 1150), (130, 158), ["fixed to the wall: 2 SS angles + M12 resin anchors"]),
              ((u(LW[0] + 100), 1250), (130, 168), ["LOW WHITE GARDEN WALL — in line with the annex side"]),
              ((u(700), KERB_H - 60), (130, 179), ["planter 0.70: 50 bark / 400 topsoil / geotextile / 100 gravel;",
                                                  "16 mm drip line + L1 LED uplight 3 W 2700 K, 24 V"]),
              ((u(CY + CLAD / 2 + 30), 1900), (130, 140.5), ["P1 star jasmine on 3 x 3 mm SS wires, up the post"]),
              ((u(500), KERB_H + 350), (130, 190), ["P2 dwarf pittosporum + P3 white lavender / gaura (≤ 0.6 m)"]),

              ((u(CY + 300), -500), (130, 222), ["Pad 900x800x700 eccentric, tied to the wall footing (verify)"])]
    if RD > HOUSE_W:
        labels.append(((u(WALL_Y0) + 40, BOS + 100), (52, 155), ["UPN 200 ledger + curved brackets on wall"]))
    else:
        labels.append(((mx, (ROD_Z + ROD_WALL_Z) / 2), (75, 72), ["Ø16 SS hanger + turnbuckle (2 no.)"]))
    for tgt, (px, py), lines in labels:
        lab(v, tgt, px, py, lines, size=1.35)
    s.text(16, 26, f"1/{vk}-03  ROOF SECTION ACROSS AT C1 — 1:25", size=2.0, weight="bold")
    s.text(16, 30, "(as client sketch " + ("A: roof runs to the wall" if RD > HOUSE_W else
                                           "B: roof stops, rods to the wall") + ")", size=1.4)

    # ---------------- D1 wall junction (1:15) / rod hanger (1:20)
    if RD > HOUSE_W:
        d = View(s, 232, 108, 15, origin=(0, 2300))
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
        for tgt, py, lines in (((40, TOS + 200), 40, ["Membrane up 150 + alu counter-flashing"]),
                               ((400, TOS + 50), 48, ["Deck & membrane"]),
                               ((40, BOS + 100), 64, ["UPN 200 HDG, M12 resin anchors @ 400"]),
                               ((25, BOS - 25), 80, ["Curved bracket R180, 10 mm, @ 1.0 m"])):
            lab(d, tgt, 292, py, lines, size=1.25)
        s.text(222, 26, "D1  ROOF TO WALL (client sketch A) — 1:15", size=1.8, weight="bold")
    else:
        d = View(s, 226, 92, 20, origin=(0, 2300))
        d.rect(-200, 2150, 200, 1250, w=0.45, mat="masonry")
        d.rect(0, ROD_WALL_Z - 100, 12, 200, w=0.25, fill=RED)
        for z in (ROD_WALL_Z - 60, ROD_WALL_Z + 60):
            d.rect(-110, z - 6, 122, 12, w=0.12, fill="#888")
        d.rect(12, ROD_WALL_Z - 6, 40, 12, w=0.2, fill="#777")
        rx, rz = STRIP + 40, ROD_Z
        d.line(50, ROD_WALL_Z, rx, rz, w=0.6, color=RED)
        mxl, mzl = (50 + rx) / 2, (ROD_WALL_Z + rz) / 2
        d.rect(mxl - 55, mzl - 14, 110, 28, w=0.2, fill="#bbb")
        rhs(d, STRIP + 50, BOS, 100, 200, 6.3)
        d.rect(STRIP + 30, ROD_Z - 40, 20, 80, w=0.2, fill="#444")
        d.circle(rx, rz, 9, w=0.2, fill="#fff")
        d.pl([(STRIP + 3, SOFFIT), (STRIP, SOFFIT), (STRIP, FTOP), (STRIP + 45, FTOP - 6)], w=0.55, closed=False,
             color="#111")
        roof_layers_y(d, STRIP + 20, STRIP + 300)
        d.text(STRIP / 2, 2450, "0.90 VOID", size=1.4, anchor="middle", color="#555")
        d.dim((0, 2200), (STRIP, 2200), -3, size=1.2)
        for tgt, py, lines in (((6, ROD_WALL_Z + 80), 40, ["Wall plate 200x150x12 SS, 4 M12 resin"]),
                               ((mxl, mzl), 52, ["Ø16 SS 316 rod + turnbuckle"]),
                               ((STRIP, 2650), 72, ["Fascia 0.43 at the void edge"]),
                               ((STRIP + 40, ROD_Z), 84, ["Fork end on 10 mm lug, edge beam"])):
            lab(d, tgt, 300, py, lines, size=1.25)
        s.text(222, 26, "D1  ROD TO WALL (client sketch B) — 1:20", size=1.8, weight="bold")

    # ---------------- D2 column C1 junction 1:15 (plants side), d-x = distance from plants edge (0) into roof
    q = View(s, 244, 166, 15, origin=(0, 2450))
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
    q.rect(0, TOS + 190, 30, 30, w=0.2, fill="#7f8c8d")
    for tgt, py, lines in (((-100, COL_TOP - 5), 136, ["Cap plate, +0.13 above roof"]),
                           ((50, BOS + 100), 148, ["FP 12 + 2 M16 to edge beam"]),
                           ((-100, 2300), 168, ["Column SHS 150 + cladding"]),
                           ((60, SOFFIT - 80), 178, ["Bracket R200, 10 mm"])):
        lab(q, tgt, 292, py, lines, size=1.25)
    s.text(222, 128, "D2  COLUMN / ROOF JUNCTION (plants side) — 1:15", size=1.8, weight="bold")

    # ---------------- D3 free corner at C2 — plan 1:15
    corner_plan(s, c, vk)
    s.text(222, 196, "D3  " + ("TIP AT C2 (triangle)" if c["tri"] else "CORNER AT C2") +
           " — PLAN 1:15", size=1.8, weight="bold")

    s.textblock(16, 250, 180, [
        ("B", "SPECIFICATION"),
        "Steel S355, hot-dip galvanised; columns & brackets powder-coated RAL 9010 or timber-clad (thermo-ash).",
        "Roof: TPO 1.5 on 18 mm marine ply on tapered firrings (fall 1:70 to the free-edge box gutter).",
        "Soffit: thermo-ash 68x20 slats, LED 2700 K in perimeter profile. Fascia 3 mm aluminium RAL 9010, 0.43 m.",
        ("Rods: Ø16 stainless 316, fork ends, turnbuckle, ≈ 30° rise; engineer to confirm wall anchors."
         if c["rods"] else "Wall ledger & brackets into sound masonry/RC — engineer to confirm anchors."),
    ], size=1.4, gap=0.25)
    s.scale_bar(130, 284, 25, 2)
    s.text(130, 282, "SCALE BAR 1:25 (section 1)", size=1.3)
    return s


VAR["V1T"].update(name=f"OPTION C2 — TRIANGLE TO THE WALL, TIP AT THE AC LINE: plants edge {(ROOF_L + TRI) / 1000:.2f}",
                  tag="OPTION C2 — TIP AT AC LINE", num="C17-C2",
                  short=f"roof to the tall wall, no void; plants edge {(ROOF_L + TRI) / 1000:.2f} ending in line with the end of "
                        f"the AC box; edge at the tall wall {ROOF_L / 1000:.2f} (kept); new raked angle; bears on the annex "
                        "ledger + a ledger on the tall wall; 2 columns against the garden wall on a shorter edge beam")
VAR["V1"].update(name="OPTION D — RECTANGLE 2.20 TO THE WALL (2.20 x 3.44, no void)", tag="OPTION D — RECTANGLE TO WALL",
                 num="C16-D",
                 short=f"option B continued over the passage to the tall wall, no void: {ROOF_L / 1000:.2f} x 3.44; bears on the "
                       "annex ledger + a ledger on the tall wall; 2 columns against the garden wall")
VK = os.environ.get("C16_VK", "V1T")


def sheets():
    return [sheet_plans(VK)]


if __name__ == "__main__":
    import build
    ss = sheets()
    print(build.to_pdf(ss, "Rev-C17_" + VK))
