"""PROPOSAL D — Green-roof canopy, reflecting pool, living wall & rainwater harvesting."""
import math
from cad import Sheet, View, break_line
from common import *  # noqa
from design import *  # noqa
from sheets_b import ladder, paving_cut, rhs
from prop_common import project, ctx_plan, ctx_elev, ctx_section_ns, cover, boq_sheet
from axo import Axo, mbox

CODE = "D"
TITLE = "Green canopy, water & living wall"
PJ = project(CODE, TITLE)

CX0, CX1, CY1 = 1100, 5400, -3600
POSTS = [(1250, -3450), (3250, -3450), (5250, -3450)]
CHS = 139.7
SOF, BOS_D, TOS_D = 2650, 2700, 2900
DECK = 2965            # mean deck top
GR_TOP = 3105          # top of sedum
FT = 3150              # fascia top
POOL = (1000, 2000, -3800, -7800)     # outer
POOL_IN = (1200, 1800, -4000, -7600)
COPE = 450
WATER = 380
LW = (100, 1550, 450, 2450)           # living wall x0,x1,z0,z1
TANK = (3500, 5600, -6400, -7600)
FIRE = (4300, -5000)
DL = [(1900, -900), (3250, -900), (4600, -900), (1900, -2500), (3250, -2500), (4600, -2500)]


def herringbone(v, x0, x1, y0, y1):
    v.rect(x0, y1, x1 - x0, y0 - y1, w=0.25, fill="#cfd0cc")
    v.rect(x0, y1, x1 - x0, 100, w=0.1, fill="#55585c")
    v.rect(x1 - 100, y1, 100, y0 - y1, w=0.1, fill="#55585c")
    # diagonal hint lines (45° herringbone)
    s = 141
    k = x0 - (y0 - y1)
    while k < x1:
        xa, ya = k, y1
        xb, yb = k + (y0 - y1), y0
        if xa < x0:
            ya += x0 - xa
            xa = x0
        if xb > x1 - 100:
            yb -= xb - (x1 - 100)
            xb = x1 - 100
        if xb > xa:
            v.line(xa, ya, xb, yb, w=0.05, color="#999")
        k += s


def plan(v):
    herringbone(v, PAV_X0, PAV_X1, 0, -8400)
    ctx_plan(v)
    v.rect(SD1[0], SD1[3], SD1[1] - SD1[0], 100, w=0.25, fill="#d0d5da")
    # pool
    v.rect(POOL[0], POOL[3], POOL[1] - POOL[0], POOL[2] - POOL[3], w=0.4, fill="#efe9dd")
    v.rect(POOL_IN[0], POOL_IN[3], POOL_IN[1] - POOL_IN[0], POOL_IN[2] - POOL_IN[3], w=0.3, fill="#2c3e50")
    v.rect(POOL_IN[0] + 150, POOL_IN[2] - 40, 300, 40, w=0.2, fill="#bdc3c7")
    # tank (below)
    v.rect(TANK[0], TANK[3], TANK[1] - TANK[0], TANK[2] - TANK[3], w=0.3, dash="3,1", color="#1f5fa8")
    v.text((TANK[0] + TANK[1]) / 2, (TANK[2] + TANK[3]) / 2, "RWH TANK 2000 L (below)", size=1.4,
           anchor="middle", color="#1f5fa8")
    v.circle(TANK[0] + 300, TANK[2] - 300, 250, w=0.3, fill="#ddd")
    # fire bowl + chairs
    v.circle(FIRE[0], FIRE[1], 450, w=0.3, fill="#8e5a3c")
    for a in range(0, 360, 90):
        x = FIRE[0] + 1300 * math.cos(math.radians(a + 45))
        y = FIRE[1] + 1300 * math.sin(math.radians(a + 45))
        v.circle(x, y, 380, w=0.15, dash="1.5,0.8", color="#777")
    # living wall
    v.rect(LW[0], 0, LW[1] - LW[0], -150, w=0.35, fill="#5f8f4b")
    # canopy
    v.rect(CX0, CY1, CX1 - CX0, -CY1, w=0.35, dash="4,1.5")
    for (x, y) in POSTS:
        v.circle(x, y, CHS / 2, w=0.35, fill="#4b3a2f")
    v.circle(1300, -3700, 60, w=0.25, fill="#1f5fa8")
    v.circle(5200, -3700, 60, w=0.25, fill="#1f5fa8")
    v.circle(5200, -3950, 250, w=0.2, fill="#bfb5a5")


