"""Architectural sheets: plans, elevations, sections (Design A)."""
from cad import Sheet, View, break_line
from common import *  # noqa
from design import *  # noqa


def lv(m):
    return f"{m:+.3f}".replace("+0.000", "±0.000")


# ======================================================================= A-100 SETTING-OUT PLAN
def sheet_a100(dxf=None):
    s = Sheet("A-100", "Courtyard setting-out & general arrangement plan", "1:50")
    s.frame()
    v = View(s, 62, 70, 50, dxf=dxf, dxf_offset=(0, 0))
    plan_paving_outline(v, grid=True)
    plan_planter(v)
    plan_walls(v)
    plan_doors(v)
    plan_drainage(v, labels=False)
    plan_screen(v)
    plan_furniture(v)
    plan_canopy_outline(v)
    plan_posts(v)
    # grids
    v.grid(600, 2300, 600, -9300, "1", end="start")
    v.grid(5200, 2300, 5200, -9300, "2", end="start")
    v.grid(-1900, 0, 8300, 0, "A", end="end")
    v.grid(-1900, -1400, 8300, -1400, "B", end="end")
    v.grid(-1900, -3050, 8300, -3050, "C", end="end")
    # dimensions — openings above façade
    v.chain([0, D01[0], D01[1], D02[0], D02[1], D03[0], D03[1], COURT_W], "x", FAC_T, 9, size=1.6)
    # canopy along front
    v.chain([0, CAN_X0, P3[0], CAN_X1, COURT_W], "x", CAN_Y1, -7, size=1.5, overall=False)
    v.chain([0, P1[0], P3[0], COURT_W], "x", FAC_T, 15, size=1.6, overall=False)
    # bottom overall
    v.chain([-BW_T, 0, KERB_X0, KERB_X1, G1[0], COURT_W, COURT_W + EW_T], "x", -8400, -14, size=1.6)
    # left Y chain
    v.chain([0, P2[1], P1[1], CAN_Y1, -8400], "y", -BW_T, 13, size=1.6)
    # right Y chain
    v.chain([0, G1[1], -EW_LEN, GATE[0], GATE[1], -8400], "y", COURT_W + EW_T, -11, size=1.6)
    # labels
    v.leader([(2900, -2300), (3600, -2000)], ["CANOPY OVER (dashed) — see A-102 / S-100"], size=1.6)
    v.leader([(P1[0] + 60, P1[1] - 60), (1500, -3700)], ["P1 post SHS 120x120x6.3, timber-clad 160x160",
                                                          "(Ø75 rainwater pipe inside)"], size=1.6)
    v.leader([(P2[0] + 80, P2[1] - 40), (1900, -1950)], ["P2 post (as P1, no RWP)"], size=1.6)
    v.leader([(P3[0], P3[1] - 60), (5900, -3800)], ["P3 — ALT. S2 ONLY", "(see S-100)"], size=1.5)
    v.leader([(4000, -5000), (4400, -5300)], ["200x200x60 concrete pavers, 3-tone,",
                                               "grid bond — see A-101"], size=1.6)
    v.leader([(925, -6400), (2200, -6800)], ["Planter kerb 150 RC, rendered, h = 400,",
                                              "230x60 precast coping — see A-302"], size=1.6)
    v.leader([(7250, -6000), (6000, -7800)], ["G01 timber lattice screen & gate", "h = 1800 — see A-600"],
             size=1.6, anchor="end")
    v.leader([(1650, -1250), (2300, -1000)], ["Lounge chair (FF&E)"], size=1.4)
    v.section_mark(2600, 1500, 2600, -4200, "A", "A-300", flip=True)
    v.section_mark(-1200, -2200, 7900, -2200, "B", "A-301")
    v.section_mark(-900, -5000, 1600, -5000, "C", "A-302")
    # elevation markers
    for (x, y, lab, ref, d) in ((3600, -6800, "A", "A-200", (0, 1)), (4300, -5600, "B", "A-201", (-1, 0)),
                                 (3000, -5600, "C", "A-201", (1, 0))):
        p = v.P(x, y)
        s.circle(p[0], p[1], 3, w=0.25, fill="#fff")
        s.text(p[0], p[1] + 0.3, lab, size=2.0, anchor="middle", weight="bold")
        s.text(p[0], p[1] + 2.2, ref, size=1.1, anchor="middle")
        tx, ty = p[0] + d[0] * 5.5, p[1] - d[1] * 5.5
        s.poly([(tx, ty), (p[0] + d[0] * 3 - d[1] * 2, p[1] - d[1] * 3 - d[0] * 2),
                (p[0] + d[0] * 3 + d[1] * 2, p[1] - d[1] * 3 + d[0] * 2)], w=0, fill="#000")
    v.level(1300, -3600, lv(paving_level(1300)), plan=True, size=1.5)
    v.level(6600, -4200, lv(LV_VALLEY), plan=True, size=1.5)
    v.level(2200, -250, "-0.015 (D01)", plan=True, size=1.5)
    v.level(425, -4800, "+0.400 coping", plan=True, size=1.5)
    t = v.P(-1900, 0)
    v.title(48, 262, "1/A-100", "COURTYARD GENERAL ARRANGEMENT PLAN", "1:50 @ A3", sub="cut plane +1.20")
    s.north_arrow(225, 30, 6)
    s.scale_bar(240, 268, 50)
    # key / legend
    x0, y0 = 268, 22
    s.text(x0, y0, "LEGEND", size=2.2, weight="bold")
    items = [("masonry", "Existing masonry wall (cut)"), ("soil", "Planter soil"), (None, "Canopy outline above (dashed)"),
             ("steel", "Steel post (cut)"), ("timber", "Timber cladding / joinery"), ("alu", "Drainage channel / gully")]
    yy = y0 + 4
    for m, t in items:
        if m:
            tint, hid = MAT[m]
            s.rect(x0, yy - 2.5, 6, 3.5, lw=0.2, fill=tint)
            if hid:
                s.rect(x0, yy - 2.5, 6, 3.5, lw=0, fill=f"url(#{hid})")
        else:
            s.rect(x0, yy - 2.5, 6, 3.5, lw=0.3, dash="1.5,0.8")
        s.text(x0 + 8, yy, t, size=1.6)
        yy += 5
    s.textblock(x0, yy + 2, 70, [
        ("B", "SETTING-OUT NOTES"),
        "1. Setting-out datum: internal corner of existing boundary wall (W) and annex façade (N) = X0 / Y0.",
        "2. Grids 1-2 / A-C are steel centrelines (posts & primary beams).",
        "3. Establish TBM ±0.000 at internal FFL of D01 before excavation.",
        "4. Check diagonals of canopy rectangle (4850 x 3150): 5783 mm ±5.",
        "5. Post P1/P2 holding-down bolts set with plywood template to ±3 mm.",
        "6. Paving grid starts at kerb face X = 1000 and façade Y = 0: full 200 units, no cuts W/E.",
        "7. Furniture & potted olive are FF&E (by owner) — shown for coordination only.",
    ], size=1.55, gap=0.4)
    return s


