"""Construction details & doors (Design A)."""
import math
from cad import Sheet, View, break_line
from common import *  # noqa
from design import *  # noqa
from sheets_b import ladder, paving_cut, rhs, upn200, soffit_slats_cut, cchan


def bolt(v, x, z, horiz=True, L=60, d=12):
    if horiz:
        v.rect(x - L / 2, z - d / 2, L, d, w=0.12, fill="#888")
        v.rect(x - L / 2 - 4, z - d, 8, 2 * d, w=0.12, fill="#555")
        v.rect(x + L / 2 - 4, z - d, 8, 2 * d, w=0.12, fill="#555")
    else:
        v.rect(x - d / 2, z - L / 2, d, L, w=0.12, fill="#888")
        v.rect(x - d, z + L / 2 - 4, 2 * d, 8, w=0.12, fill="#555")
        v.rect(x - d, z - L / 2 - 4, 2 * d, 8, w=0.12, fill="#555")


# ======================================================================= A-500 DETAILS 1
def sheet_a500(dxf=None):
    s = Sheet("A-500", "Details 1 — post base, canopy corner, eave/gutter & façade junction", "1:10 / 1:5")
    s.frame()
    # ---------------- D1 post base & footing 1:10 (X-Z looking north at P1)
    v = View(s, 16, 120, 10, origin=(150, 0), dxf=dxf, dxf_offset=(0, -60000))
    ped_top = PED_TOP - 30
    ztop = 900
    v.pl([(150, -1000), (1150, -1000), (1150, -200), (150, -200)], w=0, mat="earth")
    v.rect(150, -200, KERB_X0 - 150, SOIL_TOP + 200, w=0, mat="soil")
    v.rect(150, SOIL_TOP - 50, KERB_X0 - 150, 50, w=0, fill="#8b6b4a")
    v.rect(200, FTG_BOT, FTG, FTG_D, w=0.4, mat="rc")
    v.rect(150, FTG_BOT - 50, 900, 50, w=0.2, mat="conc")
    for x in range(260, 1000, 75):
        v.circle(x, FTG_BOT + 60, 6, w=0.1, fill="#000")
    v.line(240, FTG_BOT + 72, 960, FTG_BOT + 72, w=0.35)
    v.rect(450, FTG_BOT + FTG_D, 300, ped_top - (FTG_BOT + FTG_D), w=0.4, mat="rc")
    for x in (490, 710):
        v.line(x, FTG_BOT + 80, x, ped_top - 40, w=0.35)
        v.line(x, FTG_BOT + 80, x + (100 if x < 600 else -100), FTG_BOT + 80, w=0.35)
    for z in range(FTG_BOT + FTG_D + 50, ped_top - 30, 150):
        v.rect(480, z, 240, 0.01, w=0.25)
    v.rect(KERB_X0, FTG_BOT + FTG_D, KERB_T, COP_TOP - COP_T - (FTG_BOT + FTG_D), w=0.35, mat="rc")
    v.rect(1000, KERB_FTG_BOT, 150, KERB_FTG_D, w=0.3, mat="rc")
    v.pl([(COP_X0, COP_TOP - COP_T), (COP_X1, COP_TOP - COP_T), (COP_X1, COP_TOP), (COP_X0, COP_TOP)], w=0.3,
         mat="conc")
    paving_cut(v, [(1000, -5), (1150, -6)], z_bottom_extra=150, joints=False)
    v.rect(475, ped_top, 250, 30, w=0.2, mat="grout")
    v.rect(475, PED_TOP, 250, 15, w=0.3, mat="steel")
    v.rect(540, PED_TOP + 15, 120, ztop - PED_TOP - 15, w=0.3, fill="#5c6670")
    v.rect(546, PED_TOP + 15, 108, ztop - PED_TOP - 15, w=0.1, fill="#fff")
    v.rect(520, PED_TOP + 45, 20, ztop - PED_TOP - 45, w=0.15, mat="timber")
    v.rect(660, PED_TOP + 45, 20, ztop - PED_TOP - 45, w=0.15, mat="timber")
    break_line(v, 500, ztop, 700, ztop)
    for x in (510, 690):
        v.rect(x - 8, ped_top - 400, 16, 400 + 15 + 30 + 25, w=0.12, fill="#888")
        v.rect(x - 8, ped_top - 400, (60 if x < 600 else -60), 16, w=0.12, fill="#888")
        v.rect(x - 14, PED_TOP + 15, 28, 14, w=0.12, fill="#444")
    v.rect(562, PED_TOP - 20, 76, ztop - PED_TOP + 20, w=0.15, dash="2,1", color="#1f5fa8")
    v.pl([(545, ped_top), (545, -245), (600, -355), (1150, -355), (1150, -245), (655, -245), (655, ped_top)],
         w=0.25, color="#1f5fa8", fill="#dbe7f3")
    v.text(900, -315, "Ø110 PVC-U", size=1.3, anchor="middle", color="#1f5fa8")
    C = [
        ((600, 800), (760, 860), ["P1 SHS 120x120x6.3 S355, HDG"]),
        ((530, 700), (760, 780), ["20 thermo-ash cladding"]),
        ((600, 600), (760, 700), ["Ø75 PVC-U RWP (P1 only)"]),
        ((700, PED_TOP + 8), (760, 600), ["PL 250x250x15, 6 FW"]),
        ((690, ped_top + 15), (760, 520), ["30 non-shrink grout"]),
        ((690, 100), (880, 160), ["4 M16 8.8 HDG cast-in,", "400 emb., L-hook"]),
        ((600, 0), (380, -60), ["Pedestal 300x300", "4 Ø12 + Ø8 @ 150"]),
        ((600, -600), (380, -700), ["F1 pad 800x800x700", "C25/30, Ø12 @ 150 BW"]),
        ((600, FTG_BOT - 25), (380, -1080), ["50 blinding C12/15"]),
        ((900, 200), (950, 60), ["Kerb on pad"]),
    ]
    for tgt, txt, lines in C:
        v.leader([tgt, txt], lines, size=1.25, anchor="start" if txt[0] >= tgt[0] else "end")
    v.chain([200, 450, 750, 1000], "x", FTG_BOT, -10, size=1.3)
    v.chain([FTG_BOT, FTG_BOT + FTG_D, ped_top, PED_TOP], "y", 200, 6, size=1.2, overall=False)
    s.text(16, 16, "D1  POST BASE & PAD FOOTING F1/F2 — 1:10", size=1.9, weight="bold")
    s.text(16, 20, "P2 identical without RWP; P3 (ALT S2) identical", size=1.35)

    # ---------------- D2 corner plan at P1 1:5
    w = View(s, 128 + (600 - 430) / 5, 77, 5, origin=(600, -3050), dxf=None)
    w.rect(430, -3115, 470, 120, w=0.15, dash="1.5,0.8", color="#1f5fa8")
    w.rect(P1[0] - 60, P1[1] - 60, 120, 120, w=0.3, fill="#5c6670")
    w.rect(P1[0] - 53.7, P1[1] - 53.7, 107.4, 107.4, w=0.1, fill="#fff")
    w.circle(P1[0], P1[1], 37.5, w=0.25, fill="#dbe7f3", color="#1f5fa8")
    w.circle(P1[0], P1[1], 31.5, w=0.25, color="#1f5fa8")
    w.rect(670, -3100, 230, 100, w=0.3, fill="#5c6670")
    w.rect(676, -3094, 224, 88, w=0.1, fill="#fff")
    w.rect(660, -3056, 90, 12, w=0.2, fill="#333")
    w.rect(550, -2990, 100, 190, w=0.3, fill="#5c6670")
    w.rect(555, -2985, 90, 185, w=0.1, fill="#fff")
    w.rect(594, -2990, 12, 80, w=0.2, fill="#333")
    for x in (700, 735):
        w.circle(x, -3050, 8, w=0.15, fill="#999")
    for y in (-2965, -2930):
        w.circle(600, y, 8, w=0.15, fill="#999")
    w.pl([(500, -2800), (500, -3150), (900, -3150)], w=0.6, closed=False)
    w.line(LED_INSET + CAN_X0, -2800, LED_INSET + CAN_X0, CAN_Y1 + LED_INSET, w=0.5, color="#f39c12", dash="3,1")
    w.line(LED_INSET + CAN_X0, CAN_Y1 + LED_INSET, 900, CAN_Y1 + LED_INSET, w=0.5, color="#f39c12", dash="3,1")
    w.rect(520, -3130, 160, 160, w=0.15, dash="1,0.6", color="#8a5a2b")
    w.leader([(P1[0] - 20, P1[1] + 20), (460, -2830)], ["O1 outlet Ø63"], size=1.25, anchor="end")
    w.leader([(705, -3050), (800, -2860)], ["FP 12 welded to post,", "slotted B1, 2 M16 8.8"], size=1.25)
    w.leader([(600, -2930), (680, -2810)], ["FP 12 → B3, 2 M16"], size=1.25)
    w.leader([(860, CAN_Y1 + LED_INSET), (870, -2990)], ["LED c/l"], size=1.25)
    w.chain([500, 550, 600, 650, LED_INSET + CAN_X0], "x", CAN_Y1, -5, size=1.15, overall=False)
    w.chain([CAN_Y1, -3100, -3050, -3000, CAN_Y1 + LED_INSET], "y", 500, 7, size=1.15, overall=False)
    s.text(124, 16, "D2  CANOPY CORNER AT P1 — PLAN @ TOS — 1:5", size=1.9, weight="bold")

    # ---------------- D3 front eave / gutter / LED 1:5 (u = Y, looking west)
    e = View(s, 138, 232, 5, origin=(-3200, 2560), dxf=None)
    zg = 2934
    e.rect(-3000, BOS, 170, 200, w=0.12, fill="#e6eaee", color="#777")
    e.pl([(-2830, TOS), (-2995, TOS), (-2995, TOS + 20), (-2830, TOS + 23)], w=0.12, mat="timber")
    e.pl([(-2995, TOS + 20), (-2830, TOS + 23), (-2830, TOS + 41), (-2995, TOS + 38)], w=0.18, fill="#d9b98a")
    rhs(e, B1_Y[1], BOS, 100, 200, 6.3)
    e.rect(-3010, BOS + 40, 10, 120, w=0.15, fill="#333")
    e.rect(-3115, TOS + 8, 125, zg - TOS - 8 - 18, w=0.12, mat="timber")
    e.rect(-3115, zg - 18, 125, 18, w=0.15, fill="#d9b98a")
    e.rect(-3133, TOS - 40, 18, 3000 - TOS + 40, w=0.15, fill="#d9b98a")
    e.pl([(-2830, TOS + 43), (-2995, TOS + 40), (-2995, zg), (-3115, zg), (-3115, 3000), (-3133, 3000)], w=0.5,
         closed=False, color="#111")
    e.pl([(-3085, FASCIA_BOT + 10), (-3085, FASCIA_BOT), (-3150, FASCIA_BOT), (-3150, FASCIA_TOP),
          (-3095, FASCIA_TOP - 6), (-3095, FASCIA_TOP - 30)], w=0.55, closed=False, color="#1b1b1b")
    for z in (2700, 2900):
        e.pl([(-3147, z), (-3107, z), (-3107, z + 3), (-3144, z + 3), (-3144, z + 40), (-3147, z + 40)], w=0.12,
             fill="#999")
        bolt(e, -3104, z + 20, L=20, d=8)
    e.rect(-3090, SOFFIT + SLAT_T, 260, BOS - SOFFIT - SLAT_T, w=0.12, fill="#c9a77c", color="#7a5a3a")
    soffit_slats_cut(e, -2830, -3090)
    e.rect(-2935, SOFFIT, 25, 22, w=0.25, fill="#d0d5da")
    e.rect(-2933, SOFFIT, 21, 3, w=0.1, fill="#fff8e1")
    e.rect(-2930, SOFFIT + 8, 15, 3, w=0.1, fill="#f39c12")
    e.line(-3090, SOFFIT + SLAT_T + 1, -2830, SOFFIT + SLAT_T + 1, w=0.2, color="#222", dash="1,0.5")
    C = [
        ((-3150, 2980), (-3195, 3160), ["3 mm alu fascia RAL 9010 + capping, 10% fall in"]),
        ((-3060, zg), (-3195, 3135), ["Gutter: TPO on 18 ply sole on tapered packers"]),
        ((-2900, TOS + 32), (-3195, 3110), ["Deck: TPO / 18 ply / firring on J1"]),
        ((-3050, 2800), (-3195, 2540), ["B1 RHS 200x100x6.3"]),
        ((-3125, 2720), (-3195, 2515), ["Alu angle 40x40x3 @ 600, M8 SS to B1"]),
        ((-2922, SOFFIT + 10), (-3195, 2490), ["LED profile 25x22 + opal diffuser"]),
        ((-3005, BOS + 100), (-2880, 2800), ["J1 fin plate"]),
    ]
    for tgt, txt, lines in C:
        e.leader([tgt, txt], lines, size=1.2, anchor="start")
    e.dim((-3150, FASCIA_BOT), (-3150, FASCIA_TOP), 4, size=1.2)
    e.dim((-3115, 3000), (-2995, 3000), 3, size=1.15)
    s.text(124, 104, "D3  FRONT EAVE — GUTTER, FASCIA & LED — 1:5", size=1.9, weight="bold")
    s.text(124, 108, "section at gutter, looking west (W/E fascia: D9/A-501)", size=1.3)

    # ---------------- D4 façade junction 1:5 (u = Y)
    f = View(s, 236 + 290 / 5, 186, 5, origin=(0, 2550), dxf=None)
    f.rect(0, 2420, 220, SLAB_SOFFIT - 2420, w=0.4, mat="rc")
    f.rect(0, SLAB_SOFFIT, 220, SLAB_TOP - SLAB_SOFFIT, w=0.4, mat="rc")
    f.rect(0, SLAB_TOP, 220, 3300 - SLAB_TOP, w=0.4, mat="masonry")
    f.rect(-12, 2420, 12, 880, w=0.05, mat="render")
    break_line(f, 220, 2420, 220, 3300)
    upn200(f, 0, BOS, facing=-1)
    for z in (BOS + 60, BOS + 140):
        f.rect(-10, z - 6, 135, 12, w=0.12, fill="#888")
        f.rect(-22, z - 12, 10, 24, w=0.12, fill="#444")
    f.rect(-290, BOS, 215, 200, w=0.12, fill="#e6eaee", color="#777")
    f.rect(-200, BOS + 30, 120, 140, w=0.15, fill="#bbb")
    bolt(f, -150, BOS + 70, horiz=False, L=30, d=12)
    bolt(f, -150, BOS + 130, horiz=False, L=30, d=12)
    f.pl([(-290, TOS), (-75, TOS), (-75, TOS + 70), (-290, TOS + 66)], w=0.12, mat="timber")
    f.pl([(-290, TOS + 66), (-20, TOS + 70), (-20, TOS + 88), (-290, TOS + 84)], w=0.18, fill="#d9b98a")
    f.rect(-20, TOS + 20, 18, 160, w=0.12, fill="#d9b98a")
    f.pl([(-290, TOS + 86), (-20, TOS + 90), (-6, TOS + 104), (-6, 3150)], w=0.5, closed=False, color="#111")
    f.pl([(0, 3175), (-40, 3160), (-40, 3080), (-30, 3070)], w=0.45, closed=False, color="#7f8c8d")
    f.rect(0, 3165, 25, 12, w=0.1, fill="#333")
    f.rect(-290, SOFFIT + SLAT_T, 280, BOS - SOFFIT - SLAT_T, w=0.12, fill="#c9a77c", color="#7a5a3a")
    soffit_slats_cut(f, -10, -290)
    f.rect(-14, SOFFIT, 14, 50, w=0.12, fill="#333")
    f.rect(90, 2420, 120, 0.01, w=0)
    C = [
        ((-6, 3080), (-290, 3290), ["Membrane up 150 min, fully bonded"]),
        ((-25, 3150), (-290, 3260), ["Alu counter-flashing chased 25, PU + SS plugs"]),
        ((-150, BOS + 100), (-290, 3230), ["FP 8 welded to UPN web, 2 M12 to J1"]),
        ((-40, BOS + 15), (-290, 2600), ["L1 UPN 200 S275 HDG"]),
        ((60, BOS + 60), (-290, 2570), ["M12 resin anchors 110 emb. @ 400 stagg., into RC"]),
        ((150, 2600), (-290, 2540), ["Existing RC ring beam / lintel — verify"]),
        ((-12, 2670), (-290, 2510), ["Batten 50x38, black shadow strip at wall"]),
    ]
    for tgt, txt, lines in C:
        f.leader([tgt, txt], lines, size=1.2, anchor="start")
    f.dim((-6, TOS + 104), (-6, 3150), -3, size=1.15, text="≥150")
    s.text(232, 16, "D4  CANOPY / FAÇADE JUNCTION — 1:5", size=1.9, weight="bold")

    s.textblock(232, 222, 106, [
        ("B", "STEEL & FIXINGS"),
        "• Structural steel S355J2H (hollow) / S275JR (UPN, plates), EN 1090-2 EXC2, hot-dip galvanised EN ISO 1461 "
        "(85 µm min) after fabrication; vent/drain holes to galvaniser's requirements.",
        "• Visible steel (Option B posts): HDG + 2-coat polyester powder (duplex), RAL 9010 matt.",
        "• Bolts 8.8 HDG, washers & nyloc nuts; SS A4-70 for timber & aluminium fixings.",
        "• Isolate aluminium from galvanised steel with EPDM / nylon washers.",
        "• Cut ends & site welds: zinc-rich paint 2 coats (≥ 100 µm).",
    ], size=1.4, gap=0.3)
    return s


