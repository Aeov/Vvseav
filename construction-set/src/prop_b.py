"""PROPOSAL B — Bioclimatic louvred pergola lounge (freestanding)."""
import math
from cad import Sheet, View, break_line
from common import *  # noqa
from design import *  # noqa
from sheets_b import ladder, paving_cut, rhs
from prop_common import project, ctx_plan, ctx_elev, porcelain_grid, cover, boq_sheet
from axo import Axo, mbox

CODE = "B"
TITLE = "Bioclimatic louvred pergola lounge"
PJ = project(CODE, TITLE)

X0, X1 = 1200, 6900          # outer faces
Y0, Y1 = -450, -4050
PS = 150                     # post size
POSTS = [(X0 + 75, Y0 - 75), (X1 - 75, Y0 - 75), (X0 + 75, Y1 + 75), (X1 - 75, Y1 + 75)]
BEAM_B, BEAM_D = 150, 250
UB, TB = 2700, 2950          # underside / top of beams
PIVOT = 2830
BLADE_W, BLADE_T, PITCH = 200, 40, 200
BLADES = [X0 + BEAM_B + 100 + i * PITCH for i in range(int((X1 - X0 - 2 * BEAM_B) / PITCH))]
BENCH = (1040, 1540, -650, -3850)
SEAT = 450
PAD = 700


def plan(v, furniture=True, labels=True):
    porcelain_grid(v, PAV_X0, PAV_X1, 0, -8400)
    ctx_plan(v)
    plan_drainage(v, labels=False)
    # bench
    v.rect(BENCH[0], BENCH[3], BENCH[1] - BENCH[0], BENCH[2] - BENCH[3], w=0.3, fill="#c89a63")
    for y in range(BENCH[3] + 100, BENCH[2], 105):
        v.line(BENCH[0] + 20, y, BENCH[1] - 20, y, w=0.05, color="#7a5a3a")
    v.rect(COP_X0, BENCH[3], COP_X1 - COP_X0, BENCH[2] - BENCH[3], w=0.3, fill="#efe9dd")
    # pergola
    v.rect(X0, Y1, X1 - X0, Y0 - Y1, w=0.35, dash="4,1.5")
    for (x, y) in POSTS:
        v.rect(x - PS / 2, y - PS / 2, PS, PS, w=0.35, fill="#3a3f44")
    if furniture:
        v.rect(1700, -1200, 900, 2200 - 1200 + 0 - 1000 + 1000, w=0.15, dash="1.5,0.8", color="#777")
        v.rect(1700, -3400, 2600, 800, w=0.15, dash="1.5,0.8", color="#777")
        v.rect(2600, -2400, 1100, 600, w=0.15, dash="1.5,0.8", color="#777")
        v.circle(3200, -6200, 600, w=0.15, dash="1.5,0.8", color="#777")
        v.text(3200, -6250, "dining (FF&E)", size=1.3, anchor="middle", color="#777")
        v.text(2600, -3050, "outdoor sofa (FF&E)", size=1.3, anchor="middle", color="#777")
    # zip screen east
    v.line(X1 - 20, Y0 - PS, X1 - 20, Y1 + PS, w=0.6, color="#555", dash="2,0.6")


