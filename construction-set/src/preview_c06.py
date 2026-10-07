"""Rev C06 PREVIEW (client 07.10.2026)

Client mark-ups (site photo, C05 review):
  * the GARDEN is NOT along the side of the annex. It is a planter IN FRONT of the annex end facade, LEFT of the
    entrance: its white kerb runs out from the facade in line with the door's left jamb ("the garden ends where the
    door starts"), so the kerb and the plants-side edge of the planter are UNDER the roof; the low boundary wall is
    on its far (left) side. C1 + C2 stand in the planter.
  * TRIANGULAR versions from the first hand sketch: plants edge 3.22 + 1.26 = 4.48 m, top edge 3.22 m.

Versions (each 3 sheets: plans / views + 3D / roof section & details):
  V1   roof 3.22 x 3.44 to the tall wall (ledger + curved brackets), 2 columns on the plants side
  V2   roof 3.22 x 2.54, 0.90 m void kept open, void edge tied to the tall wall with 2 slim rods
  V1T  as V1, triangular: plants edge 4.48, wall edge 3.22, raked edge 3.66
  V2T  as V2, triangular: plants edge 4.48, void edge 3.22, raked edge 2.84

Axes: X along house/roof (house 0..8000, roof from 8000); Y across (plants edge Y = 0, tall wall face Y = 3440).
"""
import math
import random
from cad import Sheet, View, break_line, PROJECT
from common import shrub, ground, GREEN
from sheets_b import ladder, paving_cut, rhs, upn200, cchan
from axo import Axo, mbox

HOUSE_L, HOUSE_W, WALL = 8000, 2540, 200
STRIP = 900                          # passage to the lattice door (top strip in client sketch)
WALL_Y0 = HOUSE_W + STRIP            # 3440 face of TALL wall (main house, AC units) — top side
TW_T, TW_H = 250, 5000
PL = (-1000, 100)                    # planter soil, Y range (in front of the facade, left of the door)
KERB = (100, 250)                    # white stone kerb; outer face in line with the door's left jamb (ENTR[0])
KERB_H = 250                         # kerb / soil level above paving
LW = (-1200, -1000)                  # low boundary wall along the far side of the planter
LW_H = 1400
RET = (HOUSE_L - WALL, HOUSE_L)      # low return wall in the facade line, annex corner -> boundary wall (X range)
GARDEN_X0 = HOUSE_L                  # planter starts at the annex end facade ...
GARDEN_X1 = HOUSE_L + 4100           # ... and runs ~4.1 m out into the courtyard (from site photo — CONFIRM)
ROOF_L = 3220
TRI = 1260                           # triangular extension along the plants edge (client sketch)
RX0, RX1 = HOUSE_L, HOUSE_L + ROOF_L
TIP = RX1 + TRI                      # 12480
XM = RX0 + ROOF_L / 2
SOFFIT, FASCIA = 2360, 430
FTOP = SOFFIT + FASCIA
COL_TOP = FTOP + 130
HOUSE_TOP = 2920
BOS, TOS = SOFFIT + 50, SOFFIT + 250
POST, CLAD = 150, 200
ENTR = (250, 2290)                   # ENTRANCE (site photo): one opening 2.04 m wide x 2.20 high
SLIDE_W = 1060                       # 2 brown louvred SLIDING shutter panels
SLIDES = [(ENTR[1] - SLIDE_W, ENTR[1], 0), (ENTR[1] - SLIDE_W - 60, ENTR[1] - 60, 1)]   # (y0, y1, track)
LATTICE = (HOUSE_W + 50, WALL_Y0 - 50)
HEAD = 2200
ROD_Z = BOS + 100
ROD_WALL_Z = 3050
RODS_X = [XM, RX1 - 150]
RED = "#c0392b"

COLS_R = [("C1", XM, 100), ("C2", RX1 - 100, 100)]
COLS_T = [("C1", RX0 + (ROOF_L + TRI) / 2, 100), ("C2", TIP - 600, 100)]     # C1 mid plants edge, C2 0.60 from tip

