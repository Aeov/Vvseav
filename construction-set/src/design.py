"""Single source of truth for the courtyard canopy design (Design A).

Rev C02 (07.10.2026): canopy re-dimensioned to the client's hand sketch (top + side view, metres):
  roof 8.00 m long x 3.44 m deep; front beam 0.20 wide on the 2.54 m line with 0.90 m outer zone (overhang);
  posts at both ends of the front beam; underside +2.36 m; fascia band 0.43 m (top +2.79 m).
  The sketch's triangular roof extension (3.22 m + 1.26 m) is NOT part of this issue (to be studied next).

Datum: internal finished floor level (FFL) = ±0.000 = 0 mm.
Plan axes: X = east, measured from the inner face of the existing west boundary wall.
           Y = north; the annex façade face is Y = 0 and the courtyard lies at Y < 0.
All values in millimetres unless noted.
"""
import random

# ------------------------------------------------------------------ existing envelope (verify on site)
BW_T = 250            # west boundary wall thickness (existing, rendered masonry)
BW_TOP = 1800         # boundary wall top (above FFL)
COURT_W = 11600       # boundary wall -> east house wall (ASSUMED: 8.00 m roof + 3.22 m extension zone)
COURT_D = 8400        # façade -> south edge of paving
FAC_T = 300           # annex façade wall thickness
FAC_PARAPET = 3400    # annex roof parapet top (assumed)
SLAB_SOFFIT = 2950    # annex roof slab soffit (assumed — survey)
SLAB_TOP = 3150       # annex roof slab top (assumed)
EW_T = 300            # east house wall thickness
EW_LEN = 5400         # east house wall return length south of façade
EW_TOP = 5900         # east house wall eaves (2-storey, indicative)

# ------------------------------------------------------------------ openings in annex façade (structural openings)
HEAD = 2200            # door heads (ASSUMED): must stay below the canopy soffit +2.36
D01 = (1650, 2750)    # glazed aluminium door  1100 x 2400
D02 = (3150, 4950)    # insulated aluminium roller-shutter door 1800 x 2400
D03 = (5450, 6350)    # timber lattice (ventilated) door 900 x 2400
WL1 = (1400, 1900)    # wall light (x, height) — below the soffit
AC1 = (9000, 9850, 2620, 3240)  # AC outdoor unit RELOCATED east of the canopy (was above D03) (x0,x1,z0,z1)
AC2 = (-1500, -2400, 3300, 3900)  # existing AC unit on east wall (y0,y1,z0,z1)
SOLAR = (2200, 4400)  # existing solar water heater on annex roof (x range), indicative

# ------------------------------------------------------------------ planter (west)
PL_IN = 850           # internal width X 0..850
KERB_T = 150          # X 850..1000
KERB_X0, KERB_X1 = 850, 1000
COP_X0, COP_X1 = 810, 1040   # 230 wide coping, 40 mm drip overhang to paving side
COP_T = 60
COP_TOP = 400
SOIL_TOP = 340        # finished soil + mulch
PL_END_Y = -8250      # inner face of south return kerb
PL_SOUTH = -8400      # outer face of south return kerb
KERB_FTG_W, KERB_FTG_D = 450, 250   # strip footing
KERB_FTG_BOT = -650

# ------------------------------------------------------------------ paving
PAV_X0, PAV_X1 = 1000, COURT_W
PAV_Y0, PAV_Y1 = 0, -8400
PAVER = 200
PAVER_T = 60
BED_T = 30
SUB_T = 150
GEO = True
# spot levels (m) — cross-fall west->east 1:80 to drain line X = DRAIN_X; east strip falls back 1:60
DRAIN_X = COURT_W - 600
LV_KERB = -0.005
LV_VALLEY = round(LV_KERB - (DRAIN_X - PAV_X0) / 80 / 1000, 3)
LV_EASTWALL = round(LV_VALLEY + 600 / 60 / 1000, 3)
LV_GULLY = round(LV_VALLEY - 0.010, 3)
G1 = (DRAIN_X, -2200)
G2 = (DRAIN_X, -6200)
SD1 = (1500, 6500, -30, -130)   # threshold slot drain x0,x1,y0,y1
IC1 = (DRAIN_X, -8700)          # outfall to soakaway beyond
SOAK = (DRAIN_X - 600, -10200, 1200, 800)  # soakaway crate (x,y,w,h) in garden — indicative