# ======================================================================= A-101 PAVING & DRAINAGE
def sheet_a101(dxf=None):
    s = Sheet("A-101", "Paving layout, levels & surface water drainage plan", "1:50")
    s.frame()
    v = View(s, 62, 70, 50, dxf=dxf, dxf_offset=(20000, 0))
    grid = paving_pattern()
    counts = {k: 0 for k in TONES}
    for j, row in enumerate(grid):
        for i, c in enumerate(row):
            x = PAV_X0 + i * PAVER
            y = -j * PAVER
            counts[c] += 1
            v.rect(x, y - PAVER, PAVER, PAVER, w=0.04, color="#fff", fill=TONES[c][1], layer="A-PAVING")
    plan_planter(v, label=False)
    plan_walls(v, show_rooms=False)
    plan_doors(v)
    plan_drainage(v)
    plan_screen(v)
    plan_posts(v, alt=False)
    # drainage runs (Ø110 PVC-U)
    run = [(SD1[1], -80), (G1[0], -80), G1, G2, (G2[0], -8400), IC1]
    v.pl(run, w=0.35, color="#1f5fa8", closed=False, dash="3,1", layer="C-DRAIN")
    v.pl([(P1[0], P1[1]), (P1[0] + 500, P1[1] - 500), (G1[0] - 300, P1[1] - 500), (G1[0], G1[1] - 150)], w=0.35,
         color="#1f5fa8", closed=False, dash="3,1", layer="C-DRAIN")
    v.leader([(3000, P1[1] - 500), (3300, -4300)], ["Ø110 PVC-U (SN8) RWP carrier from P1 @ 1:60 min,",
                                                     "150 granular surround, cover ≥ 300"], size=1.5)
    v.leader([(G2[0], -7600), (5200, -7900)], ["Ø110 PVC-U to IC1 → soakaway SA1 /", "existing SW drain (verify)"],
             size=1.5, anchor="end")
    # spot levels
    pts = [(1100, -100), (1100, -4200), (1100, -8300), (3800, -4200), (3800, -8300), (6600, -4200), (6600, -8300),
           (7100, -1000), (7100, -7000), (2200, -250), (4050, -250), (5900, -250)]
    for (x, y) in pts:
        if (x, y) == (2200, -250):
            t = "-0.015"
        else:
            t = lv(round(paving_level(x), 3))
        v.level(x, y, t, plan=True, size=1.4)
    for g in (G1, G2):
        v.level(g[0] + 170, g[1] - 300, f"{LV_GULLY:+.3f} grate", plan=True, size=1.4)
    # fall arrows
    for y in (-1600, -5200, -7400):
        for (xa, xb) in ((1600, 5800),):
            pa, pb = v.P(xa, y), v.P(xb, y)
            s.line(pa[0], pa[1], pb[0], pb[1], w=0.3, color="#1f5fa8")
            s.poly([(pb[0], pb[1]), (pb[0] - 2.2, pb[1] - 0.9), (pb[0] - 2.2, pb[1] + 0.9)], w=0, fill="#1f5fa8")
            s.text((pa[0] + pb[0]) / 2, pa[1] - 1, "FALL 1:80", size=1.6, anchor="middle", color="#1f5fa8",
                   weight="bold")
        pa, pb = v.P(7150, y), v.P(6750, y)
        s.line(pa[0], pa[1], pb[0], pb[1], w=0.3, color="#1f5fa8")
        s.poly([(pb[0], pb[1]), (pb[0] + 1.8, pb[1] - 0.8), (pb[0] + 1.8, pb[1] + 0.8)], w=0, fill="#1f5fa8")
    v.text(6900, -4700, "1:60", size=1.4, anchor="middle", color="#1f5fa8")
    v.title(48, 262, "1/A-101", "PAVING, LEVELS & DRAINAGE PLAN", "1:50 @ A3")
    s.north_arrow(225, 30, 6)
    s.scale_bar(240, 268, 50)
    total = sum(counts.values())
    x0, y0 = 262, 20
    s.text(x0, y0, "PAVER SCHEDULE (200 x 200 x 60)", size=2.0, weight="bold")
    rows = []
    for k, (name, col, w) in TONES.items():
        rows.append([k, name, str(counts[k]), f"{counts[k] / total * 100:.0f}%", str(int(counts[k] * 1.05 + 0.99))])
    rows.append(["", "TOTAL laid", str(total), "100%", str(int(total * 1.05 + 0.99))])
    s.table(x0, y0 + 2, [("Tone", 9), ("Colour", 22), ("No.", 10), ("Mix", 10), ("+5% order", 17)], rows, size=1.6)
    for i, (k, (name, col, w)) in enumerate(TONES.items()):
        s.rect(x0 + 5.5, y0 + 7.4 + i * 3.04, 2.6, 2.2, lw=0.1, fill=col)
    s.textblock(x0, y0 + 26, 72, [
        f"Area: {(PAV_X1 - PAV_X0) * (PAV_Y0 - PAV_Y1) / 1e6:.2f} m² — {total} units, no cut units required "
        "(grid fits 31 x 42 exactly; trim only around gullies G1/G2 & slot drain).",
        ("B", "PAVING SPECIFICATION"),
        "• Pavers: vibro-pressed concrete, 200x200x60, EN 1338, class 3/R/I, slip USRV ≥ 45, square arris, "
        "through-coloured, 3 tones as schedule (match render: sand / buff / grey-taupe).",
        "• Lay grid (stack) bond, 3 mm joints, laid from paving plan colour map: lay out dry, photo-approve 4 m² "
        "before full laying.",
        "• Bed: 30 mm sharp sand (EN 13242 0/4) screeded, compacted with plate + rubber mat.",
        "• Sub-base: 150 mm Type 1 crushed aggregate in 2 layers, 98% MDD; geotextile separator on formation.",
        "• Jointing: kiln-dried silica sand, brushed & re-vibrated; or polymeric jointing sand (beige).",
        "• Tolerance: ±3 mm under 3 m straight-edge; lipping ≤ 2 mm.",
        "• Vehicle use: if D02 is used by a car, upgrade to 80 mm pavers on 250 mm sub-base.",
        ("B", "DRAINAGE"),
        "• SD1: polymer-concrete slot drain, 100 mm, stainless slot, B125, with outlet box at E end.",
        "• G1/G2: PVC-U yard gully with silt bucket, 300x300 ductile-iron/stainless grate, B125.",
        "• Pipes: Ø110 PVC-U SN8, 1:60 min, rodding access at every change of direction.",
        "• P1 rainwater (canopy 15.3 m²) and AC condensate connect to G1 run.",
        "• Outfall: IC1 Ø450 inspection chamber → SA1 soakaway crate (1.0 m³, ≥ 5 m from buildings) "
        "or existing surface-water drain. Percolation test before design is fixed.",
    ], size=1.5, gap=0.35)
    return s