def roof_plan(v):
    v.rect(-BW_T, 0, 7750, FAC_T, mat="masonry", w=0.3)
    v.rect(-BW_T, -4300, BW_T, 4300, mat="masonry", w=0.3)
    v.rect(COURT_W, -4300, EW_T, 4300, mat="masonry", w=0.3)
    v.rect(AC1[0], -300, AC1[1] - AC1[0], 300, w=0.2, fill="#eee", dash="1.5,0.8")
    v.text((AC1[0] + AC1[1]) / 2, -200, "AC1 (exist.)", size=1.3, anchor="middle")
    # frame
    v.rect(X0, Y1, X1 - X0, Y0 - Y1, w=0.4, fill="#cfd4d8")
    v.rect(X0 + BEAM_B, Y1 + BEAM_B, X1 - X0 - 2 * BEAM_B, Y0 - Y1 - 2 * BEAM_B, w=0.3, fill="#ffffff")
    for x in BLADES:
        v.rect(x - BLADE_W / 2 + 5, Y1 + BEAM_B, BLADE_W - 10, Y0 - Y1 - 2 * BEAM_B, w=0.12, fill="#e8ebee")
        v.line(x, Y1 + BEAM_B, x, Y0 - BEAM_B, w=0.06, dash="2,1", color="#888")
    for (x, y) in POSTS:
        v.rect(x - PS / 2, y - PS / 2, PS, PS, w=0.35, fill="#3a3f44")
        v.circle(x, y, 30, w=0.2, color="#1f5fa8", fill="#dbe7f3")
        v.rect(x - PAD / 2, y - PAD / 2, PAD, PAD, w=0.15, dash="1.5,0.8", color="#777")
    # gutter flow arrows in N & S beams
    for yy in (Y0 - 75, Y1 + 75):
        for (a, b) in ((3800, X0 + 300), (4300, X1 - 300)):
            pa, pb = v.P(a, yy), v.P(b, yy)
            v.s.line(pa[0], pa[1], pb[0], pb[1], w=0.3, color="#1f5fa8")
            d = 1 if pb[0] > pa[0] else -1
            v.s.poly([pb, (pb[0] - d * 1.8, pb[1] - 0.8), (pb[0] - d * 1.8, pb[1] + 0.8)], w=0, fill="#1f5fa8")
    # LED & heaters
    i = BEAM_B + 30
    v.pl([(X0 + i, Y0 - i), (X1 - i, Y0 - i), (X1 - i, Y1 + i), (X0 + i, Y1 + i)], w=0.6, color="#f39c12",
         dash="3,1")
    for x in (2600, 5400):
        v.rect(x - 600, Y1 + BEAM_B + 10, 1200, 90, w=0.25, fill="#e74c3c")
    v.tag(2600, Y1 + 500, "H1", shape="hex", r=2, size=1.3)
    v.tag(5400, Y1 + 500, "H1", shape="hex", r=2, size=1.3)
    v.rect(X1 - 130, Y1 + BEAM_B, 110, Y0 - Y1 - 2 * BEAM_B, w=0.25, fill="#777")
    # dims
    v.chain([X0, X0 + 75, X1 - 75, X1], "x", Y1, -8, size=1.4)
    v.chain([0, Y0, Y0 - 75, Y1 + 75, Y1], "y", X1, -10, size=1.4)
    v.chain([X0, X0 + BEAM_B] + [BLADES[0] - 100 + PITCH * k for k in (0, 1)] , "x", Y0, 6, size=1.2,
            overall=False)
    v.leader([(BLADES[5], -2200), (2300, -1700)], [f"{len(BLADES)} aluminium aerofoil blades 200x40, pitch 200,",
                                                   "span 3300 N-S, rotate 0–135°, motorised"], size=1.4)
    v.leader([(X1 - 75, -2200), (6200, -1300)], ["Zip screen cassette (E side)"], size=1.4, anchor="end")
    v.leader([(4300, Y0 - 75), (4600, 600)], ["N beam: integrated gutter, falls to corner posts"], size=1.4)
    v.leader([(POSTS[2][0], POSTS[2][1]), (500, -4600)], ["Post 150x150 alu, Ø50 RWP inside,",
                                                         "pad 700x700x700 (dashed)"], size=1.4, anchor="end")
    v.leader([(2600, Y1 + 200), (2900, -4600)], ["H1 IR heater 2 kW, IP65 (x2)"], size=1.4)


