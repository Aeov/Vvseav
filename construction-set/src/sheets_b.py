"""Elevations & sections (Design A)."""
import math
from cad import Sheet, View, break_line, MAT
from common import *  # noqa
from design import *  # noqa


def ladder(v, xm, levels, px, size=1.45, inside=True):
    """Level ladder: dashed line from model x=xm to paper x=px with marker & label."""
    s = v.s
    for z, lab in levels:
        p = v.P(xm, z)
        s.line(min(p[0], px), p[1], max(p[0], px), p[1], w=0.1, dash="1.2,0.8", color="#444")
        s.poly([(px, p[1]), (px - 1, p[1] - 1.6), (px + 1, p[1] - 1.6)], w=0.12, fill="#fff")
        s.poly([(px, p[1]), (px - 1, p[1] - 1.6), (px, p[1] - 1.6)], w=0, fill="#000")
        left = px < p[0]
        if not inside:
            left = not left
        s.text(px + (1.6 if left else -1.6), p[1] - 0.45, lab, size=size, anchor="start" if left else "end")


def paving_cut(v, pts, z_bottom_extra=250, joints=True, sub=SUB_T):
    """pts: [(u, z_top)] breakpoints along the cut. Draws pavers/bed/sub-base/earth."""
    u0, u1 = pts[0][0], pts[-1][0]
    top = pts
    def off(d):
        return [(u, z - d) for (u, z) in top]
    layers = [(0, PAVER_T, "paver"), (PAVER_T, PAVER_T + BED_T, "sand"),
              (PAVER_T + BED_T, PAVER_T + BED_T + sub, "subbase")]
    for a, b, m in layers:
        poly = off(a) + list(reversed(off(b)))
        v.pl(poly, w=0.15, mat=m)
    deep = PAVER_T + BED_T + sub
    poly = off(deep) + list(reversed(off(deep + z_bottom_extra)))
    v.pl(poly, w=0, mat="earth")
    v.pl(off(deep), w=0.25, closed=False, dash="2,0.6", color="#7a5c3a")  # geotextile
    v.pl(top, w=0.45, closed=False)
    if joints:
        u = u0 + PAVER
        while u < u1:
            # top z at u
            for i in range(len(top) - 1):
                if top[i][0] <= u <= top[i + 1][0]:
                    za = top[i][1] + (top[i + 1][1] - top[i][1]) * (u - top[i][0]) / (top[i + 1][0] - top[i][0])
                    v.line(u, za, u, za - PAVER_T, w=0.12, color="#fff")
                    v.line(u, za, u, za - PAVER_T, w=0.05, color="#555")
            u += PAVER


def soffit_slats_cut(v, y_from, y_to, z=SOFFIT):
    """Slats run E-W -> cut in N-S section: small rectangles."""
    y = y_from
    while y - SLAT_W >= y_to:
        v.rect(y - SLAT_W, z, SLAT_W, SLAT_T, w=0.1, mat="timber", layer="A-TIMBER")
        y -= SLAT_W + SLAT_GAP


def upn200(v, u_wall, z0, facing=-1):
    """UPN 200 cut; web against wall at u_wall, flanges point in direction facing (-1 = to -u)."""
    h, b, tw, tf = 200, 75, 8.5, 11.5
    f = facing
    pts = [(u_wall, z0), (u_wall + f * b, z0), (u_wall + f * b, z0 + tf), (u_wall + f * tw, z0 + tf),
           (u_wall + f * tw, z0 + h - tf), (u_wall + f * b, z0 + h - tf), (u_wall + f * b, z0 + h), (u_wall, z0 + h)]
    v.pl(pts, w=0.2, mat="steel", layer="S-STEEL")


def rhs(v, u0, z0, b, h, t, mat="steel"):
    v.rect(u0, z0, b, h, w=0.2, mat=mat, layer="S-STEEL")
    v.rect(u0 + t, z0 + t, b - 2 * t, h - 2 * t, w=0.12, fill="#fff", layer="S-STEEL")


def cchan(v, xc, z0, h=200, b=65, t=1.8, lip=20, facing=1):
    """Lipped C cut in section, web at xc - facing*b/2."""
    f = facing
    xw = xc - f * b / 2
    pts = [(xw + f * b, z0 + lip), (xw + f * b, z0), (xw, z0), (xw, z0 + h), (xw + f * b, z0 + h),
           (xw + f * b, z0 + h - lip)]
    v.pl(pts, w=0.35, closed=False, color="#3b4650", layer="S-STEEL")