# ======================================================================= A-102 CANOPY ROOF PLAN
def sheet_a102(dxf=None):
    s = Sheet("A-102", "Canopy roof plan — falls, gutter & membrane", "1:25")
    s.frame()
    v = View(s, 40, 40, 25, origin=(0, 600), dxf=dxf, dxf_offset=(40000, 0))
    # façade strip + roof of annex
    v.rect(-BW_T, 0, 6600, FAC_T, mat="masonry", w=0.4)
    v.rect(-BW_T, FAC_T, 6600, 300, w=0.2, fill="#f4f4f4")
    v.text(3000, FAC_T + 170, "EXISTING ANNEX ROOF (beyond) — parapet +3.400", size=1.6, anchor="middle",
           color="#666")
    v.rect(-BW_T, -3800, BW_T, 3800, mat="masonry", w=0.4)
    # deck
    v.rect(CAN_X0, CAN_Y1, CAN_X1 - CAN_X0, -CAN_Y1, w=0.5, fill="#f2f2f2")
    v.rect(CAN_X0 + 50, -2995, CAN_X1 - CAN_X0 - 100, 2995, w=0.2, fill="#e9ecef")
    # gutter
    v.rect(CAN_X0 + 50, -3115, CAN_X1 - CAN_X0 - 100, 120, w=0.3, fill="#cdd8e3")
    v.text(3000, -3075, "BOX GUTTER 120 wide, TPO lined, sole falls 1:200 to W outlet", size=1.4, anchor="middle")
    # fascia capping
    v.rect(CAN_X0, CAN_Y1, CAN_X1 - CAN_X0, 35, w=0.15, fill="#fff")
    v.rect(CAN_X0, CAN_Y1, 50, -CAN_Y1, w=0.15, fill="#fff")
    v.rect(CAN_X1 - 50, CAN_Y1, 50, -CAN_Y1, w=0.15, fill="#fff")
    # firrings (hidden)
    for x in [J_X0] + JOISTS + [J_X1]:
        v.line(x, -60, x, -2990, w=0.1, dash="2,1", color="#888")
    # outlet
    v.circle(P1[0], P1[1], 40, w=0.3, fill="#1f5fa8")
    v.rect(P1[0] - 60, P1[1] - 60, 120, 120, w=0.15, dash="1,0.6")
    # overflow scupper
    v.rect(CAN_X0, -2650, 50, 100, w=0.3, fill="#1f5fa8")
    # fall arrows
    for x in (1500, 2800, 4200):
        a, b = v.P(x, -300), v.P(x, -2700)
        s.line(a[0], a[1], b[0], b[1], w=0.35, color="#1f5fa8")
        s.poly([(b[0], b[1]), (b[0] - 1, b[1] - 2.4), (b[0] + 1, b[1] - 2.4)], w=0, fill="#1f5fa8")
        s.text(a[0] + 1.5, (a[1] + b[1]) / 2, "FALL 1:60", size=1.8, color="#1f5fa8", weight="bold", rot=-90)
    a, b = v.P(4900, -3055), v.P(1100, -3055)
    s.line(a[0], a[1] + 3.2, b[0], b[1] + 3.2, w=0.3, color="#1f5fa8")
    s.poly([(b[0], b[1] + 3.2), (b[0] + 2.2, b[1] + 2.3), (b[0] + 2.2, b[1] + 4.1)], w=0, fill="#1f5fa8")
    # levels
    v.level(2400, -150, f"+{DECK_HI / 1000:.3f} deck (high)", plan=True, size=1.6)
    v.level(2400, -2850, f"+{DECK_LO / 1000:.3f} deck (low)", plan=True, size=1.6)
    v.level(4700, -3060, f"+{GUTTER_SOLE_E / 1000:.3f}", plan=True, size=1.4)
    v.level(1000, -3060, f"+{GUTTER_SOLE_W / 1000:.3f}", plan=True, size=1.4)
    v.level(4300, -3180, f"+{FASCIA_TOP / 1000:.3f} fascia top", plan=True, size=1.4)
    # dims
    v.chain([CAN_X0, P1[0], P3[0], CAN_X1], "x", CAN_Y1, -10, size=1.7)
    v.chain([0, -2995, -3115, CAN_Y1], "y", CAN_X1, -12, size=1.7)
    v.dim((CAN_X0, 0), (CAN_X0, CAN_Y1), 14, size=1.7)
    # leaders
    v.leader([(P1[0], P1[1]), (P1[0] + 300, P1[1] - 900)], ["O1 outlet: Ø63 TPO-coated spigot with leaf guard,",
                                                            "into Ø75 PVC-U RWP inside post P1 (D2/A-500)"], size=1.6)
    v.leader([(CAN_X0 + 25, -2600), (CAN_X0 - 500, -1800)], ["Overflow scupper 100x50",
                                                             "through W fascia, 40 mm above",
                                                             "gutter sole → drips to planter"], size=1.5, anchor="end")
    v.leader([(3600, -1500), (3900, -1200)], ["1.5 mm white TPO membrane, mech. fixed / bonded",
                                              "on 18 mm marine ply on tapered firrings",
                                              "(70 → 20 mm) on each joist — see A-300"], size=1.6)
    v.leader([(2000, 0), (1700, 350)], ["Membrane turned up 150 min, aluminium counter-",
                                         "flashing chased 25 into façade, sealed (D4/A-500)"], size=1.5, anchor="end")
    v.leader([(5320, -1800), (5800, -1500)], ["Fascia capping: 3 mm alu, RAL 9010,",
                                              "10% fall inward, joints sleeved"], size=1.5)
    v.leader([(3000, -2200), (3300, -2450)], ["Stainless trailing-wire for jasmine along W & S",
                                              "fascia top (2 runs, 3 mm 316) — optional"], size=1.4)
    v.title(28, 205, "1/A-102", "CANOPY ROOF PLAN", "1:25 @ A3")
    s.north_arrow(260, 30, 6)
    s.scale_bar(240, 268, 25, 2)
    s.textblock(205, 160, 130, [
        ("B", "ROOFING NOTES"),
        "1. Deck: 18 mm WBP marine plywood (EN 636-3), staggered joints, all edges supported on firrings/noggins; "
        "screw 4.5 x 50 SS @ 150 edges / 300 field. Deck acts as diaphragm — fix to steel per S-100.",
        "2. Membrane: 1.5 mm reinforced TPO (or EPDM 1.2 mm) fully bonded; welded seams 40 mm; upstands 150 min; "
        "manufacturer's corner pre-forms; 10-year system warranty.",
        "3. Gutter: 120 x 80 (min) box gutter formed in ply, membrane lined, sole 1:200 to outlet O1. Outlet "
        "capacity 1.1 L/s ≥ design 0.65 L/s (r = 150 mm/h, A = 15.3 m²).",
        "4. Overflow scupper set 40 mm above gutter sole; discharges to planter (visible warning).",
        "5. Flood test 24 h with outlet plugged before soffit is closed.",
        "6. Vines on canopy top: keep to fascia wires only — no growth onto membrane (annual maintenance).",
    ], size=1.6, gap=0.4)
    return s