VAR = {
    "V1": dict(name="VERSION 1 — ROOF TO THE WALL", tag="V1 ROOF TO WALL", roof_d=WALL_Y0, rods=False,
               tri=False, cols=COLS_R,
               short="roof 3.22 x 3.44 up to the tall wall (bears on wall ledger + curved brackets); "
                     "2 columns on the plants side"),
    "V2": dict(name="VERSION 2 — 0.90 m VOID + 2 STEEL RODS", tag="V2 VOID + RODS", roof_d=HOUSE_W, rods=True,
               tri=False, cols=COLS_R,
               short="roof 3.22 x 2.54; 0.90 m void left open; void edge tied to the tall wall with 2 slim "
                     "Ø16 stainless rods (rising ≈ 30°); 2 columns on the plants side"),
    "V1T": dict(name="VERSION 1T — TRIANGLE, ROOF TO THE WALL", tag="V1T TRIANGLE TO WALL", roof_d=WALL_Y0,
                rods=False, tri=True, cols=COLS_T,
                short="triangular roof: plants edge 3.22 + 1.26 = 4.48, wall edge 3.22, raked edge 3.66; "
                      "runs to the tall wall (ledger + brackets); 2 columns on the plants side"),
    "V2T": dict(name="VERSION 2T — TRIANGLE, 0.90 m VOID + 2 RODS", tag="V2T TRIANGLE + RODS", roof_d=HOUSE_W,
                rods=True, tri=True, cols=COLS_T,
                short="triangular roof: plants edge 3.22 + 1.26 = 4.48, void edge 3.22, raked edge 2.84; "
                      "0.90 m void open, 2 Ø16 stainless rods to the wall; 2 columns on the plants side"),
}
ORDER = ("V1", "V2", "V1T", "V2T")
REVS = [["C06", "07.10.2026", "Garden = planter in front of the façade, left of the door, partly under roof"],
        ["C05", "07.10.2026", "Triangular versions V1T/V2T; 3D views; details D3"],
        ["C04", "07.10.2026", "Two versions V1/V2 per client sections & site photo"],
        ["C02", "07.10.2026", "Canopy to client sketch: 8.00 house, roof 3.22, u/s 2.36, fascia 0.43"]]


# ===================================================================== geometry helpers
def xend(c):
    return TIP if c["tri"] else RX1


def roof_poly(c):
    RD = c["roof_d"]
    return [(RX0, 0), (xend(c), 0), (RX1, RD), (RX0, RD)]


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
    p["rev"] = "C06"
    p["date"] = "07.10.2026"
    p["name"] = "COURTYARD ROOF — " + vk
    p["site"] = VAR[vk]["name"] + ": " + VAR[vk]["short"]
    p["status"] = "PREVIEW FOR CLIENT REVIEW — per client sketch, mark-ups & site photo; not for construction"
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


