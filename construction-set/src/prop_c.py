"""PROPOSAL C — Glulam garden room with glass roof + outdoor kitchen."""
import math
from cad import Sheet, View, break_line
from common import *  # noqa
from design import *  # noqa
from sheets_b import ladder, paving_cut
from prop_common import project, ctx_plan, ctx_elev, ctx_section_ns, cover, boq_sheet
from axo import Axo, mbox
import random

CODE = "C"
TITLE = "Timber garden room & outdoor kitchen"
PJ = project(CODE, TITLE)

RX0, RX1 = 1050, 5450            # roof extent (stops W of AC1 / D03)
RY1 = -3900                      # front edge incl. 200 overhang
FB_Y = (-3630, -3770)            # front beam 140 wide, c/l -3700
POSTS = [(1200, -3700), (5300, -3700)]
PS = 140
LEDGER_TOP = 3100
PITCH_DEG = 5.0
SLOPE = math.tan(math.radians(PITCH_DEG))
RAF_D, RAF_B = 240, 90
FB_D = 360
RAFTERS = [RX0 + 45 + i * (RX1 - RX0 - 90) / 5 for i in range(6)]
KIT = (6550, 7200, -700, -4700)  # kitchen counter x0,x1,y0,y1
KIT_ZONES = [(-700, -1300, "Tall store"), (-1300, -2200, "Sink"), (-2200, -2800, "Fridge"), (-2800, -3400, "Prep"),
             (-3400, -4200, "Gas grill"), (-4200, -4700, "Side burner")]
GX = 6250                         # relocated gully line


def raf_top(y):
    """Top of rafter at plan y (y<=0)."""
    return LEDGER_TOP - SLOPE * (-y)


FB_TOP = raf_top(-3700)
FB_BOT = FB_TOP - FB_D


def travertine(v, x0, x1, y0, y1):
    v.rect(x0, y1, x1 - x0, y0 - y1, w=0.25, fill="#e9dcc4")
    rnd = random.Random(4)
    # French pattern approximation: rows of 400 with mixed lengths
    y = y0
    sizes = [600, 400, 200]
    while y > y1:
        h = rnd.choice((400, 400, 200))
        x = x0 + rnd.choice((0, 200))
        v.line(x0, y - h, x1, y - h, w=0.05, color="#a8977a")
        while x < x1:
            v.line(x, y, x, max(y - h, y1), w=0.05, color="#a8977a")
            x += rnd.choice(sizes)
        y -= h


def plan(v):
    travertine(v, PAV_X0, PAV_X1, 0, -8400)
    ctx_plan(v)
    v.rect(SD1[0], SD1[3], SD1[1] - SD1[0], 100, w=0.25, fill="#d0d5da")
    for gy in (-2200, -6200):
        v.rect(GX - 150, gy - 150, 300, 300, w=0.3, fill="#d0d5da")
    # kitchen
    v.rect(KIT[0], KIT[3], KIT[1] - KIT[0], KIT[2] - KIT[3], w=0.4, fill="#d8d4cf")
    for a, b, lab in KIT_ZONES:
        v.line(KIT[0], b, KIT[1], b, w=0.15)
        v.text((KIT[0] + KIT[1]) / 2 - 40, (a + b) / 2, lab, size=1.25, anchor="middle", rot=90)
    v.rect(KIT[0] + 120, -1550, 400, 450, w=0.2, fill="#c9d0d6")
    v.rect(KIT[0] + 60, -4100, 520, 600, w=0.2, fill="#555")
    # roof outline & posts
    v.rect(RX0, RY1, RX1 - RX0, -RY1, w=0.35, dash="4,1.5")
    for x in RAFTERS:
        v.line(x, -60, x, RY1, w=0.1, dash="2,1.2", color="#8a5a2b")
    for (x, y) in POSTS:
        v.rect(x - PS / 2, y - PS / 2, PS, PS, w=0.35, fill="#b07a45")
    # table
    v.rect(2300, -2700, 2200, 1000, w=0.15, dash="1.5,0.8", color="#777")
    for xx in range(2500, 4500, 550):
        for yy in (-1550, -2850):
            v.rect(xx - 225, yy - 225 if yy > -2000 else yy - 225, 450, 450, w=0.1, dash="1,0.6", color="#999")
    v.text(3400, -2250, "dining 2200 x 1000 (FF&E)", size=1.3, anchor="middle", color="#777")