# ======================================================================= A-501 DETAILS 2
def sheet_a501(dxf=None):
    s = Sheet("A-501", "Details 2 — LED, soffit, back-span (S1), fascia edge & climbing wires", "1:2 / 1:5 / 1:20")
    s.frame()
    # D5 LED profile 1:2 (u = Y)
    v = View(s, 65, 62, 2, origin=(-2930, 2650), dxf=None)
    v.rect(-3000, SOFFIT + SLAT_T, 140, 38, w=0.15, fill="#c9a77c")
    for y0 in (-2895, -2960):
        v.rect(y0 - SLAT_W if y0 == -2960 else y0, SOFFIT, SLAT_W if y0 != -2960 else SLAT_W, SLAT_T, w=0.2,
               mat="timber")
    v.pl([(-2935, SOFFIT), (-2935, SOFFIT + 22), (-2910, SOFFIT + 22), (-2910, SOFFIT), (-2912, SOFFIT),
          (-2912, SOFFIT + 20), (-2933, SOFFIT + 20), (-2933, SOFFIT)], w=0.25, fill="#c9d0d6")
    v.rect(-2933, SOFFIT - 1, 21, 3, w=0.15, fill="#fffbe6")
    v.rect(-2930, SOFFIT + 10, 15, 2, w=0.1, fill="#f39c12")
    v.rect(-2925, SOFFIT + 12, 5, 2, w=0.1, fill="#333")
    v.leader([(-2922, SOFFIT + 1), (-2895, 2620)], ["Opal PMMA diffuser, clip-in"], size=1.3, anchor="start")
    v.leader([(-2922, SOFFIT + 11), (-2850, 2735)], ["24 V LED strip 14.4 W/m 2700 K"], size=1.3, anchor="start")
    v.leader([(-2911, SOFFIT + 18), (-2850, 2720)], ["Alu profile 25x22, black, to batten"], size=1.3,
             anchor="start")
    v.leader([(-2970, SOFFIT + 10), (-2995, 2600)], ["Slats cut short 5 each side"], size=1.3,
             anchor="start")
    v.dim((-2935, SOFFIT), (-2910, SOFFIT), -6, size=1.2)
    s.text(14, 16, "D5  LED PROFILE IN SOFFIT — 1:2", size=1.9, weight="bold")

    # D6 slat fixing 1:2 (u = X along slat? section across slats N-S)
    w = View(s, 30, 150, 2, origin=(-200, 2650), dxf=None)
    w.rect(-150, BOS, 100, 20, w=0.15, fill="#e6eaee", color="#666")
    w.text(-100, BOS + 6, "J1 flange", size=1.2, anchor="middle")
    w.rect(-150, SOFFIT + SLAT_T, 100, 38, w=0.2, mat="timber")
    soffit_slats_cut(w, -40, -200)
    for y in (-74, -152, -230, -308):
        pass
    w.rect(-100, SOFFIT + SLAT_T, 4, 38 + 6, w=0.1, fill="#888")
    w.rect(-150, SOFFIT + 2, 3, 56, w=0.1, fill="#888")
    w.line(-200, SOFFIT + SLAT_T + 2, -40, SOFFIT + SLAT_T + 2, w=0.35, color="#111", dash="1,0.6")
    w.leader([(-148, SOFFIT + 30), (-20, 2640)], ["SS A4 4.0x50 csk screw, 2/batten,", "pre-drilled — or concealed clip"],
             size=1.3, anchor="start")
    w.leader([(-98, SOFFIT + 50), (-20, 2745)], ["Batten 50x38 C24 treated, black,", "self-drill 5.5x45 to J1 @ 400"],
             size=1.3, anchor="start")
    w.leader([(-60, SOFFIT + SLAT_T + 2), (-20, 2700)], ["Black breathable insect fleece"], size=1.3,
             anchor="start")
    w.leader([(-170, SOFFIT + 10), (-20, 2610)], ["Slat 68x20 thermo-ash, arrises eased 2, gap 10"],
             size=1.3, anchor="start")
    w.dim((-108, SOFFIT), (-40, SOFFIT), -6, size=1.2)
    w.dim((-118, SOFFIT), (-108, SOFFIT), -10, size=1.2)
    s.text(14, 90, "D6  SOFFIT SLAT FIXING — 1:2", size=1.9, weight="bold")

    # D7 S1 back-span 1:20 (u = Y) — B2 through façade into annex
    b = View(s, 40, 230, 20, origin=(-600, 2400), dxf=None)
    b.rect(0, 2000, FAC_T, SLAB_SOFFIT - 2000, w=0.4, mat="masonry")
    b.rect(0, SLAB_SOFFIT, 2600, SLAB_TOP - SLAB_SOFFIT, w=0.4, mat="rc")
    b.rect(0, SLAB_TOP, FAC_T, FAC_PARAPET - SLAB_TOP, w=0.4, mat="masonry")
    b.rect(-10, BOS - 215, 330, 215, w=0.35, mat="conc")
    b.rect(-600, BOS, 600 + B2_TAIL, 200, w=0.35, fill="#5c6670")
    b.rect(-600, BOS + 12.5, 600 + B2_TAIL, 175, w=0.1, fill="#fff")
    b.rect(B2_TAIL - 250, TOS, 250, 40, w=0.2, mat="grout")
    for y in (B2_TAIL - 200, B2_TAIL - 60):
        b.rect(y - 8, TOS - 30, 16, 260, w=0.1, fill="#888")
    b.rect(FAC_T, 2300, 2300, 600, w=0.15, dash="2,1", color="#777")
    b.text(1450, 2350, "plasterboard bulkhead 12.5 on metal frame, FR 30", size=1.3, anchor="middle", color="#555")
    b.leader([(150, BOS - 100), (-500, 2100)], ["Precast padstone 440x300x215 C32/40", "on mortar M12, fulcrum"],
             size=1.3, anchor="start")
    b.leader([(B2_TAIL - 130, TOS + 20), (2200, 3500)], ["Tail: PL 250x250x15 + 4 M16 resin", "anchors, 30 grout"],
             size=1.3)
    b.leader([(1000, BOS + 100), (900, 3600)], ["B2 SHS 200x200x12.5, back-span 2000"], size=1.3)
    b.chain([-600, 0, FAC_T, B2_TAIL], "x", BOS, -10, size=1.3, overall=False)
    s.text(14, 172, "D7  B2 BACK-SPAN (SCHEME S1) — 1:20", size=1.9, weight="bold")
    s.text(14, 176, "Only if survey confirms RC slab & pier. Otherwise use S2 (post P3) — S-100.", size=1.3,
           color="#c0392b")

    # D8 climbing wire fixings 1:2
    c = View(s, 190, 50, 2, origin=(0, 0), dxf=None)
    c.rect(-60, -50, 60, 100, w=0.3, mat="masonry")
    c.rect(-60, -50, 60, 100, w=0.0, mat="render")
    c.rect(-50, -5, 50, 10, w=0.15, fill="#888")
    c.rect(0, -4, 40, 8, w=0.2, fill="#bbb")
    c.circle(48, 0, 8, w=0.3)
    c.circle(48, 0, 1.5, w=0.2, fill="#000")
    c.leader([(20, 4), (40, 40)], ["M8 SS stand-off eye 40, A4"], size=1.3)
    c.leader([(-30, 0), (-80, 40)], ["M8 resin anchor 70 emb."], size=1.3, anchor="end")
    c.leader([(48, -1), (70, -30)], ["3 mm 316 wire rope"], size=1.3)
    s.text(160, 16, "D8  CLIMBING WIRE FIXING — 1:2", size=1.9, weight="bold")

    # D9 west fascia & overflow 1:5 (u = X looking north)
    d = View(s, 262, 128, 5, origin=(650, 2600), dxf=None)
    rhs(d, B3_X[0], BOS, 100, 200, 5)
    d.rect(650, TOS, 200, 55, w=0.12, mat="timber")
    d.rect(560, TOS + 55, 290, 18, w=0.15, fill="#d9b98a")
    d.rect(532, TOS - 40, 18, 3000 - TOS + 40, w=0.15, fill="#d9b98a")
    d.pl([(850, TOS + 75), (560, TOS + 75), (550, 3000), (532, 3000)], w=0.5, closed=False, color="#111")
    d.pl([(560, FASCIA_BOT + 10), (560, FASCIA_BOT), (500, FASCIA_BOT), (500, FASCIA_TOP), (555, FASCIA_TOP - 6),
          (555, FASCIA_TOP - 30)], w=0.55, closed=False, color="#1b1b1b")
    d.rect(498, TOS + 30, 50, 40, w=0.3, fill="#1f5fa8")
    d.rect(560, SOFFIT + SLAT_T, 290, BOS - SOFFIT - SLAT_T, w=0.1, fill="#c9a77c")
    d.rect(560, SOFFIT, 290, SLAT_T, w=0.15, mat="timber")
    d.rect(LED_INSET + CAN_X0 - 12, SOFFIT, 25, 22, w=0.2, fill="#f39c12")
    d.leader([(520, TOS + 50), (560, 3130)], ["Overflow scupper 100x50 alu, 40 above gutter sole"], size=1.2,
             anchor="start")
    d.leader([(600, BOS + 100), (700, 2800)], ["B3 RHS 200x100x5"], size=1.2, anchor="start")
    d.leader([(LED_INSET + CAN_X0, SOFFIT), (760, 2560)], ["LED run W side"], size=1.2, anchor="start")
    s.text(232, 16, "D9  WEST FASCIA & OVERFLOW — 1:5", size=1.9, weight="bold")

    s.textblock(222, 150, 116, [
        ("B", "TIMBER"),
        "• Soffit slats & cladding: thermally-modified ash (Thermo-D) or Western Red Cedar, clear grade, "
        "PEFC/FSC, MC 12–16 %, 68x20 planed all round, ends sealed.",
        "• Finish: 2 coats UV-stable oil (e.g. hard-wax exterior oil, natural/teak tone) all faces before fixing; "
        "re-oil every 2–3 years.",
        "• Battens/firrings: C24 treated UC3 (EN 351), cut ends re-treated.",
        "• Fasteners: stainless A4; 2 mm min. gap at slat ends; stagger end joints over battens.",
        ("B", "ALUMINIUM"),
        "• Fascia 3 mm EN AW-5754 H22, folded, max 3.0 m lengths with 3 mm open joints backed by 100 mm "
        "sleeve; polyester powder RAL 9010 matt, Qualicoat class 2 (marine/coastal sites).",
        ("B", "LIGHTING CONTROL"),
        "• Draw wires & junction boxes before soffit close-up; label circuits; test at 1st fix.",
    ], size=1.45, gap=0.3)
    return s