# ======================================================================= A-103 RCP / LIGHTING / POWER
def sheet_a103(dxf=None):
    s = Sheet("A-103", "Reflected ceiling plan, lighting & power", "1:25 / 1:100")
    s.frame()
    v = View(s, 22, 34, 25, origin=(0, 300), dxf=dxf, dxf_offset=(60000, 0))
    v.rect(-BW_T, 0, 6600, FAC_T, mat="masonry", w=0.4)
    for a, b in (D01, D02, (D03[0], 6350)):
        v.rect(a, 0, b - a, FAC_T, w=0.1, fill="#fff")
    # soffit slats
    v.rect(CAN_X0, CAN_Y1, CAN_X1 - CAN_X0, -CAN_Y1, w=0.5, fill="#e9c99a")
    y = -40
    while y > CAN_Y1 + 50:
        v.line(CAN_X0 + 50, y, CAN_X1 - 50, y, w=0.06, color="#8a5a2b")
        y -= SLAT_W + SLAT_GAP
    v.rect(CAN_X0, CAN_Y1, CAN_X1 - CAN_X0, 50, w=0.2, fill="#fff")
    v.rect(CAN_X0, CAN_Y1, 50, -CAN_Y1, w=0.2, fill="#fff")
    v.rect(CAN_X1 - 50, CAN_Y1, 50, -CAN_Y1, w=0.2, fill="#fff")
    # LED strip
    i = LED_INSET
    led = [(CAN_X0 + i, -30), (CAN_X0 + i, CAN_Y1 + i), (CAN_X1 - i, CAN_Y1 + i), (CAN_X1 - i, -30)]
    v.pl(led, w=0.9, color="#f39c12", closed=False, layer="E-LIGHT")
    for (x, y) in (P1, P2):
        v.rect(x - 80, y - 80, 160, 160, w=0.2, fill="#c39a6b")
    for (x, y) in DOWNLIGHTS:
        v.circle(x, y, 60, w=0.3, fill="#fff3cd", layer="E-LIGHT")
        v.line(x - 90, y, x + 90, y, w=0.15)
        v.line(x, y - 90, x, y + 90, w=0.15)
    v.circle(WL1[0], -60, 70, w=0.3, fill="#fff3cd")
    v.tag(WL1[0] - 250, -280, "WL1", shape="hex", r=2.2, size=1.4)
    v.tag(DOWNLIGHTS[0][0] + 250, DOWNLIGHTS[0][1] - 200, "DL1", shape="hex", r=2.2, size=1.4)
    v.tag(DOWNLIGHTS[1][0] + 250, DOWNLIGHTS[1][1] - 200, "DL1", shape="hex", r=2.2, size=1.4)
    v.tag(3000, CAN_Y1 + 300, "LS1", shape="hex", r=2.2, size=1.4)
    # cable route to driver
    v.pl([(CAN_X1 - i, -30), (CAN_X1 - i, 150), (5700, 150), (5700, 900)], w=0.3, color="#c0392b", dash="2,1",
         closed=False)
    v.text(5750, 700, "→ LED drivers in UTILITY (behind D03)", size=1.4, color="#c0392b")
    v.chain([CAN_X0, CAN_X0 + i, DOWNLIGHTS[0][0], DOWNLIGHTS[1][0], CAN_X1 - i, CAN_X1], "x", CAN_Y1, -9, size=1.6)
    v.chain([0, DOWNLIGHTS[0][1], CAN_Y1 + i, CAN_Y1], "y", CAN_X1, -8, size=1.6, overall=False)
    v.leader([(1800, -1700), (2100, -2000)], ["Soffit: 68x20 thermo-ash slats, 10 mm gaps, run E-W,",
                                              "underside +2.650 — see D6/A-501"], size=1.6)
    v.leader([(CAN_X0 + i, -1500), (CAN_X0 - 400, -1200)], ["LS1 LED strip in recessed",
                                                            "alu profile, 60 from fascia"], size=1.5, anchor="end")
    v.title(22, 150, "1/A-103", "REFLECTED CEILING PLAN — CANOPY SOFFIT", "1:25 @ A3")
    # site lighting plan 1:100
    w = View(s, 263, 30, 100, dxf=None)
    w.rect(PAV_X0, PAV_Y1, PAV_X1 - PAV_X0, -PAV_Y1, w=0.2, fill="#f6f1e8")
    w.rect(0, PL_SOUTH, COP_X1, -PL_SOUTH, w=0.2, fill="#e5d6bf")
    w.rect(-BW_T, PL_SOUTH - 200, BW_T, -PL_SOUTH + 200, w=0.2, fill="#ccc")
    w.rect(-BW_T, 0, COURT_W + EW_T + BW_T, FAC_T, w=0.2, fill="#ccc")
    w.rect(COURT_W, -EW_LEN, EW_T, EW_LEN, w=0.2, fill="#ccc")
    w.rect(CAN_X0, CAN_Y1, CAN_X1 - CAN_X0, -CAN_Y1, w=0.2, dash="2,1")
    for (x, y, t) in UPLIGHTS:
        w.circle(x, y, 90, w=0.25, fill="#f39c12")
        w.text(x + 160, y - 50, t, size=1.3)
    w.circle(7050, -350, 80, w=0.25, fill="#2ecc71")
    w.text(6950, -650, "SO1", size=1.3, anchor="end")
    w.pl([(560, -400), (560, -7300)], w=0.25, color="#c0392b", dash="1.5,0.8", closed=False)
    s.text(250, 118, "2/A-103  SITE LIGHTING & POWER 1:100", size=2.0, weight="bold")
    rows = [
        ["LS1", "LED strip 24 V DC, 14.4 W/m, 2700 K, CRI ≥ 90, IP67, in 25x20 recessed alu profile, opal diffuser, mitred corners", "10.6 m", "153 W"],
        ["DL1", "Recessed soffit downlight, 7 W LED, 2700 K, 36°, IP65, Ø68 cut-out, black trim", "2", "14 W"],
        ["WL1", "Wall sconce up/down, 2 x 4 W, 2700 K, IP54, bronze, c/l +2.100", "1", "8 W"],
        ["UL1–6", "Spike spotlight 12 V, 3 W, 2700 K, 40°, IP67, adjustable, bronze; 1 m cable to junction box", "6", "18 W"],
        ["SO1", "Twin switched socket 16 A, IP66 weatherproof, RCD 30 mA, on E wall +0.450", "1", "—"],
        ["DRV", "LED drivers: 2 x 100 W 24 V constant voltage (DALI/phase-cut dimmable) + 60 W 12 V for UL", "3", "in UTILITY"],
        ["CTRL", "Astronomical time-switch + scene dimmer (dusk-on, 23:30 50%, off 01:00), smart-home ready", "1", "in UTILITY"],
    ]
    s.table(18, 160, [("Ref", 12), ("Description", 170), ("Qty", 14), ("Load", 16)], rows, size=1.55)
    s.textblock(250, 124, 88, [
        ("B", "ELECTRICAL NOTES"),
        "1. New circuits from existing consumer unit: C1 lighting (RCBO 6 A, 30 mA, Type A); C2 external socket "
        "(RCBO 16 A, 30 mA). Installer to verify capacity, earthing & bonding.",
        "2. All external work to IEC 60364-7-714 / local wiring regulations; certificate on completion.",
        "3. LV cables: 1.5 mm² H07RN-F in 20 mm conduit inside canopy void; through façade in sleeved hole, "
        "sealed. 12 V garden cable in 25 mm flexible duct 300 deep in planter.",
        "4. Driver location must be ventilated & accessible (utility, behind lattice door D03).",
        "5. Voltage drop on LS1 < 3%: feed from 2 points (NE corner & mid-front via void).",
        "6. Install draw-wires before soffit slats are fixed; test & label all circuits.",
    ], size=1.55, gap=0.35)
    return s