# ======================================================================= A-200 ELEVATION A
def sheet_a200(dxf=None):
    s = Sheet("A-200", "Elevation A — annex façade & canopy (looking north)", "1:25")
    s.frame()
    v = View(s, 44, 215, 25, dxf=dxf, dxf_offset=(0, -20000))
    # sky leaders area above; ground
    zl = paving_level
    ground(v, -250, 7350, -5, depth=250)
    # façade
    v.rect(0, -5, COURT_W, FAC_PARAPET + 5, w=0.35, fill="#f7f3ea")
    v.rect(0, FAC_PARAPET - 50, COURT_W, 50, w=0.25, fill="#efe9dd")
    # solar heater (existing) on annex roof
    v.rect(SOLAR[0], FAC_PARAPET + 150, SOLAR[1] - SOLAR[0], 450, w=0.2, dash="2,1", color="#777")
    v.circle(SOLAR[0] + 400, FAC_PARAPET + 650, 220, w=0.2, dash="2,1", color="#777")
    v.rect(SOLAR[0] + 150, FAC_PARAPET + 450, SOLAR[1] - SOLAR[0] - 300, 500, w=0.15, dash="2,1", color="#777")
    v.text((SOLAR[0] + SOLAR[1]) / 2, FAC_PARAPET + 1080, "EXISTING SOLAR WATER HEATER (retain)", size=1.4,
           anchor="middle", color="#777")
    # doors
    door_elev(v, "D01", *D01)
    door_elev(v, "D02", *D02)
    info = door_elev(v, "D03", *D03)
    for d, x in (("D01", D01), ("D02", D02), ("D03", D03)):
        v.tag((x[0] + x[1]) / 2, HEAD + 120, d, shape="rect", r=1.7, size=1.5)
    ac_unit(v, *AC1)
    # wall light
    v.rect(WL1[0] - 50, WL1[1] - 120, 100, 240, w=0.2, fill="#5a4a3c")
    # façade climbing wires + jasmine
    for x in range(100, 1600, 300):
        v.line(x, 300, x, 2600, w=0.08, color="#7f8c8d", dash="1,0.8")
    vine(v, 300, 350, 2550, seed=11, amp=90)
    vine(v, 1150, 250, 2300, seed=12, amp=80)
    # boundary wall (cut)
    v.rect(-BW_T, -5, BW_T, BW_TOP + 5, mat="masonry", w=0.45)
    v.rect(-BW_T - 25, BW_TOP, BW_T + 50, 50, w=0.3, fill="#e8e3d8")
    # planter south end (seen)
    v.rect(0, -5, KERB_X1, COP_TOP - COP_T + 5, w=0.3, mat="render")
    v.rect(0, COP_TOP - COP_T, COP_X1, COP_T, w=0.3, fill="#efe9dd")
    for i, (cx, w_, h_) in enumerate(((180, 500, 900), (520, 600, 700), (820, 450, 520), (350, 380, 1250))):
        shrub(v, cx, COP_TOP - 10, w_, h_, seed=20 + i, flowers=5)
    # posts (P1 front; P2 hidden behind)
    x = P1[0]
    v.rect(x - POST_CLAD / 2, PED_TOP, POST_CLAD, SOFFIT - PED_TOP, w=0.3, mat="timber", layer="A-TIMBER")
    vine(v, x - 40, 600, SOFFIT, seed=4, amp=70)
    vine(v, x + 40, 500, SOFFIT, seed=7, amp=60)
    # alt P3
    v.rect(P3[0] - POST / 2, -40, POST, SOFFIT + 40, w=0.2, dash="2,1", color="#c0392b")
    v.text(P3[0] + 120, 1200, "P3 (ALT. S2 only)", size=1.4, color="#c0392b", rot=90)
    # canopy fascia
    v.rect(CAN_X0, FASCIA_BOT, CAN_X1 - CAN_X0, FASCIA_TOP - FASCIA_BOT, w=0.45, fill="#ffffff")
    v.line(CAN_X0, FASCIA_BOT + 12, CAN_X1, FASCIA_BOT + 12, w=0.08, color="#999")
    # LED glow indication (reveal)
    v.line(CAN_X0 + 60, FASCIA_BOT - 6, CAN_X1 - 60, FASCIA_BOT - 6, w=0.5, color="#f39c12")
    # trailing vine along fascia top
    for xx in range(CAN_X0, 2400, 120):
        v.circle(xx + 30, FASCIA_TOP + 10 + 25 * math.sin(xx / 150), 26, w=0.08, color=GREEN, fill=GREEN_F)
    # olive pot (FF&E)
    olive_elev(v, 1400, zl(1400) * 1000, h=1900)
    # east house wall end (seen) + screen post end-on
    v.rect(COURT_W, -65, 150, 4200, w=0.35, fill="#f2eee6")
    break_line(v, COURT_W, 4135, COURT_W + 150, 4135)
    v.rect(COURT_W, -65, 100, SCR_H + 65, w=0.25, fill="#8a5a2b")
    # levels ladder (left)
    ladder(v, -BW_T, [(0, "±0.000 FFL"), (COP_TOP, "+0.400 coping"), (BW_TOP + 50, "+1.850 wall"),
                      (HEAD, "+2.400 heads"), (SOFFIT, "+2.650 soffit"), (FASCIA_TOP, "+3.020 fascia"),
                      (FAC_PARAPET, "+3.400 parapet")], 14.5)
    # chains
    v.chain([0, D01[0], D01[1], D02[0], D02[1], D03[0], D03[1], COURT_W], "x", -300, -6, size=1.6)
    v.chain([0, CAN_X0, P1[0], P3[0], CAN_X1, COURT_W], "x", -300, -16, size=1.6, overall=False)
    v.dim((CAN_X1, FASCIA_BOT), (CAN_X1, FASCIA_TOP), -8, size=1.5)
    v.dim((D02[1], 0), (D02[1], HEAD), -5, size=1.5)
    v.dim((AC1[1], HEAD), (AC1[1], SOFFIT), -5, size=1.4)
    # leaders into sky
    L = [
        ((1000, FASCIA_TOP - 100), (1300, 4500), ["FASCIA: 3 mm folded aluminium, powder-coated RAL 9010 matt,",
                                                 "370 high, concealed fixings to alu sub-frame (D3/A-500)"]),
        ((P1[0], 1900), (100, 3950), ["P1: SHS 120x120x6.3 galv. clad 4 sides 20 mm thermo-ash,",
                                       "160x160 finished; SS climbing wires x4 (OPTION B: SHS 150 painted RAL 9010)"]),
        ((2200, 1300), (3200, 4950), ["D01 glazed door: thermally-broken alu, bronze RAL 8019 / anodised,",
                                      "6T/16Ar/6T low-e, level threshold, multi-point lock — see A-600"]),
        ((4000, 1500), (4800, 4500), ["D02 insulated roller shutter, 77 mm slats, RAL 8019 matt,",
                                      "motorised + manual override — see A-600"]),
        ((5900, 1700), (5500, 4950), ["D03 ventilated lattice door, thermo-ash / iroko, 6 x 18 grid,",
                                      "79 mm openings, 36 mm bars, oiled — see A-600"]),
        ((COURT_W - 100, 2600), (5800, 3700), ["Façade: existing render, repair & repaint",
                                               "masonry paint, warm white (match render)"]),
        ((500, COP_TOP - 30), (100, 3600), ["Planter: 150 RC kerb, 2-coat render, cream; 230x60 precast coping"]),
    ]
    for tgt, txt, lines in L:
        v.leader([tgt, (tgt[0], txt[1] - 80), txt], lines, size=1.5, anchor="start")
    v.title(28, 266, "1/A-200", "ELEVATION A — ANNEX FAÇADE & CANOPY (looking north)", "1:25 @ A3",
            sub="planting shown indicatively at 3 years")
    s.scale_bar(250, 268, 25, 2)
    return s