def roof_plan(v):
    v.rect(-BW_T, 0, 7750, FAC_T, mat="masonry", w=0.3)
    v.rect(-BW_T, -4300, BW_T, 4300, mat="masonry", w=0.3)
    v.rect(COURT_W, -4300, EW_T, 4300, mat="masonry", w=0.3)
    v.rect(AC1[0], -300, AC1[1] - AC1[0], 300, w=0.2, fill="#eee", dash="1.5,0.8")
    v.rect(KIT[0], KIT[3], KIT[1] - KIT[0], KIT[2] - KIT[3], w=0.2, fill="#eee", dash="1.5,0.8")
    v.text(6875, -2700, "KITCHEN (open-air)", size=1.4, anchor="middle", rot=90, color="#777")
    v.rect(RX0, RY1, RX1 - RX0, -RY1, w=0.2, fill="#e8f2f7")
    v.rect(RX0, -90, RX1 - RX0, 90, w=0.3, fill="#c89a63")  # ledger 90x315
    v.rect(RX0, FB_Y[1], RX1 - RX0, 140, w=0.3, fill="#c89a63")
    for x in RAFTERS:
        v.rect(x - 45, RY1, 90, -RY1 - 90, w=0.25, fill="#d9a86a")
        v.rect(x - 30, RY1, 60, -RY1 - 90, w=0.15, fill="#9aa3ab")
    v.rect(RX0, RY1 - 130, RX1 - RX0, 130, w=0.25, fill="#c9d0d6")
    for x in RAFTERS[1:-1]:
        v.line(x, -1950, x + 0.01, -1950, w=0)
    for i in range(len(RAFTERS) - 1):
        v.line(RAFTERS[i] + 45, -1950, RAFTERS[i + 1] - 45, -1950, w=0.2, color="#555")
    for (x, y) in POSTS:
        v.rect(x - PS / 2, y - PS / 2, PS, PS, w=0.35, fill="#8a5a2b")
    v.circle(RX1 - 150, RY1 - 65, 40, w=0.25, fill="#1f5fa8")
    for x in (2600, 4100):
        v.circle(x, -2200, 120, w=0.25, fill="#fff3cd")
    v.chain([RX0] + [round(x) for x in RAFTERS] + [RX1], "x", RY1 - 130, -8, size=1.3)
    v.chain([0, -90, FB_Y[0], FB_Y[1], RY1, RY1 - 130], "y", RX1, -14, size=1.3, overall=False)
    v.chain([RX0, POSTS[0][0], POSTS[1][0], RX1], "x", 0, 8, size=1.3)
    v.leader([(3000, -1200), (3200, -900)], ["Glass: 8+8 HS laminated, solar-control low-e, 2 panels per bay",
                                             "(1975 long) on alu glazing bars + EPDM, fall 5° (1:11)"], size=1.4)
    v.leader([(RAFTERS[2], -2900), (3700, -3200)], ["Rafters GL24h 90x240 @ 862 c/c"], size=1.4)
    v.leader([(2000, -45), (1500, 500)], ["Ledger GL24h 90x315, M16 resin anchors @ 600"], size=1.4)
    v.leader([(2000, -3700), (1500, -4500)], ["Front beam GL24h 140x360 on 2 posts 140x140"], size=1.4)
    v.leader([(RX1 - 150, RY1 - 65), (5900, -4500)], ["Gutter 130 alu + RWP down E post"], size=1.4)
    v.leader([(2600, -2200), (1500, -2700)], ["Pendants over table (2 x IP44)"], size=1.4, anchor="end")


