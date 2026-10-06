"""Structural sheets, cover, specification, sequence & BOQ (Design A)."""
import math
from cad import Sheet, View, break_line, PROJECT
from common import *  # noqa
from design import *  # noqa
from axo import Axo, mbox, shade
from sheets_b import rhs


# ======================================================================= axonometric of design A
def axo_design_a(sheet, ox, oy, scale, grid=None):
    a = Axo(beta=28, elev=30)
    pat = grid or paving_pattern()
    # ground & pavers (layer 0)
    for j, row in enumerate(pat):
        for i, c in enumerate(row):
            x = PAV_X0 + i * PAVER
            y = -(j + 1) * PAVER
            a.poly3([(x, y, 0), (x + PAVER, y, 0), (x + PAVER, y + PAVER, 0), (x, y + PAVER, 0)], TONES[c][1],
                    stroke="#f4efe6", w=0.05, layer=0)
    for g in (G1, G2):
        a.poly3([(g[0] - 150, g[1] - 150, 2), (g[0] + 150, g[1] - 150, 2), (g[0] + 150, g[1] + 150, 2),
                 (g[0] - 150, g[1] + 150, 2)], "#6b6b6b", layer=0)
    # annex + roof
    mbox(a, -BW_T, 0, 0, COURT_W + EW_T + BW_T, 3000, FAC_PARAPET, "#f3ede2", layer=1, bias=-1e5)
    mbox(a, SOLAR[0], 1200, FAC_PARAPET, SOLAR[1] - SOLAR[0], 900, 500, "#9aa5ad", layer=1, bias=-1e5 + 10)
    # doors on façade (thin)
    for (x0, x1), col in ((D01, "#a9cde0"), (D02, "#5b4636"), (D03, "#b07a45")):
        mbox(a, x0, -25, 0, x1 - x0, 25, HEAD, col, layer=1, bias=-9e4)
    mbox(a, D01[0] + 60, -30, 30, D01[1] - D01[0] - 120, 5, HEAD - 100, "#cfe6f2", layer=1, bias=-8.9e4)
    for j in range(18):
        for i in range(6):
            pass
    mbox(a, AC1[0], -300, AC1[2], AC1[1] - AC1[0], 300, AC1[3] - AC1[2], "#efefef", layer=1, bias=-8e4)
    # boundary wall
    mbox(a, -BW_T, -8400, 0, BW_T, 8400, BW_TOP, "#efe7da", layer=1, bias=-1.2e5)
    # planter
    mbox(a, 0, PL_SOUTH, 0, KERB_X0, -PL_SOUTH, SOIL_TOP, "#7b5a3a", layer=1, bias=-7e4)
    mbox(a, KERB_X0, PL_SOUTH, 0, KERB_T, -PL_SOUTH, COP_TOP, "#f1ebdf", layer=1, bias=-6e4)
    mbox(a, 0, PL_SOUTH, 0, KERB_X0, 150, COP_TOP, "#f1ebdf", layer=1, bias=-5e4)
    # east wall (cutaway) & screen
    mbox(a, COURT_W, -EW_LEN, 0, EW_T, EW_LEN, 1000, "#e9e2d6", layer=2)
    mbox(a, COURT_W, -8400, 0, 100, 3000, 1000, "#a8723f", layer=2)
    # posts
    for (x, y) in (P2, P1):
        mbox(a, x - 80, y - 80, COP_TOP, 160, 160, SOFFIT - COP_TOP, "#c08a52", layer=2)
    # plants in planter
    rnd = random.Random(3)
    for (code, x, y, sp) in PLANTS:
        if code == "OL":
            continue
        h = {"TJ": 500, "PT": 450, "WF": 420, "RO": 450, "MY": 500, "LA": 300, "ER": 220}[code]
        a.blob(x, y, SOIL_TOP + h, sp * 0.6, fill="#6f9d58" if code != "LA" else "#8d9fc4", layer=2,
               flowers=6 if code in ("TJ", "MY", "ER", "PT") else 0, seed=int(-y) % 97)
    for (x, y) in (P1, P2):
        for z in range(700, SOFFIT, 260):
            a.blob(x + rnd.uniform(-90, 90), y - 90, z, 120, fill="#5f8f4b", layer=2, flowers=2, seed=z, bias=-5)
    for xx in range(CAN_X0, 2600, 180):
        a.blob(xx, CAN_Y1 + 40, FASCIA_TOP + 40, 110, fill="#5f8f4b", layer=3, flowers=2, seed=xx)
    for z in range(500, 2600, 280):
        a.blob(300, -60, z, 160, fill="#5f8f4b", layer=1, bias=-4e4, flowers=2, seed=z + 3)
    # olive pot
    mbox(a, 1400 - 300, -950, 0, 600, 600, 550, "#f4f4f2", layer=2)
    a.blob(1400, -650, 1500, 520, fill="#93a77a", layer=2, bias=-1, seed=8)
    # chair
    mbox(a, 1100, -1750, 0, 700, 750, 380, "#d9cbb5", layer=2)
    mbox(a, 1100, -1050, 380, 700, 120, 420, "#d9cbb5", layer=2)
    # canopy
    mbox(a, CAN_X0, CAN_Y1, FASCIA_BOT, CAN_X1 - CAN_X0, -CAN_Y1, FASCIA_TOP - FASCIA_BOT, "#ffffff", layer=4)
    a.poly3([(CAN_X0 + 50, CAN_Y1 + 50, FASCIA_TOP + 1), (CAN_X1 - 50, CAN_Y1 + 50, FASCIA_TOP + 1),
             (CAN_X1 - 50, -50, FASCIA_TOP + 1), (CAN_X0 + 50, -50, FASCIA_TOP + 1)], "#e4e7ea", layer=5)
    a.render(sheet, ox, oy, scale)