# ======================================================================= A-201 ELEVATIONS B & C
def sheet_a201(dxf=None):
    s = Sheet("A-201", "Elevations B (looking west) & C (looking east)", "1:50")
    s.frame()
    # ---- ELEVATION B: model (Y, Z), north to the right
    v = View(s, 22 + 8650 / 50, 112, 50, dxf=dxf, dxf_offset=(30000, -20000))
    ground(v, -8650, 300, -5, depth=200)
    # boundary wall face beyond
    v.rect(-8650, 0, 8650, BW_TOP, w=0.3, fill="#f7f3ea")
    v.rect(-8650, BW_TOP, 8650, 50, w=0.25, fill="#efe9dd")
    for z in (600, 1000, 1400, 1750):
        v.line(-8250, z, 0, z, w=0.08, color="#7f8c8d", dash="1,0.8")
    # façade cut (right) + annex roof
    v.rect(0, -5, FAC_T, FAC_PARAPET + 5, mat="masonry", w=0.4)
    v.rect(FAC_T, SLAB_SOFFIT, 300, SLAB_TOP - SLAB_SOFFIT, mat="rc", w=0.3)
    break_line(v, FAC_T + 300, SLAB_SOFFIT - 100, FAC_T + 300, SLAB_TOP + 100)
    # planter kerb face (seen)
    v.rect(PL_SOUTH, -5, -PL_SOUTH, COP_TOP - COP_T + 5, w=0.3, mat="render")
    v.rect(PL_SOUTH, COP_TOP - COP_T, -PL_SOUTH, COP_T, w=0.3, fill="#efe9dd")
    v.line(-4200, -5, -4200, COP_TOP - COP_T, w=0.15)
    v.text(-4200, -150, "MJ", size=1.3, anchor="middle")
    seeds = [(-7900, 500, 450), (-7400, 650, 800), (-7000, 550, 600), (-6300, 700, 900), (-5700, 500, 550),
             (-5300, 600, 750), (-4600, 550, 650), (-3900, 700, 950), (-3300, 450, 500), (-2400, 550, 800),
             (-2000, 600, 600), (-700, 500, 700), (-300, 450, 1100)]
    for i, (y, w_, h_) in enumerate(seeds):
        shrub(v, y, COP_TOP - 10, w_, h_, seed=40 + i, flowers=4)
    for (x, y) in (P1, P2):
        v.rect(y - POST_CLAD / 2, COP_TOP, POST_CLAD, SOFFIT - COP_TOP, w=0.3, mat="timber")
        vine(v, y, COP_TOP + 200, SOFFIT, seed=int(-y) % 17, amp=50)
    # canopy east fascia (seen)
    v.rect(CAN_Y1, FASCIA_BOT, -CAN_Y1, FASCIA_TOP - FASCIA_BOT, w=0.4, fill="#fff")
    v.line(CAN_Y1 + 60, FASCIA_BOT - 4, -60, FASCIA_BOT - 4, w=0.45, color="#f39c12")
    ladder(v, -8650, [(0, "±0.000"), (COP_TOP, "+0.400"), (BW_TOP, "+1.800"), (SOFFIT, "+2.650"),
                      (FASCIA_TOP, "+3.020")], 14, size=1.4)
    v.chain([-8400, -4200, P1[1], P2[1], 0], "y", -300, -5, size=1.5)
    v.dim((CAN_Y1, FASCIA_TOP), (0, FASCIA_TOP), 5, size=1.5)
    v.leader([(-6000, 1200), (-6000, 2500), (-5500, 2700)], ["Existing boundary wall: repair render, 2 coats",
                                                            "masonry paint; SS wires 3 mm @ 400 (A-104)"], size=1.45)
    v.leader([(-1400, 2200), (-1400, 3600), (-900, 3700)], ["P2 post, jasmine trained on 4 SS wires"], size=1.45)
    v.leader([(-2800, FASCIA_TOP - 50), (-3600, 3700), (-4400, 3700)], ["Canopy E fascia, RAL 9010"], size=1.45,
             anchor="end")
    v.title(16, 122, "1/A-201", "ELEVATION B — PLANTER & BOUNDARY WALL (looking west)", "1:50 @ A3")

    # ---- ELEVATION C: model (u = -Y, Z), north to the left
    w = View(s, 40, 240, 50, dxf=dxf, dxf_offset=(30000, -30000))
    ground(w, -300, 8650, -65, depth=200)
    w.rect(-FAC_T, -65, FAC_T, FAC_PARAPET + 65, mat="masonry", w=0.4)
    # east house wall face
    w.rect(0, -65, EW_LEN, 4300, w=0.35, fill="#f7f3ea")
    break_line(w, 0, 4235, EW_LEN, 4235)
    w.text(EW_LEN / 2, 3700, "EXISTING HOUSE WALL — openings per survey (not shown)", size=1.4, anchor="middle",
           color="#777")
    ac_unit(w, -AC2[0], -AC2[1], AC2[2], AC2[3])
    w.rect(EW_LEN - 120, -65, 120, 4300, w=0.2, fill="#efe9dd")
    # screen + gate
    for a, b in SCR_POSTS:
        w.rect(-a, -65, a - b, SCR_H + 65, w=0.3, fill="#8a5a2b")
    lattice_panel(w, 5500, 6400, 50, SCR_H - 50, pitch=125, bar=38)
    lattice_panel(w, 6510, 7490, 60, SCR_H - 60, pitch=122, bar=38)
    lattice_panel(w, 7600, 8300, 50, SCR_H - 50, pitch=117, bar=38)
    w.rect(6510, 60, 980, SCR_H - 120, w=0.45, fill="none")
    w.text(7000, SCR_H + 120, "G01 gate", size=1.4, anchor="middle")
    # canopy cut (poche) + posts beyond hidden
    w.rect(0, FASCIA_BOT, -CAN_Y1, FASCIA_TOP - FASCIA_BOT, w=0.3, fill="#555")
    w.text(-CAN_Y1 / 2, FASCIA_BOT + 120, "CANOPY (cut at X = 1100) — see A-300", size=1.3, anchor="middle",
           color="#fff")
    # gullies
    for g in (G1, G2):
        w.rect(-g[1] - 150, LV_GULLY * 1000 - 300, 300, 300, w=0.2, dash="1,0.6", color="#1f5fa8")
    ladder(w, -300, [(0, "±0.000"), (SCR_H, "+1.800"), (SOFFIT, "+2.650"), (FASCIA_TOP, "+3.020"),
                     (FAC_PARAPET, "+3.400")], 14, size=1.4)
    w.chain([0, -G1[1], EW_LEN, -GATE[0], -GATE[1], 8400], "x", -400, -5, size=1.5)
    w.leader([(-AC2[0] - 200, AC2[2]), (2000, 2600), (2600, 2600)], ["AC outdoor unit (existing) — condensate",
                                                                     "to G1 in 20 mm PVC, chased"], size=1.45)
    w.leader([(5900, 1100), (5900, 2600), (6300, 2600)], ["G01: thermo-ash lattice screen h = 1800,",
                                                          "posts 100x100 on galv. post shoes — A-600"], size=1.45)
    w.title(16, 262, "2/A-201", "ELEVATION C — HOUSE WALL & SCREEN (looking east)", "1:50 @ A3")
    s.scale_bar(270, 268, 50)
    return s