# ------------------------------------------------------------------ canopy (per client sketch, Rev C02)
CAN_L, CAN_D = 8000, 3440       # roof plan size: 8.00 m along façade x 3.44 m projection
CAN_X0 = 300                    # west outer face of fascia (over the planter, as render)
CAN_X1 = CAN_X0 + CAN_L         # east outer face of fascia
CAN_Y1 = -CAN_D                 # outer face of front fascia
BEAM_LINE = -2540               # c/l of front beam: 2.54 m from façade (sketch)
OVERHANG = CAN_D + BEAM_LINE    # 0.90 m from beam c/l to front edge (sketch)
SOFFIT = 2360                   # underside of slats = underside of fascia (sketch 2,36)
FASCIA_BOT = SOFFIT
FASCIA_TOP = SOFFIT + 430       # fascia band 0.43 m (sketch) -> +2.790
BOS = SOFFIT + 50               # bottom of primary steel (20 slat + 30 batten)
TOS = BOS + 200                 # top of steel (all 200 deep)
FIR_HI, FIR_LO = 60, 15         # tapered firrings (fall to front ~1:76)
DECK_HI = TOS + FIR_HI + 18     # top of ply at façade
DECK_LO = TOS + FIR_LO + 18     # top of ply at front gutter edge
GUTTER_Y = (CAN_Y1 + 30, CAN_Y1 + 150)   # front box gutter (120 wide) inside fascia
GUTTER_SOLE_MID = TOS + 20      # gutter sole high point (middle), falls 1:200 to both ends
GUTTER_SOLE_END = GUTTER_SOLE_MID - 20
POST = 150                      # SHS 150x150x8
POST_CLAD = 200                 # finished 200x200 (timber clad), = 0.20 beam width
P1 = (CAN_X0 + 100, BEAM_LINE)  # west post (in planter)
P2 = (CAN_X1 - 100, BEAM_LINE)  # east post (in planter box PB2)
P3 = None                       # (Rev C01 alternative — no longer required)
PED_TOP = 420                   # concrete pedestal / base-plate level
FTG = 900                       # pad 900x900
FTG_D = 700
FTG_BOT = -900                  # underside of pad (min. — or frost depth / bearing stratum)
B1_Y = (BEAM_LINE + 100, BEAM_LINE - 100)   # front beam SHS 200x200x10 (0.20 wide, sketch)
B3_X = (P1[0] - 50, P1[0] + 50)  # west side beam RHS 200x100x6.3, ledger -> front edge (over P1)
B2_X = (P2[0] - 50, P2[0] + 50)  # east side beam (mirror)
LEDGER_Y = (0, -75)
J_X0, J_X1 = B3_X[1], B2_X[0]
N_BAYS = 13
JOISTS = [J_X0 + (J_X1 - J_X0) * i / N_BAYS for i in range(1, N_BAYS)]
JOIST_SPACING = (J_X1 - J_X0) / N_BAYS
OUTRIG_Y = (B1_Y[1], CAN_Y1 + 50)     # outriggers RHS 150x100x5 cantilever from B1 to fascia sub-frame
PB2 = (P2[0] - 350, P2[0] + 350, BEAM_LINE - 350, BEAM_LINE + 350)   # planter box around P2 (x0,x1,y0,y1)
LED_INSET = 240                 # LED profile c/l from fascia outer face (clears 200 posts by 40)
SLAT_W, SLAT_T, SLAT_GAP = 68, 20, 10
BATTEN = (50, 30)

DOWNLIGHTS = [(2200, -1200), (4050, -1200), (5900, -1200), (7300, -1200)]
UPLIGHTS = [(650, -2300, "UL1"), (650, -1100, "UL2"), (420, -4300, "UL3"), (420, -5700, "UL4"),
            (420, -7100, "UL5"), (300, -600, "UL6"), (P2[0], BEAM_LINE - 260, "UL7")]

# ------------------------------------------------------------------ east screen & gate
SCR_X = (COURT_W, COURT_W + 100)
SCR_POSTS = [(-5400, -5500), (-6400, -6500), (-7500, -7600), (-8300, -8400)]
GATE = (-6500, -7500)
SCR_H = 1800

