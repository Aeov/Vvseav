"""Rev C03 PREVIEW — client mark-up of C02 (07.10.2026):
 * Roof edge ends on the marked line: roof 3.22 m (X) x 2.54 m (Y). The 0.90 m strip towards the plants
   stays EMPTY (no roof, no structure).
 * Columns: 2 on the plants side (middle of that edge + top-right corner); front-right column kept.
 * Section: roof frames into the side of the column; column rises above the roof; small bracket under the
   roof/column junction (client section sketches).
House 8.00 m. Roof underside +2.36, fascia band 0.43 (top +2.79). Triangular extension: next step.

Axes as the sketch TOP view: X along house/roof (house 0..8000, roof 8000..11220); Y across
(front edge Y = 0, roof edge on plants side Y = 2540, free strip to Y = 3440). Z above ground ±0.000.
"""
import math
from cad import Sheet, View, break_line, PROJECT
from common import shrub, vine, ground, GREEN, GREEN_F
from sheets_b import ladder, paving_cut, rhs, upn200, cchan

# ----------------------------------------------------------------- geometry (mm)
HOUSE_L, DEPTH = 8000, 3440
WALL = 200
ROOF_D = 2540                     # roof ends on the client's marked line
FREE = DEPTH - ROOF_D             # 900 empty strip towards the plants
ROOF_L = 3220
RX0, RX1 = HOUSE_L, HOUSE_L + ROOF_L
SOFFIT, FASCIA = 2360, 430
FTOP = SOFFIT + FASCIA            # 2790
COL_TOP = FTOP + 130              # column rises above the roof (client section)
HOUSE_TOP = COL_TOP               # house top line (assumed — survey)
BOS = SOFFIT + 50
TOS = BOS + 200
DECK_HI, DECK_LO = TOS + 60 + 18, TOS + 15 + 18
POST, CLAD = 150, 200
XM = RX0 + ROOF_L / 2             # middle of plants-side edge
COLS = [("C1", XM, ROOF_D - 100), ("C2", RX1 - 100, ROOF_D - 100), ("C3", RX1 - 100, 100)]
LEDGER_X = (RX0, RX0 + 75)
B_PL = (ROOF_D - 150, ROOF_D - 50)   # plants-side edge beam RHS 200x100 (Y range)
B_FR = (50, 150)                     # front edge beam (Y range)
B_END = (RX1 - 150, RX1 - 50)        # end beam between C3 and C2 (X range)
J_Y = [150 + (ROOF_D - 300) * i / 4 for i in range(1, 4)]
GUT_X = (RX1 - 170, RX1 - 50)
DOOR = (700, 1700)                # assumed door in house end wall (Y range) — verify
FTG, FTG_D, FTG_BOT = 800, 700, -900

PJ = dict(PROJECT)
PJ["rev"] = "C03"
PJ["date"] = "07.10.2026"
PJ["status"] = "PREVIEW FOR CLIENT REVIEW — per client sketch & mark-up; not for construction until confirmed"
PJ["site"] = "Roof 3.22 x 2.54 m at end of existing 8.00 m house; 0.90 m strip to plants kept free"


def sheet(num, title, scale):
    s = Sheet(num, title, scale, project=PJ)
    s.frame()
    return s


def notes(s, x, y, w=74):
    s.textblock(x, y, w, [
        ("B", "CLIENT DIMENSIONS (m)"),
        "House 8.00 · Roof 3.22 x 2.54 (edge on marked line) · free strip to plants 0.90 · columns 0.20 · "
        "roof underside 2.36 · fascia band 0.43 (top 2.79) · column top +2.92.",
        "Columns: C1 middle + C2 corner on plants side; C3 front-right corner.",
        "Triangular extension (+1.26) — next step, not shown.",
    ], size=1.5, gap=0.3)


def plants_band(v, x0, x1, y0, y1, seed=1):
    v.rect(x0, y0, x1 - x0, y1 - y0, w=0.15, fill="#e6f0dc", color="#7fa86a")
    import random
    r = random.Random(seed)
    x = x0 + 250
    while x < x1 - 150:
        v.circle(x, (y0 + y1) / 2 + r.uniform(-60, 60), r.uniform(150, 230), w=0.15, color=GREEN, fill="#cfe3c0")
        x += r.uniform(380, 520)