# ===================================================================== plan context
def site_plan(v, c, labels=True):
    """Plan in model coords: garden (bottom, ends at the door line), annex, passage, tall wall (top), roof."""
    RD = c["roof_d"]
    XR = xend(c) + 1500
    # courtyard paving in front of the annex (incl. under the roof)
    v.rect(RX0, LW[1], XR - RX0, WALL_Y0 - LW[1], w=0, fill="#f3eee4")
    for x in range(RX0 + 600, XR, 600):
        v.line(x, LW[1], x, WALL_Y0, w=0.05, color="#d9d1c2")
    for y in range(LW[1] + 600, WALL_Y0, 600):
        v.line(RX0, y, XR, y, w=0.05, color="#d9d1c2")
    # GARDEN: planter in front of the facade, left of the door — kerb in line with the door jamb, partly under roof
    v.rect(GARDEN_X0, PL[0], GARDEN_X1 - GARDEN_X0, PL[1] - PL[0], w=0.15, fill="#efe4d0", color="#bba")
    v.rect(GARDEN_X0, KERB[0], GARDEN_X1 - GARDEN_X0, KERB[1] - KERB[0], w=0.3, fill="#f7f4ee")
    v.rect(GARDEN_X1 - 150, PL[0], 150, KERB[1] - PL[0], w=0.3, fill="#f7f4ee")
    plants(v, GARDEN_X0 + 20, GARDEN_X1 - 120, PL[0] + 50, PL[1] - 150, seed=3)
    # low boundary wall (far side of the planter) + low return wall in the facade line to the annex corner
    v.rect(RET[0], LW[0], XR - RET[0], LW[1] - LW[0], mat="masonry", w=0.35)
    v.rect(RET[0], LW[1], RET[1] - RET[0], 0 - LW[1], mat="masonry", w=0.35)
    # tall wall (top)
    v.rect(-300, WALL_Y0, XR + 300, TW_T, mat="masonry", w=0.45)
    # annex
    v.rect(0, 0, HOUSE_L, HOUSE_W, mat="masonry", w=0.45)
    v.rect(WALL, WALL, HOUSE_L - 2 * WALL, HOUSE_W - 2 * WALL, w=0.3, fill="#fbfaf7")
    v.rect(HOUSE_L - WALL, ENTR[0], WALL, ENTR[1] - ENTR[0], w=0.15, fill="#fff")
    mid = (ENTR[0] + ENTR[1]) / 2
    v.rect(HOUSE_L - 140, ENTR[0], 25, mid - ENTR[0] + 40, w=0.15, fill="#cfe3ef")      # glass sliding door
    v.rect(HOUSE_L - 110, mid - 40, 25, ENTR[1] - mid + 40, w=0.15, fill="#cfe3ef")
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
        v.text(RET[0] - 150, -330, "GARDEN / PLANTER (exist.) ≈ 4.10 x 1.25 m ►", size=1.4, anchor="end",
               color="#3f6b2e", weight="bold")
        v.text(RET[0] - 150, -650, "kerb in line with the door jamb — part UNDER the roof", size=1.25,
               anchor="end", color="#3f6b2e")
        v.text(RET[0] - 150, LW[0] + 50, "LOW BOUNDARY WALL (exist.) ►", size=1.25, anchor="end", color="#333",
               weight="bold")
        v.text(GARDEN_X1 + 150, -600, "PAVING", size=1.3, color="#8a7f6c")
    # roof
    poly = roof_poly(c)
    v.pl(poly, w=0, fill="#dfe5ea", opacity=0.75)
    for (a, b, tr) in SLIDES:                                                          # brown louvred slides
        v.rect(HOUSE_L + 10 + tr * 45, a, 35, b - a, w=0.25, fill="#6e5544")
    v.line(HOUSE_L + 5, ENTR[0] - 150, HOUSE_L + 5, ENTR[1] + 150, w=0.15, dash="1.5,0.8")
    v.pl(poly, w=0.5, dash="4,1.5")
    if labels:
        v.text(HOUSE_L + 260, (ENTR[0] + ENTR[1]) / 2, "entrance: brown sliders", size=1.2, anchor="middle",
               rot=90, color="#5f4838", weight="bold")
    for (lb, x, y) in c["cols"]:
        col(v, x, y, lb if labels else None, lab_dy=520)
    if c["rods"]:
        for x in RODS_X:
            v.line(x, HOUSE_W - 60, x, WALL_Y0, w=0.4, color=RED)
            v.rect(x - 60, WALL_Y0, 120, 30, w=0.2, fill=RED)