# ------------------------------------------------------------------ planting (plan positions)
PLANTS = [
    # code, x, y, spread
    ("TJ", P1[0], P1[1], 600), ("TJ", 500, -1300, 550), ("TJ", 300, -250, 500), ("TJ", 1300, -150, 400),
    ("TJ", P2[0], P2[1], 550),
    ("PT", 380, -2200, 650), ("PT", 420, -3900, 700), ("PT", 420, -6300, 700),
    ("WF", 600, -4600, 550), ("WF", 600, -7000, 550),
    ("RO", 650, -5300, 500), ("RO", 650, -7700, 450),
    ("MY", 300, -5100, 650), ("MY", 300, -7400, 650),
    ("LA", 680, -3600, 420), ("LA", 700, -6100, 420),
    ("ER", 760, -2400, 300), ("ER", 760, -4200, 300), ("ER", 760, -5800, 300), ("ER", 760, -7900, 300),
    ("ER", 760, -6800, 300), ("TJ", 300, -6000, 450), ("TJ", 300, -3300, 450),
    ("OL", 1400, -650, 900),
]
PLANT_SCHED = {
    "TJ": ("Trachelospermum jasminoides", "Star jasmine (climber)", "2 L, 60–90 cm, on canes", "On posts, façade & wall wires"),
    "PT": ("Pittosporum tobira 'Nana'", "Dwarf mock orange", "10 L, 40–50 cm", "Evergreen mound, scented"),
    "WF": ("Westringia fruticosa", "Coastal rosemary", "7.5 L, 40 cm", "Fine grey-green foliage"),
    "RO": ("Rosmarinus officinalis 'Miss Jessopp'", "Upright rosemary", "5 L, 40 cm", "Aromatic, drought tolerant"),
    "MY": ("Myrtus communis 'Tarentina'", "Dwarf myrtle", "10 L, 50–60 cm", "White flowers, evergreen"),
    "LA": ("Lavandula angustifolia 'Hidcote'", "English lavender", "3 L", "Front of border"),
    "ER": ("Erigeron karvinskianus", "Mexican fleabane", "2 L", "Spills over coping edge"),
    "OL": ("Olea europaea (multi-stem)", "Olive tree in pot", "1.8–2.0 m, 50 L", "Pot: 600 Ø fibre-clay, white"),
}

# ------------------------------------------------------------------ paving colour pattern
TONES = {"S": ("Sand / cream", "#e6d6bb", 0.42), "B": ("Buff / beige", "#cdb48f", 0.33),
         "G": ("Grey-taupe", "#a39c98", 0.25)}


def paving_pattern(seed=7):
    nx = (PAV_X1 - PAV_X0) // PAVER
    ny = (PAV_Y0 - PAV_Y1) // PAVER
    rnd = random.Random(seed)
    keys = list(TONES)
    wts = [TONES[k][2] for k in keys]
    grid = [[None] * nx for _ in range(ny)]
    # base 2x2 blocks then 1x1 accents, giving the clustered "pixel" look of the render
    for by in range(0, ny, 2):
        for bx in range(0, nx, 2):
            c = rnd.choices(keys, wts)[0]
            for j in range(2):
                for i in range(2):
                    if by + j < ny and bx + i < nx:
                        grid[by + j][bx + i] = c
    for j in range(ny):
        for i in range(nx):
            if rnd.random() < 0.28:
                grid[j][i] = rnd.choices(keys, wts)[0]
    return grid  # grid[row from façade][col from west]


# ------------------------------------------------------------------ structural (preliminary) calcs
LOADS = {
    "gk_area": 0.65,   # kN/m2 frame+joists 0.20, ply+firrings 0.15, membrane 0.03, soffit 0.15, services 0.02, vines 0.10
    "gk_fascia": 0.25,  # kN/m fascia + gutter upstand + LED
    "qk": 0.75,        # kN/m2 maintenance (roof cat. H) — not combined with snow
    "sk": 1.00,        # kN/m2 snow (ASSUMED — set from site altitude/zone)
    "wk_up": 0.91,     # kN/m2 net wind uplift (qp 0.70 x cp,net -1.3, ASSUMED)
}
E = 210000.0