def col_plan(v, x, y, label=None):
    v.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.25, fill="#e7c79a")
    v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
    if label:
        v.tag(x, y + (330 if y > 1000 else -330), label, shape="circle", r=2.0, size=1.4)


# ================================================================= P-01 TOP VIEW / PLANS
def plan_house(v):
    v.rect(0, 0, HOUSE_L, DEPTH, mat="masonry", w=0.45)
    v.rect(WALL, WALL, HOUSE_L - 2 * WALL, DEPTH - 2 * WALL, w=0.3, fill="#fbfaf7")
    v.line(WALL, ROOF_D, HOUSE_L - WALL, ROOF_D, w=0.12, dash="2,1", color="#999")
    v.rect(HOUSE_L - WALL, DOOR[0], WALL, DOOR[1] - DOOR[0], w=0.15, fill="#fff")
    v.line(HOUSE_L - WALL, DOOR[0], HOUSE_L - WALL - (DOOR[1] - DOOR[0]), DOOR[0], w=0.25)
    v.arc(HOUSE_L - WALL, DOOR[0], DOOR[1] - DOOR[0], 90, 180, w=0.12)
    v.text(HOUSE_L / 2, 1500, "EXISTING HOUSE", size=2.4, anchor="middle", weight="bold", color="#555")
    v.text(HOUSE_L / 2, 1100, "(internal layout indicative)", size=1.6, anchor="middle", color="#777")


def sheet_p01():
    s = sheet("P-01", "Top view — site plan & roof plan (Rev C03 preview)", "1:50 / 1:25")
    v = View(s, 40, 92, 50)
    v.rect(-300, -1000, RX1 + 1300, 1000, w=0, fill="#f3eee4")
    v.text(5000, -650, "COURTYARD / PAVING (extent per site)", size=1.6, anchor="middle", color="#888")
    plants_band(v, RX0, RX1 + 900, DEPTH, DEPTH + 500, seed=2)
    v.text(RX0 + 1700, DEPTH + 650, "PLANTS", size=1.6, anchor="middle", color="#4f7a3d", weight="bold")
    plan_house(v)
    v.rect(RX0, 0, ROOF_L, ROOF_D, w=0, fill="#eef0f2")
    v.rect(RX0, ROOF_D, ROOF_L, FREE, w=0.15, dash="1,1", color="#888", fill="#fbfbf8")
    v.text(RX0 + ROOF_L / 2, ROOF_D + FREE / 2 - 80, "0.90 FREE — no roof", size=1.6, anchor="middle", color="#555")
    for (lab, x, y) in COLS:
        col_plan(v, x, y, lab)
    v.rect(RX0, 0, ROOF_L, ROOF_D, w=0.45, dash="4,1.5")
    v.text(RX0 + ROOF_L / 2, 1450, "ROOF OVER", size=2.2, anchor="middle", weight="bold")
    v.text(RX0 + ROOF_L / 2, 1050, "3.22 x 2.54 m", size=1.9, anchor="middle")
    v.chain([0, HOUSE_L, RX1], "x", 0, -14, size=1.8)
    v.chain([RX0, XM, RX1], "x", DEPTH + 500, 8, size=1.6, overall=False)
    v.chain([0, ROOF_D, DEPTH], "y", RX1 + 900, -10, size=1.8, overall=True)
    v.section_mark(RX0 - 900, 1270, RX1 + 1400, 1270, "A", "P-03", flip=True)
    v.section_mark(XM, -800, XM, DEPTH + 1100, "B", "P-03")
    v.title(16, 130, "1/P-01", "TOP VIEW — HOUSE & ROOF", "1:50 @ A3", sub="roof edge on client's marked line")
    # ---- roof plan 1:25
    w = View(s, -235, 285, 25)
    w.rect(RX0 - 1200, 0, 1200, DEPTH, mat="masonry", w=0.4)
    w.text(RX0 - 600, DEPTH / 2, "HOUSE", size=1.8, anchor="middle", rot=90, color="#555")
    w.rect(RX0, ROOF_D, ROOF_L, FREE, w=0.15, dash="1,1", color="#888")
    w.text(RX0 + ROOF_L / 2, ROOF_D + FREE / 2 - 60, "0.90 free strip — no roof (towards plants)", size=1.6,
           anchor="middle", color="#555")
    w.rect(RX0, 0, ROOF_L, ROOF_D, w=0.5, fill="#eef0f2")
    for (y0, h) in ((0, 50), (ROOF_D - 50, 50)):
        w.rect(RX0, y0, ROOF_L, h, w=0.15, fill="#fff")
    w.rect(RX1 - 50, 0, 50, ROOF_D, w=0.15, fill="#fff")
    w.rect(GUT_X[0], 50, GUT_X[1] - GUT_X[0], ROOF_D - 100, w=0.25, fill="#cdd8e3")
    for (lab, x, y) in COLS:
        w.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.3, fill="#e7c79a")
        w.text(x, y - 40, lab, size=1.3, anchor="middle", weight="bold")
    for (lab, x, y) in COLS[1:]:
        w.circle(x, y + (-150 if y > 1000 else 150), 30, w=0.3, fill="#1f5fa8")
    for y in (650, 1300, 1950):
        a, b = w.P(RX0 + 300, y), w.P(RX1 - 400, y)
        s.line(a[0], a[1], b[0], b[1], w=0.35, color="#1f5fa8")
        s.poly([b, (b[0] - 2.2, b[1] - 0.9), (b[0] - 2.2, b[1] + 0.9)], w=0, fill="#1f5fa8")
        s.text((a[0] + b[0]) / 2, a[1] - 1, "FALL 1:70", size=1.5, anchor="middle", color="#1f5fa8", weight="bold")
    w.chain([RX0, XM, RX1], "x", 0, -7, size=1.5)
    w.chain([0, ROOF_D, DEPTH], "y", RX1, -9, size=1.5, overall=True)
    w.leader([(RX1 - 110, 1300), (RX1 + 350, 1500)], ["Box gutter 120, TPO lined,", "outlets into C2 + C3"], size=1.4)
    w.leader([(RX0 + 1200, 900), (RX0 + 1400, 400)], ["1.5 TPO / 18 ply / firrings, fall to end"], size=1.4)
    s.text(16, 147, "2/P-01  ROOF PLAN — 1:25", size=2.2, weight="bold")
    s.textblock(190, 166, 145, [
        ("B", "NOTES"),
        "1. Roof edge on the client's marked line: roof 3.22 x 2.54 m; 0.90 m strip towards the plants left free.",
        "2. Columns 200x200: C1 (middle) + C2 (corner) on the plants side, C3 front-right. Roof frames into the column "
        "sides; columns rise 0.13 above the roof.",
        "3. Roof attached to the house end wall (steel ledger); falls 1:70 to a concealed gutter at the free end; "
        "rainwater down C2 and C3.",
        "4. Door in house end wall shown dashed — confirm position.",
        "5. Triangular extension (+1.26 m) — next step.",
    ], size=1.55, gap=0.35)
    s.north_arrow(320, 28, 5)
    s.scale_bar(240, 268, 50)
    return s