def roof_plan(v):
    v.rect(-BW_T, 0, 6500, FAC_T, mat="masonry", w=0.3)
    v.rect(-BW_T, -4300, BW_T, 4300, mat="masonry", w=0.3)
    v.rect(CX0, CY1, CX1 - CX0, -CY1, w=0.45, fill="#4b3a2f")
    v.rect(CX0 + 50, CY1 + 50, CX1 - CX0 - 100, -CY1 - 100, w=0.15, fill="#bfb8a8")
    v.rect(CX0 + 350, CY1 + 350, CX1 - CX0 - 700, -CY1 - 400, w=0.25, fill="#8fb36f")
    import random
    rnd = random.Random(5)
    for i in range(160):
        x = rnd.uniform(CX0 + 400, CX1 - 400)
        y = rnd.uniform(CY1 + 400, -400)
        v.circle(x, y, rnd.uniform(25, 60), w=0.06, color="#5d8a4a", fill="#a9c98c")
    for x in (1300, 5200):
        v.rect(x - 150, CY1 + 60, 300, 300, w=0.3, fill="#ddd")
        v.circle(x, CY1 + 210, 50, w=0.25, fill="#1f5fa8")
    for (x, y) in POSTS:
        v.circle(x, y, CHS / 2, w=0.2, dash="1,0.6")
    for x in range(CX0 + 500, CX1 - 300, 450):
        v.line(x, -60, x, CY1 + 150, w=0.06, dash="2,1.2", color="#777")
    v.chain([CX0, POSTS[0][0], POSTS[1][0], POSTS[2][0], CX1], "x", CY1, -8, size=1.4)
    v.chain([0, -350, CY1 + 350, CY1], "y", CX1, -10, size=1.4, overall=True)
    v.leader([(3200, -1800), (3500, -1500)], ["Extensive sedum roof: sedum mat / 80 substrate / filter fleece /",
                                              "25 drainage-retention board / root barrier / 1.5 EPDM / 18 ply",
                                              "on firrings (1:60 to S); saturated 1.30 kN/m²"], size=1.4)
    v.leader([(1300, CY1 + 210), (600, -4300)], ["Outlet + inspection box → rain chain", "into pool (W)"],
             size=1.4, anchor="end")
    v.leader([(5200, CY1 + 210), (5700, -4300)], ["Outlet → rain chain → basin → RWH tank"], size=1.4)
    v.leader([(CX0 + 200, -1500), (500, -1200)], ["300 gravel margin", "(fire break / access)"], size=1.4,
             anchor="end")


def elev(v):
    ctx_elev(v, extra_levels=[(SOF, "+2.650 soffit"), (FT, "+3.150 fascia")])
    # living wall
    v.rect(LW[0], LW[2], LW[1] - LW[0], LW[3] - LW[2], w=0.35, fill="#6f9d58")
    import random
    rnd = random.Random(2)
    for i in range(110):
        x = rnd.uniform(LW[0] + 40, LW[1] - 40)
        z = rnd.uniform(LW[2] + 40, LW[3] - 40)
        v.circle(x, z, rnd.uniform(25, 70), w=0.06, color="#3f6b30", fill=rnd.choice(("#86b36a", "#5c8f45",
                                                                                      "#a7c98f", "#c9a0c2")))
    for x in range(LW[0], LW[1] + 1, 500):
        v.line(x, LW[2], x, LW[3], w=0.06, color="#2f4f24")
    for i, (cx, w_, h_) in enumerate(((180, 500, 600), (650, 520, 500))):
        shrub(v, cx, COP_TOP - 10, w_, h_, seed=320 + i, flowers=3)
    # pool south end
    v.rect(POOL[0], -5, POOL[1] - POOL[0], COPE - 50 + 5, w=0.3, mat="render")
    v.rect(POOL[0] - 25, COPE - 50, POOL[1] - POOL[0] + 50, 50, w=0.3, fill="#e3ddd2")
    # canopy
    for (x, y) in POSTS:
        v.rect(x - CHS / 2, -5, CHS, SOF + 5, w=0.35, fill="#4b3a2f")
    v.rect(CX0, SOF, CX1 - CX0, FT - SOF, w=0.45, fill="#4b3a2f")
    v.line(CX0 + 20, SOF + 20, CX1 - 20, SOF + 20, w=0.1, color="#8a7060")
    for x in range(CX0 + 100, CX1 - 50, 140):
        v.circle(x, FT + 25, 35, w=0.06, color="#5d8a4a", fill="#a9c98c")
    # rain chain
    z = SOF
    while z > COPE:
        v.circle(1300, z, 22, w=0.15)
        z -= 70
    v.chain([0, CX0, POSTS[0][0], POSTS[1][0], POSTS[2][0], CX1, COURT_W], "x", -300, -8, size=1.45)
    v.dim((CX1, SOF), (CX1, FT), -6, size=1.4)
    L = [
        ((3300, FT - 200), (2800, 4300), ["Fascia 500 mm anodised alu, dark bronze; sedum roof behind"]),
        ((3250, 1500), (3700, 3900), ["3 slim posts CHS 139.7x6.3, MIO bronze"]),
        ((800, 1600), (100, 3650), ["Living wall 1.45 x 2.0 m, modular cassettes, drip-fed from RWH"]),
        ((1300, 1200), (900, 4650), ["Rain chain (copper) into pool"]),
        ((1500, COPE - 20), (4300, 4650), ["Raised reflecting pool, coping +0.45 (seat edge)"]),
    ]
    for tgt, txt, lines in L:
        v.leader([tgt, (tgt[0], txt[1] - 80), txt], lines, size=1.5, anchor="start")