def elev(v):
    ctx_elev(v, extra_levels=[(UB, "+2.700 u/s beam"), (TB, "+2.950 top")])
    for i, (cx, w_, h_) in enumerate(((180, 500, 800), (520, 600, 650), (350, 380, 1150))):
        shrub(v, cx, COP_TOP - 10, w_, h_, seed=120 + i, flowers=4)
    # bench end (seen)
    v.rect(BENCH[0], -5, BENCH[1] - BENCH[0], SEAT + 5, w=0.3, mat="render")
    v.rect(BENCH[0] - 20, SEAT - 45, BENCH[1] - BENCH[0] + 40, 45, w=0.3, mat="timber")
    v.rect(COP_X0, COP_TOP, COP_X1 - COP_X0, 850 - COP_TOP, w=0.3, mat="render")
    v.rect(BENCH[0] + 20, SEAT, 120, 380, w=0.15, fill="#d8d2c6")
    # posts & front beam
    for x in (X0, X1 - PS):
        v.rect(x, -5, PS, UB + 5, w=0.35, fill="#3a3f44")
    v.rect(X0, UB, X1 - X0, BEAM_D, w=0.4, fill="#4a5056")
    v.line(X0 + PS, UB + 30, X1 - PS, UB + 30, w=0.45, color="#f39c12")
    for x in BLADES:
        v.rect(x - BLADE_T / 2, TB - 10, BLADE_T, 60, w=0.1, fill="#cfd4d8")
    # zip screen cassette (end)
    v.rect(X1 - 130, UB - 110, 110, 110, w=0.25, fill="#777")
    v.chain([0, X0, X0 + PS, X1 - PS, X1, COURT_W], "x", -300, -8, size=1.5)
    v.dim((X1, 0), (X1, UB), -8, size=1.5)
    L = [
        ((3600, TB - 100), (3300, 4300), ["Freestanding bioclimatic pergola, extruded aluminium, RAL 7016 matt"]),
        ((X0 + 75, 1500), (300, 3900), ["Posts 150x150 alu (concealed RWP), base shroud"]),
        ((BENCH[0] + 200, SEAT - 20), (300, 3650), ["Built-in bench: iroko slats on rendered plinth, cushions"]),
        ((5000, UB + 30), (4700, 3900), ["Integrated warm-white LED in beams, dimmable"]),
        ((X1 - 75, UB - 55), (5600, 4650), ["Zip screen E side, 3.3 x 2.55 m, wind class 3"]),
    ]
    for tgt, txt, lines in L:
        v.leader([tgt, (tgt[0], txt[1] - 80), txt], lines, size=1.5, anchor="start")