# ================================================================= P-02 ELEVATIONS
def sheet_p02():
    s = sheet("P-02", "Elevations — front, plants side & end (Rev C03 preview)", "1:50")
    # ---- front elevation (looking at Y = 0 side)
    v = View(s, 30, 62, 50)
    ground(v, -500, RX1 + 600, 0, depth=200)
    v.rect(0, 0, HOUSE_L, HOUSE_TOP, w=0.4, fill="#f7f3ea")
    v.text(HOUSE_L / 2, 1200, "EXISTING HOUSE — 8.00 m", size=2.2, anchor="middle", weight="bold", color="#555")
    # C1 beyond (lighter)
    v.rect(XM - CLAD / 2, 0, CLAD, SOFFIT, w=0.15, fill="#f1e2cb", color="#b08a5a")
    v.rect(RX0, SOFFIT, ROOF_L, FASCIA, w=0.45, fill="#ffffff")
    v.rect(RX1 - CLAD, 0, CLAD, COL_TOP, w=0.35, mat="timber")
    v.line(RX0 + 30, SOFFIT - 6, RX1 - CLAD - 30, SOFFIT - 6, w=0.5, color="#f39c12")
    v.chain([0, HOUSE_L, XM, RX1], "x", 0, -8, size=1.5)
    ladder(v, -500, [(0, "±0.000"), (SOFFIT, "+2.360 u/s"), (FTOP, "+2.790"), (COL_TOP, "+2.920")], 14, size=1.35)
    v.dim((RX1, 0), (RX1, SOFFIT), -5, size=1.4)
    v.dim((RX1, SOFFIT), (RX1, FTOP), -5, size=1.4)
    s.text(16, 14, "1/P-02  FRONT ELEVATION (long side) — 1:50", size=2.0, weight="bold")

    # ---- plants-side elevation (section along the plants edge, looking towards the plants side wall line)
    w = View(s, 30, 150, 50)
    ground(w, -500, RX1 + 600, 0, depth=200)
    w.rect(0, 0, HOUSE_L, HOUSE_TOP, w=0.4, fill="#f7f3ea")
    w.rect(HOUSE_L - 600, HOUSE_TOP - 430, 600, 430, w=0.3, fill="#efe9dd")
    w.text(HOUSE_L / 2, 1200, "EXISTING HOUSE", size=2.2, anchor="middle", weight="bold", color="#555")
    w.rect(RX0, SOFFIT, ROOF_L, FASCIA, w=0.45, fill="#ffffff")
    for (lab, x, y) in COLS[:2]:
        w.rect(x - CLAD / 2, 0, CLAD, COL_TOP, w=0.35, mat="timber")
        w.text(x, COL_TOP + 120, lab, size=1.5, anchor="middle", weight="bold")
        # bracket under roof both sides of column
        for sgn in (-1, 1):
            if x + sgn * CLAD / 2 > RX1:
                continue
            cx = x + sgn * CLAD / 2
            pts = [(cx, SOFFIT), (cx + sgn * 180, SOFFIT)]
            for k in range(7):
                a = math.radians(90 * k / 6)
                pts.append((cx + sgn * (180 - 180 * math.sin(a)), SOFFIT - 180 + 180 * math.cos(a)))
            w.pl(pts, w=0.25, fill="#c9d0d6")
    for i in range(6):
        shrub(w, RX0 + 300 + i * 600, 0, 420, 380 + (i % 3) * 120, seed=40 + i, flowers=3,
              fill="#eef5e8", color="#8aa97a")
    w.chain([RX0, XM, RX1], "x", 0, -8, size=1.5)
    w.dim((0, 0), (RX1, 0), -16, size=1.5)
    w.leader([(XM + 100, SOFFIT - 120), (XM + 700, 1500)], ["Steel bracket 180 under roof/column junction"],
             size=1.4, anchor="start")
    w.leader([(XM, COL_TOP - 50), (XM - 1200, 3500)], ["Column rises 0.13 above roof"], size=1.4, anchor="start")
    s.text(16, 102, "2/P-02  PLANTS-SIDE ELEVATION — 2 COLUMNS (C1 middle, C2 corner) — 1:50", size=2.0,
           weight="bold")

    # ---- end view (looking at free end, Y horizontal)
    e = View(s, 40, 268, 50)
    ground(e, -400, DEPTH + 800, 0, depth=200)
    e.rect(-200, 0, DEPTH + 400, HOUSE_TOP, w=0.15, fill="#f7f3ea", color="#999")
    e.rect(DOOR[0], 0, DOOR[1] - DOOR[0], 2150, w=0.15, fill="#a9cde0", dash="2,1")
    e.rect(0, SOFFIT, ROOF_D, FASCIA, w=0.45, fill="#ffffff")
    for y in (0, ROOF_D - CLAD):
        e.rect(y, 0, CLAD, COL_TOP, w=0.35, mat="timber")
    for i in range(3):
        shrub(e, ROOF_D + FREE + 150 + i * 220, 0, 320, 600, seed=60 + i, flowers=3)
    e.chain([0, ROOF_D, DEPTH], "x", 0, -6, size=1.4)
    e.text(ROOF_D + FREE / 2, 1300, "0.90 free", size=1.4, anchor="middle", rot=90, color="#555")
    s.text(16, 196, "3/P-02  END VIEW (free end) — 1:50", size=2.0, weight="bold")
    notes(s, 262, 196)
    s.scale_bar(150, 268, 50)
    return s