def elev(v):
    ctx_elev(v, extra_levels=[(FB_BOT, f"+{FB_BOT / 1000:.3f} u/s beam"), (LEDGER_TOP, "+3.100 ledger top")])
    for i, (cx, w_, h_) in enumerate(((180, 500, 800), (520, 600, 650), (350, 380, 1150))):
        shrub(v, cx, COP_TOP - 10, w_, h_, seed=220 + i, flowers=4)
    for (x, y) in POSTS:
        v.rect(x - PS / 2, 30, PS, FB_BOT - 30, w=0.35, mat="timber")
        v.rect(x - 60, -5, 120, 35, w=0.25, fill="#999")
    v.rect(RX0, FB_BOT, RX1 - RX0, FB_D, w=0.4, mat="timber")
    for x in RAFTERS:
        zt = raf_top(RY1)
        v.rect(x - 45, zt - RAF_D, 90, RAF_D, w=0.25, fill="#d9a86a")
    v.rect(RX0, raf_top(RY1) - 130, RX1 - RX0, 130, w=0.3, fill="#c9d0d6")
    v.line(RX0, raf_top(RY1) + 20, RX1, raf_top(RY1) + 20, w=0.4, color="#7aa5c0")
    # kitchen end (seen) & BBQ hood? none
    v.rect(KIT[0], -60, KIT[1] - KIT[0], 900 + 60, w=0.35, mat="render")
    v.rect(KIT[0] - 30, 900, KIT[1] - KIT[0] + 30, 25, w=0.3, fill="#3b3b3b")
    v.chain([0, RX0, POSTS[0][0], POSTS[1][0], RX1, KIT[0], COURT_W], "x", -300, -8, size=1.5)
    v.dim((RX0, 0), (RX0, FB_BOT), 8, size=1.5)
    L = [
        ((3000, FB_BOT + 150), (2600, 4300), ["Front beam GL24h 140x360, oiled, alu gutter on face"]),
        ((POSTS[0][0], 1500), (300, 3950), ["Posts GL24h 140x140 on SS post shoes (50 clear)"]),
        ((3000, raf_top(RY1) + 20), (3800, 4650), ["Glass roof 5°, 8+8 laminated solar-control"]),
        ((KIT[0] + 300, 925), (5600, 3700), ["Outdoor kitchen: 20 sintered-stone top +0.92, render carcass"]),
    ]
    for tgt, txt, lines in L:
        v.leader([tgt, (tgt[0], txt[1] - 80), txt], lines, size=1.5, anchor="start")