# ======================================================================= A-600 DOORS & SCREENS
def sheet_a600(dxf=None):
    s = Sheet("A-600", "Door & screen schedule, elevations & joinery details", "1:25 / 1:20 / 1:5")
    s.frame()
    # elevations
    for i, (kind, ox, rng) in enumerate((("D01", 22, D01), ("D02", 82, D02), ("D03", 172, D03))):
        sc = 25
        v = View(s, ox - rng[0] / sc, 125, sc, dxf=None)
        v.rect(rng[0] - 150, -5, rng[1] - rng[0] + 300, HEAD + 300, w=0.2, fill="#f7f3ea")
        info = door_elev(v, kind, rng[0], rng[1])
        v.dim((rng[0], 0), (rng[1], 0), -6, size=1.4)
        v.dim((rng[1], 0), (rng[1], HEAD), -5, size=1.4)
        v.line(rng[0] - 200, -5, rng[1] + 200, -5, w=0.5)
        s.text(ox, 132 + 6, f"{kind} — elevation from courtyard 1:25", size=1.7, weight="bold")
        if kind == "D03":
            d3 = info
    # G01 screen 1:50
    g = View(s, 230 - (-(-5400)) / 50 * 0, 125, 50, origin=(5400, 0), dxf=None)
    for a, b in SCR_POSTS:
        g.rect(-a, 0, a - b, SCR_H + 50, w=0.3, fill="#8a5a2b")
    lattice_panel(g, 5500, 6400, 50, SCR_H - 50, pitch=125, bar=38)
    lattice_panel(g, 6510, 7490, 60, SCR_H - 60, pitch=122, bar=38)
    lattice_panel(g, 7600, 8300, 50, SCR_H - 50, pitch=117, bar=38)
    g.rect(6510, 60, 980, SCR_H - 120, w=0.5)
    g.line(5300, 0, 8500, 0, w=0.5)
    g.chain([5400, 6400, 6500, 7500, 7600, 8300, 8400], "x", 0, -6, size=1.3, overall=True)
    g.dim((8400, 0), (8400, SCR_H + 50), -5, size=1.3)
    s.text(230, 138, "G01 — screen & gate (from courtyard) 1:50", size=1.7, weight="bold")

    # D03 horizontal section 1:5 (through stile + lattice)
    h = View(s, 30, 168, 5, origin=(5450, 0), dxf=None)
    h.rect(5450 - 60, 0, 60, 120, w=0.3, mat="masonry")
    h.rect(5450, 0, 30, 120, w=0.25, mat="timber")
    h.rect(5483, 20, 90, 54, w=0.3, mat="timber")
    h.rect(5480 + 3, 74, 10, 18, w=0.15, fill="#8a5a2b")
    x = 5573
    a, b = d3["open"]
    bar = d3["bar"]
    for k in range(3):
        h.rect(x + k * (a + bar), 29, 0.01, 36, w=0)
        if k > 0:
            h.rect(x + k * (a + bar) - bar, 29, bar, 36, w=0.25, mat="timber")
    h.line(5573, 29, 5573 + 3 * (a + bar), 29, w=0.1, dash="1,0.6")
    h.line(5573, 65, 5573 + 3 * (a + bar), 65, w=0.1, dash="1,0.6")
    h.rect(5573, 22, 3 * (a + bar), 2, w=0.1, fill="#888")
    h.leader([(5465, 60), (5440, -40)], ["Lining 30 + stop 10x18"], size=1.25, anchor="start")
    h.leader([(5530, 47), (5540, -70)], ["Stile 90x54 thermo-ash / iroko"], size=1.25, anchor="start")
    h.leader([(5573 + a + bar / 2, 47), (5700, -100)], [f"Lattice bars {bar}x36, half-lapped, PU glued + SS pins"],
             size=1.25, anchor="start")
    h.leader([(5650, 23), (5800, -130)], ["SS 316 insect mesh 1.0 mm (inside face, optional)"], size=1.25,
             anchor="start")
    h.dim((5573 + bar + a, 29), (5573 + bar + a + a, 29), -4, size=1.2, text=f"{a:.0f}")
    s.text(16, 150, "D03 — horizontal section at stile 1:5", size=1.7, weight="bold")

    rows = [
        ["D01", "Hall entrance", "1100 x 2400 S.O.", "Thermally-broken aluminium single door, inward opening, "
         "slim 60 frame, bronze (RAL 8019 matt or bronze anodised). 6T/16Ar/6T low-e (Ug ≤ 1.1), Uw ≤ 1.6.",
         "Multi-point lock, 3 hinges, 300 SS pull bar, euro cylinder, drop-seal, level threshold ≤ 15 + SD1"],
        ["D02", "Store / workshop", "1800 x 2400 S.O.", "Insulated aluminium roller shutter, 77 mm double-skin "
         "PU-foamed slats, RAL 8019 matt, 80 side guides, 300 coil box concealed inside above head. Wind class 3.",
         "Tubular motor 230 V + manual override, obstacle safety edge, 2 remotes, push-button inside"],
        ["D03", "Utility / plant", "900 x 2400 S.O.", f"Timber lattice ventilated door, outward opening. Leaf "
         f"{d3['leaf'][0]:.0f} x {d3['leaf'][1]:.0f} x 54. Stiles 90, top rail 110, bottom rail 200. Lattice 6 x 18 "
         f"openings {d3['open'][0]:.0f} x {d3['open'][1]:.0f}, bars 36. Free vent area ≈ "
         f"{6 * 18 * d3['open'][0] * d3['open'][1] / 1e6:.2f} m².",
         "3 SS 102 hinges, lever lock (sashlock), SS kick plate inside, door stay; oiled"],
        ["G01", "East screen & gate", "3000 x 1800", "Thermo-ash lattice screen 45 x 38 bars @ ~120, posts "
         "100x100 on HDG post shoes on 400x400x600 pads. Gate leaf 980 x 1680.",
         "2 HD SS strap hinges, gravity latch both sides, drop bolt, gate stop"],
    ]
    s.table(130, 158, [("Ref", 10), ("Location", 22), ("Size", 24), ("Description", 92), ("Ironmongery", 60)],
            rows, size=1.4)
    s.textblock(130, 238, 208, [
        "Joinery notes: all external joinery sizes to be confirmed by site measure after openings are made good. "
        "Timber joinery factory-finished all 6 faces (oil), MC 12–15 %. Aluminium systems to EN 14351-1; "
        "installation to manufacturer's details with EPDM membranes to reveals, low-expansion PU foam & external "
        "silicone (colour matched). D02 coil box requires 300 x 300 clear zone inside head — check interior.",
    ], size=1.45)
    return s