# ================================================================= P-03 SECTIONS
def roof_layers_x(v, x0, x1):
    """Deck/firring/membrane between x0 (high, house) and x1 (low, gutter) in an X-Z view."""
    v.pl([(x0, TOS), (x1, TOS), (x1, TOS + 15), (x0, TOS + 60)], w=0.12, mat="timber")
    v.pl([(x0, TOS + 60), (x1, TOS + 15), (x1, TOS + 33), (x0, TOS + 78)], w=0.18, fill="#d9b98a")
    v.line(x0, TOS + 80, x1, TOS + 35, w=0.45, color="#111")


def sheet_p03():
    s = sheet("P-03", "Sections A-A (along roof) & B-B (across roof at C1) — Rev C03 preview", "1:20 / 1:25")
    # ---- A-A along X at Y = 1270, looking towards plants side (columns C1, C2 beyond)
    v = View(s, 40 - (RX0 - 700) / 20, 172, 20)
    paving_cut(v, [(RX0, -15), (RX1 + 500, -20)], z_bottom_extra=200)
    v.rect(RX0 - WALL, -600, WALL, HOUSE_TOP + 600 - 200, w=0.4, mat="masonry")
    v.rect(RX0 - 700, HOUSE_TOP - 200, 700, 200, w=0.35, mat="rc")
    break_line(v, RX0 - 700, -200, RX0 - 700, HOUSE_TOP + 50)
    for (lab, x, y) in COLS[:2]:
        v.rect(x - CLAD / 2, 0, CLAD, COL_TOP, w=0.2, fill="#efd9b8", color="#8a5a2b")
        v.text(x, COL_TOP + 60, lab, size=1.5, anchor="middle", weight="bold")
    upn200(v, RX0, BOS, facing=1)
    for z in (BOS + 60, BOS + 140):
        v.rect(RX0 - 130, z - 6, 140, 12, w=0.12, fill="#888")
    v.rect(LEDGER_X[1], BOS, B_END[0] - LEDGER_X[1], 200, w=0.15, fill="#e6eaee", color="#666")
    v.text((LEDGER_X[1] + B_END[0]) / 2 - 300, BOS + 80, "J1 lipped C200 joists @ ~600", size=1.4, anchor="middle")
    roof_layers_x(v, RX0 + 20, GUT_X[0])
    v.pl([(RX0 + 20, TOS + 80), (RX0 + 6, TOS + 90), (RX0 + 6, TOS + 240)], w=0.45, closed=False, color="#111")
    v.pl([(RX0, TOS + 260), (RX0 + 40, TOS + 245), (RX0 + 40, TOS + 170)], w=0.35, closed=False, color="#7f8c8d")
    rhs(v, B_END[0], BOS, 100, 200, 6.3)
    zg = TOS + 15
    v.rect(GUT_X[0], zg - 3, GUT_X[1] - GUT_X[0], 18, w=0.15, fill="#d9b98a")
    v.pl([(GUT_X[0], TOS + 35), (GUT_X[0], zg + 15), (GUT_X[1], zg + 15), (GUT_X[1], FTOP - 30)], w=0.45,
         closed=False, color="#111")
    v.pl([(RX1 - 60, SOFFIT), (RX1, SOFFIT), (RX1, FTOP), (RX1 - 45, FTOP - 6)], w=0.5, closed=False, color="#111")
    v.rect(RX0 + 10, SOFFIT + 20, RX1 - 70 - RX0, 30, w=0.1, fill="#c9a77c")
    x = RX0 + 20
    while x + 68 < RX1 - 60:
        v.rect(x, SOFFIT, 68, 20, w=0.08, mat="timber")
        x += 78
    v.rect(RX1 - 300, SOFFIT, 25, 22, w=0.2, fill="#f39c12")
    ladder(v, RX0 - 700, [(0, "±0.000"), (SOFFIT, "+2.360 u/s"), (BOS, "+2.410"), (TOS, "+2.610"),
                          (FTOP, "+2.790 top"), (COL_TOP, "+2.920 col.")], 14.5, size=1.35)
    v.chain([RX0, XM, RX1], "x", -400, -4, size=1.4)
    for tgt, txt, lines in (
            ((RX0 + 40, BOS + 100), (RX0 + 400, 3050), ["Ledger UPN 200, M12 resin anchors into house wall"]),
            ((RX0 + 1500, TOS + 55), (RX0 + 1300, 2950), ["1.5 TPO / 18 ply / tapered firrings (fall 1:70)"]),
            ((RX0 + 20, TOS + 200), (RX0 + 400, 3150), ["Membrane up 150 + alu counter-flashing"]),
            ((B_END[0] + 50, BOS + 100), (RX1 - 1500, 1800), ["End beam RHS 200x100 (C3 → C2)"]),
            ((RX1, 2600), (RX1 - 1500, 2050), ["Fascia 3 mm alu, 0.43 band"]),
            ((RX0 + 1000, SOFFIT + 10), (RX0 + 900, 1400), ["Soffit: 68x20 thermo-ash slats on battens"])):
        v.leader([tgt, txt], lines, size=1.4, anchor="start")
    s.text(16, 16, "1/P-03  SECTION A-A — ALONG ROOF (house → free end), columns C1/C2 beyond — 1:20", size=2.1,
           weight="bold")

    # ---- B-B across Y at X = XM through C1 (client sketch: roof frames into column side)
    w = View(s, 40, 272, 25)
    paving_cut(w, [(-300, -15), (DEPTH + 300, -15)], z_bottom_extra=150, joints=False)
    plants_b = [(ROOF_D + FREE + 120 + i * 230) for i in range(2)]
    for i, y in enumerate(plants_b):
        shrub(w, y, 0, 330, 700, seed=80 + i, flowers=3)
    rhs(w, B_FR[0], BOS, 100, 200, 6.3)
    for y in J_Y:
        cchan(w, y, BOS, facing=1)
    w.rect(60, TOS + 38, ROOF_D - 260, 18, w=0.15, fill="#d9b98a")
    w.line(60, TOS + 58, ROOF_D - 200, TOS + 58, w=0.45, color="#111")
    w.rect(60, SOFFIT, ROOF_D - 260, 20, w=0.12, mat="timber")
    w.rect(0, SOFFIT, 3, FASCIA, w=0.35, fill="#222")
    # column C1 cut + edge beam framing into its side + bracket
    w.rect(ROOF_D - CLAD, 0, CLAD, COL_TOP, w=0.35, mat="timber")
    w.rect(ROOF_D - CLAD + 25, 0, POST, COL_TOP - 10, w=0.3, fill="#5c6670")
    w.rect(ROOF_D - CLAD - 100, BOS, 100, 200, w=0.3, fill="#7d8790")
    pts = [(ROOF_D - CLAD, SOFFIT), (ROOF_D - CLAD - 200, SOFFIT)]
    for k in range(7):
        a = math.radians(90 * k / 6)
        pts.append((ROOF_D - CLAD - 200 + 200 * math.sin(a), SOFFIT - 200 + 200 * math.cos(a)))
    w.pl(pts, w=0.3, fill="#c9d0d6")
    w.rect(ROOF_D - CLAD - 30, COL_TOP - 10, CLAD + 60, 10, w=0.2, fill="#888")
    ladder(w, DEPTH + 300, [(0, "±0.000"), (SOFFIT, "+2.360"), (FTOP, "+2.790"), (COL_TOP, "+2.920")], 205,
           size=1.35, inside=False)
    w.chain([0, ROOF_D - CLAD, ROOF_D, DEPTH], "x", -300, -4, size=1.35)
    w.text(ROOF_D + FREE / 2, 1300, "0.90 FREE", size=1.5, anchor="middle", rot=90, color="#555")
    for tgt, txt, lines in (
            ((ROOF_D - 100, 1500), (ROOF_D + 1100, 1900), ["Column C1 SHS 150x150x8, timber-clad 200x200"]),
            ((ROOF_D - CLAD - 50, BOS + 100), (ROOF_D + 1100, 3100), ["Edge beam frames into column side (fin plate)"]),
            ((ROOF_D - CLAD - 80, SOFFIT - 80), (ROOF_D + 1100, 2300), ["Steel bracket R 200 under junction"]),
            ((ROOF_D - 100, COL_TOP - 5), (ROOF_D + 1100, 3350), ["Column cap 0.13 above roof"]),
            ((J_Y[1], BOS + 100), (600, 3300), ["Joists C200, deck, membrane"])):
        w.leader([tgt, txt], lines, size=1.35, anchor="start")
    s.text(16, 168, "2/P-03  SECTION B-B — ACROSS ROOF AT C1 (as client sketch) — 1:25", size=2.1, weight="bold")
    s.scale_bar(240, 270, 20, 2)
    return s