def rhs_props(h, b, t, fy=355):
    I = (b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12 * 0.975
    Wpl = (b * h ** 2 / 4 - (b - 2 * t) * (h - 2 * t) ** 2 / 4) * 0.975
    A = (b * h - (b - 2 * t) * (h - 2 * t)) * 0.97
    mass = A * 7850e-6
    return {"I": I, "Wpl": Wpl, "A": A, "mass": mass, "fy": fy}


def calcs():
    """Preliminary member checks for Rev C02 frame (posts at both ends of an 8 m front beam)."""
    L = LOADS
    uls_area = max(1.35 * L["gk_area"] + 1.5 * L["sk"], 1.35 * L["gk_area"] + 1.5 * L["qk"])
    sls_area = L["gk_area"] + L["sk"]
    up_area = 1.0 * L["gk_area"] - 1.5 * L["wk_up"]
    rows = []
    out = {"uls": uls_area, "sls": sls_area, "uplift": up_area}
    g = 9.81 / 1000

    # J1 joists: ledger -> front beam
    s = JOIST_SPACING / 1000
    Lj = (abs(B1_Y[0]) - abs(LEDGER_Y[1])) / 1000
    wj = uls_area * s
    Mj = wj * Lj ** 2 / 8
    Ij = 4.05e6
    Mrd_j = 0.80 * (Ij / 100) * 350 / 1e6
    dj = 5 * (sls_area * s) * (Lj * 1000) ** 4 / (384 * E * Ij)
    rows.append(["J1 joists", "Lipped C 200x65x20x1.8 S350GD+Z275 @ %d c/c" % round(JOIST_SPACING),
                 f"SS L={Lj:.2f} m", f"{Mj:.1f}", f"{Mrd_j:.1f}", f"{Mj / Mrd_j:.2f}", f"{dj:.1f} (L/{Lj * 1000 / dj:.0f})"])
    Rj = wj * Lj / 2
    Rjs = sls_area * s * Lj / 2

    # O1 outriggers: cantilever from B1 outer face to front fascia (0.90 sketch zone)
    po = rhs_props(150, 100, 5.0)
    Lo = (abs(OUTRIG_Y[1]) - abs(B1_Y[1])) / 1000 + 0.05
    wo = uls_area * s + 1.35 * po["mass"] * g
    Po = 1.35 * (L["gk_fascia"] + 0.10) * s          # fascia + gutter water at tip
    Mo = wo * Lo ** 2 / 2 + Po * Lo
    Mrdo = po["Wpl"] * 355 / 1e6
    do = (sls_area * s) * (Lo * 1000) ** 4 / (8 * E * po["I"]) + (L["gk_fascia"] + 0.1) * s * 1000 * (Lo * 1000) ** 3 / (3 * E * po["I"])
    rows.append(["O1 outriggers", "RHS 150x100x5 S355J2H, end-plate welded to B1, @ J1 c/c",
                 f"cantilever {Lo:.2f} m", f"{Mo:.1f}", f"{Mrdo:.1f}", f"{Mo / Mrdo:.2f}", f"{do:.1f} tip"])
    Ro = wo * Lo + Po                                   # load into B1 per outrigger
    To = Mo                                             # torque into B1 per outrigger

    # B1 front beam (sketch: 0.20 wide) spanning between posts at both ends
    p = rhs_props(200, 200, 10.0)
    Lb1 = (P2[0] - P1[0]) / 1000
    w1 = (Rj + Ro) / s + 1.35 * p["mass"] * g
    w1s = (Rjs + (sls_area * s * Lo + (L["gk_fascia"] + 0.1) * s)) / s + p["mass"] * g
    M1 = w1 * Lb1 ** 2 / 8
    Mrd1 = p["Wpl"] * p["fy"] / 1e6
    d1 = 5 * w1s * (Lb1 * 1000) ** 4 / (384 * E * p["I"])
    rows.append(["B1 front beam", "SHS 200x200x10 S355J2H (0.20 wide)", f"SS L={Lb1:.2f} m (post c/c)",
                 f"{M1:.1f}", f"{Mrd1:.1f}", f"{M1 / Mrd1:.2f}", f"{d1:.1f} (L/{Lb1 * 1000 / d1:.0f}); precamber 15"])
    # torsion from outriggers (net of joist eccentricity, conservative: outriggers only)
    tq = To / s * Lb1 / 2
    Wt = 2 * (200 - 10) ** 2 * 10
    tau = tq * 1e6 / Wt
    rows.append(["B1 torsion", "outrigger moments -> end connections C3", "per support",
                 f"T={tq:.1f} kNm", f"τ={tau:.0f} MPa ≪ 205", f"{tau / 205:.2f}", "rigid C3 end plates to posts"])
    R1 = w1 * Lb1 / 2
    R1s = w1s * Lb1 / 2
    out["R1"] = R1

    # B3 / B2 side beams: ledger -> post (back-span) + cantilever to front edge
    p3 = rhs_props(200, 100, 6.3)
    Lb3 = (abs(P1[1]) - abs(LEDGER_Y[1])) / 1000
    Lc3 = (abs(OUTRIG_Y[1]) - abs(P1[1])) / 1000
    w3 = uls_area * (s / 2 + 0.05) + 1.35 * (L["gk_fascia"] + p3["mass"] * g)
    M3 = max(w3 * Lb3 ** 2 / 8, w3 * Lc3 ** 2 / 2)
    Mrd3 = p3["Wpl"] * 355 / 1e6
    rows.append(["B3/B2 side beams", "RHS 200x100x6.3 S355J2H", f"{Lb3:.2f} m + cantilever {Lc3:.2f} m",
                 f"{M3:.1f}", f"{Mrd3:.1f}", f"{M3 / Mrd3:.2f}", "< 3 mm"])
    R3 = w3 * (Lb3 / 2 + Lc3) + w3 * Lc3 ** 2 / 2 / Lb3

    # ledger
    wl = Rj / s
    rows.append(["L1 ledger", "UPN 200 S275, galv., M12 resin anchors @ 400 stagg.", f"{(J_X1 - J_X0) / 1000:.2f} m",
                 f"V={wl:.1f} kN/m", "anchor V,Rd ≈ 6.0 kN", f"{wl * 0.4 / 6.0:.2f}", "—"])

    # posts
    pp = rhs_props(150, 150, 8.0)
    N1 = R1 + R3 + 1.35 * 0.35
    Hc = (BOS - PED_TOP) / 1000
    i_r = (pp["I"] / pp["A"]) ** 0.5
    lam = Hc * 1000 / i_r / (93.9 * (235 / 355) ** 0.5)
    phi = 0.5 * (1 + 0.49 * (lam - 0.2) + lam ** 2)
    chi = min(1.0, 1 / (phi + (phi ** 2 - lam ** 2) ** 0.5))
    Nb = chi * pp["A"] * 355 / 1000
    rows.append(["P1/P2 posts", "SHS 150x150x8 S355J2H, clad to 200x200 (Ø75 RWP inside)", f"pinned, H={Hc:.2f} m",
                 f"N={N1:.1f} kN", f"Nb,Rd={Nb:.0f} kN", f"{N1 / Nb:.2f}", "—"])
    area_p = (Lb1 / 2) * ((Lj / 2) + Lo + 0.1) + (Lb3 / 2 + Lc3) * 0.35
    upl = -up_area * area_p
    Wf = (FTG / 1000) ** 2 * (FTG_D / 1000) * 24 + 0.3 * 0.3 * ((PED_TOP - (FTG_BOT + FTG_D)) / 1000) * 24
    Ns = R1s + 3.0
    qb = (Ns + Wf) / (FTG / 1000) ** 2
    rows.append(["F1/F2 pad footings", "900x900x700 C25/30 + 300x300 pedestal", "bearing (SLS)",
                 f"q={qb:.0f} kPa", "allow. ≥ 100 kPa (verify)", f"{qb / 100:.2f}",
                 f"uplift {upl:.1f} kN vs W={Wf:.1f} kN"])
    out["rows"] = rows
    out["N1"] = N1
    out["uplift_P1"] = upl
    out["d1"] = d1
    return out


if __name__ == "__main__":
    c = calcs()
    for r in c["rows"]:
        print(r)
    print(c["uls"], c["sls"], c["uplift"], c["N1"], c["d1"])