def section(v):
    """N-S section at X = 3000 (pier between D01/D02), looking west."""
    ctx_section_ns(v, y_min=-4400, y_max=1100, zt=-20, door=False)
    # posts beyond & planter beyond
    v.rect(-4400, -5, 4400, COP_TOP - COP_T + 5, w=0.15, mat="render", color="#888")
    v.rect(-4400, COP_TOP - COP_T, 4400, COP_T, w=0.15, fill="#efe9dd", color="#888")
    for i, (y, w_, h_) in enumerate(((-4100, 500, 600), (-3000, 650, 800), (-1800, 500, 700), (-700, 550, 900))):
        shrub(v, y, COP_TOP - 10, w_, h_, seed=230 + i, flowers=3, fill="#eef5e8", color="#8aa97a")
    v.rect(-3700 - PS / 2, 30, PS, FB_BOT - 30, w=0.2, fill="#efd9b8", color="#8a5a2b")
    # rafter beyond (seen) — sloping
    yb = RY1
    v.pl([(-90, LEDGER_TOP), (yb, raf_top(yb)), (yb, raf_top(yb) - RAF_D), (-90, LEDGER_TOP - RAF_D)], w=0.2,
         fill="#ead2ad")
    # ledger cut
    v.rect(-90, LEDGER_TOP - 315, 90, 315, w=0.35, mat="timber")
    for z in (LEDGER_TOP - 90, LEDGER_TOP - 225):
        v.rect(-110, z - 8, 240, 16, w=0.12, fill="#888")
    # front beam cut
    v.rect(FB_Y[1], FB_BOT, 140, FB_D, w=0.35, mat="timber")
    # glass cut (between rafters) on glazing bar line
    v.pl([(-60, LEDGER_TOP + 25), (yb, raf_top(yb) + 25), (yb, raf_top(yb) + 42), (-60, LEDGER_TOP + 42)], w=0.2,
         mat="glass")
    v.pl([(0, LEDGER_TOP + 180), (-80, LEDGER_TOP + 60), (-80, LEDGER_TOP + 40)], w=0.4, closed=False, color="#555")
    # gutter
    v.pl([(yb + 20, raf_top(yb) - 20), (yb - 110, raf_top(yb) - 20), (yb - 110, raf_top(yb) - 150),
          (yb + 20, raf_top(yb) - 150)], w=0.3, fill="#c9d0d6")
    # shade blind
    v.line(-150, LEDGER_TOP - RAF_D - 40, yb + 300, raf_top(yb + 300) - RAF_D - 40, w=0.25, dash="3,1",
           color="#b07a45")
    # table (FF&E)
    v.rect(-2700, 720, 1000, 30, w=0.15, fill="#ddd")
    v.rect(-2650, 0, 40, 720, w=0.15, fill="#ddd")
    v.rect(-1790, 0, 40, 720, w=0.15, fill="#ddd")
    ladder(v, 1100, [(0, "±0.000"), (HEAD, "+2.400"), (FB_BOT, f"+{FB_BOT / 1000:.3f} u/s beam"),
                     (LEDGER_TOP, "+3.100"), (FAC_PARAPET, "+3.400")], 300, size=1.35, inside=False)
    v.chain([RY1, FB_Y[1], FB_Y[0], -90, 0], "x", -800, -4, size=1.35)
    C = [
        ((-2000, raf_top(-2000) + 35), (-2600, 3700), ["8+8 HS laminated glass on EPDM, alu capping bar"]),
        ((-45, LEDGER_TOP - 150), (-1500, 3350), ["Ledger GL24h 90x315 + M16 resin anchors @ 600"]),
        ((-1500, raf_top(-1500) - 120), (-2900, 2900), ["Rafter GL24h 90x240 beyond"]),
        ((-700, LEDGER_TOP - RAF_D - 50), (-2400, 2550), ["Motorised textile shade under glass (option)"]),
        ((FB_Y[1] + 70, FB_BOT + 150), (-4350, 1700), ["Front beam 140x360"]),
        ((yb - 50, raf_top(yb) - 80), (-4350, 3250), ["Alu box gutter 130"]),
        ((-1000, -30), (-1600, -600), ["30 travertine / 30 mortar / 100 C20 slab / 150 Type 1"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.4, anchor="start")


def axo(s, ox, oy, scale):
    a = Axo(beta=28, elev=30)
    a.poly3([(PAV_X0, -8400, 0), (PAV_X1, -8400, 0), (PAV_X1, 0, 0), (PAV_X0, 0, 0)], "#e9dcc4", stroke="#b8a888")
    mbox(a, -BW_T, 0, 0, COURT_W + EW_T + BW_T, 3000, FAC_PARAPET, "#f3ede2", layer=1, bias=-1e5)
    for (x0, x1), col in ((D01, "#a9cde0"), (D02, "#5b4636"), (D03, "#b07a45")):
        mbox(a, x0, -25, 0, x1 - x0, 25, HEAD, col, layer=1, bias=-9e4)
    mbox(a, AC1[0], -300, AC1[2], AC1[1] - AC1[0], 300, AC1[3] - AC1[2], "#efefef", layer=1, bias=-8e4)
    mbox(a, -BW_T, -8400, 0, BW_T, 8400, BW_TOP, "#efe7da", layer=1, bias=-1.2e5)
    mbox(a, 0, PL_SOUTH, 0, KERB_X0, -PL_SOUTH, SOIL_TOP, "#7b5a3a", layer=1, bias=-7e4)
    mbox(a, KERB_X0, PL_SOUTH, 0, KERB_T, -PL_SOUTH, COP_TOP, "#f1ebdf", layer=1, bias=-6e4)
    for (code, x, y, sp) in PLANTS:
        if code != "OL":
            a.blob(x, y, SOIL_TOP + 450, sp * 0.6, fill="#6f9d58", layer=2, flowers=4, seed=int(-y) % 91)
    mbox(a, COURT_W, -EW_LEN, 0, EW_T, EW_LEN, 1000, "#e9e2d6", layer=2)
    mbox(a, KIT[0], KIT[3], 0, KIT[1] - KIT[0], KIT[2] - KIT[3], 900, "#ece6dc", layer=2)
    mbox(a, KIT[0] - 30, KIT[3], 900, KIT[1] - KIT[0] + 30, KIT[2] - KIT[3], 25, "#3b3b3b", layer=2, bias=-1)
    mbox(a, KIT[0] + 60, -4100, 925, 520, 600, 120, "#777", layer=2, bias=-2)
    mbox(a, COURT_W, -8400, 0, 100, 3000, 1000, "#a8723f", layer=2)
    mbox(a, 2300, -2700, 0, 2200, 1000, 740, "#c9b79c", layer=2)
    for (x, y) in POSTS:
        mbox(a, x - 70, y - 70, 0, PS, PS, FB_BOT, "#b98552", layer=3)
    mbox(a, RX0, FB_Y[1], FB_BOT, RX1 - RX0, 140, FB_D, "#c89a63", layer=4)
    for x in RAFTERS:
        a.poly3([(x - 45, 0, LEDGER_TOP), (x + 45, 0, LEDGER_TOP), (x + 45, RY1, raf_top(RY1)),
                 (x - 45, RY1, raf_top(RY1))], "#d9a86a", layer=5)
        a.poly3([(x + 45, 0, LEDGER_TOP), (x + 45, RY1, raf_top(RY1)), (x + 45, RY1, raf_top(RY1) - RAF_D),
                 (x + 45, 0, LEDGER_TOP - RAF_D)], "#b9864e", layer=5, bias=1)
    a.poly3([(RX0, 0, LEDGER_TOP + 30), (RX1, 0, LEDGER_TOP + 30), (RX1, RY1, raf_top(RY1) + 30),
             (RX0, RY1, raf_top(RY1) + 30)], "#cfe6f2", stroke="#7aa5c0", layer=6)
    s.add('')
    a.render(s, ox, oy, scale)


def details(s):
    # DC1 glazing bar 1:2
    v = View(s, 70, 70, 2, origin=(0, 0))
    v.rect(-45, -120, 90, 120, w=0.3, mat="timber")
    v.rect(-30, 0, 60, 12, w=0.2, fill="#9aa3ab")
    v.rect(-45 - 70, 12, 70 + 27, 18, w=0.15, mat="glass")
    v.rect(18, 12, 97, 18, w=0.15, mat="glass")
    v.rect(-27, 6, 9, 8, w=0.1, fill="#222")
    v.rect(18, 6, 9, 8, w=0.1, fill="#222")
    v.pl([(-35, 30), (35, 30), (35, 38), (5, 44), (-5, 44), (-35, 38)], w=0.25, fill="#9aa3ab")
    v.rect(-3, -40, 6, 80, w=0.1, fill="#666")
    v.leader([(0, 42), (60, 80)], ["Alu capping bar + EPDM, SS screws @ 300"], size=1.3, anchor="start")
    v.leader([(80, 21), (100, 50)], ["8+8 HS lam. glass, solar control"], size=1.3, anchor="start")
    v.leader([(-22, 9), (-110, 60)], ["EPDM gasket on alu base bar"], size=1.3, anchor="end")
    v.leader([(0, -60), (60, -80)], ["Rafter GL24h 90x240"], size=1.3, anchor="start")
    s.text(16, 18, "DC1  GLAZING BAR ON RAFTER — 1:2", size=1.9, weight="bold")
    # DC2 post shoe 1:5
    p = View(s, 60, 236, 10, origin=(0, 0))
    paving_cut(p, [(-300, -20), (300, -20)], z_bottom_extra=150, joints=False)
    p.rect(-250, -500, 500, 300, w=0.3, mat="rc")
    p.rect(-60, -20, 120, 10, w=0.25, fill="#999")
    p.rect(-6, -10, 12, 60, w=0.2, fill="#999")
    p.rect(-60, 50, 120, 10, w=0.25, fill="#999")
    p.rect(-70, 60, 140, 500, w=0.3, mat="timber")
    break_line(p, -90, 540, 90, 540)
    p.leader([(0, 20), (120, 120)], ["SS 316 post shoe, 50 stand-off,", "M12 bolts through post"], size=1.3,
             anchor="start")
    p.leader([(0, -300), (120, -330)], ["Pad 500x500x600 C25/30 (verify)"], size=1.3, anchor="start")
    p.leader([(0, 300), (120, 330)], ["Post GL24h 140x140, end-grain sealed"], size=1.3, anchor="start")
    s.text(16, 160, "DC2  POST SHOE — 1:10", size=1.9, weight="bold")
    # DC3 kitchen counter section 1:10 (u = X)
    k = View(s, 165, 230, 10, origin=(6550, 0))
    k.rect(KIT[1], -200, 200, 1800, mat="masonry", w=0.4)
    k.rect(KIT[1] - 12, 900, 12, 600, w=0.1, fill="#cfc8bd")
    k.rect(KIT[0] + 40, -5, 100, 880, w=0.3, mat="masonry")
    k.rect(KIT[1] - 110, -5, 100, 880, w=0.3, mat="masonry")
    k.rect(KIT[0] - 30, 880, KIT[1] - KIT[0] + 30, 20, w=0.3, fill="#3b3b3b")
    k.rect(KIT[0] + 40, 875, KIT[1] - KIT[0] - 150, 5, w=0.1, fill="#888")
    k.rect(KIT[0] + 150, 400, 350, 450, w=0.2, dash="1.5,0.8")
    k.text(KIT[0] + 325, 600, "SS door / drawer", size=1.2, anchor="middle")
    k.rect(KIT[0] - 300, -60, 300, 60, w=0.2, fill="#e9dcc4")
    k.rect(KIT[0] + 40, -150, KIT[1] - KIT[0] - 40, 150, w=0.2, mat="rc")
    k.leader([(KIT[0] + 200, 900), (KIT[0] - 300, 1300)], ["20 mm sintered stone top, 30 overhang, +0.92"],
             size=1.3, anchor="start")
    k.leader([(KIT[0] + 90, 400), (KIT[0] - 300, 1150)], ["100 dense block carcass, render, plinth upstand"],
             size=1.3, anchor="start")
    k.leader([(KIT[1] - 6, 1200), (KIT[0] - 300, 1600)], ["Porcelain splashback to +1.50"], size=1.3,
             anchor="start")
    s.text(130, 160, "DC3  OUTDOOR KITCHEN COUNTER — 1:10", size=1.9, weight="bold")
    s.textblock(258, 18, 80, [
        ("B", "STRUCTURE (preliminary)"),
        "• Glulam GL24h (EN 14080), service class 3 — use durable-species lamellas (larch/Douglas) or treated; "
        "oil finish; tops of beams capped with alu flashing.",
        f"• Front beam 140x360 span 4.1 m: M ≈ 9 kNm, σ ≈ 3 MPa ≪ 17 MPa.",
        "• Rafters 90x240 @ 862 span 3.7 m: δ ≈ 3 mm (L/1400).",
        "• Ledger 90x315: 2 M16 resin anchors @ 600 into RC ring beam (survey!).",
        "• Loads: glass 0.45, timber 0.15, snow 1.0 kN/m² (assumed).",
        "• Bracing: knee braces in façade plane not needed — ledger + 2 posts + glass/bars diaphragm; add "
        "SS diagonal tie-rods in roof plane if engineer requires.",
        ("B", "KITCHEN SERVICES"),
        "• Cold water 15 mm from utility (frost drain-down valve), sink waste 40 mm → trap → gully G1 (relocated "
        "to X = 6250).",
        "• LPG 2 x 11 kg in ventilated cupboard (low-level vents), regulator, hose ≤ 1.5 m; or natural gas by "
        "Gas Safe/licensed fitter.",
        "• Power: 16 A RCBO, 2 twin IP66 sockets + fridge spur; LED strip under top.",
        "• Grill sits OUTSIDE the glass roof (smoke & heat) — keep 1.0 m clear of AC2.",
    ], size=1.45, gap=0.3)


def boq():
    area = (PAV_X1 - PAV_X0) * 8.4 / 1000
    return [
        ["1", "PRELIMINARIES & SURVEY", "", "", ""],
        ["1.1", "Survey incl. ring-beam check for ledger", "item", "1", ""],
        ["2", "GROUNDWORKS & DRAINAGE", "", "", ""],
        ["2.1", "Strip & excavate", "m³", f"{area * 0.3:.1f}", ""],
        ["2.2", "Post pads 500x500x600", "no", "2", ""],
        ["2.3", "Gullies relocated to X = 6250, Ø110 drains", "item", "1", ""],
        ["2.4", "C20 slab 100 under travertine + mesh", "m²", f"{area:.1f}", ""],
        ["3", "GLULAM STRUCTURE", "", "", ""],
        ["3.1", "Ledger GL24h 90x315", "m", f"{(RX1 - RX0) / 1000:.1f}", ""],
        ["3.2", "Front beam GL24h 140x360", "m", f"{(RX1 - RX0) / 1000:.1f}", ""],
        ["3.3", "Rafters GL24h 90x240", "m", f"{6 * 3.95:.1f}", ""],
        ["3.4", "Posts GL24h 140x140 + SS shoes", "no", "2", ""],
        ["3.5", "Resin anchors M16, hangers, bolts", "item", "1", ""],
        ["4", "GLAZED ROOF", "", "", ""],
        ["4.1", "8+8 HS laminated solar-control glass", "m²", f"{(RX1 - RX0) * 3.95 / 1000:.1f}", ""],
        ["4.2", "Alu glazing bars, cappings, flashings", "m", "32", ""],
        ["4.3", "Alu box gutter + RWP", "m", "4.4", ""],
        ["4.4", "Motorised under-glass textile shade (option)", "m²", f"{(RX1 - RX0) * 3.6 / 1000:.1f}", ""],
        ["5", "OUTDOOR KITCHEN", "", "", ""],
        ["5.1", "Block carcass + render, 4.0 m", "m", "4.0", ""],
        ["5.2", "Sintered stone worktop 20 mm", "m", "4.0", ""],
        ["5.3", "Built-in gas grill 800, side burner, sink + tap", "item", "1", ""],
        ["5.4", "Outdoor fridge 600, SS doors & drawers", "item", "1", ""],
        ["5.5", "Water, waste, gas & power services", "item", "1", ""],
        ["6", "PAVING", "", "", ""],
        ["6.1", "Tumbled travertine 30 mm French pattern on mortar", "m²", f"{area:.1f}", ""],
        ["7", "LIGHTING & POWER", "", "", ""],
        ["7.1", "Pendants x2, under-counter LED, uplights", "item", "1", ""],
        ["8", "PLANTER (as Design A) + herbs", "m", "8.4", ""],
        ["9", "CONTINGENCY", "%", "10", ""],
    ]


def sheets():
    reg = [("C-000", "Cover, concept & register"), ("C-100", "General arrangement plan 1:50"),
           ("C-101", "Roof & structure plan 1:25"), ("C-200", "Elevation A 1:25"),
           ("C-300", "Section A-A (N-S) 1:20"), ("C-500", "Details 1:2 / 1:5 / 1:10"), ("C-600", "Schedules & BOQ")]
    compare = [["Roof", "Opaque membrane", "Glass (bright)"], ["Material", "Steel + timber", "Glulam timber"],
               ["Cooking", "—", "Outdoor kitchen 4 m"], ["Load on façade", "Ledger", "Ledger (lighter)"],
               ["Paving", "Concrete pavers", "Travertine"], ["Cost class", "€€", "€€€"],
               ["Daylight to doors", "Reduced", "Maintained"], ["Maintenance", "Oil timber", "Clean glass, oil"]]
    out = [cover(CODE, TITLE, "Glulam garden room with a glass roof for dining, plus an open-air outdoor kitchen "
                 "along the house wall and tumbled travertine paving.", axo,
                 ["Warm timber structure with a 5° glass roof keeps the doors and hall bright while giving all-weather "
                  "dining for 8. Cooking happens in the open air beside it: a 4 m built-in kitchen with grill, sink "
                  "and fridge along the east wall, with services next to the existing utility room."],
                 ["• GL24h larch glulam, 6 rafters @ 862, front beam on 2 posts (no post mid-span).",
                  "• 8+8 laminated solar-control glass, optional motorised shade.",
                  "• Outdoor kitchen: grill outside the roof, sink & fridge, sintered-stone top.",
                  "• Tumbled travertine in French pattern; planter & jasmine retained."], compare, reg)]
    s = Sheet("C-100", "Proposal C — general arrangement plan", "1:50", project=PJ)
    s.frame()
    v = View(s, 62, 70, 50)
    plan(v)
    v.chain([0, KERB_X1, RX0, POSTS[0][0], POSTS[1][0], RX1, KIT[0], COURT_W], "x", -8400, -10, size=1.4)
    v.chain([0, KIT[2], -3700, KIT[3], -8400], "y", COURT_W + EW_T, -11, size=1.4)
    v.leader([(3400, -3300), (3800, -4800)], ["Glass-roofed garden room over (dashed) — C-101"], size=1.6)
    v.leader([(6700, -3800), (5000, -5600)], ["Outdoor kitchen 4.0 m (DC3)"], size=1.6, anchor="end")
    v.leader([(4000, -7000), (4300, -7600)], ["Tumbled travertine, French pattern"], size=1.6)
    v.title(48, 262, "1/C-100", "GENERAL ARRANGEMENT PLAN", "1:50 @ A3")
    s.north_arrow(225, 30, 6)
    s.scale_bar(240, 268, 50)
    s.textblock(262, 22, 74, [
        ("B", "NOTES"),
        "1. Roof stops at X = 5450 so AC1 above D03 stays in the open (no relocation needed).",
        "2. Gullies G1/G2 move west to X = 6250 (clear of kitchen); falls 1:80 to them, kitchen side 1:60.",
        "3. Kitchen waste connects to G1 via trap; water from utility; LPG cupboard ventilated.",
        "4. Travertine: 30 mm tumbled, filled, frost-resistant; laid on 30 mortar bed on 100 slab.",
        "5. Planter & planting as A-104; add herbs (thyme, oregano, sage) at S end.",
    ], size=1.55, gap=0.4)
    out.append(s)
    s = Sheet("C-101", "Proposal C — roof & structure plan", "1:25", project=PJ)
    s.frame()
    v = View(s, 34, 34, 25, origin=(0, 300))
    roof_plan(v)
    v.title(22, 214, "1/C-101", "ROOF, STRUCTURE & LIGHTING PLAN", "1:25 @ A3")
    s.scale_bar(240, 268, 25, 2)
    out.append(s)
    s = Sheet("C-200", "Proposal C — elevation A (looking north)", "1:25", project=PJ)
    s.frame()
    v = View(s, 44, 215, 25)
    elev(v)
    v.title(28, 266, "1/C-200", "ELEVATION A — GARDEN ROOM & KITCHEN (looking north)", "1:25 @ A3")
    s.scale_bar(250, 268, 25, 2)
    out.append(s)
    s = Sheet("C-300", "Proposal C — section A-A (N-S at X = 3000)", "1:20", project=PJ)
    s.frame()
    v = View(s, 245, 200, 20)
    section(v)
    v.title(28, 262, "1/C-300", "SECTION A-A", "1:20 @ A3", sub="through ledger, glass roof & front beam, looking west")
    s.scale_bar(240, 268, 20, 2)
    out.append(s)
    s = Sheet("C-500", "Proposal C — details", "1:2 / 1:5 / 1:10", project=PJ)
    s.frame()
    details(s)
    out.append(s)
    out.append(boq_sheet(CODE, TITLE, boq(), "Glass supplier to confirm panel build-up, heat-soak and fixings; "
                         "kitchen appliances to client selection (allow cut-outs per manufacturer)."))
    return out