# ================================================================= P-04 FRAMING & DETAILS
def sheet_p04():
    s = sheet("P-04", "Roof framing plan & column details (Rev C03 preview)", "1:25 / 1:10")
    v = View(s, 40 - (RX0 - 600) / 25, 140, 25)
    v.rect(RX0 - 600, 0, 600, DEPTH, mat="masonry", w=0.4)
    v.rect(RX0, ROOF_D, ROOF_L, FREE, w=0.15, dash="1,1", color="#888")
    v.text(RX0 + ROOF_L / 2, ROOF_D + FREE / 2 - 60, "0.90 free — no roof", size=1.6, anchor="middle", color="#555")
    v.rect(RX0, 0, ROOF_L, ROOF_D, w=0.2, dash="3,1.2", color="#777")
    v.rect(LEDGER_X[0], 150, 75, ROOF_D - 300, w=0.3, fill="#5c6670")
    v.rect(RX0 + 75, B_FR[0], RX1 - 200 - RX0 - 75, 100, w=0.35, fill="#7d8790")
    v.rect(RX0 + 75, B_PL[0], XM - 100 - RX0 - 75, 100, w=0.35, fill="#7d8790")
    v.rect(XM + 100, B_PL[0], RX1 - 200 - XM - 100, 100, w=0.35, fill="#7d8790")
    v.rect(B_END[0], 200, 100, ROOF_D - 400, w=0.35, fill="#7d8790")
    for y in J_Y:
        v.rect(LEDGER_X[1], y - 32, B_END[0] - LEDGER_X[1], 65, w=0.2, fill="#c9d0d6")
    for (lab, x, y) in COLS:
        v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
        v.tag(x + (0 if lab == "C1" else 330), y + (330 if y > 1000 else -330), lab, shape="circle", r=2.0, size=1.4)
    v.tag(RX0 + 300, ROOF_D / 2, "L1", shape="rect", r=1.8, size=1.4)
    v.tag(RX0 + 900, 100, "B3", shape="rect", r=1.8, size=1.4)
    v.tag(RX0 + 900, ROOF_D - 100, "B2", shape="rect", r=1.8, size=1.4)
    v.tag(B_END[0] + 50, ROOF_D / 2, "B1", shape="rect", r=1.8, size=1.4)
    for y in J_Y:
        v.tag(RX0 + 2300, y, "J1", shape="rect", r=1.4, size=1.1)
    v.chain([RX0, XM, RX1], "x", 0, -8, size=1.3)
    v.chain([0, 150] + [round(y) for y in J_Y] + [ROOF_D - 150, ROOF_D, DEPTH], "y", RX1, -12, size=1.2)
    s.text(16, 16, "1/P-04  ROOF FRAMING PLAN @ TOS +2.610 — 1:25", size=2.1, weight="bold")
    rows = [
        ["L1", "UPN 200 S275 HDG ledger on house wall", "1", "2.24 m", "M12 resin anchors @ 400"],
        ["B1", "RHS 200x100x6.3 end beam", "1", "2.14 m", "C3 → C2"],
        ["B2", "RHS 200x100x6.3 plants-side edge beam", "2", "1.4 / 1.3", "house → C1 → C2"],
        ["B3", "RHS 200x100x6.3 front edge beam", "1", "3.0 m", "house → C3"],
        ["J1", "Lipped C 200x65x20x1.8", "3", "2.99 m", "@ ~600 c/c"],
        ["C1-C3", "SHS 150x150x8, clad to 200x200", "3", "2.92 m", "RWP in C2 + C3; pads 800x800x700"],
    ]
    s.table(16, 165, [("Mark", 14), ("Member", 64), ("No.", 9), ("Length", 17), ("Note", 46)], rows, size=1.45)
    s.textblock(16, 205, 150, [
        ("B", "STRUCTURE (preliminary — engineer to confirm)"),
        "Roof 3.22 x 2.54 m, G 0.65 + snow 1.0 kN/m² (assumed). Max beam span 3.0 m: M ≈ 4 kNm (≈ 5 % capacity). "
        "Columns N ≈ 8 kN. Plywood deck acts as diaphragm to house wall. All steel hot-dip galvanised.",
    ], size=1.5, gap=0.3)

    # ---- D1 column / roof junction 1:10 (client section sketch)
    d = View(s, 238, 132, 10, origin=(ROOF_D - 200, SOFFIT))
    d.rect(ROOF_D - CLAD, 1500, CLAD, COL_TOP - 1500, w=0.35, mat="timber")
    d.rect(ROOF_D - CLAD + 25, 1500, POST, COL_TOP - 1510, w=0.3, fill="#5c6670")
    d.rect(ROOF_D - CLAD + 33, 1500, POST - 16, COL_TOP - 1510, w=0.1, fill="#fff")
    d.rect(ROOF_D - CLAD - 30, COL_TOP - 10, CLAD + 60, 10, w=0.25, fill="#888")
    break_line(d, ROOF_D - CLAD - 20, 1500, ROOF_D + 20, 1500)
    d.rect(ROOF_D - CLAD - 900, BOS, 900, 200, w=0.3, fill="#7d8790")
    d.rect(ROOF_D - CLAD - 900, BOS + 6, 900, 188, w=0.1, fill="#fff")
    d.rect(ROOF_D - CLAD - 100, BOS + 40, 100, 120, w=0.2, fill="#444")
    for z in (BOS + 70, BOS + 130):
        d.circle(ROOF_D - CLAD - 50, z, 9, w=0.2, fill="#999")
    pts = [(ROOF_D - CLAD, SOFFIT), (ROOF_D - CLAD - 200, SOFFIT)]
    for k in range(7):
        a = math.radians(90 * k / 6)
        pts.append((ROOF_D - CLAD - 200 + 200 * math.sin(a), SOFFIT - 200 + 200 * math.cos(a)))
    d.pl(pts, w=0.3, fill="#c9d0d6")
    d.pl([(ROOF_D - CLAD - 900, TOS + 40), (ROOF_D - CLAD, TOS + 40), (ROOF_D - CLAD, FTOP - 20)], w=0.45,
         closed=False, color="#111")
    d.rect(ROOF_D - CLAD - 900, SOFFIT, 900, 20, w=0.12, mat="timber")
    d.rect(ROOF_D - CLAD - 900, SOFFIT + 20, 900, 30, w=0.1, fill="#c9a77c")
    for tgt, txt, lines in (
            ((ROOF_D - 100, 2000), (ROOF_D + 120, 2100), ["SHS 150x150x8 +", "25 thermo-ash cladding"]),
            ((ROOF_D - 100, COL_TOP - 5), (ROOF_D + 120, 3050), ["Cap plate, column", "+0.13 above roof"]),
            ((ROOF_D - CLAD - 50, BOS + 100), (ROOF_D + 120, 2700), ["FP 12 welded to column,", "2 M16 into edge beam"]),
            ((ROOF_D - CLAD - 60, SOFFIT - 60), (ROOF_D + 120, 2300), ["Bracket R 200, 10 mm", "plate, welded"]),
            ((ROOF_D - CLAD - 400, TOS + 40), (ROOF_D - CLAD - 900, 3050), ["Membrane turned up", "column 150"])):
        d.leader([tgt, txt], lines, size=1.25, anchor="start")
    s.text(212, 16, "D1  ROOF / COLUMN JUNCTION — 1:10", size=2.0, weight="bold")
    s.text(212, 20, "(as client section sketch)", size=1.4)

    # ---- D2 column base 1:10
    b = View(s, 262, 248, 10, origin=(0, 0))
    b.pl([(-450, -950), (450, -950), (450, -80), (-450, -80)], w=0, mat="earth")
    paving_cut(b, [(-450, -15), (-120, -15)], z_bottom_extra=60, joints=False)
    paving_cut(b, [(120, -15), (450, -15)], z_bottom_extra=60, joints=False)
    b.rect(-400, FTG_BOT, FTG, FTG_D, w=0.4, mat="rc")
    b.rect(-150, FTG_BOT + FTG_D, 300, -15 - (FTG_BOT + FTG_D) - 60, w=0.35, mat="rc")
    b.rect(-125, -75, 250, 15, w=0.3, mat="steel")
    b.rect(-75, -60, 150, 360, w=0.3, fill="#5c6670")
    b.rect(-100, -30, 25, 330, w=0.12, mat="timber")
    b.rect(75, -30, 25, 330, w=0.12, mat="timber")
    break_line(b, -130, 300, 130, 300)
    for tgt, txt, lines in (((90, -70), (150, 150), ["PL 250x250x15, 4 M16"]),
                            ((0, -500), (150, -500), ["Pad 800x800x700", "C25/30"])):
        b.leader([tgt, txt], lines, size=1.25, anchor="start")
    s.text(212, 196, "D2  COLUMN BASE — 1:10", size=2.0, weight="bold")
    return s


def sheets():
    return [sheet_p01(), sheet_p02(), sheet_p03(), sheet_p04()]


if __name__ == "__main__":
    import build
    ss = sheets()
    for s in ss:
        build.preview(s, "../preview/" + s.number + ".png", scale=1.2)
    print(build.to_pdf(ss, "Rev-C03_Preview_4-sheets"))