# ===================================================================== SHEET 1: PLANS
def sheet_plans(vk):
    c = VAR[vk]
    RD = c["roof_d"]
    XE = xend(c)
    s = Sheet(f"{vk}-01", f"{c['tag']}\ntop view & roof framing", "1:50 / 1:30", project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color=RED)
    v = View(s, 40, 90, 50)
    site_plan(v, c)
    cx = RX0 + (ROOF_L if not c["tri"] else ROOF_L + TRI * 0.35) / 2
    v.text(cx, RD / 2 + 200, "ROOF", size=2.4, anchor="middle", weight="bold")
    v.text(cx, RD / 2 - 250, (f"3.22 x {RD / 1000:.2f} m" if not c["tri"] else
                              f"3.22 / 4.48 x {RD / 1000:.2f} m"), size=1.9, anchor="middle")
    if c["rods"]:
        v.text(RX0 + 120, HOUSE_W + STRIP / 2 - 60, "0.90 VOID — 2 Ø16 SS rods to wall", size=1.4, color=RED,
               weight="bold")
    xs = [0, HOUSE_L, RX1] + ([TIP] if c["tri"] else [])
    v.chain(xs, "x", LW[0], -12, size=1.6)
    cs = [RX0] + [x for (_, x, _) in c["cols"]] + [XE] if c["tri"] else [RX0, XM, RX1]
    v.chain(cs, "x", LW[0], -5, size=1.4, overall=False)
    v.chain([LW[0], LW[1], 0, KERB[1], HOUSE_W, WALL_Y0], "y", XE + 1200, -6, size=1.4, overall=False)
    v.chain([0, HOUSE_W, WALL_Y0], "y", XE + 1200, -12, size=1.6)
    if c["tri"]:
        adim(v, (TIP, 0), (RX1, RD), -4, f"{rake_len(c):.0f}", size=1.4)
        v.text(TIP + 150, 120, f"{tip_angle(c):.1f}°", size=1.4)
    v.title(40, 135, f"1/{vk}-01", "TOP VIEW — ANNEX, GARDEN & ROOF", "1:50 @ A3",
            sub="— garden = planter in front of the façade, left of the door; trees = background")
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
        w.line(RX0, yk, gx1, yk, w=0.25, dash="2,1", color="#3f6b2e")
    w.text(RX0 + 2200, KERB[1] + 60, "planter kerb below (garden under the roof edge)", size=1.2, color="#3f6b2e")
    beam = dict(w=0.35, fill="#7d8790")
    w.rect(RX0, 150, 75, HOUSE_W - 300, w=0.3, fill="#5c6670")                     # ledger on annex
    if RD > HOUSE_W:                                                               # trimmer over the passage
        w.rect(RX0, HOUSE_W - 150, 100, WALL_Y0 - 75 - (HOUSE_W - 150), w=0.3, fill="#7d8790")
        w.leader([(RX0 + 50, HOUSE_W + 450), (RX0 - 600, HOUSE_W + 250)], ["RHS trimmer over passage", "annex → wall ledger"],
                 size=1.2, anchor="end")
    if not c["tri"]:
        if RD > HOUSE_W:
            w.rect(RX0 + 75, WALL_Y0 - 75, ROOF_L - 75, 75, w=0.3, fill="#5c6670")  # ledger on tall wall
        w.rect(RX0 + 75, 50, ROOF_L - 275, 100, **beam)                              # plants edge beam
        if RD == HOUSE_W:
            w.rect(RX0 + 75, RD - 150, ROOF_L - 175, 100, **beam)                    # void edge beam
        w.rect(RX1 - 150, 200, 100, RD - 350, **beam)                                # end beam
    else:
        w.pl(band(c, 50, 150, 0, 150, x_from=RX0 + 75), **beam)                      # plants edge beam
        if RD > HOUSE_W:
            w.pl(band(c, WALL_Y0 - 75, WALL_Y0, 0, 150, x_from=RX0 + 75), w=0.3, fill="#5c6670")
            ytop = WALL_Y0 - 75
        else:
            w.pl(band(c, RD - 150, RD - 50, 0, 150, x_from=RX0 + 75), **beam)        # void edge beam
            ytop = RD - 50
        w.pl(band(c, 50, ytop, 50, 150), **beam)                                     # raked edge beam
    nj = 3 if RD < 3000 else 4
    for i in range(1, nj + 1):
        y = 150 + (RD - 300) * i / (nj + 1)
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
    yc = [0, HOUSE_W, WALL_Y0]
    w.chain(yc, "y", XE, -8, size=1.4, overall=False)
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
        items += [f"Triangle: plants edge 3.22 + 1.26 = 4.48 m; raked edge {rake_len(c) / 1000:.2f} m at "
                  f"{tip_angle(c):.1f}° to the plants edge.",
                  f"C1 in the middle of the 4.48 edge ({(cl[0][1] - RX0) / 1000:.2f} from the façade); "
                  f"C2 0.60 m in from the tip (the tip cantilevers 0.60).",
                  "Joists run from the annex ledger to the raked edge beam (max. span ≈ 4.2 m)."]
    else:
        items += ["C1 in the middle of the plants edge, C2 at the corner."]
    items += [("B", "COMMON"),
              "Roof 3.22 m from the annex façade along the top edge. Underside +2.36, fascia 0.43 (top +2.79); "
              "columns 200x200, 0.13 above roof, curved bracket under the junction (client section).",
              "Garden = existing planter in front of the façade, left of the door: white kerb in line with the door "
              "jamb (0.25 from the corner), so kerb + edge of the planter are UNDER the roof; C1 + C2 stand in the "
              "planter. Planter length ≈ 4.10 m (from site photo — confirm).",
              "Falls 1:70 to the concealed gutter at the free edge; rainwater down C2."]
    s.textblock(214, 146, 126, items, size=1.45, gap=0.25)
    s.text(214, 197, f"3/{vk}-01  3D — BIRD'S EYE (from the plants side, over the low wall)", size=1.8,
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
    B(RET[0], LW[0], 0, XR - RET[0], LW[1] - LW[0], LW_H, "#f1ede6", layer=wl, w=0.2)
    B(RET[0], LW[1], 0, RET[1] - RET[0], 0 - LW[1], LW_H, "#f1ede6", layer=wl - 0.05, w=0.2)
    B(GARDEN_X0, PL[0], 0, GARDEN_X1 - GARDEN_X0, PL[1] - PL[0], KERB_H - 30, "#7d5f42", layer=4)
    B(GARDEN_X0, KERB[0], 0, GARDEN_X1 - GARDEN_X0, KERB[1] - KERB[0], KERB_H, "#f4f1ea", layer=4.1 if mir else 4.05,
      w=0.2)
    B(GARDEN_X1 - 150, PL[0], 0, 150, KERB[1] - PL[0], KERB_H, "#f4f1ea", layer=4.2, w=0.2)
    rnd = random.Random(5)
    x = GARDEN_X0 + 300
    i = 0
    while x < GARDEN_X1 - 300:
        BL(x, (PL[0] + PL[1]) / 2 - 30 + rnd.uniform(-150, 150), KERB_H + 520 + rnd.uniform(0, 600),
           480 + rnd.uniform(0, 160),
           fill="#9cc47f" if i % 3 else "#86b56a", stroke="#4f7a3d", layer=4.3, seed=20 + i, flowers=4)
        x += rnd.uniform(420, 620)
        i += 1
    # roof: side fascias first (back-facing ones end up under the top), then the top
    poly = roof_poly(c)
    P3([(RX0, 0, SOFFIT), (XE, 0, SOFFIT), (XE, 0, FTOP), (RX0, 0, FTOP)], "#ffffff", w=0.3, layer=5.95)
    P3([(XE, 0, SOFFIT), (RX1, RD, SOFFIT), (RX1, RD, FTOP), (XE, 0, FTOP)], "#f2f3f4", w=0.3, layer=5.96)
    if RD < WALL_Y0:
        P3([(RX0, RD, SOFFIT), (RX1, RD, SOFFIT), (RX1, RD, FTOP), (RX0, RD, FTOP)], "#ffffff", w=0.3, layer=5.94)
    P3([(x_, y_, FTOP) for (x_, y_) in poly], "#e3e8ec", w=0.3, layer=6)
    for (lb, xc, yc) in c["cols"]:
        for sgn in (-1, 1):
            xf = xc + sgn * CLAD / 2
            if (sgn > 0 and xf > XE - 250) or (sgn < 0 and xf < RX0 + 250):
                continue
            arc = [(xf + sgn * (200 - 200 * math.sin(math.radians(90 * k_ / 8))), 100,
                    SOFFIT - 200 + 200 * math.cos(math.radians(90 * k_ / 8))) for k_ in range(9)]
            P3([(xf, 100, SOFFIT), (xf + sgn * 200, 100, SOFFIT)] + arc, "#c9d0d6", w=0.15, layer=6.5)
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
        note(tp((RX0 + RX1) / 2, RD, FTOP + 150), "3.22")
        note(tp((RX0 + XE) / 2, -1500, 0), "plants edge " + ("4.48 (3.22 + 1.26)" if c["tri"] else "3.22"),
             size=1.4)
        if c["tri"]:
            note(tp(TIP + 250, -250, SOFFIT - 300), "+1.26 triangle", size=1.4, anchor="start")
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
    ground(e, LW[0] - 100, WALL_Y0 + TW_T + 200, 0, depth=200)
    e.rect(LW[1], 0, 0 - LW[1], LW_H, w=0.3, fill="#f4f1ea")                       # low return wall (facade line)
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
    e.text(1200, HOUSE_TOP + 150, "solar heater / AC (exist.)", size=1.2, anchor="middle", color="#888")
    e.rect(0, SOFFIT, RD, FASCIA, w=0.45, fill="#ffffff")
    # garden (planter) in FRONT of the facade, left of the door, partly under the roof
    for i, (cu, hh, ww) in enumerate(((-780, 1500, 520), (-380, 2000, 650), (-60, 1700, 480), (120, 1150, 300))):
        shrub(e, cu, KERB_H, ww, hh, seed=90 + i, flowers=5)
    e.rect(0, 0, CLAD, COL_TOP, w=0.35, mat="timber")
    bracket(e, CLAD, SOFFIT, 1)
    e.text(100, COL_TOP + 100, "C2 (C1 behind)", size=1.3, anchor="start", weight="bold")
    e.rect(PL[0], 0, KERB[1] - PL[0], KERB_H, w=0.3, fill="#f4f1ea")                # planter end kerb (nearest)
    e.rect(LW[0], 0, LW[1] - LW[0], LW_H, mat="masonry", w=0.35)                    # low boundary wall (end)
    lab(e, (KERB[1] - 20, KERB_H - 40), 82, 152, ["garden kerb in line with the door jamb —",
                                                  "planter runs UNDER the roof (C1, C2 stand in it)"], size=1.3)
    if c["rods"]:
        e.line(HOUSE_W - 60, ROD_Z, WALL_Y0, ROD_WALL_Z, w=0.5, color=RED)
        e.rect(WALL_Y0 - 20, ROD_WALL_Z - 70, 20, 140, w=0.2, fill=RED)
    e.chain([LW[1], 0, HOUSE_W, WALL_Y0], "x", 0, -7, size=1.4)
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
    p.rect(GARDEN_X0, 0, GARDEN_X1 - GARDEN_X0, KERB_H, w=0.25, fill="#cdb79a")       # planter (soil) under roof
    p.rect(GARDEN_X1 - 150, 0, 150, KERB_H, w=0.3, fill="#f4f1ea")
    for i, x in enumerate(range(GARDEN_X0 + 300, GARDEN_X1 - 250, 560)):
        shrub(p, x, KERB_H, 560, 1000 + (i % 3) * 380, seed=150 + i, flowers=3)
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
    p.rect(RET[0], 0, XE + 500 - RET[0], LW_H, w=0.25, dash="2.5,1.2", color="#555")   # boundary wall in front
    p.text(RET[0] + 120, LW_H + 80, "low boundary wall in front (dashed)", size=1.2, color="#555")
    lab(p, (GARDEN_X0 + 500, KERB_H + 300), 84, 163, ["garden (planter) in front of the façade — runs under the "
                                                      "roof, C1 + C2 stand in it"], size=1.3)
    s.text(16, 158, f"2/{vk}-02  PLANTS-SIDE ELEVATION — C1 + C2 — 1:50" +
           ("   (plants edge 3.22 + 1.26 = 4.48)" if c["tri"] else ""), size=1.9, weight="bold")

    # ---- 3: section across at C1 (1:50 overview — refined at 1:25 on sheet -03)
    def u(y):
        return WALL_Y0 + TW_T - y
    w = View(s, 214, 124, 50)
    paving_cut(w, [(u(WALL_Y0), -15), (u(KERB[1]), -15)], z_bottom_extra=150, joints=False)
    w.rect(u(WALL_Y0 + TW_T), -300, TW_T, 4300, w=0.35, mat="masonry")
    w.rect(u(PL[1]), -300, PL[1] - PL[0], KERB_H - 30 + 300, w=0.15, mat="soil")       # planter (cut)
    w.rect(u(KERB[1]), -150, KERB[1] - KERB[0], KERB_H + 150, w=0.3, fill="#f4f1ea")  # kerb (cut)
    w.rect(u(LW[1]), -300, LW[1] - LW[0], LW_H + 300, w=0.3, mat="masonry")         # boundary wall (cut)
    shrub(w, u(-450), KERB_H, 800, 1500, seed=131, flowers=4)
    w.rect(u(RD), SOFFIT, RD, FASCIA, w=0.35, fill="#e6eaee")
    w.rect(u(CLAD), 0, CLAD, COL_TOP, w=0.3, mat="timber")
    bracket(w, u(CLAD), SOFFIT, -1)
    if RD > HOUSE_W:
        bracket(w, u(WALL_Y0), SOFFIT + 50, 1, r=180)
    if c["rods"]:
        w.line(u(RD - 100), ROD_Z, u(WALL_Y0), ROD_WALL_Z, w=0.45, color=RED)
    ladder(w, u(WALL_Y0 + TW_T), [(0, "±0.000"), (SOFFIT, "+2.360"), (FTOP, "+2.790")], 210, size=1.3,
           inside=False)
    cc = [u(WALL_Y0)] + ([u(RD)] if RD < WALL_Y0 else []) + [u(KERB[1]), u(0), u(LW[1])]
    w.chain(cc, "x", -300, -4, size=1.2, overall=False)
    lab(w, (u(-300), KERB_H - 60), 318, 110, ["planter (exist.):", "kerb + C1 under", "the roof edge"], size=1.25)
    s.text(200, 26, f"3/{vk}-02  SECTION ACROSS AT C1 — 1:50 (refined: {vk}-03)", size=1.9, weight="bold")
    s.text(200, 30, "tall wall left — plants side right", size=1.4)

    # ---- 4: 3D
    s.text(200, 150, f"4/{vk}-02  3D — EYE LEVEL, SAME DIRECTION AS THE SITE PHOTO", size=1.9, weight="bold")
    axo_view(s, c, 200, 156, 338, 284, beta=70, elev=12, eye=True)

    s.textblock(16, 255, 178, [("B", "NOTES"), VAR[vk]["short"] + ".",
                               "Underside +2.36, fascia 0.43 (top +2.79); columns 0.13 above roof.",
                               "Garden = existing planter in front of the façade, left of the door; its kerb is in "
                               "line with the door jamb, so part of it is UNDER the roof (C1 + C2 stand in it). "
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
    # beams (RHS 200x100 in plan = 100 wide)
    q.pl(band(c, 50, 150, 0, 150, x_from=x_l), w=0.3, fill="#9aa3ab")
    yb = 50 if c["tri"] else CLAD
    q.pl(band(c, yb, ytop, 50, 150), w=0.3, fill="#9aa3ab")
    q.pl(band(c, 56, 144, 0, 156, x_from=x_l + 6), w=0.1, fill="#e9ecef")
    q.pl(band(c, yb + 6, ytop, 56, 144), w=0.1, fill="#e9ecef")
    nj = 3 if RD < 3000 else 4
    y1 = 150 + (RD - 300) / (nj + 1)
    q.pl(band(c, y1 - 32, y1 + 32, 0, 150, x_from=x_l), w=0.2, fill="#c9d0d6")
    # concealed box gutter (above the beams) along the free edge; side outlet into C2 (post runs on above roof)
    cx2 = c["cols"][-1][1]
    if c["tri"]:
        g = [(cx2 + CLAD / 2, 25), (inset_x(c, 25, 25), 25), (inset_x(c, ytop, 25), ytop),
             (inset_x(c, ytop, 145), ytop), (inset_x(c, 145, 145), 145), (cx2 + CLAD / 2, 145)]
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
    q.rect(cx2 - CLAD / 2, 0, CLAD, CLAD, w=0.3, mat="timber")
    q.rect(cx2 - POST / 2, 25, POST, POST, w=0.3, fill="#5c6670")
    q.rect(cx2 - POST / 2 + 8, 33, POST - 16, POST - 16, w=0.15, fill="#fff")
    q.circle(cx2, 100, 37, w=0.3, color="#1f6fb2", fill="#dbe9f6")
    if c["tri"]:
        q.rect(cx2 + 20, 85 - 38, CLAD / 2 - 20 + 20, 76, w=0.3, color="#1f6fb2", fill="#dbe9f6")
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
        rows += [((cx2 - 90, 180), ["C2 SHS 150x150x8 + 25 thermo-ash"]),
                 ((cx2 - 300, 100), ["RHS 200x100x6.3 plants edge beam"]),
                 ((cx2 + 60, 85), ["Side outlet Ø75 through SHS → downpipe in C2"]),
                 ((cx2 + 300, 0), fasc)]
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
    s = Sheet(f"{vk}-03", f"{c['tag']}\nroof section & details", "1:30 / 1:15 / 1:20", project=project(vk))
    s.frame()
    s.text(16, 14, c["name"], size=3.2, weight="bold", color=RED)

    def u(y):
        return WALL_Y0 + TW_T - y

    # ---------------- S1 section across at C1, 1:25 (tall wall LEFT, plants side RIGHT — client sketches)
    v = View(s, 36, 194, 30)
    paving_cut(v, [(u(WALL_Y0), -15), (u(KERB[1]), -15)], z_bottom_extra=200)
    v.rect(u(WALL_Y0 + TW_T), -600, TW_T, 4200, w=0.45, mat="masonry")
    break_line(v, u(WALL_Y0 + TW_T), 3600, u(WALL_Y0), 3600)
    # existing planter (garden) under the roof edge: soil, white kerb, low boundary wall, shrubs
    v.rect(u(PL[1]), -400, PL[1] - PL[0], KERB_H - 30 + 400, w=0.15, mat="soil")
    v.rect(u(KERB[1]), -200, KERB[1] - KERB[0], KERB_H + 200, w=0.35, fill="#f4f1ea")
    v.rect(u(LW[1]), -600, LW[1] - LW[0], LW_H + 600, w=0.35, mat="masonry")
    shrub(v, u(-300), KERB_H, 520, 1300, seed=140, flowers=4)
    shrub(v, u(-720), KERB_H, 480, 1050, seed=141, flowers=4)
    # column C1 + base + pad below the paving
    v.rect(u(CLAD), 0, CLAD, COL_TOP, w=0.35, mat="timber")
    v.rect(u(100 + POST / 2), -60, POST, COL_TOP - 10 + 60, w=0.3, fill="#5c6670")
    v.rect(u(CLAD) - 30, COL_TOP - 10, CLAD + 60, 10, w=0.25, fill="#888")
    v.rect(u(100 + 400), -900, 800, 700, w=0.3, mat="rc")
    v.rect(u(100 + 150), -200, 300, 140, w=0.3, mat="rc")
    # roof structure
    nj = 3 if RD < 3000 else 4
    for i in range(1, nj + 1):
        y = 150 + (RD - 300) * i / (nj + 1)
        cchan(v, u(y), BOS, facing=-1)
    roof_layers_y(v, u(RD - 50), u(CLAD))
    bracket(v, u(CLAD), SOFFIT, -1)
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
    cc = [u(WALL_Y0)] + ([u(RD)] if RD < WALL_Y0 else []) + [u(KERB[1]), u(0), u(LW[1]), u(LW[0])]
    v.chain(cc, "x", -900, -4, size=1.3, overall=True)
    labels = [((u(RD * 0.45), TOS + 50), (118, 124), ["1.5 TPO / 18 ply / firrings / C200 joists"]),
              ((u(RD * 0.25), SOFFIT + 10), (118, 131), ["68x20 thermo-ash slats on battens, LED in edge profile"]),
              ((u(100), BOS + 100), (118, 138), ["RHS 200x100x6.3 plants edge beams frame into C1 each side (D2)"]),
              ((u(CLAD) - 80, SOFFIT - 90), (118, 145), ["Steel bracket R200 (10 mm), welded / bolted"]),
              ((u(100), 1300), (118, 162), ["C1 SHS 150x150x8 + 25 thermo-ash = 200x200, stands in the planter"]),
              ((u(-350), KERB_H + 20), (118, 181), ["Existing planter: white kerb in line with the door jamb —",
                                                   "kerb + edge of the planter are UNDER the roof"]),
              ((u(300), -500), (118, 216), ["Pad 800x800x700 C30/37 in the planter, 4 M16 cast-in"]),
              ((u(LW[0] + 100), 1000), (201, 140), ["low boundary", "wall (exist.)"])]
    if RD > HOUSE_W:
        labels.append(((u(WALL_Y0) + 40, BOS + 100), (52, 155), ["UPN 200 ledger + curved brackets on wall"]))
    else:
        labels.append(((mx, (ROD_Z + ROD_WALL_Z) / 2), (100, 86), ["Ø16 SS rod + turnbuckle (2 no.)"]))
    for tgt, (px, py), lines in labels:
        lab(v, tgt, px, py, lines, size=1.35)
    s.text(16, 26, f"1/{vk}-03  ROOF SECTION ACROSS AT C1 — 1:30 (planter under the roof edge)", size=2.0,
           weight="bold")
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
    s.scale_bar(130, 284, 30, 2)
    s.text(130, 282, "SCALE BAR 1:30 (section 1)", size=1.3)
    return s


def sheets():
    out = []
    for vk in ORDER:
        out += [sheet_plans(vk), sheet_views(vk), sheet_details(vk)]
    return out


if __name__ == "__main__":
    import build
    ss = sheets()
    print(build.to_pdf(ss, "Rev-C06_All-4-Versions"))