def section_ew(v):
    """E-W section at Y = -2200 looking north."""
    # façade beyond
    v.rect(0, 0, COURT_W, FAC_PARAPET, w=0.15, fill="#fbf9f4", color="#999")
    door_elev(v, "D01", *D01)
    door_elev(v, "D02", *D02)
    door_elev(v, "D03", *D03)
    ac_unit(v, *AC1)
    # posts beyond (north)
    for x in (X0, X1 - PS):
        v.rect(x, 0, PS, UB, w=0.2, fill="#6b7177")
    # porcelain paving cut
    zt = -15
    pts = [(PAV_X0 + 0, LV_KERB * 1000), (6450, paving_level(6450) * 1000)]
    v.pl([(pts[0][0], pts[0][1]), (pts[1][0], pts[1][1]), (pts[1][0], pts[1][1] - 20), (pts[0][0], pts[0][1] - 20)],
         w=0.2, fill="#d9d4cc")
    v.pl([(pts[0][0], pts[0][1] - 20), (pts[1][0], pts[1][1] - 20), (pts[1][0], pts[1][1] - 60),
          (pts[0][0], pts[0][1] - 60)], w=0.15, mat="sand")
    v.pl([(pts[0][0], pts[0][1] - 60), (pts[1][0], pts[1][1] - 60), (pts[1][0], pts[1][1] - 210),
          (pts[0][0], pts[0][1] - 210)], w=0.15, mat="subbase")
    v.pl([(pts[0][0], pts[0][1] - 210), (pts[1][0], pts[1][1] - 210), (pts[1][0], -700), (pts[0][0], -700)], w=0,
         mat="earth")
    v.rect(6450, -800, 750, 700, w=0.15, mat="earth")
    v.rect(6300, LV_GULLY * 1000 - 750, 600, 700, w=0.2, mat="conc")
    v.rect(6450, LV_GULLY * 1000 - 600, 300, 600, w=0.25, fill="#cfd6dc")
    v.rect(6750, -90, 450, 90, w=0.2, fill="#d9d4cc")
    # boundary wall & planter
    v.rect(-BW_T, -700, BW_T, BW_TOP + 700, mat="masonry", w=0.45)
    v.rect(0, -300, KERB_X0, SOIL_TOP + 300, w=0.15, mat="soil")
    v.rect(KERB_X0, -400, 150, 850 + 400, w=0.3, mat="rc")
    v.rect(COP_X0, 850, COP_X1 - COP_X0, 60, w=0.3, mat="conc")
    shrub(v, 400, SOIL_TOP, 650, 800, seed=131, flowers=5)
    # bench cut
    v.rect(BENCH[0] + 360, -5, 140, SEAT - 45, w=0.3, mat="masonry")
    v.rect(BENCH[0], -5, 140, SEAT - 45, w=0.3, mat="masonry")
    v.rect(BENCH[0] - 20, SEAT - 45, BENCH[1] - BENCH[0] + 40, 45, w=0.3, mat="timber")
    v.pl([(BENCH[0] + 20, SEAT), (BENCH[1] - 30, SEAT), (BENCH[1] - 30, SEAT + 120), (BENCH[0] + 20, SEAT + 120)],
         w=0.15, fill="#e9e4da")
    v.pl([(BENCH[0] + 20, SEAT + 120), (BENCH[0] + 160, SEAT + 120), (BENCH[0] + 100, 850),
          (BENCH[0] + 10, 850)], w=0.15, fill="#e9e4da")
    # E & W beams cut, blades cut
    for x in (X0, X1 - BEAM_B):
        v.rect(x, UB, BEAM_B, BEAM_D, w=0.3, fill="#4a5056")
        v.rect(x + 25, UB + 120, 100, 100, w=0.15, fill="#dbe7f3")
    for x in BLADES:
        pts = []
        for k in range(12):
            a = 2 * math.pi * k / 12
            pts.append((x + math.cos(a) * BLADE_T / 2 * (1.0 if math.cos(a) > 0 else 0.6),
                        PIVOT + math.sin(a) * BLADE_W / 2))
        v.pl(pts, w=0.15, fill="#cfd4d8")
        v.line(x - 95, PIVOT - 18, x + 95, PIVOT + 18, w=0.08, dash="1,0.6", color="#777")
    v.rect(X1 - 130, UB - 110, 110, 110, w=0.25, fill="#777")
    v.line(X1 - 75, UB - 110, X1 - 75, 60, w=0.4, color="#555", dash="3,1")
    ladder(v, -250, [(0, "±0.000"), (SEAT, "+0.450 seat"), (850, "+0.850 back"), (UB, "+2.700"), (PIVOT, "+2.830 pivot"),
                     (TB, "+2.950"), (FAC_PARAPET, "+3.400")], 14.5, size=1.35)
    v.chain([-BW_T, 0, KERB_X1, BENCH[1], X0, X1, COURT_W], "x", -800, -4, size=1.35)
    C = [
        ((BLADES[8], PIVOT), (3000, 3600), ["Blades shown open 90° (closed = dashed), pivot pins in nylon bushes"]),
        ((X0 + 75, UB + 170), (1300, 3850), ["Beam 150x250 with integrated gutter (blue)"]),
        ((BENCH[0] + 250, SEAT - 20), (2000, 900), ["Iroko 45 slats on 2 x 140 block plinths, rendered"]),
        ((X1 - 75, 1500), (5200, 1800), ["Zip screen (lowered)"]),
        ((3000, -30), (2600, -500), ["20 porcelain / 40 drainage mortar / 150 Type 1"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.4, anchor="start")


def axo(s, ox, oy, scale):
    a = Axo(beta=28, elev=30)
    for x in range(PAV_X0, PAV_X1, 600):
        for y in range(0, -8400, -600):
            w = min(600, PAV_X1 - x)
            a.poly3([(x, y - 600, 0), (x + w, y - 600, 0), (x + w, y, 0), (x, y, 0)], "#d9d4cc", stroke="#b5afa6",
                    w=0.05)
    mbox(a, -BW_T, 0, 0, COURT_W + EW_T + BW_T, 3000, FAC_PARAPET, "#f3ede2", layer=1, bias=-1e5)
    for (x0, x1), col in ((D01, "#a9cde0"), (D02, "#5b4636"), (D03, "#b07a45")):
        mbox(a, x0, -25, 0, x1 - x0, 25, HEAD, col, layer=1, bias=-9e4)
    mbox(a, AC1[0], -300, AC1[2], AC1[1] - AC1[0], 300, AC1[3] - AC1[2], "#efefef", layer=1, bias=-8e4)
    mbox(a, -BW_T, -8400, 0, BW_T, 8400, BW_TOP, "#efe7da", layer=1, bias=-1.2e5)
    mbox(a, 0, PL_SOUTH, 0, KERB_X0, -PL_SOUTH, SOIL_TOP, "#7b5a3a", layer=1, bias=-7e4)
    mbox(a, KERB_X0, PL_SOUTH, 0, KERB_T, -PL_SOUTH, COP_TOP, "#f1ebdf", layer=1, bias=-6e4)
    mbox(a, KERB_X0, BENCH[3], 0, KERB_T + 40, BENCH[2] - BENCH[3], 850, "#f1ebdf", layer=1, bias=-5.5e4)
    mbox(a, BENCH[0], BENCH[3], 0, BENCH[1] - BENCH[0], BENCH[2] - BENCH[3], SEAT, "#c89a63", layer=1, bias=-5e4)
    mbox(a, BENCH[0] + 40, BENCH[3] + 40, SEAT, 420, BENCH[2] - BENCH[3] - 80, 110, "#ece7dd", layer=1, bias=-4.9e4)
    mbox(a, COURT_W, -EW_LEN, 0, EW_T, EW_LEN, 1000, "#e9e2d6", layer=2)
    mbox(a, COURT_W, -8400, 0, 100, 3000, 1000, "#a8723f", layer=2)
    for (code, x, y, sp) in PLANTS:
        if code == "OL":
            continue
        a.blob(x, y, SOIL_TOP + 450, sp * 0.6, fill="#6f9d58", layer=2, flowers=4, seed=int(-y) % 97)
    # furniture
    mbox(a, 1700, -3400, 0, 2600, 800, 420, "#e3ddd2", layer=2)
    mbox(a, 2600, -2400, 0, 1100, 600, 380, "#8d8478", layer=2)
    mbox(a, 2700, -6700, 0, 1000, 1000, 740, "#bfb5a5", layer=2)
    # pergola
    for (x, y) in POSTS:
        mbox(a, x - 75, y - 75, 0, PS, PS, UB, "#454b51", layer=3)
    mbox(a, X0, Y0 - BEAM_B, UB, X1 - X0, BEAM_B, BEAM_D, "#4a5056", layer=4)
    mbox(a, X0, Y1 + BEAM_B, UB, BEAM_B, Y0 - Y1 - 2 * BEAM_B, BEAM_D, "#4a5056", layer=4)
    for x in BLADES:
        mbox(a, x - 25, Y1 + BEAM_B, PIVOT - 60, 50, Y0 - Y1 - 2 * BEAM_B, 120, "#d3d8dc", layer=4, stroke="#777",
             w=0.06)
    mbox(a, X1 - BEAM_B, Y1 + BEAM_B, UB, BEAM_B, Y0 - Y1 - 2 * BEAM_B, BEAM_D, "#4a5056", layer=5)
    mbox(a, X0, Y1, UB, X1 - X0, BEAM_B, BEAM_D, "#4a5056", layer=5)
    a.render(s, ox, oy, scale)


def details(s):
    # DB1 post base 1:10
    v = View(s, 60, 150, 10, origin=(0, 0))
    v.pl([(-450, -900), (450, -900), (450, -60), (-450, -60)], w=0, mat="earth")
    v.rect(-350, -760, 700, 700, w=0.4, mat="rc")
    v.rect(-400, -810, 800, 50, w=0.2, mat="conc")
    v.rect(-450, -60, 900, 40, w=0.2, mat="sand")
    v.rect(-450, -20, 900, 20, w=0.2, fill="#d9d4cc")
    v.rect(-150, -60, 300, 15, w=0.3, fill="#5c6670")
    v.rect(-75, -45, 150, 900, w=0.3, fill="#3a3f44")
    v.rect(-71, -45, 142, 900, w=0.1, fill="#fff")
    v.rect(-100, -45, 200, 120, w=0.2, fill="#4a5056")
    v.rect(-25, -45, 50, 900, w=0.15, dash="1.5,0.8", color="#1f5fa8")
    v.pl([(-25, -60), (-25, -260), (300, -260), (450, -260), (450, -200), (25, -200), (25, -60)], w=0.2,
         color="#1f5fa8", fill="#dbe7f3")
    for x in (-110, 110):
        v.rect(x - 8, -200, 16, 160, w=0.12, fill="#888")
    break_line(v, -120, 855, 120, 855)
    for tgt, txt, lines in (((0, 600), (200, 700), ["Post 150x150x4 alu extrusion"]),
                            ((0, 20), (200, 350), ["Base shroud 200x200x120 alu"]),
                            ((110, -100), (200, 120), ["4 M16 chem. anchors, base PL 300x300x15"]),
                            ((0, -400), (200, -450), ["Pad 700x700x700 C25/30, mesh A393"]),
                            ((300, -230), (200, -620), ["Ø50 RWP → Ø110 to gully G1 / channel"])):
        v.leader([tgt, txt], lines, size=1.3, anchor="start")
    s.text(16, 50, "DB1  POST BASE — 1:10", size=1.9, weight="bold")

    # DB2 beam + blade 1:5
    b = View(s, 150, 80, 5, origin=(0, 2700))
    b.pl([(0, UB), (150, UB), (150, TB), (130, TB), (130, UB + 120), (20, UB + 120), (20, TB), (0, TB)], w=0.35,
         fill="#4a5056")
    b.rect(20, UB + 120, 110, 10, w=0.1, fill="#dbe7f3")
    b.rect(150, UB + 20, 20, 25, w=0.2, fill="#f39c12")
    for k, ang in enumerate((90, 0)):
        cx = 300 + k * 220
        pts = []
        for j in range(16):
            a = 2 * math.pi * j / 16
            px = math.cos(a) * BLADE_W / 2
            pz = math.sin(a) * BLADE_T / 2 * (1 if math.sin(a) > 0 else 0.5)
            r = math.radians(ang)
            pts.append((cx + px * math.cos(r) - pz * math.sin(r), PIVOT + px * math.sin(r) + pz * math.cos(r)))
        b.pl(pts, w=0.25, fill="#cfd4d8", dash=None if k == 0 else "1,0.6")
        b.circle(cx, PIVOT, 8, w=0.2, fill="#fff")
    b.leader([(75, TB - 10), (60, 3060)], ["Beam 150x250 alu, RAL 7016"], size=1.3, anchor="start")
    b.leader([(75, UB + 125), (250, 3030)], ["Integrated gutter 110x100"], size=1.3, anchor="start")
    b.leader([(160, UB + 30), (250, 2620)], ["LED strip 24 V in channel"], size=1.3, anchor="start")
    b.leader([(300, PIVOT + 80), (420, 3000)], ["Blade 200x40 open"], size=1.3, anchor="start")
    b.leader([(600, PIVOT), (560, 2660)], ["closed (rain sensor)"], size=1.3, anchor="start")
    s.text(130, 50, "DB2  BEAM, GUTTER & BLADE — 1:5", size=1.9, weight="bold")

    # DB3 bench 1:10
    c = View(s, 185, 232, 10, origin=(1000, 0))
    c.rect(700, -300, 150, 1150, w=0.3, mat="rc")
    c.rect(500, -300, 200, SOIL_TOP + 300, w=0.15, mat="soil")
    c.rect(690, 850, 280, 60, w=0.3, mat="conc")
    c.rect(BENCH[0] - 200 + 360, -5, 140, SEAT - 45, w=0.3, mat="masonry")
    c.rect(BENCH[0] - 200 + 0, -5, 140, SEAT - 45, w=0.3, mat="masonry")
    c.rect(BENCH[0] - 220, SEAT - 45, 540, 45, w=0.3, mat="timber")
    c.pl([(BENCH[0] - 180, SEAT), (BENCH[0] + 270, SEAT), (BENCH[0] + 270, SEAT + 120), (BENCH[0] - 180, SEAT + 120)],
         w=0.15, fill="#e9e4da")
    c.rect(BENCH[0] - 260, -80, 600, 75, w=0.15, fill="#d9d4cc")
    c.leader([(BENCH[0], SEAT - 20), (1250, 700)], ["Iroko 95x45 slats, 8 gaps,", "SS screws to bearers"],
             size=1.3, anchor="start")
    c.leader([(BENCH[0] - 130, 200), (1250, 300)], ["140 block plinths,", "rendered, 1 m c/c"], size=1.3,
             anchor="start")
    c.leader([(775, 600), (1250, 1000)], ["Kerb raised to +0.85"], size=1.3, anchor="start")
    s.text(150, 160, "DB3  BUILT-IN BENCH — 1:10", size=1.9, weight="bold")

    s.textblock(262, 50, 76, [
        ("B", "SYSTEM SPEC (performance)"),
        "• Proprietary freestanding bioclimatic pergola (e.g. Renson Algarve / Biossun / Brustor or equal), "
        "designed & certified by supplier to EN 1991-1-3/-1-4 for site snow & wind; CE marked.",
        "• Extruded aluminium 6063-T6, powder coat RAL 7016 Qualicoat cl. 2.",
        "• Blades: aerofoil 200 mm, rotation 0–135°, watertight when closed (rain-sensor auto-close).",
        "• Drive: 24 V linear actuator, rain + wind sensors, remote / app; manual crank override.",
        "• Drainage: blades → integrated gutters → 4 posts → Ø110 to gullies.",
        "• Lighting: perimeter LED 2700 K dimmable; 2 x 2 kW IR heaters on S beam.",
        "• Zip screen: E side, PVC-free screen fabric 5% openness, wind class 3 (e.g. Fixscreen).",
        "• Foundations: pad sizes are indicative — confirm with supplier's reactions (uplift!).",
        ("B", "ADVANTAGES"),
        "• No load on existing façade (freestanding) — no structural survey of annex needed.",
        "• Adjustable shade/vent, fully closable to rain; heaters extend use to winter evenings.",
    ], size=1.45, gap=0.3)


def boq():
    area = (PAV_X1 - PAV_X0) * 8.4 / 1000
    return [
        ["1", "PRELIMINARIES", "", "", ""],
        ["1.1", "Survey, set-up, protection, clean", "item", "1", ""],
        ["2", "GROUNDWORKS & DRAINAGE", "", "", ""],
        ["2.1", "Strip & excavate to formation", "m³", f"{area * 0.25:.1f}", ""],
        ["2.2", "Pads 700x700x700 C25/30 + mesh", "no", "4", ""],
        ["2.3", "Ø110 drains incl. post connections", "m", "28", ""],
        ["2.4", "SD1 slot drain 5 m, gullies G1/G2", "item", "1", ""],
        ["3", "PERGOLA SYSTEM (supplier)", "", "", ""],
        ["3.1", f"Bioclimatic pergola {(X1 - X0) / 1000:.1f} x {(Y0 - Y1) / 1000:.1f} m, 4 posts, motorised",
         "no", "1", ""],
        ["3.2", "Integrated LED + dimmer", "item", "1", ""],
        ["3.3", "IR heaters 2 kW IP65", "no", "2", ""],
        ["3.4", "Zip screen E side 3.3 x 2.55", "no", "1", ""],
        ["3.5", "Rain/wind sensors, app control", "item", "1", ""],
        ["4", "PAVING", "", "", ""],
        ["4.1", "Type 1 sub-base 150", "m²", f"{area:.1f}", ""],
        ["4.2", "20 mm porcelain 600x600 R11 on 40 drainage mortar + primer", "m²", f"{area:.1f}", ""],
        ["5", "PLANTER & BENCH", "", "", ""],
        ["5.1", "Planter (as Design A A-302) incl. planting & drip", "m", "8.4", ""],
        ["5.2", "Kerb raised to +0.85 along bench", "m", "3.2", ""],
        ["5.3", "Bench plinths + iroko seat 500 deep", "m", "3.2", ""],
        ["5.4", "Outdoor cushions (FF&E allowance)", "item", "1", ""],
        ["6", "ELECTRICAL", "", "", ""],
        ["6.1", "Dedicated 16 A RCBO circuit for pergola + heaters 20 A", "item", "1", ""],
        ["6.2", "Uplights UL1-6, sockets SO1-2 IP66", "item", "1", ""],
        ["7", "FINISHES", "", "", ""],
        ["7.1", "Façade & wall repair/repaint", "m²", "40", ""],
        ["8", "CONTINGENCY", "%", "7.5", ""],
    ]


def sheets():
    reg = [("B-000", "Cover, concept & register"), ("B-100", "General arrangement plan 1:50"),
           ("B-101", "Pergola roof & structure plan 1:25"), ("B-200", "Elevation A 1:25"),
           ("B-300", "Section B-B (E-W) 1:25"), ("B-500", "Details 1:10 / 1:5"), ("B-600", "Schedules & BOQ")]
    out = []
    compare = [["Roof", "Fixed, membrane", "Adjustable louvres"], ["Load on façade", "Yes (ledger)", "None"],
               ["Survey of annex", "Required", "Not required"], ["Winter use", "Medium", "High (heaters)"],
               ["Rain protection", "Full", "Full when closed"], ["Cost class", "€€", "€€€"],
               ["Lead time", "4–6 wk", "6–8 wk (system)"], ["Maintenance", "Oil timber", "Wash, sensors"]]
    out.append(cover(CODE, TITLE, "Freestanding motorised aluminium louvre roof over a lounge, built-in bench "
                     "on the planter, large-format porcelain paving, zip screen & heaters.", axo,
                     ["A freestanding 5.7 x 3.6 m bioclimatic pergola replaces the fixed canopy: rotating blades give "
                      "shade, ventilation or full rain-cover at the touch of a button. Because it stands on its own 4 "
                      "posts it puts no load on the existing annex — the main structural risk of Design A disappears."],
                     ["• Louvres 0–135°, rain sensor auto-close, wind sensor open.",
                      "• Lounge zone with 3.2 m built-in iroko bench against the raised planter.",
                      "• 600x600 porcelain paving, warm greige, R11 anti-slip.",
                      "• Integrated dimmable LED, 2 IR heaters, east zip screen hides AC/wall."], compare, reg))
    s = Sheet("B-100", "Proposal B — general arrangement plan", "1:50", project=PJ)
    s.frame()
    v = View(s, 62, 70, 50)
    plan(v)
    v.chain([0, KERB_X1, BENCH[1], X0, X1, COURT_W], "x", -8400, -10, size=1.5)
    v.chain([0, Y0, Y1, -8400], "y", -BW_T, 12, size=1.5)
    v.leader([(4000, -2200), (4300, -5000)], ["Bioclimatic pergola over (dashed) — B-101"], size=1.6)
    v.leader([(BENCH[0] + 250, -2200), (2200, -4700)], ["Built-in bench 3.2 m (DB3)"], size=1.6)
    v.leader([(5000, -6800), (5200, -7400)], ["Porcelain 600x600x20 R11, greige, 3 mm joints,",
                                              "falls as Design A (A-101)"], size=1.6)
    v.title(48, 262, "1/B-100", "GENERAL ARRANGEMENT PLAN", "1:50 @ A3")
    s.north_arrow(225, 30, 6)
    s.scale_bar(240, 268, 50)
    s.textblock(262, 22, 74, [
        ("B", "NOTES"),
        "1. Existing walls, doors D01–D03, planter, G01 screen & drainage as Design A unless noted.",
        "2. Pergola is freestanding: 450 mm clear of façade (AC1 unit stays). Optional fabric gap-closer.",
        "3. Post positions to be confirmed by supplier — keep clear of gullies G1/G2 and D03 swing.",
        "4. Porcelain: R11, PEI V, frost resistant, 20 mm; joints 3 mm polymer jointing compound.",
        "5. Planting as A-104; jasmine on SS wires on post faces optional.",
    ], size=1.55, gap=0.4)
    out.append(s)
    s = Sheet("B-101", "Proposal B — pergola roof & structure plan", "1:25", project=PJ)
    s.frame()
    v = View(s, 34 - 0, 40, 25, origin=(0, 300))
    roof_plan(v)
    v.title(22, 205, "1/B-101", "PERGOLA ROOF, DRAINAGE & LIGHTING PLAN", "1:25 @ A3")
    s.scale_bar(240, 268, 25, 2)
    s.textblock(22, 222, 314, [
        "Blades closed = watertight roof (rain drains along blades into N & S gutter beams, then down all 4 posts). "
        "Open 90° = full ventilation; 135° = evening sun-shading. Snow: blades auto-open when snow load sensor "
        "triggers (supplier option) or stay closed if designed for site snow. All dimensions to be confirmed by "
        "supplier's shop drawings.",
    ], size=1.6)
    out.append(s)
    s = Sheet("B-200", "Proposal B — elevation A (looking north)", "1:25", project=PJ)
    s.frame()
    v = View(s, 44, 215, 25)
    elev(v)
    v.title(28, 266, "1/B-200", "ELEVATION A — PERGOLA & FAÇADE (looking north)", "1:25 @ A3")
    s.scale_bar(250, 268, 25, 2)
    out.append(s)
    s = Sheet("B-300", "Proposal B — section B-B (E-W at Y = -2200)", "1:25", project=PJ)
    s.frame()
    v = View(s, 52, 200, 25)
    section_ew(v)
    v.title(24, 262, "1/B-300", "SECTION B-B", "1:25 @ A3", sub="through bench, pergola & gully G1, looking north")
    s.scale_bar(260, 268, 25, 2)
    out.append(s)
    s = Sheet("B-500", "Proposal B — details", "1:10 / 1:5", project=PJ)
    s.frame()
    details(s)
    out.append(s)
    out.append(boq_sheet(CODE, TITLE, boq(), "Pergola system price to be obtained from 2–3 approved suppliers "
                         "including foundations design; all other items measured from drawings."))
    return out