def section(v):
    """N-S at X = 1500 looking west: living wall, canopy, pool."""
    # paving permeable
    def perm(y0, y1, zt=-20):
        v.rect(y1, zt - 80, y0 - y1, 80, w=0.2, fill="#cfd0cc")
        v.rect(y1, zt - 130, y0 - y1, 50, w=0.15, mat="gravel")
        v.rect(y1, zt - 480, y0 - y1, 350, w=0.15, mat="subbase")
        v.rect(y1, zt - 900, y0 - y1, 420, w=0, mat="earth")
        v.line(y1, zt, y0, zt, w=0.4)
    perm(-120, POOL[2] + 0)
    PL3 = -6300
    v.rect(SD1[3], -245, 100, 230, w=0.25, mat="alu")
    # façade wall (solid at X=1500)
    v.rect(0, -900, FAC_T, SLAB_SOFFIT + 900, w=0.3, mat="masonry")
    v.rect(0, SLAB_SOFFIT, 900, SLAB_TOP - SLAB_SOFFIT, w=0.3, mat="rc")
    v.rect(0, SLAB_TOP, FAC_T, FAC_PARAPET - SLAB_TOP, w=0.3, mat="masonry")
    v.rect(FAC_T, -220, 600, 150, w=0.25, mat="rc")
    break_line(v, 900, SLAB_SOFFIT - 60, 900, SLAB_TOP + 60)
    # living wall
    v.rect(-150, LW[2], 150, LW[3] - LW[2], w=0.3, fill="#6f9d58")
    v.rect(-20, LW[2], 20, LW[3] - LW[2], w=0.15, fill="#9aa3ab")
    v.rect(-200, LW[2] - 80, 200, 80, w=0.25, fill="#9aa3ab")
    # canopy cut
    v.pl([(0, BOS_D), (CY1 + 100, BOS_D), (CY1 + 100, TOS_D), (0, TOS_D)], w=0.2, fill="#e6eaee")
    v.rect(CY1 + 50, BOS_D, 100, 200, w=0.3, mat="steel")
    v.rect(CY1 + 56, BOS_D + 6, 88, 188, w=0.1, fill="#fff")
    v.pl([(0, BOS_D), (-75, BOS_D), (-75, TOS_D), (0, TOS_D)], w=0.25, mat="steel")
    v.pl([(-75, TOS_D + 70), (CY1 + 150, TOS_D + 20), (CY1 + 150, TOS_D + 38), (-75, TOS_D + 88)], w=0.2,
         fill="#d9b98a")
    v.pl([(-75, TOS_D + 90), (CY1 + 350, TOS_D + 45), (CY1 + 350, TOS_D + 70), (-75, TOS_D + 115)], w=0.1,
         fill="#555")
    v.pl([(-300, TOS_D + 115), (CY1 + 350, TOS_D + 70), (CY1 + 350, GR_TOP), (-300, GR_TOP + 40)], w=0.15,
         mat="soil")
    v.pl([(-75, TOS_D + 115), (-300, TOS_D + 115), (-300, GR_TOP + 40), (-75, GR_TOP + 40)], w=0.1, mat="gravel")
    v.pl([(CY1 + 350, TOS_D + 50), (CY1 + 50, TOS_D + 40), (CY1 + 50, GR_TOP - 20), (CY1 + 350, GR_TOP - 10)],
         w=0.1, mat="gravel")
    v.line(-300, GR_TOP + 40, CY1 + 350, GR_TOP, w=0.6, color="#5d8a4a")
    v.pl([(CY1 + 50, FT), (CY1, FT), (CY1, SOF), (CY1 + 80, SOF)], w=0.5, closed=False)
    v.rect(CY1 + 80, SOF, -CY1 - 80, 12, w=0.15, fill="#f2f2f2")
    for (x, y) in DL:
        if x == 1900:
            v.rect(y - 40, SOF, 80, 60, w=0.15, fill="#fff3cd")
    v.pl([(-75, 3170), (-20, 3170), (-20, TOS_D + 90)], w=0.4, closed=False, color="#7f8c8d")
    # post beyond
    v.rect(-3450 - CHS / 2, 0, CHS, SOF, w=0.15, fill="#a99383", color="#4b3a2f")
    # planter & boundary wall beyond
    v.rect(PL3, -5, -PL3, COP_TOP - COP_T + 5, w=0.12, mat="render", color="#999")
    # pool cut (lengthwise)
    v.rect(PL3, -450, POOL[2] - PL3, 300, w=0.3, mat="rc")
    v.rect(POOL[2] - 200, -150, 200, COPE - 50 + 150, w=0.3, mat="rc")
    v.rect(POOL[2] - 225, COPE - 50, 250, 50, w=0.3, mat="conc")
    v.rect(PL3, -150, POOL_IN[2] - PL3, WATER + 150, w=0.1, fill="#5d8fb5")
    v.line(PL3, WATER, POOL_IN[2], WATER, w=0.3, color="#1f5fa8")
    z = SOF
    while z > WATER:
        v.circle(-3700, z, 22, w=0.15)
        z -= 70
    v.rect(-3700 - 60, SOF - 20, 120, 20, w=0.2, fill="#888")
    break_line(v, PL3, -900, PL3, 600)
    ladder(v, 900, [(0, "±0.000"), (WATER, "+0.380 water"), (COPE, "+0.450 coping"), (SOF, "+2.650 soffit"),
                    (TOS_D, "+2.900 TOS"), (FT, "+3.150 fascia"), (FAC_PARAPET, "+3.400")], 310, size=1.3,
           inside=False)
    v.chain([POOL_IN[2], POOL[2], CY1, 0], "x", -900, -4, size=1.3)
    C = [
        ((-2000, GR_TOP - 10), (-5200, 3500), ["Sedum mat + 80 extensive substrate + fleece + 25 drainage board"]),
        ((-2000, TOS_D + 75), (-5200, 3330), ["Root barrier / 1.5 EPDM / 18 ply / firrings 1:60 / C200 joists @ 450"]),
        ((CY1 + 20, 2900), (-5200, 3160), ["Fascia 3 mm bronze anodised alu, 500 high"]),
        ((-1500, SOF + 6), (-5200, 2450), ["Soffit 12 mm fibre-cement, white, on battens; 6 x 7 W downlights"]),
        ((-75, 1500), (-2500, 1900), ["Living wall cassettes on alu rails, 10 air gap, base drip gutter"]),
        ((-3700, 1500), (-6200, 1500), ["Copper rain chain into pool"]),
        ((-5500, 200), (-6200, 1000), ["RC pool 200 walls & 300 base, EPDM liner, black"]),
        ((-2000, -40), (-3500, -1100), ["80 permeable pavers / 50 grit 2–6 / 350 open-graded 4/20"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.35, anchor="start")


def axo(s, ox, oy, scale):
    a = Axo(beta=28, elev=30)
    a.poly3([(PAV_X0, -8400, 0), (PAV_X1, -8400, 0), (PAV_X1, 0, 0), (PAV_X0, 0, 0)], "#cfd0cc", stroke="#999")
    a.poly3([(PAV_X0, -8400, 1), (PAV_X1, -8400, 1), (PAV_X1, -8300, 1), (PAV_X0, -8300, 1)], "#55585c")
    mbox(a, -BW_T, 0, 0, COURT_W + EW_T + BW_T, 3000, FAC_PARAPET, "#f3ede2", layer=1, bias=-1e5)
    for (x0, x1), col in ((D01, "#a9cde0"), (D02, "#5b4636"), (D03, "#b07a45")):
        mbox(a, x0, -25, 0, x1 - x0, 25, HEAD, col, layer=1, bias=-9e4)
    mbox(a, LW[0], -150, LW[2], LW[1] - LW[0], 150, LW[3] - LW[2], "#5f8f4b", layer=1, bias=-8.5e4)
    mbox(a, AC1[0], -300, AC1[2], AC1[1] - AC1[0], 300, AC1[3] - AC1[2], "#efefef", layer=1, bias=-8e4)
    mbox(a, -BW_T, -8400, 0, BW_T, 8400, BW_TOP, "#efe7da", layer=1, bias=-1.2e5)
    mbox(a, 0, PL_SOUTH, 0, KERB_X0, -PL_SOUTH, SOIL_TOP, "#7b5a3a", layer=1, bias=-7e4)
    mbox(a, KERB_X0, PL_SOUTH, 0, KERB_T, -PL_SOUTH, COP_TOP, "#f1ebdf", layer=1, bias=-6e4)
    for (code, x, y, sp) in PLANTS:
        if code != "OL":
            a.blob(x, y, SOIL_TOP + 450, sp * 0.6, fill="#6f9d58", layer=2, flowers=4, seed=int(-y) % 89)
    mbox(a, POOL[0], POOL[3], 0, POOL[1] - POOL[0], POOL[2] - POOL[3], COPE, "#e3ddd2", layer=2)
    a.poly3([(POOL_IN[0], POOL_IN[3], COPE + 2), (POOL_IN[1], POOL_IN[3], COPE + 2),
             (POOL_IN[1], POOL_IN[2], COPE + 2), (POOL_IN[0], POOL_IN[2], COPE + 2)], "#2c3e50", layer=2, bias=-1)
    mbox(a, COURT_W, -EW_LEN, 0, EW_T, EW_LEN, 1000, "#e9e2d6", layer=2)
    mbox(a, COURT_W, -8400, 0, 100, 3000, 1000, "#a8723f", layer=2)
    mbox(a, FIRE[0] - 450, FIRE[1] - 450, 0, 900, 900, 350, "#8e5a3c", layer=2)
    for k in range(4):
        ang = math.radians(45 + 90 * k)
        mbox(a, FIRE[0] + 1300 * math.cos(ang) - 350, FIRE[1] + 1300 * math.sin(ang) - 350, 0, 700, 700, 400,
             "#ded6c8", layer=2)
    for (x, y) in POSTS:
        mbox(a, x - 70, y - 70, 0, 140, 140, SOF, "#4b3a2f", layer=3)
    mbox(a, CX0, CY1, SOF, CX1 - CX0, -CY1, FT - SOF, "#4b3a2f", layer=4)
    a.poly3([(CX0 + 300, CY1 + 300, FT + 2), (CX1 - 300, CY1 + 300, FT + 2), (CX1 - 300, -300, FT + 2),
             (CX0 + 300, -300, FT + 2)], "#8fb36f", stroke="#5d8a4a", layer=5)
    import random
    rnd = random.Random(9)
    for i in range(50):
        a.blob(rnd.uniform(CX0 + 400, CX1 - 400), rnd.uniform(CY1 + 400, -400), FT + 40, 90, fill="#a9c98c",
               stroke="#6c9a52", layer=6, seed=i, flowers=1)
    a.render(s, ox, oy, scale)


def details(s):
    # DD1 pool wall & coping 1:10
    v = View(s, 70, 140, 10, origin=(1000, 0))
    v.pl([(700, -600), (1450, -600), (1450, -100), (700, -100)], w=0, mat="earth")
    v.rect(POOL[0], -450, 500, 300, w=0.35, mat="rc")
    v.rect(POOL[0], -150, 200, COPE - 50 + 150, w=0.35, mat="rc")
    v.rect(POOL[0] - 25, COPE - 50, 250, 50, w=0.35, mat="conc")
    v.rect(POOL_IN[0], -150, 300, WATER + 150, w=0.1, fill="#5d8fb5")
    v.line(POOL_IN[0], -150, POOL_IN[0], COPE - 60, w=0.6, color="#111")
    v.line(POOL_IN[0], -150, POOL_IN[0] + 300, -150, w=0.6, color="#111")
    v.rect(POOL[0] - 150, -400, 150, COP_TOP + 400, w=0.3, mat="rc")
    v.rect(700, -200, 150, SOIL_TOP + 200, w=0.1, mat="soil")
    v.leader([(POOL[0] + 100, COPE - 25), (1250, 700)], ["Precast coping 250x50, 25 drip both sides"], size=1.3,
             anchor="start")
    v.leader([(POOL_IN[0], 200), (1250, 560)], ["1.0 EPDM liner on 300 g underlay, black"], size=1.3,
             anchor="start")
    v.leader([(POOL[0] + 100, 0), (1250, 420)], ["200 RC wall C35/45 XC4, Ø10 @ 200 EF"], size=1.3,
             anchor="start")
    v.leader([(POOL[0] + 250, -300), (1250, -350)], ["300 RC base on 50 blinding + 150 Type 1"], size=1.3,
             anchor="start")
    v.leader([(POOL[0] - 75, 0), (700, 800)], ["Planter kerb (existing design)"], size=1.3, anchor="end")
    s.text(16, 52, "DD1  RAISED POOL WALL & COPING — 1:10", size=1.9, weight="bold")
    # DD2 living wall 1:10 (u = -Y outward)
    w = View(s, 200, 125, 20, origin=(0, 1400))
    w.rect(0, 400, 300, 2100, w=0.35, mat="masonry")
    w.rect(-12, 400, 12, 2100, w=0.05, fill="#111")
    w.rect(-52, 450, 40, 2000, w=0.15, fill="#9aa3ab")
    for z in range(450, 2450, 500):
        w.rect(-152, z + 5, 100, 490, w=0.2, fill="#7b5a3a")
        w.circle(-170, z + 250, 60, w=0.1, fill="#6f9d58")
        w.circle(-150, z + 120, 45, w=0.1, fill="#86b36a")
    w.rect(-220, 360, 220, 90, w=0.25, fill="#9aa3ab")
    w.leader([(-6, 1900), (350, 2700)], ["Waterproof backing: 2 coats tanking slurry"], size=1.3, anchor="start")
    w.leader([(-32, 1600), (350, 2400)], ["Alu rails 40 + 10 air gap, SS anchors"], size=1.3, anchor="start")
    w.leader([(-100, 1200), (350, 1200)], ["500x500 planted cassettes,", "drip line per row"], size=1.3,
             anchor="start")
    w.leader([(-110, 400), (350, 400)], ["Drip gutter → planter"], size=1.3, anchor="start")
    s.text(150, 52, "DD2  LIVING WALL — 1:20", size=1.9, weight="bold")
    # DD3 permeable paving 1:10
    p = View(s, 60, 222, 10, origin=(0, 0))
    p.rect(-450, -80, 900, 80, w=0.25, fill="#cfd0cc")
    for x in range(-450, 450, 100):
        p.line(x, -80, x, 0, w=0.15, color="#fff")
    p.rect(-450, -130, 900, 50, w=0.2, mat="gravel")
    p.rect(-450, -480, 900, 350, w=0.2, mat="subbase")
    p.line(-450, -480, 450, -480, w=0.4, dash="2,0.6", color="#7a5c3a")
    p.rect(-450, -600, 900, 120, w=0, mat="earth")
    p.leader([(0, -40), (500, 60)], ["80 permeable concrete pavers, 8 mm joints with 2–6 grit"], size=1.3,
             anchor="start")
    p.leader([(0, -105), (500, -110)], ["50 bedding grit 2–6.3"], size=1.3, anchor="start")
    p.leader([(0, -300), (500, -300)], ["350 open-graded sub-base 4/20 (storage 30% voids)"], size=1.3,
             anchor="start")
    p.leader([(0, -480), (500, -470)], ["Geotextile; infiltration ≥ 1e-5 m/s (test)"], size=1.3, anchor="start")
    s.text(16, 208, "DD3  PERMEABLE PAVING (SuDS) — 1:10", size=1.9, weight="bold")
    s.textblock(258, 18, 80, [
        ("B", "WATER SYSTEMS"),
        "• Pool: 600 x 3600, water depth 530; submersible pump 3 m³/h + 9 W UV clarifier + skimmer box; weir "
        "blade at N end; overflow at +0.40 to soakaway; mains top-up via float valve + RPZ backflow.",
        "• Rain chains: 2 no. copper; W into pool, E into gravel basin → RWH tank.",
        "• RWH tank 2000 L flat underground, inlet filter, calmed inlet, 0.5 kW pump, controller; feeds "
        "living wall, planter drip & pool top-up; overflow to SA1 soakaway.",
        ("B", "GREEN ROOF"),
        "• FLL / GRO code; sedum mix ≥ 8 species; 300 gravel margins & around outlets; inspection 2x/yr.",
        "• Saturated load 1.30 kN/m² → joists C200 @ 450, beams as A + front beam RHS 200x100 on 3 CHS posts.",
        ("B", "STRUCTURE"),
        "• Ledger to façade as Design A (survey). Posts CHS 139.7x6.3 on 250 base plates, pads 600x600x700.",
        "• ULS ≈ 4.1 kN/m²: front beam spans 2.0 m — trivial; joists 3.3 m @ 450 M ≈ 2.5 kNm.",
    ], size=1.42, gap=0.3)


def boq():
    area = (PAV_X1 - PAV_X0) * 8.4 / 1000
    return [
        ["1", "PRELIMINARIES & SURVEY", "", "", ""],
        ["1.1", "Survey, percolation test, set-up", "item", "1", ""],
        ["2", "GROUNDWORKS", "", "", ""],
        ["2.1", "Excavate for permeable build-up (0.5 m)", "m³", f"{area * 0.5:.1f}", ""],
        ["2.2", "RWH tank 2000 L excavation & install", "item", "1", ""],
        ["2.3", "Post pads 600x600x700", "no", "3", ""],
        ["3", "CANOPY STRUCTURE", "", "", ""],
        ["3.1", "Steel frame HDG (ledger, beams, C200 @ 450)", "t", "0.75", ""],
        ["3.2", "CHS 139.7x6.3 posts, MIO bronze", "no", "3", ""],
        ["3.3", "Ply deck, firrings, EPDM, flashings", "m²", f"{(CX1 - CX0) * 3.6 / 1000:.1f}", ""],
        ["3.4", "Green roof system (sedum, substrate, layers)", "m²", f"{(CX1 - CX0 - 600) * 3.0 / 1000:.1f}", ""],
        ["3.5", "Bronze fascia 500 mm", "m", f"{(CX1 - CX0 + 7200) / 1000:.1f}", ""],
        ["3.6", "Fibre-cement soffit + 6 downlights", "m²", f"{(CX1 - CX0) * 3.6 / 1000:.1f}", ""],
        ["3.7", "Outlets, inspection boxes, 2 copper rain chains", "item", "1", ""],
        ["4", "WATER FEATURE", "", "", ""],
        ["4.1", "RC raised pool incl. liner, coping", "item", "1", ""],
        ["4.2", "Pump, UV, weir, skimmer, lighting 2 x 12 V", "item", "1", ""],
        ["5", "LIVING WALL", "", "", ""],
        ["5.1", "Modular living wall 1.45 x 2.0 incl. plants", "m²", "2.9", ""],
        ["5.2", "Irrigation controller & dosing", "item", "1", ""],
        ["6", "PAVING", "", "", ""],
        ["6.1", "Permeable pavers 80 herringbone + border", "m²", f"{area:.1f}", ""],
        ["6.2", "Open-graded sub-base 350 + grit 50 + geotextile", "m²", f"{area:.1f}", ""],
        ["7", "PLANTER (as A) & FIRE BOWL (FF&E)", "item", "1", ""],
        ["8", "ELECTRICAL", "item", "1", ""],
        ["9", "CONTINGENCY", "%", "10", ""],
    ]


def sheets():
    reg = [("D-000", "Cover, concept & register"), ("D-100", "General arrangement plan 1:50"),
           ("D-101", "Green roof & structure plan 1:25"), ("D-200", "Elevation A 1:25"),
           ("D-300", "Section A-A (N-S) 1:25"), ("D-500", "Details 1:10"), ("D-600", "Schedules & BOQ")]
    compare = [["Roof", "Membrane", "Sedum green roof"], ["Water", "Gullies to drain", "SuDS + 2000 L reuse"],
               ["Biodiversity", "Planter", "Roof + wall + pool"], ["Cooling", "Shade", "Shade + evap."],
               ["Posts", "2 timber-clad", "3 slim CHS"], ["Cost class", "€€", "€€€"],
               ["Maintenance", "Low", "Medium (pump, wall)"], ["Load on façade", "Ledger", "Ledger"]]
    out = [cover(CODE, TITLE, "Sedum-roofed bronze canopy, raised reflecting pool fed by rain chains, a living wall "
                 "and permeable paving that harvests rainwater for irrigation.", axo,
                 ["A sustainable, cooling courtyard: every drop of rain is either stored (2000 L tank), reused "
                  "(living wall, planter, pool top-up) or infiltrated through permeable paving. The canopy carries "
                  "an extensive sedum roof seen from the house above; rain chains turn storms into a feature."],
                 ["• 4.3 x 3.6 m canopy, 3 slim bronze posts, sedum roof, white soffit with downlights.",
                  "• Raised reflecting pool 600 x 3600 with seat-height coping and weir.",
                  "• Living wall beside D01; drip-fed from harvested rain.",
                  "• Permeable herringbone paving (no gullies), fire bowl lounge."], compare, reg)]
    s = Sheet("D-100", "Proposal D — general arrangement plan", "1:50", project=PJ)
    s.frame()
    v = View(s, 62, 70, 50)
    plan(v)
    v.chain([0, KERB_X1, POOL[1], CX0, CX1, COURT_W], "x", -8400, -10, size=1.4)
    v.chain([0, CY1, POOL[2], POOL[3], -8400], "y", -BW_T, 12, size=1.4)
    v.leader([(3300, -2000), (3600, -4300)], ["Green-roof canopy over (dashed) — D-101"], size=1.6)
    v.leader([(1500, -6000), (2600, -6800)], ["Raised reflecting pool (DD1)"], size=1.6)
    v.leader([(800, -60), (2400, -1400)], ["Living wall on façade (DD2)"], size=1.6)
    v.leader([(FIRE[0], FIRE[1]), (5300, -5600)], ["Fire bowl Ø900 (FF&E)"], size=1.6)
    v.title(48, 262, "1/D-100", "GENERAL ARRANGEMENT PLAN", "1:50 @ A3")
    s.north_arrow(225, 30, 6)
    s.scale_bar(240, 268, 50)
    s.textblock(262, 22, 74, [
        ("B", "NOTES"),
        "1. Paving is permeable (SuDS): no gullies; SD1 slot drain kept at door thresholds only.",
        "2. Fall 1:100 away from façade even though permeable (exceedance).",
        "3. Pool & planter share footing line; pool wall independent with 10 mm joint.",
        "4. Fire bowl ≥ 2.0 m from canopy edge & planting; bioethanol or wood.",
        "5. Percolation test required (BRE 365 or local) to size SA1 & confirm sub-base storage.",
    ], size=1.55, gap=0.4)
    out.append(s)
    s = Sheet("D-101", "Proposal D — green roof & structure plan", "1:25", project=PJ)
    s.frame()
    v = View(s, 40, 34, 25, origin=(0, 300))
    roof_plan(v)
    v.title(22, 214, "1/D-101", "GREEN ROOF, DRAINAGE & STRUCTURE PLAN", "1:25 @ A3")
    s.scale_bar(240, 268, 25, 2)
    out.append(s)
    s = Sheet("D-200", "Proposal D — elevation A (looking north)", "1:25", project=PJ)
    s.frame()
    v = View(s, 44, 215, 25)
    elev(v)
    v.title(28, 266, "1/D-200", "ELEVATION A — GREEN CANOPY, POOL & LIVING WALL", "1:25 @ A3")
    s.scale_bar(250, 268, 25, 2)
    out.append(s)
    s = Sheet("D-300", "Proposal D — section A-A (N-S at X = 1500)", "1:25", project=PJ)
    s.frame()
    v = View(s, 270, 196, 25)
    section(v)
    v.title(24, 262, "1/D-300", "SECTION A-A", "1:25 @ A3", sub="through living wall, green roof & pool, looking west")
    s.scale_bar(240, 268, 25, 2)
    out.append(s)
    s = Sheet("D-500", "Proposal D — details", "1:10", project=PJ)
    s.frame()
    details(s)
    out.append(s)
    out.append(boq_sheet(CODE, TITLE, boq(), "Green roof & living wall by specialist (design & install, 2-year "
                         "maintenance). Pool pump/UV sized by supplier."))
    return out
