"""Rev C02 PREVIEW — roof per client hand sketch (metres):
House 8.00 m long x 3.44 m deep (sketch: 0.90 + 0.20 + 2.54 internal split).
Roof 3.22 m long x 3.44 m deep, attached to the house end wall, in line with the house.
Posts at the two free corners. Underside +2.36, fascia band 0.43 (top +2.79).
Triangular extension (+1.26) NOT included — next step.

Axes (as the sketch TOP view): X along the house/roof length (house X 0..8000, roof X 8000..11220),
Y across (bottom edge Y = 0, top edge Y = 3440). Z = height above finished ground ±0.000.
"""
import math
from cad import Sheet, View, break_line, PROJECT
from common import shrub, vine, ground, GREEN, GREEN_F
from sheets_b import ladder, paving_cut, rhs, upn200, cchan
from sheets_c import bolt

# ----------------------------------------------------------------- geometry (mm)
HOUSE_L, DEPTH = 8000, 3440
WALL = 200
SPLIT = 2540                      # 2.54 from bottom edge; 0.90 zone above (sketch)
ROOF_L = 3220
RX0, RX1 = HOUSE_L, HOUSE_L + ROOF_L
SOFFIT, FASCIA = 2360, 430
FTOP = SOFFIT + FASCIA            # 2790
BOS = SOFFIT + 50
TOS = BOS + 200
DECK_HI, DECK_LO = TOS + 60 + 18, TOS + 15 + 18
POST, CLAD = 150, 200
POSTS = [(RX1 - 100, 100), (RX1 - 100, DEPTH - 100)]   # flush with the free corners (side view)
B1_X = (RX1 - 150, RX1 - 50)      # front beam RHS 200x100 between posts (along Y)
SIDE_Y = [(50, 150), (DEPTH - 150, DEPTH - 50)]          # side beams RHS 200x100 (along X)
LEDGER_X = (RX0, RX0 + 75)
J_Y0, J_Y1 = 150, DEPTH - 150
NJB = 6
JOISTS = [J_Y0 + (J_Y1 - J_Y0) * i / NJB for i in range(1, NJB)]
GUT_X = (RX1 - 170, RX1 - 50)     # front box gutter over B1 zone
HOUSE_TOP = FTOP                  # sketch: house & roof share the top line (survey!)
DOOR = (900, 1900)                # assumed door in house end wall (Y range) — verify
FTG, FTG_D, FTG_BOT, PED_TOP = 800, 700, -900, 420

PJ = dict(PROJECT)
PJ["rev"] = "C02"
PJ["date"] = "07.10.2026"
PJ["status"] = "PREVIEW FOR CLIENT REVIEW — dimensions per client sketch; not for construction until confirmed"
PJ["site"] = "Roof (canopy) 3.22 x 3.44 m attached to end of existing 8.00 m house — per client hand sketch"


def sheet(num, title, scale):
    s = Sheet(num, title, scale, project=PJ)
    s.frame()
    return s


def dims_note(s, x, y):
    s.textblock(x, y, 74, [
        ("B", "CLIENT SKETCH DIMENSIONS (m)"),
        "House length 8.00 · Roof length 3.22 · Depth 3.44 (= 0.90 + 2.54) · wall / beam 0.20 · "
        "Roof underside 2.36 · Fascia band 0.43 (top 2.79).",
        "Triangular roof extension (+1.26) — next step, not shown.",
    ], size=1.5, gap=0.3)