# ======================================================================= A-000 COVER
def sheet_a000(register):
    s = Sheet("A-000", "Cover sheet, drawing register & project information", "NTS")
    s.frame()
    s.text(16, 20, "COURTYARD CANOPY & GARDEN TERRACE", size=7, weight="bold")
    s.text(16, 28, "Construction drawing set — Design A (as client renders): timber-soffit steel canopy, raised "
                   "planter, 3-tone paving, lattice joinery", size=2.6)
    s.line(16, 31, 336, 31, w=0.6)
    axo_design_a(s, 88, 118, 60)
    s.text(16, 38, "AXONOMETRIC VIEW FROM SOUTH-EAST (east wall & screen shown cut away at 1.0 m) — NTS", size=1.8,
           weight="bold")
    # register
    x0 = 222
    s.text(x0, 40, "DRAWING REGISTER", size=2.4, weight="bold")
    rows = [[n, t] for (n, t) in register]
    s.table(x0, 42, [("No.", 16), ("Title", 100)], rows, size=1.5)
    s.textblock(16, 214, 200, [
        ("B", "PROJECT SUMMARY"),
        f"• Canopy: {(CAN_X1 - CAN_X0) / 1000:.2f} x {-CAN_Y1 / 1000:.2f} m flat steel canopy, 370 mm white "
        "aluminium fascia, thermo-ash slatted soffit with perimeter warm-white LED, membrane roof draining through "
        "post P1.",
        "• Structure: galvanised steel frame (UPN ledger, RHS beams, lipped-C joists) on 2 timber-clad posts; "
        "east corner by cantilever S1 (as render) or post P3 S2 (recommended where existing structure is unverified).",
        f"• Planter: {(-PL_SOUTH) / 1000:.1f} m long x 1.0 m raised RC planter, rendered, precast coping, drip "
        "irrigation, star jasmine & Mediterranean shrubs, 6 uplights.",
        f"• Paving: {(PAV_X1 - PAV_X0) * (-PAV_Y1) / 1e6:.1f} m² 200x200 concrete pavers in 3 tones, cross-falls to "
        "2 gullies + threshold slot drain.",
        "• Joinery: glazed alu door D01, roller shutter D02, timber lattice door D03, lattice screen & gate G01.",
        ("B", "STATUS"),
        "Issued for construction / tender, subject to: (1) measured & level survey, (2) structural engineer's "
        "design & sign-off, (3) any planning/building permit required locally, (4) utility survey before digging.",
    ], size=1.5, gap=0.35)
    return s