# ======================================================================= A-104 PLANTING & IRRIGATION
def sheet_a104(dxf=None):
    s = Sheet("A-104", "Planting & irrigation plan", "1:50")
    s.frame()
    v = View(s, 62, 34, 25, origin=(0, 300), dxf=dxf, dxf_offset=(80000, 0))
    # planter at 1:25 in two halves (north half then south half side by side)
    halves = [(0, -4200, 0), (-4200, -8400, 1)]
    for (ya, yb, k) in halves:
        vv = View(s, 40 + k * 95, 34, 25, origin=(-400, ya), dxf=None)
        vv.rect(-BW_T, yb - 150, BW_T, ya - yb + 150 + (FAC_T if k == 0 else 0), mat="masonry", w=0.4)
        vv.pl([(0, ya), (KERB_X0, ya), (KERB_X0, max(yb, PL_END_Y)), (0, max(yb, PL_END_Y))], w=0, mat="soil",
              opacity=0.5)
        vv.rect(COP_X0, yb if k == 0 else PL_SOUTH, COP_X1 - COP_X0, ya - (yb if k == 0 else PL_SOUTH), w=0.3,
                fill="#f3efe6")
        if k == 1:
            vv.rect(0, PL_SOUTH, COP_X1, 230, w=0.3, fill="#f3efe6")
        if k == 0:
            vv.rect(-BW_T, 0, 2200, FAC_T, mat="masonry", w=0.4)
            vv.rect(COP_X1, ya - 1, 1100, -0.01, w=0)
        # drip lines
        for dx in (230, 600):
            vv.line(dx, ya - 60 if k == 0 else ya, dx, max(yb, PL_END_Y + 60), w=0.25, color="#1f5fa8", dash="2,0.6")
        for (code, x, y, sp) in PLANTS:
            if yb <= y <= ya and code != "OL":
                vv.circle(x, y, sp / 2, w=0.18, color=GREEN, fill="#e3f0d8")
                vv.circle(x, y, 18, w=0, fill=GREEN)
                vv.text(x, y - 40, code, size=1.5, anchor="middle", weight="bold", color="#2c4a20")
        for (x, y, t) in UPLIGHTS:
            if yb <= y <= ya:
                vv.circle(x, y, 40, w=0.2, fill="#f39c12")
        for (x, y) in (P1, P2):
            if yb <= y <= ya:
                vv.rect(x - 80, y - 80, 160, 160, w=0.25, fill="#c39a6b")
                vv.rect(x - 60, y - 60, 120, 120, w=0.2, fill="#222")
        # wall wires
        vv.line(-15, ya, -15, max(yb, PL_END_Y), w=0.25, color="#7f8c8d", dash="0.5,0.8")
        if k == 0:
            vv.circle(1400, -650, 300, w=0.2, fill="#f7f7f4")
            vv.circle(1400, -650, 400, w=0.18, color=GREEN, fill="none", dash="1,0.6")
            vv.text(1400, -680, "OL", size=1.5, anchor="middle", weight="bold")
            vv.line(1100, -650, 850, -650, w=0.2, color="#1f5fa8", dash="1,0.5")
            vv.chain([0, P2[1], P1[1], -4200], "y", -BW_T, 7, size=1.5, overall=False)
        else:
            vv.chain([-4200, PL_END_Y, PL_SOUTH], "y", -BW_T, 7, size=1.5, overall=False)
        vv.dim((0, yb + 50 if k else ya - 200), (KERB_X0, yb + 50 if k else ya - 200), -4 if k else 4, size=1.4)
        s.text(vv.P(400, ya)[0], 30, "NORTH HALF (Y 0 → -4.2 m)" if k == 0 else "SOUTH HALF (Y -4.2 → -8.4 m)",
               size=1.7, anchor="middle", weight="bold")
    s.text(42, 270, "1/A-104  PLANTER PLANTING PLAN — 1:25 @ A3 (shown in two halves, north at top)", size=2.2,
           weight="bold")
    # schedule
    counts = {}
    for (code, *_r) in PLANTS:
        counts[code] = counts.get(code, 0) + 1
    rows = [[k, PLANT_SCHED[k][0], PLANT_SCHED[k][1], PLANT_SCHED[k][2], str(counts.get(k, 0)), PLANT_SCHED[k][3]]
            for k in PLANT_SCHED]
    s.table(162, 18, [("Code", 9), ("Botanical name", 38), ("Common", 24), ("Spec at planting", 25), ("Qty", 8),
                      ("Notes", 72)][:6], rows, size=1.5)
    s.textblock(162, 62, 176, [
        ("B", "SOIL & PLANTER BUILD-UP (see C-C / A-302)"),
        "Topsoil: 300 mm screened multipurpose topsoil BS 3882 / equiv. + 25% composted green waste, pH 6.5–7.5; "
        "50 mm composted bark mulch (10–40 mm) to finish +0.340 (60 below coping). Subsoil: loosen existing to 300 mm "
        "depth before backfilling. Drainage: 100 mm 10–20 mm clean gravel on geotextile at formation — no closed base.",
        ("B", "IRRIGATION"),
        "• 2 runs 16 mm inline drip pipe, 2.0 L/h PC drippers @ 330 c/c, laid on soil under mulch, pinned @ 1.0 m "
        "(total 2 x 8.2 m + 4 m to pot = 20.5 m).",
        "• 1 spur 4 mm to olive pot with 2 x 4 L/h stake drippers.",
        "• Header: 20 mm MDPE in 50 mm duct through façade at X = 300, from utility: stop-valve + double check "
        "valve (backflow) + 120-mesh filter + 2.0 bar regulator + 24 V solenoid + 2-zone controller with rain sensor.",
        "• Flush valve at south end of each run. Program: 2 x 15 min/day summer, 1 x 10 min spring/autumn.",
        ("B", "CLIMBER SUPPORT"),
        "• Posts: 4 no. 3 mm 316 SS wires per post, vertical, on 40 mm stand-off eyes @ 600 vertical; tensioner at top.",
        "• Boundary wall: horizontal 3 mm 316 SS wires @ 400 (+0.60, +1.00, +1.40, +1.75), vertical @ 1.5 m, "
        "eyes on M8 resin anchors; full 8.2 m length.",
        "• Façade W of D01: vertical wires @ 300, X = 100 → 1500, to +2.60.",
        ("B", "PLANTING NOTES"),
        "• Plant Sept–Nov or Mar–Apr. Water in thoroughly; 12-month establishment & defects period, replace failures.",
        "• Tie jasmine to wires on planting; train 2 leaders per post spiralling; pinch to keep fascia line clear.",
        "• Uplights UL1–UL6 set before mulching; aim after dark with client.",
        "• Olive pot: 600 Ø x 550 h fibre-clay, white, 50 mm drainage gravel, feet; loam-based compost (JI No.3).",
    ], size=1.55, gap=0.35)
    # legend
    lx, ly = 162, 238
    s.text(lx, ly, "LEGEND", size=1.8, weight="bold")
    s.line(lx, ly + 3, lx + 8, ly + 3, w=0.3, color="#1f5fa8", dash="2,0.6")
    s.text(lx + 10, ly + 3.6, "16 mm drip line", size=1.5)
    s.circle(lx + 4, ly + 7.5, 1.0, w=0.2, fill="#f39c12")
    s.text(lx + 10, ly + 8, "Uplight UL (see A-103)", size=1.5)
    s.line(lx, ly + 11.5, lx + 8, ly + 11.5, w=0.3, color="#7f8c8d", dash="0.5,0.8")
    s.text(lx + 10, ly + 12, "SS climbing wires on wall", size=1.5)
    s.circle(lx + 4, ly + 16, 1.6, w=0.2, color=GREEN, fill="#e3f0d8")
    s.text(lx + 10, ly + 16.5, "Plant (code), circle = spread at 3 yrs", size=1.5)
    s.north_arrow(320, 245, 5)
    return s