# ================================================================= P-01 TOP VIEW / PLANS
def plan_house(v, detail=True):
    v.rect(0, 0, HOUSE_L, DEPTH, mat="masonry", w=0.45)
    v.rect(WALL, WALL, HOUSE_L - 2 * WALL, SPLIT - 2 * WALL + WALL, w=0.3, fill="#fbfaf7")
    v.rect(WALL, SPLIT, HOUSE_L - 2 * WALL, DEPTH - SPLIT - WALL, w=0.3, fill="#fbfaf7")
    # door in end wall (assumed)
    v.rect(HOUSE_L - WALL, DOOR[0], WALL, DOOR[1] - DOOR[0], w=0.15, fill="#fff")
    v.line(HOUSE_L - WALL, DOOR[0], HOUSE_L - WALL - (DOOR[1] - DOOR[0]), DOOR[0], w=0.25)
    v.arc(HOUSE_L - WALL, DOOR[0], DOOR[1] - DOOR[0], 90, 180, w=0.12)
    if detail:
        v.text(HOUSE_L / 2, SPLIT / 2, "EXISTING HOUSE", size=2.4, anchor="middle", weight="bold", color="#555")
        v.text(HOUSE_L / 2, SPLIT / 2 - 400, "(internal layout indicative)", size=1.6, anchor="middle", color="#777")


def plan_roof_outline(v, dashed=True):
    v.rect(RX0, 0, ROOF_L, DEPTH, w=0.45, dash="4,1.5" if dashed else None)


def plan_posts(v):
    for (x, y) in POSTS:
        v.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.2, fill="#e7c79a")
        v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")


def sheet_p01():
    s = sheet("P-01", "Top view — site plan & roof plan (Rev C02 preview)", "1:50 / 1:25")
    # ---- overall top view 1:50
    v = View(s, 40, 88, 50)
    v.rect(-300, -1000, RX1 + 1300, 1000, w=0, fill="#f3eee4")        # paving in front (indicative)
    v.text(5000, -650, "COURTYARD / PAVING (extent per site)", size=1.6, anchor="middle", color="#888")
    plan_house(v)
    v.rect(RX0, 0, ROOF_L, DEPTH, w=0, fill="#f3eee4")
    plan_posts(v)
    plan_roof_outline(v)
    v.line(RX0, SPLIT, RX1, SPLIT, w=0.12, dash="2,1", color="#777")
    v.text(RX0 + ROOF_L / 2, DEPTH / 2 + 250, "ROOF OVER", size=2.2, anchor="middle", weight="bold")
    v.text(RX0 + ROOF_L / 2, DEPTH / 2 - 250, "3.22 x 3.44 m", size=1.9, anchor="middle")
    v.chain([0, HOUSE_L, RX1], "x", 0, -14, size=1.8)
    v.chain([0, SPLIT - WALL, SPLIT, DEPTH], "y", 0, 10, size=1.6, texts=["2340", "200", "900"], overall=False)
    v.chain([0, SPLIT, DEPTH], "y", RX1, -10, size=1.8, overall=True)
    v.section_mark(RX0 - 900, 1500, RX1 + 900, 1500, "A", "P-03", flip=True)
    v.section_mark(9600, -800, 9600, DEPTH + 700, "B", "P-03")
    v.title(16, 126, "1/P-01", "TOP VIEW — HOUSE & ROOF", "1:50 @ A3", sub="dimensions in mm (sketch in m)")
    # ---- roof plan 1:25
    w = View(s, -235, 287, 25)
    w.rect(RX0 - 1200, 0, 1200, DEPTH, mat="masonry", w=0.4)
    w.text(RX0 - 600, DEPTH / 2, "HOUSE", size=1.8, anchor="middle", rot=90, color="#555")
    w.rect(RX0, 0, ROOF_L, DEPTH, w=0.5, fill="#eef0f2")
    w.rect(RX0, 0, ROOF_L, 50, w=0.15, fill="#fff")
    w.rect(RX0, DEPTH - 50, ROOF_L, 50, w=0.15, fill="#fff")
    w.rect(RX1 - 50, 0, 50, DEPTH, w=0.15, fill="#fff")
    w.rect(GUT_X[0], 50, GUT_X[1] - GUT_X[0], DEPTH - 100, w=0.25, fill="#cdd8e3")
    for (x, y) in POSTS:
        w.rect(x - CLAD / 2, y - CLAD / 2, CLAD, CLAD, w=0.2, dash="1.5,0.8")
        w.circle(x, y, 40, w=0.3, fill="#1f5fa8")
    for y in (900, 1700, 2500):
        a, b = w.P(RX0 + 300, y), w.P(RX1 - 400, y)
        s.line(a[0], a[1], b[0], b[1], w=0.35, color="#1f5fa8")
        s.poly([b, (b[0] - 2.2, b[1] - 0.9), (b[0] - 2.2, b[1] + 0.9)], w=0, fill="#1f5fa8")
        s.text((a[0] + b[0]) / 2, a[1] - 1, "FALL 1:70", size=1.6, anchor="middle", color="#1f5fa8", weight="bold")
    w.level(RX0 + 250, 300, f"+{DECK_HI / 1000:.3f} deck high", plan=True, size=1.4)
    w.level(RX1 - 900, 300, f"+{DECK_LO / 1000:.3f} deck low", plan=True, size=1.4)
    w.chain([RX0, RX1 - 150, RX1], "x", 0, -7, size=1.5)
    w.chain([0, 150, SPLIT, DEPTH - 150, DEPTH], "y", RX1, -9, size=1.4, overall=True)
    w.leader([(RX1 - 110, 1800), (RX1 + 350, 2100)], ["Box gutter 120 wide, TPO lined,", "falls to outlets at both posts"],
             size=1.4)
    w.leader([(POSTS[1][0], POSTS[1][1]), (RX1 + 350, 3300)], ["Outlet Ø63 → RWP Ø75 inside post"], size=1.4)
    w.leader([(RX0 + 1200, 2000), (RX0 + 1400, 2900)], ["1.5 TPO / 18 ply / firrings 60→15"], size=1.4)
    s.text(16, 143, "2/P-01  ROOF PLAN — 1:25", size=2.2, weight="bold")
    s.textblock(190, 165, 145, [
        ("B", "NOTES"),
        "1. All dimensions per client hand sketch (07.10.2026), metres converted to mm. Verify on site before ordering.",
        "2. Roof attached to the house end wall with a steel ledger; free end on 2 corner posts (200 x 200 finished).",
        "3. Roof falls 1:70 away from the house to a concealed box gutter inside the front fascia; rainwater down both posts.",
        "4. Door in house end wall shown dashed — position/size to be confirmed by survey.",
        "5. The 0.90 / 0.20 / 2.54 split of the house depth is drawn as sketched (internal wall / zone line).",
        "6. Triangular extension (+1.26 m) is the next step and is not part of this preview.",
    ], size=1.55, gap=0.35)
    s.north_arrow(320, 28, 5)
    s.scale_bar(240, 268, 50)
    return s