# ======================================================================= A-300 SECTION A-A
def sheet_a300(dxf=None):
    s = Sheet("A-300", "Section A-A — canopy, door threshold & paving (N-S at X = 2600)", "1:20")
    s.frame()
    v = View(s, 225, 200, 20, dxf=dxf, dxf_offset=(0, -40000))
    zt = paving_level(2600) * 1000
    # --- ground & paving
    paving_cut(v, [(-3750, zt), (-200, zt), (-130, -15)], z_bottom_extra=320)
    # slot drain SD1 body
    sx0, sx1 = SD1[3], SD1[2]
    v.rect(sx0 - 100, -15 - 330, 100 + 100 + (sx1 - sx0), 330 - 15, w=0.2, mat="conc")
    v.rect(sx0, -15 - 230, sx1 - sx0, 230, w=0.25, mat="alu")
    v.rect(sx0 + 8, -15 - 222, sx1 - sx0 - 16, 200, w=0.1, fill="#fff")
    v.rect((sx0 + sx1) / 2 - 6, -15 - 22, 12, 22, w=0.1, fill="#fff")
    # existing internal floor & foundation
    v.rect(FAC_T, -70, 1000, 70, w=0.2, mat="sand")
    v.rect(FAC_T, -220, 1000, 150, w=0.25, mat="rc")
    v.rect(0, -900, FAC_T, 900 - 0, w=0.2, mat="masonry")
    v.rect(-150, -1100, 600, 250, w=0.2, dash="2,1", color="#666")
    v.text(150, -1050, "existing ftg (verify)", size=1.2, anchor="middle", color="#666")
    break_line(v, FAC_T + 1000, -250, FAC_T + 1000, 50)
    # threshold & door D01
    v.rect(90, -15, 120, 35, w=0.2, fill="#888")
    v.rect(120, 20, 60, HEAD - 70 - 20, w=0.15, fill="#5a4a3c")
    v.rect(140, 90, 20, HEAD - 70 - 160, w=0.12, mat="glass")
    v.rect(90, HEAD - 70, 120, 70, w=0.2, fill="#5a4a3c")
    # lintel / ring beam / slab / parapet
    v.rect(0, HEAD, FAC_T, SLAB_SOFFIT - HEAD, w=0.3, mat="rc")
    v.rect(0, SLAB_SOFFIT, FAC_T + 1000, SLAB_TOP - SLAB_SOFFIT, w=0.3, mat="rc")
    v.rect(0, SLAB_TOP, FAC_T, FAC_PARAPET - SLAB_TOP - 40, w=0.3, mat="masonry")
    v.rect(-30, FAC_PARAPET - 40, FAC_T + 60, 40, w=0.25, fill="#e8e3d8")
    v.rect(FAC_T, SLAB_TOP, 1000, 80, w=0.15, mat="insul")
    break_line(v, FAC_T + 1000, SLAB_SOFFIT - 80, FAC_T + 1000, SLAB_TOP + 160)
    v.rect(-12, 0, 12, HEAD, w=0.05, mat="render")
    # --- beyond (looking west): boundary wall, planter, posts, olive
    v.rect(-3750, 0, 3750, BW_TOP, w=0.12, fill="#fbf9f4", color="#999")
    v.rect(-3750, -5, 3750, COP_TOP - COP_T + 5, w=0.18, mat="render", color="#777")
    v.rect(-3750, COP_TOP - COP_T, 3750, COP_T, w=0.18, fill="#efe9dd", color="#777")
    for i, (y, w_, h_) in enumerate(((-3500, 500, 600), (-2600, 650, 800), (-2100, 500, 500), (-900, 550, 700),
                                      (-450, 400, 1100))):
        shrub(v, y, COP_TOP - 10, w_, h_, seed=60 + i, flowers=4, fill="#eef5e8", color="#8aa97a")
    for (x, y) in (P1, P2):
        v.rect(y - POST_CLAD / 2, COP_TOP, POST_CLAD, SOFFIT - COP_TOP, w=0.25, fill="#efd9b8", color="#8a5a2b")
    olive_elev(v, -650, zt, h=1900, seed=9)
    # --- canopy
    # joist beyond (seen) at X=2319
    v.rect(-3000, BOS, 3000 - 75, 200, w=0.15, fill="#e6eaee", color="#666")
    v.text(-1500, BOS + 80, "J1 lipped C200 beyond (@ 556 c/c)", size=1.4, anchor="middle", color="#444")
    # firring (seen) on joist
    v.pl([(-75, TOS), (-2995, TOS), (-2995, TOS + 20), (-75, TOS + 70)], w=0.12, mat="timber")
    # ply deck cut + membrane
    v.pl([(-2995, TOS + 20), (-20, TOS + 70), (-20, TOS + 88), (-2995, TOS + 38)], w=0.18, fill="#d9b98a")
    v.pl([(-2995, TOS + 38), (-20, TOS + 88), (-20, 3150)], w=0.45, closed=False, color="#111")
    # counter flashing
    v.pl([(0, 3170), (-40, 3150), (-40, 3080)], w=0.35, closed=False, color="#7f8c8d")
    # ledger
    upn200(v, 0, BOS, facing=-1)
    for z in (BOS + 60, BOS + 140):
        v.line(0, z, 140, z, w=0.3, color="#333")
    # B1 cut
    rhs(v, B1_Y[1], BOS, 100, 200, 6.3)
    # gutter
    zg = GUTTER_SOLE_W + (GUTTER_SOLE_E - GUTTER_SOLE_W) * (2600 - J_X0) / (J_X1 - J_X0)
    v.rect(-3115, TOS + 8, 125, zg - TOS - 8 - 18, w=0.1, mat="timber")
    v.rect(-3115, zg - 18, 125, 18, w=0.15, fill="#d9b98a")
    v.rect(-3133, TOS, 18, 3000 - TOS, w=0.15, fill="#d9b98a")
    v.pl([(-2995, TOS + 38), (-2995, zg), (-3115, zg), (-3115, 3000), (-3133, 3000)], w=0.45, closed=False,
         color="#111")
    # fascia (alu) + sub-frame
    v.pl([(-3090, FASCIA_BOT), (-3150, FASCIA_BOT), (-3150, FASCIA_TOP), (-3100, FASCIA_TOP - 5),
          (-3100, FASCIA_TOP - 25)], w=0.5, closed=False, color="#1b1b1b")
    v.rect(-3147, FASCIA_BOT + 40, 40, 40, w=0.12, fill="#aaa")
    # soffit battens (seen) + slats (cut)
    v.rect(-3090, SOFFIT + SLAT_T, 3030, BOS - SOFFIT - SLAT_T, w=0.12, fill="#c9a77c", color="#7a5a3a")
    soffit_slats_cut(v, -40, -3080)
    # LED profile
    v.rect(-2935, SOFFIT, 25, 22, w=0.2, fill="#f39c12")
    # vertical scale dims
    ladder(v, 1300, [(0, "±0.000 FFL int."), (HEAD, "+2.400 head"), (SOFFIT, "+2.650 soffit"), (BOS, "+2.710 BOS"),
                     (TOS, "+2.910 TOS"), (SLAB_SOFFIT, "+2.950 slab sof. (survey)"),
                     (DECK_HI, "+2.998 deck high"), (SLAB_TOP, "+3.150 slab (survey)"),
                     (FAC_PARAPET, "+3.400 parapet")], 294, size=1.35, inside=False)
    ladder(v, -3750, [(zt, f"{zt / 1000:+.3f} paving"), (COP_TOP, "+0.400 coping"), (BW_TOP, "+1.800 wall"),
                      (DECK_LO, "+2.948 deck low"), (FASCIA_TOP, "+3.020 fascia")], 15, size=1.35)
    v.chain([CAN_Y1, P1[1], P2[1], 0], "x", -700, -4, size=1.4)
    v.dim((CAN_Y1, FASCIA_TOP), (0, FASCIA_TOP), 22, size=1.5)
    v.chain([CAN_Y1, B1_Y[1], B1_Y[0]], "x", FASCIA_TOP, 16, size=1.3, overall=False)
    v.dim((SD1[3], -15), (SD1[2], -15), 4, size=1.3)
    # callouts (left & top)
    C = [
        ((-1600, TOS + 54), (-1900, 3480), ["1.5 mm TPO membrane / 18 mm marine ply / tapered firrings 70→20 (1:60)"]),
        ((-3050, zg), (-3300, 3330), ["Box gutter 120 x 80, TPO lined, falls 1:200 W to O1"]),
        ((-3150, 2850), (-3500, 3180), ["3 mm alu fascia RAL 9010, alu angle sub-frame"]),
        ((-3050, BOS + 100), (-3500, 2450), ["B1 RHS 200x100x6.3"]),
        ((-2922, SOFFIT), (-2800, 2350), ["LS1 LED profile 25x20 recessed"]),
        ((-1800, SOFFIT + 10), (-1500, 2200), ["68x20 thermo-ash slats, 10 gaps, on 50x38 battens to J1"]),
        ((-40, BOS + 100), (-900, 2050), ["L1 UPN 200 ledger, M12 resin anchors @ 400 stagg."]),
        ((-40, 3110), (500, 3600), ["Membrane up 150, alu counter-flashing chased & sealed"]),
        ((150, 1200), (700, 1300), ["D01 (existing opening)"]),
        ((-80, -40), (500, -500), ["SD1 slot drain 100, polymer concrete, C20 surround"]),
        ((-1000, zt - 30), (-1300, -600), ["60 pavers / 30 sand / 150 Type 1 / geotextile"]),
        ((-1400, 1500), (-1300, 1700), ["P2 / P1 beyond (in planter)"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.4)
    v.title(28, 262, "1/A-300", "SECTION A-A", "1:20 @ A3", sub="through D01, canopy & slot drain, looking west")
    s.scale_bar(240, 268, 20, 2)
    return s


# ======================================================================= A-301 SECTION B-B
def sheet_a301(dxf=None):
    s = Sheet("A-301", "Section B-B — planter, canopy & courtyard (E-W at Y = -2200)", "1:25")
    s.frame()
    v = View(s, 40 + 300 / 25, 190, 25, dxf=dxf, dxf_offset=(30000, -40000))
    # façade beyond
    v.rect(0, 0, COURT_W, FAC_PARAPET, w=0.15, fill="#fbf9f4", color="#999")
    door_elev(v, "D01", *D01)
    door_elev(v, "D02", *D02)
    door_elev(v, "D03", *D03)
    ac_unit(v, *AC1)
    v.rect(WL1[0] - 50, WL1[1] - 120, 100, 240, w=0.2, fill="#5a4a3c")
    olive_elev(v, 1400, LV_KERB * 1000, h=1900, seed=73)
    pts = [(PAV_X0, LV_KERB * 1000), (6450, paving_level(6450) * 1000), (6750, paving_level(6750) * 1000),
           (PAV_X1, LV_EASTWALL * 1000)]
    paving_cut(v, [pts[0], pts[1]], z_bottom_extra=420)
    paving_cut(v, [pts[2], pts[3]], z_bottom_extra=420)
    # gully G1 cut
    gz = LV_GULLY * 1000
    v.rect(6300, gz - 750, 600, 700, w=0.2, mat="conc")
    v.rect(6450, gz - 600, 300, 600, w=0.25, fill="#cfd6dc")
    v.rect(6470, gz - 580, 260, 560, w=0.1, fill="#fff")
    v.rect(6450, gz - 20, 300, 20, w=0.2, fill="#555")
    v.rect(6750, gz - 520, 450, 110, w=0.2, fill="#9aa3ab")
    v.text(6600, gz - 330, "G1", size=1.6, anchor="middle", weight="bold")
    # boundary wall cut + neighbour ground
    v.rect(-BW_T, -700, BW_T, BW_TOP + 700, mat="masonry", w=0.45)
    v.rect(-BW_T - 25, BW_TOP, BW_T + 50, 50, w=0.3, fill="#e8e3d8")
    v.rect(-BW_T - 100, -1000, BW_T + 200, 300, w=0.15, dash="2,1", color="#666")
    v.pl([(-300, -100), (-BW_T, -100), (-BW_T, -700), (-300, -700)], w=0, mat="earth")
    # planter
    v.rect(0, -300, KERB_X0, 100, w=0.15, mat="gravel")
    v.rect(10, -200, KERB_X0 - 10, SOIL_TOP - 50 + 200, w=0.15, mat="soil")
    v.rect(10, SOIL_TOP - 50, KERB_X0 - 10, 50, w=0.15, fill="#8b6b4a")
    v.rect(0, -300, 10, SOIL_TOP + 300, w=0.05, fill="#111")
    v.pl([(0, -700), (KERB_X0, -700), (KERB_X0, -300), (0, -300)], w=0, mat="earth")
    v.rect(KERB_X0 - 75, KERB_FTG_BOT, KERB_FTG_W, KERB_FTG_D, w=0.3, mat="rc")
    v.rect(KERB_X0, KERB_FTG_BOT + KERB_FTG_D, KERB_T - 15, COP_TOP - COP_T - KERB_FTG_BOT - KERB_FTG_D, w=0.3,
           mat="rc")
    v.rect(KERB_X1 - 15, -90, 15, COP_TOP - COP_T + 90, w=0.1, mat="render")
    v.rect(COP_X0, COP_TOP - COP_T, COP_X1 - COP_X0, COP_T, w=0.3, mat="conc")
    shrub(v, 380, SOIL_TOP, 650, 700, seed=71, flowers=6)
    vine(v, 30, SOIL_TOP, BW_TOP, seed=72, amp=25)
    # P2 beyond (Y=-1400)
    v.rect(P2[0] - POST_CLAD / 2, SOIL_TOP, POST_CLAD, SOFFIT - SOIL_TOP, w=0.25, fill="#efd9b8", color="#8a5a2b")
    # east wall cut
    v.rect(COURT_W, -900, 150, 4500, mat="masonry", w=0.45)
    break_line(v, COURT_W, 3600, COURT_W + 150, 3600)
    break_line(v, COURT_W + 150, -900, COURT_W + 150, 3600)
    # canopy cut
    yc = -2200
    fir = 70 - 50 * (abs(yc) - 75) / 2925
    deck = TOS + fir + 18
    rhs(v, B3_X[0], BOS, 100, 200, 5)
    v.rect(B2_X[0], BOS, 200, 200, w=0.2, mat="steel")
    v.rect(B2_X[0] + 12.5, BOS + 12.5, 175, 175, w=0.12, fill="#fff")
    for x in JOISTS:
        cchan(v, x, BOS, facing=1)
    for x in [B3_X[0] + 50] + JOISTS + [B2_X[0] + 100]:
        v.rect(x - 22, TOS, 45, fir, w=0.1, mat="timber")
        v.rect(x - 25, SOFFIT + SLAT_T, 50, BOS - SOFFIT - SLAT_T, w=0.1, mat="timber")
    v.rect(B3_X[0], TOS + fir, B2_X[1] - B3_X[0], 18, w=0.15, fill="#d9b98a")
    v.line(B3_X[0], deck + 2, B2_X[1], deck + 2, w=0.45, color="#111")
    v.rect(560, SOFFIT, 4780, SLAT_T, w=0.12, mat="timber")
    for x in (CAN_X0, CAN_X1 - 3):
        v.rect(x, FASCIA_BOT, 3, FASCIA_TOP - FASCIA_BOT, w=0.35, fill="#222")
    v.line(CAN_X0, FASCIA_TOP, CAN_X0 + 70, FASCIA_TOP - 7, w=0.4)
    v.line(CAN_X1, FASCIA_TOP, CAN_X1 - 70, FASCIA_TOP - 7, w=0.4)
    for x in (CAN_X0 + LED_INSET - 12, CAN_X1 - LED_INSET - 12):
        v.rect(x, SOFFIT, 25, 22, w=0.15, fill="#f39c12")
    ladder(v, -300, [(LV_KERB * 1000, f"{LV_KERB:+.3f}"), (COP_TOP, "+0.400 coping"), (BW_TOP, "+1.800 wall"),
                     (HEAD, "+2.400 heads"), (SOFFIT, "+2.650 soffit"), (TOS, "+2.910 TOS"),
                     (FASCIA_TOP, "+3.020 fascia"), (FAC_PARAPET, "+3.400 parapet")], 14.5, size=1.35)
    v.chain([-BW_T, 0, KERB_X0, KERB_X1, G1[0], COURT_W], "x", -1000, -4, size=1.4)
    v.chain([CAN_X0, P1[0]] + [round(x) for x in JOISTS] + [P3[0], CAN_X1], "x", FASCIA_TOP, 8, size=1.2,
            overall=True)
    C = [
        ((300, 100), (1700, -700), ["Planter: 50 mulch / 450 topsoil / geotextile / 100 drainage gravel, open base"]),
        ((5, 600), (1700, 1500), ["Tanking slurry + 8 mm HDPE drainage sheet on wall"]),
        ((900, 150), (1700, 600), ["150 RC kerb on 450x250 strip ftg — see C-C"]),
        ((3000, BOS + 100), (2800, 3700), ["J1 lipped C200x65x1.8 @ 556 c/c — S-100"]),
        ((5200, BOS + 100), (5600, 3650), ["B2 SHS 200x200x12.5 (S1) / RHS 200x100 (S2)"]),
        ((600, BOS + 100), (1100, 3850), ["B3 RHS 200x100x5"]),
        ((6600, gz - 300), (5500, -800), ["G1 yard gully 300, silt bucket, Ø110 outlet, C20 surround"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.4)
    v.title(24, 262, "1/A-301", "SECTION B-B", "1:25 @ A3", sub="through planter, canopy & gully G1, looking north")
    s.scale_bar(260, 268, 25, 2)
    return s


# ======================================================================= A-302 SECTION C-C + DRAINAGE DETAILS
def sheet_a302(dxf=None):
    s = Sheet("A-302", "Section C-C planter & paving / drainage details", "1:10")
    s.frame()
    v = View(s, 60, 175, 10, origin=(-400, 0), dxf=dxf, dxf_offset=(60000, -40000))
    # ground beyond
    v.pl([(-450, -100), (-BW_T, -100), (-BW_T, -750), (-450, -750)], w=0, mat="earth")
    v.rect(-BW_T, -750, BW_T, 950 + 750, mat="masonry", w=0.45)
    v.rect(-BW_T - 12, -100, 12, 1050, w=0.05, mat="render")
    break_line(v, -BW_T - 40, 950, 40, 950)
    # existing wall footing (dashed)
    v.rect(-400, -900, 550, 150, w=0.2, dash="2,1", color="#666")
    # planter fill
    v.pl([(0, -750), (KERB_X0 - 75, -750), (KERB_X0 - 75, -400), (0, -400)], w=0, mat="earth")
    v.rect(0, -400, KERB_X0, 100, w=0.15, mat="earth")
    v.rect(10, -300, KERB_X0 - 10, 100, w=0.2, mat="gravel")
    v.line(10, -200, KERB_X0, -200, w=0.35, dash="2,0.6", color="#7a5c3a")
    v.rect(10, -200, KERB_X0 - 10, SOIL_TOP - 50 + 200, w=0.2, mat="soil")
    v.rect(10, SOIL_TOP - 50, KERB_X0 - 10, 50, w=0.15, fill="#8b6b4a")
    v.rect(0, -300, 4, 950, w=0.05, fill="#111")
    v.rect(4, -300, 8, 950, w=0.05, fill="#555")
    # kerb
    v.rect(KERB_X0 - 75, KERB_FTG_BOT, KERB_FTG_W, KERB_FTG_D, w=0.35, mat="rc")
    v.rect(KERB_X0, KERB_FTG_BOT + KERB_FTG_D, KERB_T - 15, COP_TOP - COP_T - KERB_FTG_BOT - KERB_FTG_D - 10,
           w=0.35, mat="rc")
    v.rect(KERB_X0 - 4, -300, 4, COP_TOP - COP_T + 300 - 10, w=0.05, fill="#111")
    v.rect(KERB_X1 - 15, -90, 15, COP_TOP - COP_T + 90 - 10, w=0.15, mat="render")
    v.rect(COP_X0, COP_TOP - COP_T - 10, COP_X1 - COP_X0, 10, w=0.1, fill="#999")
    v.pl([(COP_X0, COP_TOP - COP_T), (COP_X1, COP_TOP - COP_T), (COP_X1, COP_TOP - 5), (COP_X1 - 5, COP_TOP),
          (COP_X0, COP_TOP)], w=0.35, mat="conc")
    v.line(COP_X1 - 20, COP_TOP - COP_T, COP_X1 - 20, COP_TOP - COP_T + 8, w=0.3)  # drip
    # rebar
    for z in (KERB_FTG_BOT + 50,):
        for x in (KERB_X0 - 20, KERB_X0 + 75, KERB_X0 + 170):
            v.circle(x, z, 6, w=0.1, fill="#000")
    v.pl([(KERB_X0 + 70, KERB_FTG_BOT + 50), (KERB_X0 + 70, COP_TOP - COP_T - 40)], w=0.3, closed=False)
    v.pl([(KERB_X0 + 70, KERB_FTG_BOT + 50), (KERB_X0 - 40, KERB_FTG_BOT + 50)], w=0.3, closed=False)
    v.circle(KERB_X0 + 50, COP_TOP - COP_T - 60, 5, w=0.1, fill="#000")
    v.circle(KERB_X0 + 50, -250, 5, w=0.1, fill="#000")
    # paving
    paving_cut(v, [(KERB_X1, LV_KERB * 1000), (1400, LV_KERB * 1000 - 5)], z_bottom_extra=300)
    break_line(v, 1400, -600, 1400, 40)
    # drip line & uplight cable
    v.circle(230, SOIL_TOP - 60, 8, w=0.2, fill="#1f5fa8")
    v.circle(600, SOIL_TOP - 60, 8, w=0.2, fill="#1f5fa8")
    v.circle(420, -60, 12, w=0.2, fill="#fff")
    shrub(v, 400, SOIL_TOP, 600, 550, seed=81, flowers=6)
    for z in (600,):
        v.circle(-4 - 25, z, 4, w=0.15, fill="#999")
        v.line(-4, z, -60, z, w=0.3, color="#555")
    C = [
        ((COP_X0 + 100, COP_TOP), (1150, 700), ["Precast reconstituted-stone coping 230x60, cream, 10 mm",
                                                "drip groove, bedded M12 mortar on DPC; joints 5 mm sealed"]),
        ((KERB_X0 + 70, 100), (1150, 280), ["150 RC upstand C30/37 (135 + 15 render), Ø10 @ 300 vert.",
                                            "+ 2 Ø10 horiz. top / mid; cover 40; MJ @ 4.2 m dowelled"]),
        ((KERB_X0 + 100, KERB_FTG_BOT + 120), (1150, -480), ["Strip footing 450x250 C25/30, 3 Ø12 B,",
                                                             "on 50 blinding, formation -0.650 min"]),
        ((KERB_X0 - 2, 0), (1150, -180), ["2 coats flexible cementitious tanking slurry to inner face"]),
        ((KERB_X1 - 7, 150), (1150, 80), ["2 coat render 15 mm, sand/cement 1:4, masonry paint (cream)"]),
        ((450, SOIL_TOP - 25), (-200, 850), ["50 composted bark mulch to +0.340"]),
        ((450, 100), (-430, 520), ["Topsoil 450 (BS 3882) + 25% compost"]),
        ((450, -200), (-430, 380), ["Non-woven geotextile 150 g/m²"]),
        ((450, -260), (-430, 240), ["100 clean gravel 10–20 mm"]),
        ((420, -400), (-430, -560), ["Existing subsoil loosened 300 — free-draining base"]),
        ((8, 350), (-430, 690), ["HDPE 8 mm dimpled drainage sheet + bitumen-free slurry on wall"]),
        ((230, SOIL_TOP - 60), (-430, 120), ["16 mm drip line x2 (A-104)"]),
        ((420, -60), (-430, -40), ["25 duct for 12 V uplight cable"]),
        ((-30, 600), (-430, 980), ["SS wire 3 mm on 40 stand-off eye, M8 resin anchor"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.4, maxw=30 if txt[0] > 1000 else None)
    ladder(v, 1400, [(COP_TOP, "+0.400"), (SOIL_TOP, "+0.340 soil"), (LV_KERB * 1000, f"{LV_KERB:+.3f} paving"),
                     (KERB_FTG_BOT, "-0.650 u/s ftg")], 243, size=1.4, inside=False)
    v.chain([-BW_T, 0, KERB_X0, KERB_X1, 1400], "x", -750, -6, size=1.5, overall=False)
    v.chain([KERB_FTG_BOT, KERB_FTG_BOT + KERB_FTG_D, -300, -200, SOIL_TOP, COP_TOP], "y", -BW_T, 22, size=1.4,
            overall=False)
    v.title(22, 262, "1/A-302", "SECTION C-C — RAISED PLANTER", "1:10 @ A3", sub="at Y = -5000, looking north")

    # ---- D-SD1 threshold slot drain 1:10 (u = Y)
    w = View(s, 296, 62, 10, dxf=None)
    paving_cut(w, [(-420, -18), (-140, -15)], z_bottom_extra=150)
    w.rect(-240, -360, 260, 345, w=0.2, mat="conc")
    w.rect(-130, -260, 100, 245, w=0.25, mat="alu")
    w.rect(-122, -252, 84, 220, w=0.1, fill="#fff")
    w.rect(-86, -40, 12, 25, w=0.1, fill="#fff")
    w.rect(0, -400, 300, 400, w=0.2, mat="rc")
    w.rect(0, -400, 300, 400, w=0.2, mat="masonry")
    w.rect(20, -15, 120, 35, w=0.2, fill="#888")
    w.rect(60, 20, 60, 380, w=0.15, fill="#5a4a3c")
    w.rect(300, -70, 120, 70, w=0.2, mat="sand")
    w.rect(300, -220, 120, 150, w=0.2, mat="rc")
    w.rect(-12, -400, 12, 400, w=0.05, fill="#111")
    w.leader([(-80, -15), (-300, 300)], ["Slot drain SD1, 100 polymer", "concrete, SS slot 12, B125"], size=1.3,
             anchor="start")
    w.leader([(-180, -300), (-420, -470)], ["C20/25 bed & haunch 100"], size=1.3, anchor="start")
    w.leader([(-6, -200), (60, -470)], ["Tanking 300 up wall"], size=1.3)
    w.leader([(80, 2), (150, 250)], ["Level threshold ≤ 15"], size=1.3)
    w.dim((-130, -260), (-30, -260), -4, size=1.3)
    s.text(250, 16, "2/A-302  THRESHOLD SLOT DRAIN SD1 — 1:10", size=2.0, weight="bold")

    # ---- gully detail 1:10
    g = View(s, 292, 128, 10, dxf=None)
    paving_cut(g, [(-420, -80), (-150, -85)], z_bottom_extra=200, joints=False)
    paving_cut(g, [(150, -85), (420, -80)], z_bottom_extra=200, joints=False)
    g.rect(-300, -850, 600, 770, w=0.2, mat="conc")
    g.rect(-150, -700, 300, 615, w=0.25, fill="#cfd6dc")
    g.rect(-130, -680, 260, 575, w=0.1, fill="#fff")
    g.rect(-110, -500, 220, 380, w=0.15, dash="1.5,0.8", color="#555")
    g.rect(-150, -105, 300, 20, w=0.2, fill="#444")
    g.rect(150, -560, 270, 110, w=0.2, fill="#9aa3ab")
    g.leader([(0, -95), (-150, 100)], ["300x300 grate B125, DI / SS"], size=1.3, anchor="start")
    g.leader([(0, -400), (60, -250)], ["Silt bucket"], size=1.3)
    g.leader([(300, -500), (230, -700)], ["Ø110 outlet"], size=1.3)
    g.leader([(-250, -800), (-150, -900)], ["C20/25 surround 150"], size=1.3, anchor="start")
    s.text(250, 110, "3/A-302  YARD GULLY G1 / G2 — 1:10", size=2.0, weight="bold")

    # ---- paving edge restraint 1:10
    e = View(s, 288, 240, 10, dxf=None)
    paving_cut(e, [(-420, -110), (0, -115)], z_bottom_extra=150)
    e.rect(0, -265, 50, 265 - 115 + 10, w=0.25, mat="conc")
    e.pl([(-100, -265), (150, -265), (150, -150), (50, -100), (50, -265)], w=0.15, mat="conc")
    e.rect(-100, -340, 250, 75, w=0.2, mat="conc")
    e.pl([(150, -105), (420, -105), (420, -300), (150, -300)], w=0, mat="grass")
    e.leader([(25, -120), (-400, 80)], ["PCC edging 50x150 on C20 bed & haunch, flush (S edge)"],
             size=1.3, anchor="start")
    s.text(250, 222, "4/A-302  SOUTH EDGE RESTRAINT — 1:10", size=2.0, weight="bold")
    s.scale_bar(150, 270, 10, 1)
    return s