# ======================================================================= A-001 GENERAL NOTES & SPEC
def sheet_a001():
    s = Sheet("A-001", "General notes, assumptions & outline specification", "NTS")
    s.frame()
    col = 104
    c1 = [
        ("H", "1  GENERAL"),
        "1.1 These drawings define a buildable design derived from the client's concept renders. Dimensions "
        "marked existing are assumed and MUST be verified by a measured survey before fabrication.",
        "1.2 Datum ±0.000 = internal finished floor level at D01. All levels in metres, dimensions in mm.",
        "1.3 Work to comply with local building regulations, Eurocodes (EN 1990/1991/1993/1995/1992) or local "
        "equivalent, manufacturers' instructions and good practice.",
        "1.4 The contractor is responsible for temporary works, propping, setting out and site safety.",
        "1.5 Hold points (H) require designer / engineer inspection before proceeding — see A-002.",
        ("H", "2  KEY ASSUMPTIONS (VERIFY)"),
        "2.1 Courtyard 7.20 x 8.40 m between boundary wall and house wall; façade straight & plumb ±10 mm.",
        "2.2 Annex façade has an RC ring beam / lintel at +2.40 to +2.95 suitable for M12 resin anchors "
        "(else: through-bolts with backing plates or independent post line — consult engineer).",
        "2.3 Ground: firm natural soil, allowable bearing ≥ 100 kPa at -0.90; no services in footing zones.",
        "2.4 Snow 1.0 kN/m², peak wind pressure 0.70 kN/m² (sheltered courtyard). Adjust to site.",
        "2.5 Existing walls are sound; boundary wall ownership/party-wall consent confirmed by client.",
        ("H", "3  DEMOLITION & PREPARATION"),
        "3.1 Remove existing paving / topsoil in work area to formation (-0.25 under paving, -0.30 in planter).",
        "3.2 Protect façade, doors, AC units & solar heater pipework; isolate external circuits.",
        "3.3 Locate & mark all buried services (CAT scan) before excavation.",
        ("H", "4  CONCRETE"),
        "4.1 Footings C25/30 XC2, kerb upstand C30/37 XC4/XF1, blinding C12/15. Max aggregate 20 mm, S3.",
        "4.2 Reinforcement B500B, cover 50 (cast against blinding 40), 40 for kerb. Laps 50Ø.",
        "4.3 Cure 7 days min; no loading of pads before 7 days / 70 % strength.",
        ("H", "5  STRUCTURAL STEEL — see S-001"),
        "5.1 Fabrication to EN 1090-2 EXC2, CE marked; shop drawings to engineer for approval before fabrication.",
        "5.2 All steel hot-dip galvanised; visible posts (Option B) duplex coated RAL 9010.",
        ("H", "6  ROOFING"),
        "6.1 18 mm marine ply (EN 636-3) on C24 tapered firrings; 1.5 mm TPO fully bonded; 150 upstands.",
        "6.2 Gutter/outlet/overflow per A-102 & D3; 24 h flood test (H).",
    ]
    c2 = [
        ("H", "7  CARPENTRY & SOFFIT"),
        "7.1 Thermo-ash (or WRC) 68x20 slats @ 78 pitch on 50x38 battens; oil finish all faces pre-fixing.",
        "7.2 Post cladding 20 mm boards, mitred, SS fixings, 30 mm gap above base plate.",
        ("H", "8  METALWORK & FASCIA"),
        "8.1 3 mm aluminium fascia/capping, RAL 9010 matt, concealed fixings; bimetallic isolation.",
        ("H", "9  MASONRY / RENDER"),
        "9.1 Kerb external faces: 2-coat render 15 mm, cream masonry paint (sample panel 1 m² for approval).",
        "9.2 Boundary wall & façade: repair cracks, 1 coat stabiliser + 2 coats acrylic masonry paint.",
        ("H", "10 PAVING & DRAINAGE — see A-101 / A-302"),
        "10.1 200x200x60 pavers, 3 tones laid to colour map; Type 1 sub-base 150; falls 1:80 / 1:60.",
        "10.2 SD1 slot drain, G1/G2 gullies, Ø110 PVC-U SN8 to soakaway/SW drain; CCTV or air test before backfill.",
        ("H", "11 SOFT LANDSCAPE & IRRIGATION — see A-104"),
        "11.1 Topsoil BS 3882 + compost; plants to schedule; 12-month establishment & replacement.",
        "11.2 Drip irrigation with controller, backflow protection & rain sensor.",
        ("H", "12 ELECTRICAL & LIGHTING — see A-103"),
        "12.1 Licensed electrician; RCBO protection; IP65+ fittings; test certificate on completion.",
        ("H", "13 JOINERY — see A-600"),
        "13.1 D01 alu glazed door, D02 insulated roller shutter, D03 lattice door, G01 screen/gate.",
        ("H", "14 TOLERANCES"),
        "14.1 Steel: ±3 mm positions, ±2 mm levels at bearings. Fascia line ±3 mm over 3 m.",
        "14.2 Soffit plane ±3 mm / 3 m, slat gaps 10 ±1 mm. Paving ±3 mm / 3 m.",
        ("H", "15 MAINTENANCE"),
        "15.1 Gutter & outlet: clean every 3 months (needles from pines!). Re-oil timber 2–3 yrs.",
        "15.2 Inspect membrane & sealants annually; prune vines off membrane; flush drip lines each spring.",
        ("H", "16 OPTIONS"),
        "OPT-A posts timber-clad (render 1) | OPT-B posts white SHS 150 (render 2)",
        "S1 cantilever east corner (as render) | S2 post P3 (lower cost, no work to existing structure)",
        ("H", "ABBREVIATIONS"),
        "BOS bottom of steel · TOS top of steel · FFL finished floor level · HDG hot-dip galvanised · RWP rainwater "
        "pipe · S.O. structural opening · MJ movement joint · c/c centres · FP fin plate · PL plate · TBM temporary "
        "bench mark · SW surface water · FF&E furniture, fixtures & equipment.",
    ]
    s.textblock(16, 14, col, c1, size=1.6, gap=0.3)
    s.textblock(16 + col + 8, 14, col, c2, size=1.6, gap=0.3)
    s.textblock(16 + 2 * (col + 8), 14, 100, [
        ("H", "MATERIAL & COLOUR SCHEDULE"),
    ], size=1.6)
    rows = [
        ["Fascia / capping", "Alu 3 mm", "RAL 9010 matt"],
        ["Soffit / cladding", "Thermo-ash", "Natural oil"],
        ["Posts Opt-B", "Steel duplex", "RAL 9010"],
        ["D01 frame", "Aluminium", "RAL 8019 / bronze"],
        ["D02 shutter", "Aluminium", "RAL 8019 matt"],
        ["D03 / G01", "Thermo-ash / iroko", "Teak-tone oil"],
        ["Kerb & walls", "Render + paint", "Warm white / cream"],
        ["Coping", "Precast recon. stone", "Cream / sand"],
        ["Pavers S", "Concrete", "Sand / cream"],
        ["Pavers B", "Concrete", "Buff / beige"],
        ["Pavers G", "Concrete", "Grey-taupe"],
        ["Grates", "Stainless / DI", "Satin / black"],
        ["LED", "24 V strip", "2700 K, CRI 90"],
    ]
    s.table(16 + 2 * (col + 8), 24, [("Element", 34), ("Material", 32), ("Finish", 32)], rows, size=1.5)
    y = 24 + 4 + 13 * 3.6 + 8
    sw = [("#ffffff", "RAL 9010"), ("#e7c79a", "Thermo-ash"), ("#5a4a3c", "RAL 8019"), ("#b07a45", "Lattice"),
          ("#f3ede2", "Render"), ("#e6d6bb", "Paver S"), ("#cdb48f", "Paver B"), ("#a39c98", "Paver G")]
    for i, (c, n) in enumerate(sw):
        xx = 16 + 2 * (col + 8) + (i % 4) * 25
        yy = y + (i // 4) * 14
        s.rect(xx, yy, 20, 8, lw=0.2, fill=c)
        s.text(xx, yy + 11, n, size=1.4)
    return s


# ======================================================================= A-002 SEQUENCE & QA
def sheet_a002():
    s = Sheet("A-002", "Construction sequence, hold points & programme", "NTS")
    s.frame()
    steps = [
        ["1", "Survey & approvals", "Measured + level survey; structural survey of annex (slab, ring beam, pier); "
         "utility scan; engineer confirms S1 or S2; shop drawings approved.", "H1 survey review", "1 wk"],
        ["2", "Ordering", "Steel (2–3 wk), D01/D02 (4–6 wk), joinery D03/G01 (3–4 wk), pavers (1–2 wk), plants.",
         "Samples approved", "—"],
        ["3", "Site set-up & strip", "Protect façade/doors/AC; strip paving & topsoil to formation; set TBM.", "", "2 d"],
        ["4", "Excavate & drainage", "Dig footings, kerb trench, gully & pipe trenches; lay Ø110 drains, IC1, SA1.",
         "H2 formation & drains test", "3 d"],
        ["5", "Concrete 1", "Blinding; pads F1/F2 with cast-in RWP bend; kerb strip footing; HD bolts by template.",
         "H3 rebar & bolt positions", "2 d"],
        ["6", "Concrete 2", "Pedestals; kerb upstand (MJ @ 4.2 m); cure 7 days.", "H4 kerb line & level", "2 d"],
        ["7", "Steel erection", "Ledger anchors (pull-test 3 no.); posts plumb & grout; beams, joists; bolts torqued.",
         "H5 steel inspection", "2 d"],
        ["8", "Roof", "Firrings, ply deck, gutter, outlet, TPO, flashings; overflow.", "H6 24 h flood test", "3 d"],
        ["9", "1st fix services", "LED/downlight cabling in void, conduit through façade, drivers in utility; irrigation "
         "header sleeve.", "H7 1st fix inspection", "1 d"],
        ["10", "Soffit & fascia", "Battens, insect fleece, LED profiles, slats; fascia/capping; post cladding.",
         "Mock-up 1 m² approved", "4 d"],
        ["11", "Planter", "Tanking, drainage sheet, gravel, geotextile, topsoil; coping; render & paint.", "", "3 d"],
        ["12", "Paving", "Sub-base, slot drain, gullies, bedding, pavers to colour map, jointing, vibrate.",
         "H8 levels & falls", "4 d"],
        ["13", "Joinery", "Install D01, D02 (motor), D03, G01 screen & gate.", "", "2 d"],
        ["14", "Planting & irrigation", "Wires, plants, drip lines, controller, mulch, uplights aimed.", "", "2 d"],
        ["15", "2nd fix & test", "Connect fittings, test & certify, program controls; snag; clean.",
         "H9 handover", "2 d"],
    ]
    s.table(16, 16, [("#", 7), ("Stage", 34), ("Work", 180), ("Hold point / QA", 52), ("Dur.", 14)], steps,
            size=1.6)
    s.textblock(16, 200, 320, [
        ("B", "PROGRAMME"),
        "Indicative site duration ≈ 6–7 weeks after a 4–6 week procurement period (doors are the long lead). "
        "Stages 9–14 overlap where trades allow. Weather windows: membrane & concrete not below +5 °C or in rain.",
        ("B", "HEALTH & SAFETY"),
        "Working at height (canopy at +3.0 m): mobile towers / scaffold with guard-rails, no work from ladders on "
        "deck. Lifting: beams ≤ 140 kg (B2 S1 ≈ 380 kg — use hoist / 2-man lift with lifting aid). Excavations "
        "> 1.2 m none planned. Silica dust: wet-cut pavers & coping. Electrical: isolate & lock-off; RCD tools.",
        ("B", "HANDOVER DOCUMENTS"),
        "As-built drawings, steel & galvanising certificates, membrane warranty, electrical certificate, door/motor "
        "manuals, irrigation programme, plant list & maintenance schedule (A-001 §15).",
    ], size=1.6, gap=0.35)
    return s


# ======================================================================= S-001 STRUCTURAL NOTES & CALCS
def sheet_s001():
    c = calcs()
    s = Sheet("S-001", "Structural design basis, loads & preliminary member checks", "NTS", series="STRUCTURAL")
    s.frame()
    s.textblock(16, 14, 150, [
        ("H", "DESIGN BASIS"),
        "• Codes: EN 1990, EN 1991-1-1/-1-3/-1-4, EN 1993-1-1/-1-3/-1-8, EN 1992-1-1, EN 1997-1 (or local "
        "equivalents & National Annex values). Consequence class CC1, design life 50 yrs.",
        "• Structural system: steel grillage — UPN ledger on façade (pinned), RHS perimeter beams, lipped-C joists "
        "spanning N–S, posts P1/P2 pinned at base. Plywood deck forms a horizontal diaphragm, transferring wind & "
        "notional loads to the façade ledger (façade = lateral restraint).",
        "• East front corner: S1 = cantilever B2 with back-span into annex (as render) | S2 = post P3 (alt.).",
        ("H", "CHARACTERISTIC LOADS"),
        f"• Permanent gk = {LOADS['gk_area']:.2f} kN/m² (steel 0.20, deck 0.15, membrane 0.03, soffit 0.15, "
        f"services 0.02, vines 0.10) + fascia line {LOADS['gk_fascia']:.2f} kN/m.",
        f"• Imposed (roof cat. H, not combined with snow) qk = {LOADS['qk']:.2f} kN/m², Qk = 1.0 kN.",
        f"• Snow sk = {LOADS['sk']:.2f} kN/m² (ASSUMED — engineer to set from altitude/zone; check drift against "
        "annex parapet).",
        f"• Wind: qp = 0.70 kN/m² ASSUMED; canopy net cp,net = -1.3 (uplift) / +0.8 → wk,up = {LOADS['wk_up']:.2f} kN/m².",
        ("H", "COMBINATIONS"),
        f"• ULS gravity 1.35G + 1.5S = {c['uls']:.2f} kN/m²   • SLS G + S = {c['sls']:.2f} kN/m²",
        f"• ULS uplift 1.0G – 1.5W = {c['uplift']:.2f} kN/m² (net upward) → HD bolts & pad self-weight checked.",
        ("H", "DEFLECTION LIMITS"),
        "• Beams L/250 total, L/360 variable; cantilever L/180 (2L/360). Fascia line: precamber B2 (S1) 8 mm.",
    ], size=1.55, gap=0.3)
    rows = c["rows"]
    s.table(16, 128, [("Member", 30), ("Section / spec", 70), ("Span / case", 40), ("MEd / action", 22),
                      ("Resistance", 34), ("Util.", 12), ("Deflection / note", 50)], rows, size=1.45)
    s.textblock(176, 14, 160, [
        ("H", "MATERIALS"),
        "• Hollow sections S355J2H EN 10219; UPN & plates S275JR EN 10025-2; cold-formed C S350GD+Z275 EN 10346.",
        "• Bolts 8.8 HDG EN 15048 / ISO 4014; HD bolts M16 8.8 HDG; resin anchors with ETA (e.g. vinylester / epoxy, "
        "M12 x 110 into C20/25+ concrete, characteristic tension ≥ 15 kN — pull-test 3 no. to 1.5 x working load).",
        "• Welds: fillet 6 mm min. all-round to base & cap plates, E42 electrodes; FPs 12 mm.",
        "• Concrete C25/30 (pads), C30/37 (kerb); reinforcement B500B.",
        ("H", "CONNECTION SCHEDULE (see S-101)"),
        "C1 J1→L1: FP 8x100x170 welded to UPN web, 2 M12 8.8 through J1 web.",
        "C2 J1→B1: FP 8 shop-welded to B1 web, 2 M12 8.8.",
        "C3 B1/B3→P1: FP 12 shop-welded to P1 faces into slotted beam ends, 2 M16 8.8 + 12 mm plug welds.",
        "C4 B3→P2: B3 continuous over P2 cap PL 200x200x12, 4 M12 8.8 through-bolts with spacer tubes.",
        "C5 B3/B2→façade: end PL 10 bolted to UPN / wall via 4 M12 resin anchors.",
        "C6 B2 (S1): padstone bearing + tail PL 250x250x15, 4 M16 resin anchors to slab soffit, grout pack.",
        "C7 B2→P3 (S2): as C3.",
        "C8 Base plates: PL 250x250x15, 4 M16 HD bolts 180 c/c, 30 grout.",
        ("H", "FOUNDATIONS"),
        "F1/F2 (F3 for S2): 800x800x700 pad, underside ≥ -0.90 (or to frost depth / firm stratum); "
        "Ø12 @ 150 both ways bottom; 300x300 pedestal to +0.390. Blind 50 C12/15.",
        ("H", "ENGINEER TO CONFIRM"),
        "Existing ring beam & anchor capacity; S1 back-span reaction on slab & pier; site snow/wind; soil bearing; "
        "diaphragm fixings (ply to steel: 4.8 self-drilling @ 150 edges / 300 field).",
    ], size=1.5, gap=0.3)
    return s


# ======================================================================= S-100 FRAMING PLAN
def sheet_s100(dxf=None):
    s = Sheet("S-100", "Canopy steel framing plan & foundation plan", "1:25 / 1:50", series="STRUCTURAL")
    s.frame()
    v = View(s, 40, 72, 25, origin=(0, 0), dxf=dxf, dxf_offset=(0, -80000))
    # façade
    v.rect(-BW_T, 0, 5900, FAC_T, mat="masonry", w=0.3)
    v.rect(-BW_T, FAC_T, 5900, 650, w=0.1, fill="#f6f6f6", color="#aaa")
    v.text(2700, FAC_T + 380, "EXISTING ANNEX (S1 back-span dashed, continues to +2.30 m — D7/A-501)", size=1.6,
           anchor="middle", color="#777")
    # ledger
    v.rect(J_X0, -75, J_X1 - J_X0, 75, w=0.3, fill="#5c6670", layer="S-STEEL")
    # beams
    v.rect(B3_X[0], B1_Y[0], 100, -B1_Y[0] - 0, w=0.35, fill="#7d8790", layer="S-STEEL")
    v.rect(P1[0] + 60, B1_Y[1], P3[0] - P1[0] - 160, 100, w=0.35, fill="#7d8790", layer="S-STEEL")
    v.rect(B2_X[0], B1_Y[1], 200, -B1_Y[1], w=0.35, fill="#7d8790", layer="S-STEEL")
    v.rect(B2_X[0], FAC_T, 200, 650, w=0.25, dash="2,1", color="#c0392b")
    # joists
    for x in JOISTS:
        v.rect(x - 32, B1_Y[0], 65, -B1_Y[0] - 75, w=0.2, fill="#c9d0d6", layer="S-STEEL")
    # posts
    for (x, y), lab in ((P1, "P1"), (P2, "P2")):
        v.rect(x - 60, y - 60, 120, 120, w=0.3, fill="#222", layer="S-STEEL")
    v.rect(P3[0] - 60, P3[1] - 60, 120, 120, w=0.3, dash="1,0.6", color="#c0392b")
    # grids
    v.grid(600, 1150, 600, -3500, "1", end="start")
    v.grid(5200, 1150, 5200, -3500, "2", end="start")
    v.grid(-450, 0, 5900, 0, "A", end="start")
    v.grid(-450, -1400, 5900, -1400, "B", end="start")
    v.grid(-450, -3050, 5900, -3050, "C", end="start")
    # marks
    v.tag(2900, -3050, "B1", shape="rect", r=2.0, size=1.6)
    v.tag(600, -700, "B3", shape="rect", r=2.0, size=1.6)
    v.tag(600, -2250, "B3", shape="rect", r=2.0, size=1.6)
    v.tag(5200, -1500, "B2", shape="rect", r=2.0, size=1.6)
    v.tag(2900, -40, "L1", shape="rect", r=2.0, size=1.6)
    for i, x in enumerate(JOISTS):
        v.tag(x, -1700, "J1", shape="rect", r=1.6, size=1.2)
    for (x, y), lab in ((P1, "P1"), (P2, "P2"), (P3, "P3")):
        v.tag(x - 350, y + 250, lab, shape="circle", r=2.2, size=1.6)
    for (x, y, lab) in ((J_X0 + 200, -60, "C5"), (2319, -110, "C1"), (2319, -2970, "C2"), (P1[0] + 200, P1[1] + 150, "C3"),
                        (P2[0] + 200, P2[1] + 150, "C4"), (5200, 150, "C6"), (5050, -3200, "C7")):
        v.tag(x, y, lab, shape="hex", r=1.8, size=1.2, fill="#fff3cd")
    v.chain([CAN_X0, P1[0], P1[0] + 60] + [round(x) for x in JOISTS] + [B2_X[0], P3[0], CAN_X1], "x", CAN_Y1, -8,
            size=1.2)
    v.chain([FAC_T, 0, P2[1], P1[1], CAN_Y1], "y", CAN_X1, -16, size=1.4, overall=False)
    s.text(16, 236, "SCHEME S1 (as render): B2 cantilever SHS 200x200x12.5 + 2.0 m back-span (red dashed).", size=1.6,
           weight="bold")
    s.text(16, 241, "SCHEME S2 (alternative): add post P3 + pad F3 (red dashed square); B2 becomes RHS 200x100x6.3 "
                   "simply supported. Engineer to select after survey.", size=1.6, color="#c0392b")
    v.title(16, 218, "1/S-100", "CANOPY FRAMING PLAN @ TOS +2.910", "1:25 @ A3", sub="all steel top-flush, BOS +2.710")
    s.textblock(16, 248, 320, [
        "Plywood deck diaphragm: 18 mm ply fixed to J1/beams with 4.8 mm self-drilling wood-to-steel screws @ 150 edges "
        "/ 300 field. All steel HDG. Temporary bracing until deck fixed. Connections C1–C8: see S-101. Foundations: "
        "see S-101 foundation plan & D1/A-500.",
    ], size=1.6)
    return s


# ======================================================================= S-101 CONNECTIONS
def sheet_s101():
    s = Sheet("S-101", "Typical steel connection details", "1:5 / 1:10", series="STRUCTURAL")
    s.frame()

    def title(x, y, t):
        s.text(x, y, t, size=1.8, weight="bold")

    # C1 joist to ledger elevation 1:5 (u = Y)
    v = View(s, 50, 62, 10, origin=(0, 2700))
    v.rect(0, 2600, 120, 420, mat="rc", w=0.3)
    v.pl([(0, BOS), (-75, BOS), (-75, BOS + 11.5), (-8.5, BOS + 11.5), (-8.5, TOS - 11.5), (-75, TOS - 11.5),
          (-75, TOS), (0, TOS)], w=0.25, mat="steel")
    v.rect(-200, BOS + 30, 192, 140, w=0.2, fill="#bbb")
    v.rect(-300, BOS, 230, 200, w=0.15, fill="#e6eaee", color="#666")
    for z in (BOS + 70, BOS + 130):
        v.circle(-150, z, 7, w=0.2, fill="#777")
        v.rect(-8.5, z - 6 + 10, 110, 12, w=0.1, fill="#888")
    v.leader([(-100, BOS + 170), (-260, 3000)], ["FP 8x170x140 shop-welded 6 FW to UPN web"], size=1.3,
             anchor="start")
    v.leader([(-150, BOS + 70), (-260, 2640)], ["2 M12 8.8 through J1 web, 35 edge"], size=1.3, anchor="start")
    v.leader([(60, BOS + 140), (40, 3060)], ["M12 resin anchor"], size=1.3, anchor="start")
    v.dim((-150, BOS + 70), (-150, BOS + 130), 8, size=1.2)
    title(16, 18, "C1  J1 → LEDGER L1 — 1:10")

    # C3 beam to post elevation 1:5 (u = X)
    c = View(s, 128, 62, 10, origin=(600, 2700))
    c.rect(540, 2600, 120, 330, w=0.3, fill="#5c6670")
    c.rect(546, 2600, 108, 324, w=0.1, fill="#fff")
    c.rect(530, TOS, 140, 12, w=0.25, fill="#5c6670")
    c.circle(600, TOS + 6, 38, w=0.2, color="#1f5fa8")
    c.rect(660, BOS + 40, 110, 120, w=0.25, fill="#bbb")
    c.rect(670, BOS, 220, 200, w=0.3, fill="#7d8790")
    c.rect(676, BOS + 6, 214, 188, w=0.1, fill="#fff")
    c.rect(670, BOS + 94, 110, 12, w=0.1, fill="#444")
    for z in (BOS + 70, BOS + 130):
        c.circle(730, z, 9, w=0.2, fill="#777")
    c.leader([(700, BOS + 160), (780, 3010)], ["FP 12x120x110 welded to P1, 6 FW"], size=1.3, anchor="start")
    c.leader([(730, BOS + 70), (800, 2630)], ["2 M16 8.8 through slotted B1"], size=1.3, anchor="start")
    c.leader([(600, TOS + 12), (480, 3010)], ["Cap PL 12, Ø80 hole for RWP"], size=1.3, anchor="end")
    title(100, 18, "C3  B1 → P1 (B3 similar) — 1:10")

    # C4 B3 over P2 cap 1:5 (u = Y)
    d = View(s, 250, 62, 10, origin=(-1400, 2700))
    d.rect(-1460, 2560, 120, 150, w=0.3, fill="#5c6670")
    d.rect(-1500, BOS - 12, 200, 12, w=0.25, fill="#5c6670")
    d.rect(-1650, BOS, 500, 200, w=0.3, fill="#7d8790")
    for y in (-1460, -1340):
        d.rect(y - 6, BOS - 12, 12, 224, w=0.15, fill="#888")
        d.rect(y - 12, TOS, 24, 10, w=0.1, fill="#444")
    d.leader([(-1340, TOS), (-1250, 3020)], ["4 M12 8.8 through-bolts + 25 spacer tubes"], size=1.3, anchor="start")
    d.leader([(-1400, BOS - 6), (-1250, 2620)], ["Cap PL 200x200x12"], size=1.3, anchor="start")
    title(205, 18, "C4  B3 continuous over P2 — 1:10")

    # C8 base plate plan 1:5
    b = View(s, 60, 165, 5, origin=(0, 0))
    b.rect(-125, -125, 250, 250, w=0.35, fill="#5c6670")
    b.rect(-60, -60, 120, 120, w=0.3, fill="#7d8790")
    b.rect(-53.7, -53.7, 107.4, 107.4, w=0.1, fill="#fff")
    b.circle(0, 0, 40, w=0.25, color="#1f5fa8")
    for x in (-90, 90):
        for y in (-90, 90):
            b.circle(x, y, 11, w=0.25, fill="#fff")
            b.circle(x, y, 8, w=0.2, fill="#777")
    b.chain([-125, -90, 90, 125], "x", -125, -5, size=1.2)
    b.chain([-125, -90, 90, 125], "y", -125, 5, size=1.2, overall=False)
    b.leader([(90, 90), (160, 160)], ["4 M16 HD bolts in Ø22 holes,", "plate washers 50x50x6"], size=1.3,
             anchor="start")
    b.leader([(0, 40), (160, 60)], ["Ø80 hole (P1 RWP)"], size=1.3, anchor="start")
    title(16, 120, "C8  BASE PLATE PL 250x250x15 — plan 1:5")

    # C6 S1 tail 1:10 (plan of anchors) + C5
    t = View(s, 170, 170, 10, origin=(0, 0))
    t.rect(-125, -125, 250, 250, w=0.35, fill="#5c6670")
    t.rect(-100, -125, 200, 250, w=0.2, fill="#7d8790")
    for x in (-90, 90):
        for y in (-90, 90):
            t.circle(x, y, 10, w=0.2, fill="#777")
    t.leader([(90, 90), (160, 150)], ["4 M16 resin anchors into slab soffit", "(S1 tail, engineer to verify)"],
             size=1.3, anchor="start")
    title(140, 120, "C6  S1 TAIL PLATE — plan 1:10")
    # foundation plan 1:50
    f = View(s, 30, 208, 50, origin=(0, 0))
    f.rect(-BW_T, -3650, BW_T, 3650 + FAC_T, mat="masonry", w=0.3)
    f.rect(-BW_T, 0, 5900, FAC_T, mat="masonry", w=0.3)
    f.rect(KERB_X0 - 75, -3650, KERB_FTG_W, 3650, w=0.2, fill="#e2e2df")
    for (x, y), lab in ((P1, "F1"), (P2, "F2")):
        f.rect(x - 400, y - 400, 800, 800, w=0.35, fill="#cfcfcf")
        f.rect(x - 150, y - 150, 300, 300, w=0.25, fill="#999")
        f.text(x, y - 650, lab, size=1.6, anchor="middle", weight="bold")
    f.rect(P3[0] - 400, P3[1] - 400, 800, 800, w=0.3, dash="1.5,0.8", color="#c0392b")
    f.text(P3[0], P3[1] - 650, "F3 (S2)", size=1.5, anchor="middle", color="#c0392b")
    f.chain([0, 200, 1000], "x", -3650, -4, size=1.3, overall=False)
    f.chain([0, P2[1], P1[1]], "y", -BW_T, 6, size=1.3, overall=False)
    s.text(16, 199, "FOUNDATION PLAN — 1:50", size=1.9, weight="bold")
    s.text(150, 205, "MEMBER SCHEDULE", size=1.9, weight="bold")
    rows = [
        ["L1", "UPN 200 S275 HDG", "1", f"{(J_X1 - J_X0) / 1000:.2f}", "25.3", f"{25.3 * (J_X1 - J_X0) / 1000:.0f}"],
        ["B1", "RHS 200x100x6.3 S355", "1", f"{(P3[0] - P1[0] - 160) / 1000:.2f}", "28.1",
         f"{28.1 * (P3[0] - P1[0] - 160) / 1000:.0f}"],
        ["B2 (S1)", "SHS 200x200x12.5 S355", "1", f"{(B2_TAIL - B1_Y[1]) / 1000:.2f}", "71.6",
         f"{71.6 * (B2_TAIL - B1_Y[1]) / 1000:.0f}"],
        ["B2 (S2)", "RHS 200x100x6.3 S355", "1", f"{-B1_Y[1] / 1000:.2f}", "28.1", f"{28.1 * -B1_Y[1] / 1000:.0f}"],
        ["B3", "RHS 200x100x5 S355", "1", f"{-B1_Y[0] / 1000:.2f}", "22.6", f"{22.6 * -B1_Y[0] / 1000:.0f}"],
        ["J1", "Lipped C 200x65x20x1.8", str(len(JOISTS)), "2.92", "5.0", f"{5.0 * 2.92 * len(JOISTS):.0f}"],
        ["P1/P2", "SHS 120x120x6.3 S355", "2", "2.48", "21.4", f"{21.4 * 2.48 * 2:.0f}"],
        ["P3 (S2)", "SHS 120x120x6.3 S355", "1", "2.48", "21.4", f"{21.4 * 2.48:.0f}"],
        ["Plates", "Base/cap/FP/tail plates", "—", "—", "—", "≈ 45"],
    ]
    s.table(150, 208, [("Mark", 16), ("Section", 52), ("No.", 9), ("L (m)", 14), ("kg/m", 13), ("Mass kg", 16)],
            rows, size=1.45)
    s.textblock(150, 252, 186, [
        "Total steel ≈ 1.0 t (S1) / 0.7 t (S2) incl. plates — galvanise as 1 batch. Mark all members per this "
        "schedule; bolt sets bagged & labelled per connection.",
    ], size=1.5)


    s.textblock(222, 120, 116, [
        ("B", "FABRICATION NOTES"),
        "• Shop-weld all fin plates, cap & base plates; site connections bolted only (no site welding).",
        "• Slotted ends of RHS for fin plates: slot width 14 for FP 12, seal ends with 3 mm cap plates welded "
        "(galvanising vent holes Ø10 at ends, plug after).",
        "• Bolt holes: +2 mm clearance (M12 → Ø14, M16 → Ø18); slotted holes in FP for ±5 mm tolerance at L1.",
        "• Pre-camber B2 (S1) 8 mm at tip — confirm with engineer.",
        "• Torque 8.8 bolts to snug-tight + ¼ turn (non-preloaded).",
        "• Provide temporary bracing until deck diaphragm is fixed.",
    ], size=1.45, gap=0.3)
    return s


# ======================================================================= Q-001 BOQ
def boq_rows():
    grid = paving_pattern()
    n = sum(len(r) for r in grid)
    area = (PAV_X1 - PAV_X0) * (-PAV_Y1) / 1e6
    can = (CAN_X1 - CAN_X0) * (-CAN_Y1) / 1e6
    rows = [
        ["1", "PRELIMINARIES & SURVEY", "", "", ""],
        ["1.1", "Measured, level & structural survey; utility scan", "item", "1", ""],
        ["1.2", "Site set-up, protection, skip hire, clean", "item", "1", ""],
        ["2", "EARTHWORKS & DRAINAGE", "", "", ""],
        ["2.1", "Strip paving/topsoil to formation, dispose", "m³", f"{area * 0.25 + 8.4 * 0.85 * 0.3:.1f}", ""],
        ["2.2", "Excavate pads F1/F2 (+F3 S2) 0.8x0.8x0.95", "m³", f"{0.8 * 0.8 * 0.95 * 2:.2f}", ""],
        ["2.3", "Excavate kerb strip footing 0.45 wide", "m³", f"{8.55 * 0.45 * 0.65:.2f}", ""],
        ["2.4", "Ø110 PVC-U SN8 drain incl. bedding & surround", "m", "22", ""],
        ["2.5", "SD1 slot drain 100 mm, B125, incl. outlet", "m", "5.0", ""],
        ["2.6", "Yard gully 300 with silt bucket & grate", "no", "2", ""],
        ["2.7", "IC1 inspection chamber Ø450", "no", "1", ""],
        ["2.8", "SA1 soakaway crate 1.0 m³ incl. geotextile (or connect to SW)", "item", "1", ""],
        ["3", "CONCRETE", "", "", ""],
        ["3.1", "Blinding C12/15 50 mm", "m²", f"{0.9 * 0.9 * 2 + 8.55 * 0.45:.1f}", ""],
        ["3.2", "Pads C25/30 800x800x700 incl. rebar Ø12 @150 BW", "no", "2 (+1 S2)", ""],
        ["3.3", "Pedestals 300x300 incl. 4Ø12 + links, cast-in bolts", "no", "2 (+1 S2)", ""],
        ["3.4", "Kerb strip footing 450x250 C25/30, 3Ø12", "m", "8.55", ""],
        ["3.5", "Kerb upstand 135x(1050) C30/37 incl. Ø10 @300", "m", "8.55 + 0.85", ""],
        ["4", "STRUCTURAL STEEL (S-100)", "", "", ""],
        ["4.1", "Supply, fabricate, HDG & erect steel per schedule (S1)", "t", "1.0", ""],
        ["4.1a", "Alternative S2 (incl. P3) — deduct/add", "t", "0.7", ""],
        ["4.2", "M12 resin anchors to façade incl. pull tests", "no", "30", ""],
        ["4.3", "S1 padstone + tail anchorage + bulkhead", "item", "1", ""],
        ["5", "ROOFING", "", "", ""],
        ["5.1", "Tapered firrings C24", "m", f"{len(JOISTS) * 3 + 6:.0f}", ""],
        ["5.2", "18 mm marine plywood deck", "m²", f"{can:.1f}", ""],
        ["5.3", "1.5 mm TPO membrane incl. upstands, gutter lining", "m²", f"{can + 3.5:.1f}", ""],
        ["5.4", "Outlet O1 Ø63 + leaf guard; overflow scupper", "item", "1", ""],
        ["5.5", "Alu counter-flashing chased to façade", "m", "4.9", ""],
        ["6", "FASCIA, SOFFIT & CLADDING", "", "", ""],
        ["6.1", "3 mm alu fascia & capping RAL 9010, 370 high", "m", f"{(CAN_X1 - CAN_X0 - CAN_Y1 * 2) / 1000:.1f}", ""],
        ["6.2", "Soffit battens 50x38 treated", "m", f"{(len(JOISTS) + 4) * 3.1:.0f}", ""],
        ["6.3", "Thermo-ash slats 68x20 (+10% waste)", "m", f"{can / 0.078 * 1.1:.0f}", ""],
        ["6.4", "Black insect fleece", "m²", f"{can:.1f}", ""],
        ["6.5", "Post cladding 20 mm thermo-ash, 160 sq, h 2.25", "no", "2", ""],
        ["7", "PLANTER & WALLS", "", "", ""],
        ["7.1", "Tanking slurry + HDPE drainage sheet", "m²", f"{8.25 * 0.75 + 8.4 * 0.75:.1f}", ""],
        ["7.2", "Drainage gravel 100 + geotextile", "m²", f"{0.85 * 8.25:.1f}", ""],
        ["7.3", "Topsoil + compost (450) & mulch (50)", "m³", f"{0.85 * 8.25 * 0.5:.2f}", ""],
        ["7.4", "Precast coping 230x60", "m", "9.4", ""],
        ["7.5", "Render 2 coats + paint, kerb external faces", "m²", f"{(8.55 + 1.0) * 0.45:.1f}", ""],
        ["7.6", "Repair & repaint boundary wall & façade", "m²", f"{8.4 * 1.8 + 7.2 * 3.4:.0f}", ""],
        ["7.7", "SS climbing wires 3 mm incl. eyes & tensioners", "m", "70", ""],
        ["8", "PAVING", "", "", ""],
        ["8.1", "Type 1 sub-base 150 + geotextile", "m²", f"{area:.1f}", ""],
        ["8.2", "Sand bed 30 + 200x200x60 pavers 3-tone + jointing", "m²", f"{area:.1f}", ""],
        ["8.3", f"  (paver count {n} + 5% = {int(n * 1.05) + 1})", "no", f"{int(n * 1.05) + 1}", ""],
        ["8.4", "PCC edging 50x150 S edge on haunch", "m", "6.2", ""],
        ["9", "JOINERY & DOORS (A-600)", "", "", ""],
        ["9.1", "D01 alu glazed door 1100x2400 incl. ironmongery", "no", "1", ""],
        ["9.2", "D02 insulated roller shutter 1800x2400 motorised", "no", "1", ""],
        ["9.3", "D03 timber lattice door 900x2400 incl. lining", "no", "1", ""],
        ["9.4", "G01 lattice screen 3.0 m x 1.8 incl. gate & posts", "item", "1", ""],
        ["10", "ELECTRICAL & LIGHTING (A-103)", "", "", ""],
        ["10.1", "LS1 LED strip + profiles + drivers", "m", "10.6", ""],
        ["10.2", "DL1 downlights / WL1 wall light / UL1-6 spikes", "no", "2 / 1 / 6", ""],
        ["10.3", "Circuits, RCBOs, socket SO1, controls, testing", "item", "1", ""],
        ["11", "SOFT LANDSCAPE & IRRIGATION (A-104)", "", "", ""],
        ["11.1", "Plants per schedule incl. olive & pot", "item", "1", ""],
        ["11.2", "Drip irrigation system incl. controller", "item", "1", ""],
        ["12", "CONTINGENCY (existing structure risk)", "%", "10", ""],
    ]
    return rows


def sheet_q001():
    s = Sheet("Q-001", "Bill of quantities (tender schedule — rates by contractor)", "NTS", series="QUANTITIES")
    s.frame()
    rows = boq_rows()
    half = 33
    heads = {i for i, r in enumerate(rows) if r[0].isdigit() and "." not in r[0]}
    for k, part in enumerate((rows[:half], rows[half:])):
        fills = {i: "#efece6" for i, r in enumerate(part) if r[0].isdigit() and "." not in r[0]}
        s.table(16 + k * 162, 14, [("Item", 11), ("Description", 92), ("Unit", 12), ("Qty", 22), ("Rate / Total", 22)],
                part, size=1.45, fills=fills, wrap=True)
    s.textblock(16, 262, 320, [
        "Quantities are net, measured from the drawings (no waste unless stated). Contractor to verify on site & price "
        "each line; state lead times for items 4, 9. Excel version: output/BOQ_Design-A.xlsx.",
    ], size=1.5)
    return s