# ================================================================= P-02 SIDE & END VIEWS
def sheet_p02():
    s = sheet("P-02", "Side view & end view (Rev C02 preview)", "1:50 / 1:25")
    # ---- side view 1:50 (looking at the Y = 0 long side)
    v = View(s, 30, 95, 50)
    ground(v, -500, RX1 + 600, 0, depth=250)
    v.rect(0, 0, HOUSE_L, HOUSE_TOP, w=0.4, fill="#f7f3ea")
    v.rect(0, HOUSE_TOP - 60, HOUSE_L, 60, w=0.25, fill="#efe9dd")
    v.text(HOUSE_L / 2, 1300, "EXISTING HOUSE — 8.00 m", size=2.4, anchor="middle", weight="bold", color="#555")
    v.text(HOUSE_L / 2, 1000, "(height & openings to be surveyed)", size=1.6, anchor="middle", color="#777")
    # roof fascia & post
    v.rect(RX0, SOFFIT, ROOF_L, FASCIA, w=0.45, fill="#ffffff")
    v.line(RX0, SOFFIT - 6, RX1 - CLAD, SOFFIT - 6, w=0.5, color="#f39c12")
    v.rect(RX1 - CLAD, 0, CLAD, SOFFIT, w=0.35, mat="timber")
    vine(v, RX1 - 100, 300, SOFFIT, seed=3, amp=60)
    v.chain([0, HOUSE_L, RX1], "x", 0, -9, size=1.7)
    v.dim((RX1, 0), (RX1, SOFFIT), -6, size=1.6)
    v.dim((RX1, SOFFIT), (RX1, FTOP), -6, size=1.6)
    v.dim((RX1, 0), (RX1, FTOP), -14, size=1.6)
    ladder(v, -500, [(0, "±0.000"), (SOFFIT, "+2.360 u/s roof"), (FTOP, "+2.790 top")], 14, size=1.5)
    v.leader([(RX0 + 1600, SOFFIT + 200), (RX0 + 800, 3700)], ["Fascia band 0.43 m, 3 mm aluminium RAL 9010"], size=1.6)
    v.leader([(RX1 - 100, 1500), (RX1 + 500, 1900)], ["Post 200x200 (SHS 150 timber-clad)"], size=1.6)
    v.title(16, 120, "1/P-02", "SIDE VIEW — HOUSE + ROOF", "1:50 @ A3", sub="as client sketch side view")
    # ---- end view 1:25 (looking at the free end, X = RX1, Y horizontal)
    w = View(s, 70, 250, 25)
    ground(w, -400, DEPTH + 400, 0, depth=200)
    w.rect(-300, 0, DEPTH + 600, HOUSE_TOP + 0, w=0.2, fill="#f7f3ea", color="#999")
    w.text(DEPTH / 2, HOUSE_TOP - 250, "house end wall beyond", size=1.5, anchor="middle", color="#777")
    w.rect(DOOR[0], 0, DOOR[1] - DOOR[0], 2150, w=0.2, fill="#a9cde0", dash="2,1")
    w.text((DOOR[0] + DOOR[1]) / 2, 1000, "door (verify)", size=1.4, anchor="middle", rot=90, color="#555")
    w.rect(0, SOFFIT, DEPTH, FASCIA, w=0.45, fill="#ffffff")
    w.line(CLAD, SOFFIT - 6, DEPTH - CLAD, SOFFIT - 6, w=0.5, color="#f39c12")
    for y in (0, DEPTH - CLAD):
        w.rect(y, 0, CLAD, SOFFIT, w=0.35, mat="timber")
    w.chain([0, CLAD, SPLIT, DEPTH - CLAD, DEPTH], "x", 0, -7, size=1.5)
    w.dim((0, 0), (DEPTH, 0), -14, size=1.6)
    w.chain([0, SOFFIT, FTOP], "y", DEPTH, -8, size=1.6)
    w.leader([(DEPTH / 2, FTOP - 100), (DEPTH / 2 + 400, 3300)], ["Front fascia 0.43 / concealed gutter behind"],
             size=1.5)
    w.leader([(DEPTH - 100, 1200), (DEPTH + 500, 1500)], ["2 corner posts"], size=1.5)
    s.text(16, 142, "2/P-02  END VIEW (free end of roof) — 1:25", size=2.2, weight="bold")
    dims_note(s, 262, 150)
    s.scale_bar(240, 268, 25, 2)
    return s


# ================================================================= P-03 SECTIONS
def sheet_p03():
    s = sheet("P-03", "Sections A-A (along roof) & B-B (across roof) — Rev C02 preview", "1:20 / 1:25")
    # ---- A-A longitudinal at Y = 1500, looking north (+Y); X horizontal
    v = View(s, 40 - (RX0 - 700) / 20, 172, 20)
    paving_cut(v, [(RX0, -15), (RX1 + 500, -20)], z_bottom_extra=200)
    # house end wall cut + slab
    v.rect(RX0 - WALL, -600, WALL, HOUSE_TOP + 600 - 200, w=0.4, mat="masonry")
    v.rect(RX0 - 700, HOUSE_TOP - 200, 700, 200, w=0.35, mat="rc")
    v.rect(RX0 - 700, -150, 500, 150, w=0.3, mat="rc")
    break_line(v, RX0 - 700, -200, RX0 - 700, HOUSE_TOP + 50)
    # ledger
    upn200(v, RX0, BOS, facing=1)
    for z in (BOS + 60, BOS + 140):
        v.rect(RX0 - 130, z - 6, 140, 12, w=0.12, fill="#888")
    # joist beyond, firring, deck, membrane
    v.rect(LEDGER_X[1], BOS, B1_X[0] - LEDGER_X[1], 200, w=0.15, fill="#e6eaee", color="#666")
    v.text((LEDGER_X[1] + B1_X[0]) / 2, BOS + 80, "J1 lipped C200 beyond @ ~520 c/c", size=1.4, anchor="middle")
    v.pl([(LEDGER_X[1], TOS), (GUT_X[0], TOS), (GUT_X[0], TOS + 15), (LEDGER_X[1], TOS + 60)], w=0.12, mat="timber")
    v.pl([(RX0 + 20, TOS + 60), (GUT_X[0], TOS + 15), (GUT_X[0], TOS + 33), (RX0 + 20, TOS + 78)], w=0.18,
         fill="#d9b98a")
    v.pl([(GUT_X[0], TOS + 33), (RX0 + 20, TOS + 78), (RX0 + 6, TOS + 90), (RX0 + 6, TOS + 240)], w=0.45,
         closed=False, color="#111")
    v.pl([(RX0, TOS + 260), (RX0 + 40, TOS + 245), (RX0 + 40, TOS + 170)], w=0.35, closed=False, color="#7f8c8d")
    # front beam B1 cut + gutter + fascia
    rhs(v, B1_X[0], BOS, 100, 200, 6.3)
    zg = TOS + 15
    v.rect(GUT_X[0], TOS + 5, GUT_X[1] - GUT_X[0], 10, w=0.1, mat="timber")
    v.rect(GUT_X[0], zg - 3, GUT_X[1] - GUT_X[0], 18, w=0.15, fill="#d9b98a")
    v.rect(GUT_X[1], BOS + 40, 18, FTOP - 30 - BOS - 40, w=0.15, fill="#d9b98a")
    v.pl([(GUT_X[0], TOS + 33), (GUT_X[0], zg + 15), (GUT_X[1], zg + 15), (GUT_X[1], FTOP - 30), (GUT_X[1] + 18, FTOP - 30)],
         w=0.45, closed=False, color="#111")
    v.pl([(RX1 - 60, SOFFIT), (RX1, SOFFIT), (RX1, FTOP), (RX1 - 45, FTOP - 6), (RX1 - 45, FTOP - 30)], w=0.5,
         closed=False, color="#111")
    # soffit: battens (seen) + slats cut? slats run along Y -> cut in A-A
    v.rect(RX0 + 10, SOFFIT + 20, RX1 - 70 - RX0, 30, w=0.1, fill="#c9a77c")
    x = RX0 + 20
    while x + 68 < RX1 - 60:
        v.rect(x, SOFFIT, 68, 20, w=0.08, mat="timber")
        x += 78
    v.rect(RX1 - 300, SOFFIT, 25, 22, w=0.2, fill="#f39c12")
    # post beyond
    v.rect(RX1 - CLAD, 0, CLAD, SOFFIT, w=0.2, fill="#efd9b8", color="#8a5a2b")
    ladder(v, RX0 - 700, [(0, "±0.000"), (SOFFIT, "+2.360 u/s"), (BOS, "+2.410 BOS"), (TOS, "+2.610 TOS"),
                          (DECK_HI, f"+{DECK_HI / 1000:.3f} deck"), (FTOP, "+2.790 top")], 14.5, size=1.35)
    v.chain([RX0, B1_X[0], RX1], "x", -400, -4, size=1.4)
    v.dim((RX1, SOFFIT), (RX1, FTOP), -6, size=1.4)
    C = [
        ((RX0 + 40, BOS + 100), (RX0 + 500, 3050), ["Ledger UPN 200 HDG, M12 resin anchors @ 400 into house wall"]),
        ((RX0 + 1500, TOS + 50), (RX0 + 1400, 2950), ["1.5 TPO / 18 ply / tapered firrings (fall 1:70)"]),
        ((RX0 + 20, TOS + 200), (RX0 + 500, 3150), ["Membrane up 150 + alu counter-flashing chased into wall"]),
        ((B1_X[0] + 50, BOS + 100), (RX1 - 1600, 1800), ["Front beam RHS 200x100x6.3"]),
        ((GUT_X[0] + 60, zg + 10), (RX1 - 1600, 1650), ["Box gutter 120, TPO lined"]),
        ((RX1, 2600), (RX1 - 1600, 2150), ["Fascia 3 mm alu, 0.43 band"]),
        ((RX0 + 1000, SOFFIT + 10), (RX0 + 900, 1400), ["Soffit: 68x20 thermo-ash slats, 10 gaps, on 50x30 battens"]),
        ((RX1 - 288, SOFFIT), (RX1 - 1600, 1250), ["LED strip in recessed profile"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.4, anchor="start")
    s.text(16, 16, "1/P-03  SECTION A-A — ALONG ROOF (house wall → free end) — 1:20", size=2.2, weight="bold")

    # ---- B-B transverse at X = 9600 looking +X (towards free end); Y horizontal
    w = View(s, 268, 262, 50)
    paving_cut(w, [(-100, -15), (DEPTH + 100, -15)], z_bottom_extra=150, joints=False)
    for (y0, y1) in SIDE_Y:
        rhs(w, y0, BOS, 100, 200, 6.3)
    for y in JOISTS:
        cchan(w, y, BOS, facing=1)
    for y in [100] + JOISTS + [DEPTH - 100]:
        w.rect(y - 22, TOS, 45, 38, w=0.1, mat="timber")
        w.rect(y - 25, SOFFIT + 20, 50, 30, w=0.1, mat="timber")
    w.rect(50, TOS + 38, DEPTH - 100, 18, w=0.15, fill="#d9b98a")
    w.line(50, TOS + 58, DEPTH - 50, TOS + 58, w=0.45, color="#111")
    w.rect(60, SOFFIT, DEPTH - 120, 20, w=0.12, mat="timber")
    for y in (0, DEPTH - 3):
        w.rect(y, SOFFIT, 3, FASCIA, w=0.35, fill="#222")
    for (x, y) in POSTS:
        w.rect(y - CLAD / 2, 0, CLAD, SOFFIT, w=0.2, fill="#efd9b8", color="#8a5a2b")
    w.rect(CLAD, SOFFIT - 0.1, DEPTH - 2 * CLAD, 0.1, w=0)
    w.chain([0, SPLIT, DEPTH], "x", -200, -4, size=1.3)
    w.dim((DEPTH, 0), (DEPTH, SOFFIT), -3, size=1.2)
    w.dim((DEPTH, SOFFIT), (DEPTH, FTOP), -3, size=1.2)
    w.leader([(JOISTS[2], BOS + 100), (600, 1500)], ["J1 C200 joists", "side beams RHS 200x100"], size=1.3,
             anchor="start")
    s.text(266, 192, "2/P-03  SECTION B-B 1:50", size=1.9, weight="bold")
    s.text(266, 196, "across roof, looking to free end", size=1.4)
    s.scale_bar(240, 268, 20, 2)
    return s


# ================================================================= P-04 FRAMING & DETAILS
def sheet_p04():
    s = sheet("P-04", "Roof framing plan & key details (Rev C02 preview)", "1:25 / 1:10 / 1:5")
    # ---- framing plan 1:25 (X right, Y up)
    v = View(s, 40 - (RX0 - 600) / 25, 165, 25)
    v.rect(RX0 - 600, 0, 600, DEPTH, mat="masonry", w=0.4)
    v.rect(RX0, 0, ROOF_L, DEPTH, w=0.2, dash="3,1.2", color="#777")
    v.rect(LEDGER_X[0], 150, 75, DEPTH - 300, w=0.3, fill="#5c6670")
    for (y0, y1) in SIDE_Y:
        v.rect(RX0 + 75, y0, B1_X[0] - RX0 - 75 + 0, 100, w=0.35, fill="#7d8790")
    v.rect(B1_X[0], 150, 100, DEPTH - 300, w=0.35, fill="#7d8790")
    for y in JOISTS:
        v.rect(LEDGER_X[1], y - 32, B1_X[0] - LEDGER_X[1], 65, w=0.2, fill="#c9d0d6")
    for (x, y) in POSTS:
        v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222")
    v.tag(RX0 + 300, DEPTH / 2, "L1", shape="rect", r=1.8, size=1.4)
    v.tag(RX0 + 1600, 100, "B2", shape="rect", r=1.8, size=1.4)
    v.tag(RX0 + 1600, DEPTH - 100, "B2", shape="rect", r=1.8, size=1.4)
    v.tag(B1_X[0] + 50, DEPTH / 2, "B1", shape="rect", r=1.8, size=1.4)
    for y in JOISTS:
        v.tag(RX0 + 2200, y, "J1", shape="rect", r=1.4, size=1.1)
    for i, (x, y) in enumerate(POSTS):
        v.tag(x + 380, y + (250 if i else -250), f"P{i + 1}", shape="circle", r=2.0, size=1.4)
    v.chain([RX0, LEDGER_X[1], B1_X[0], B1_X[1], RX1], "x", 0, -8, size=1.3)
    v.chain([0, 150] + [round(y) for y in JOISTS] + [DEPTH - 150, DEPTH], "y", RX1, -14, size=1.2)
    s.text(16, 16, "1/P-04  ROOF FRAMING PLAN @ TOS +2.610 — 1:25", size=2.2, weight="bold")
    rows = [
        ["L1", "UPN 200 S275 HDG ledger", "1", "3.14 m", "M12 resin anchors @ 400 stagg."],
        ["B1", "RHS 200x100x6.3 S355 front beam", "1", "3.14 m", "span 3.24 between posts"],
        ["B2", "RHS 200x100x6.3 S355 side beams", "2", "3.00 m", "ledger → posts"],
        ["J1", "Lipped C 200x65x20x1.8 S350GD", str(len(JOISTS)), "2.99 m", f"@ {round((J_Y1 - J_Y0) / NJB)} c/c"],
        ["P1/P2", "SHS 150x150x8 S355, clad to 200x200", "2", "2.41 m", "Ø75 RWP inside, pads 800x800x700"],
    ]
    s.table(16, 178, [("Mark", 14), ("Member", 62), ("No.", 9), ("Length", 15), ("Note", 50)], rows, size=1.45)
    s.textblock(16, 210, 150, [
        ("B", "STRUCTURE (preliminary — engineer to confirm)"),
        "Loads: G 0.65 kN/m², snow 1.0 kN/m² (assumed), wind uplift checked. B1: M ≈ 6 kNm (≈ 8 % of capacity), "
        "deflection < 3 mm. Posts N ≈ 13 kN. Deck plywood acts as diaphragm to the house wall. All steel hot-dip galvanised.",
    ], size=1.5, gap=0.3)

    # ---- D1 post base 1:10 (Y horizontal at P2)
    d = View(s, 262, 100, 10, origin=(0, 0))
    d.pl([(-500, -1000), (500, -1000), (500, -80), (-500, -80)], w=0, mat="earth")
    paving_cut(d, [(-500, -15), (-120, -15)], z_bottom_extra=60, joints=False)
    paving_cut(d, [(120, -15), (500, -15)], z_bottom_extra=60, joints=False)
    d.rect(-400, FTG_BOT, FTG, FTG_D, w=0.4, mat="rc")
    d.rect(-150, FTG_BOT + FTG_D, 300, -15 - (FTG_BOT + FTG_D) - 60, w=0.35, mat="rc")
    d.rect(-125, -75, 250, 15, w=0.3, mat="steel")
    d.rect(-75, -60, 150, 660, w=0.3, fill="#5c6670")
    d.rect(-67, -60, 134, 660, w=0.1, fill="#fff")
    d.rect(-100, -30, 25, 630, w=0.12, mat="timber")
    d.rect(75, -30, 25, 630, w=0.12, mat="timber")
    d.rect(-35, -60, 70, 660, w=0.15, dash="2,1", color="#1f5fa8")
    d.pl([(-40, -75), (-40, -350), (500, -350), (500, -250), (40, -250), (40, -75)], w=0.2, color="#1f5fa8",
         fill="#dbe7f3")
    for x in (-90, 90):
        d.rect(x - 8, -480, 16, 420, w=0.1, fill="#888")
    break_line(d, -130, 600, 130, 600)
    for tgt, txt, lines in (((0, 450), (150, 560), ["SHS 150x150x8 + 25 thermo-ash", "cladding = 200x200"]),
                            ((90, -70), (150, 230), ["PL 250x250x15, 4 M16", "HD bolts, 30 grout"]),
                            ((0, -500), (150, -560), ["Pad 800x800x700 C25/30", "Ø12 @ 150 B.W."]),
                            ((300, -300), (150, -760), ["RWP Ø75 → Ø110 drain"])):
        d.leader([tgt, txt], lines, size=1.25, anchor="start")
    s.text(212, 16, "D1  POST BASE — 1:10", size=2.0, weight="bold")

    # ---- D2 free-end eave 1:5 (X horizontal)
    e = View(s, 214, 288, 5, origin=(RX1 - 300, SOFFIT))
    rhs(e, B1_X[0], BOS, 100, 200, 6.3)
    e.rect(RX1 - 300, BOS, 150, 200, w=0.12, fill="#e6eaee", color="#777")
    e.rect(GUT_X[0], TOS + 5, GUT_X[1] - GUT_X[0], 10, w=0.1, mat="timber")
    e.rect(GUT_X[0], TOS + 12, GUT_X[1] - GUT_X[0], 18, w=0.15, fill="#d9b98a")
    e.rect(GUT_X[1], BOS + 40, 18, FTOP - 30 - BOS - 40, w=0.15, fill="#d9b98a")
    e.pl([(RX1 - 300, TOS + 38), (GUT_X[0], TOS + 33), (GUT_X[0], TOS + 30), (GUT_X[1], TOS + 30),
          (GUT_X[1], FTOP - 30), (GUT_X[1] + 18, FTOP - 30)], w=0.5, closed=False, color="#111")
    e.pl([(RX1 - 60, SOFFIT + 10), (RX1 - 60, SOFFIT), (RX1, SOFFIT), (RX1, FTOP), (RX1 - 45, FTOP - 6),
          (RX1 - 45, FTOP - 30)], w=0.55, closed=False, color="#111")
    e.rect(RX1 - 300, SOFFIT + 20, 240, 30, w=0.1, fill="#c9a77c")
    x = RX1 - 300
    while x + 68 < RX1 - 60:
        e.rect(x, SOFFIT, 68, 20, w=0.1, mat="timber")
        x += 78
    e.rect(RX1 - 300 + 5, SOFFIT, 25, 22, w=0.2, fill="#f39c12")
    e.dim((RX1, SOFFIT), (RX1, FTOP), -4, size=1.3)
    for tgt, txt, lines in (((RX1, 2650), (RX1 + 120, 2700), ["Alu fascia 3 mm", "RAL 9010, 430 high"]),
                            ((GUT_X[0] + 60, TOS + 25), (RX1 + 120, 2560), ["Gutter 120, TPO"]),
                            ((B1_X[0] + 50, BOS + 100), (RX1 + 120, 2440), ["B1 RHS 200x100"]),
                            ((RX1 - 288, SOFFIT), (RX1 + 120, 2380), ["LED + slats"])):
        e.leader([tgt, txt], lines, size=1.25, anchor="start")
    s.text(212, 199, "D2  FREE-END EAVE / FASCIA 0.43 — 1:5", size=1.9, weight="bold")
    return s


def sheets():
    return [sheet_p01(), sheet_p02(), sheet_p03(), sheet_p04()]


if __name__ == "__main__":
    import build
    ss = sheets()
    for s in ss:
        build.preview(s, "../preview/" + s.number + ".png", scale=1.2)
    print(build.to_pdf(ss, "Rev-C02_Preview_4-sheets"))
