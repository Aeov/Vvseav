"""Single source of truth for the courtyard canopy design (Design A — as rendered).

Datum: internal finished floor level (FFL) = ±0.000 = 0 mm.
Plan axes: X = east, measured from the inner face of the existing west boundary wall.
           Y = north; the annex façade face is Y = 0 and the courtyard lies at Y < 0.
All values in millimetres unless noted.
"""
import random

# ------------------------------------------------------------------ existing envelope (verify on site)
BW_T = 250            # west boundary wall thickness (existing, rendered masonry)
BW_TOP = 1800         # boundary wall top (above FFL)
COURT_W = 7200        # boundary wall inner face -> east house wall face
COURT_D = 8400        # façade -> south edge of paving
FAC_T = 300           # annex façade wall thickness
FAC_PARAPET = 3400    # annex roof parapet top (assumed)
SLAB_SOFFIT = 2950    # annex roof slab soffit (assumed — survey)
SLAB_TOP = 3150       # annex roof slab top (assumed)
EW_T = 300            # east house wall thickness
EW_LEN = 5400         # east house wall return length south of façade
EW_TOP = 5900         # east house wall eaves (2-storey, indicative)

# ------------------------------------------------------------------ openings in annex façade (structural openings)
HEAD = 2400
D01 = (1650, 2750)    # glazed aluminium door  1100 x 2400
D02 = (3150, 4950)    # insulated aluminium roller-shutter door 1800 x 2400
D03 = (5450, 6350)    # timber lattice (ventilated) door 900 x 2400
WL1 = (1400, 2100)    # wall light (x, height)
AC1 = (5600, 6450, 2620, 3240)  # existing AC outdoor unit on façade (x0,x1,z0,z1)
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
PAV_X0, PAV_X1 = 1000, 7200
PAV_Y0, PAV_Y1 = 0, -8400
PAVER = 200
PAVER_T = 60
BED_T = 30
SUB_T = 150
GEO = True
# spot levels (m) — cross-fall west->east 1:80 to drain line X=6600; east strip falls back 1:60
LV_KERB = -0.005
LV_VALLEY = -0.075
LV_EASTWALL = -0.065
LV_GULLY = -0.085
G1 = (6600, -2200)
G2 = (6600, -6200)
SD1 = (1500, 6500, -30, -130)   # threshold slot drain x0,x1,y0,y1
IC1 = (6600, -8700)             # outfall to soakaway beyond
SOAK = (6000, -10200, 1200, 800)  # soakaway crate (x,y,w,h) in garden — indicative

# ------------------------------------------------------------------ canopy
CAN_X0, CAN_X1 = 500, 5350      # outer faces of fascia (west, east)
CAN_Y1 = -3150                  # outer face of front fascia
SOFFIT = 2650                   # underside of timber slats
BOS = 2710                      # bottom of all primary steel (200 deep)
TOS = 2910                      # top of steel
FASCIA_TOP = 3020
FASCIA_BOT = 2650
DECK_HI = 2998                  # top of ply at façade (high side)
DECK_LO = 2948                  # top of ply at front (low side)
GUTTER_SOLE_E = 2945
GUTTER_SOLE_W = 2925
P1 = (600, -3050)
P2 = (600, -1400)
P3 = (5200, -3050)              # ALTERNATIVE S2 only
POST = 120                      # SHS 120x120x6.3
POST_CLAD = 160                 # finished size, option A (timber clad)
PED_TOP = 420                   # concrete pedestal / base-plate level
FTG = 800                       # pad 800x800
FTG_D = 700
FTG_BOT = -900                  # underside of pad (min. — or frost depth / bearing stratum)
B1_Y = (-3000, -3100)
B3_X = (550, 650)
B2_X = (5100, 5300)
LEDGER_Y = (0, -75)
J_X0, J_X1 = 650, 5100
N_BAYS = 8
JOISTS = [J_X0 + (J_X1 - J_X0) * i / N_BAYS for i in range(1, N_BAYS)]
JOIST_SPACING = (J_X1 - J_X0) / N_BAYS
B2_TAIL = 2300                  # S1 back-span end (Y) inside the annex
LED_INSET = 220                 # LED profile c/l from fascia OUTER face (clears posts)
SLAT_W, SLAT_T, SLAT_GAP = 68, 20, 10
BATTEN = (50, 38)

DOWNLIGHTS = [(2200, -1000), (4050, -1000)]
UPLIGHTS = [(560, -2800, "UL1"), (560, -1150, "UL2"), (420, -4300, "UL3"), (420, -5700, "UL4"),
            (420, -7100, "UL5"), (300, -600, "UL6")]

# ------------------------------------------------------------------ east screen & gate
SCR_X = (7200, 7300)
SCR_POSTS = [(-5400, -5500), (-6400, -6500), (-7500, -7600), (-8300, -8400)]
GATE = (-6500, -7500)
SCR_H = 1800

# ------------------------------------------------------------------ planting (plan positions)
PLANTS = [
    # code, x, y, spread
    ("TJ", 600, -3050, 600), ("TJ", 600, -1400, 600), ("TJ", 300, -250, 500), ("TJ", 1300, -150, 400),
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
    L = LOADS
    uls_area = max(1.35 * L["gk_area"] + 1.5 * L["sk"], 1.35 * L["gk_area"] + 1.5 * L["qk"])
    sls_area = L["gk_area"] + L["sk"]
    up_area = 1.0 * L["gk_area"] - 1.5 * L["wk_up"]
    rows = []
    out = {"uls": uls_area, "sls": sls_area, "uplift": up_area}

    # joists: lipped C 200x65x20x1.8, S350GD
    s = JOIST_SPACING / 1000
    Lj = (abs(B1_Y[0]) - abs(LEDGER_Y[1])) / 1000
    wj = uls_area * s
    Mj = wj * Lj ** 2 / 8
    Ij = 4.05e6
    Mrd_j = 0.80 * (Ij / 100) * 350 / 1e6
    dj = 5 * (sls_area * s) * (Lj * 1000) ** 4 / (384 * E * Ij)
    rows.append(["J1 joists", "Lipped C 200x65x20x1.8 S350GD+Z275 @ %d c/c" % JOIST_SPACING,
                 f"SS L={Lj:.2f} m", f"{Mj:.1f}", f"{Mrd_j:.1f}", f"{Mj / Mrd_j:.2f}", f"{dj:.1f} (L/{Lj * 1000 / dj:.0f})"])
    Rj = wj * Lj / 2

    # B1 front beam
    p = rhs_props(200, 100, 6.3)
    Lb1 = (P3[0] - P1[0]) / 1000
    trib = Lj / 2 + 0.15
    w1 = uls_area * trib + 1.35 * (L["gk_fascia"] + p["mass"] * 9.81 / 1000)
    w1s = sls_area * trib + L["gk_fascia"] + p["mass"] * 9.81 / 1000
    M1 = w1 * Lb1 ** 2 / 8
    Mrd1 = p["Wpl"] * p["fy"] / 1e6
    d1 = 5 * w1s * (Lb1 * 1000) ** 4 / (384 * E * p["I"])
    rows.append(["B1 front beam", "RHS 200x100x6.3 S355J2H", f"SS L={Lb1:.2f} m", f"{M1:.1f}", f"{Mrd1:.1f}",
                 f"{M1 / Mrd1:.2f}", f"{d1:.1f} (L/{Lb1 * 1000 / d1:.0f})"])
    R1 = w1 * Lb1 / 2
    R1s = w1s * Lb1 / 2
    out["R1"] = R1

    # B3 west edge beam (continuous over P2)
    p3 = rhs_props(200, 100, 5.0)
    w3 = uls_area * (s / 2 + 0.1) + 1.35 * (L["gk_fascia"] + p3["mass"] * 9.81 / 1000)
    Lmax = abs(P1[1] - P2[1]) / 1000
    M3 = w3 * Lmax ** 2 / 8
    Mrd3 = p3["Wpl"] * 355 / 1e6
    rows.append(["B3 west beam", "RHS 200x100x5 S355J2H", f"2-span, max {Lmax:.2f} m", f"{M3:.1f}", f"{Mrd3:.1f}",
                 f"{M3 / Mrd3:.2f}", "< 1 mm"])

    # B2 east beam, S1 cantilever with back-span
    p2 = rhs_props(200, 200, 12.5)
    p2["I"] = 5.13e7
    Lc = abs(B1_Y[0] + B1_Y[1]) / 2 / 1000
    Lbk = 2.0
    w2 = uls_area * (s / 2) + 1.35 * (L["gk_fascia"] + p2["mass"] * 9.81 / 1000)
    w2s = sls_area * (s / 2) + L["gk_fascia"] + p2["mass"] * 9.81 / 1000
    M2 = R1 * Lc + w2 * Lc ** 2 / 2
    Mrd2 = p2["Wpl"] * 355 / 1e6
    M2s = R1s * Lc + w2s * Lc ** 2 / 2
    EI = E * p2["I"]
    d2 = (R1s * 1000 * (Lc * 1000) ** 3 / (3 * EI) + w2s * (Lc * 1000) ** 4 / (8 * EI)
          + M2s * 1e6 * Lbk * 1000 / (3 * EI) * Lc * 1000)
    T = M2 / Lbk
    Rw = R1 + w2 * Lc + T
    rows.append(["B2 east beam (S1)", "SHS 200x200x12.5 S355J2H, precamber 8 mm",
                 f"cantilever {Lc:.2f} m + back-span {Lbk:.1f} m", f"{M2:.1f}", f"{Mrd2:.1f}", f"{M2 / Mrd2:.2f}",
                 f"{d2:.1f} tip (L/{Lc * 1000 / d2:.0f})"])
    out.update({"T": T, "Rw": Rw, "M2": M2, "d2": d2})

    # B2 S2 alternative: simply supported on wall + P3
    pS = rhs_props(200, 100, 6.3)
    M2b = w2 * Lc ** 2 / 8
    rows.append(["B2 east beam (S2 alt.)", "RHS 200x100x6.3 S355J2H on post P3", f"SS L={Lc:.2f} m",
                 f"{M2b:.1f}", f"{Mrd1:.1f}", f"{M2b / Mrd1:.2f}", "< 2 mm"])

    # ledger
    wl = Rj / s
    rows.append(["L1 ledger", "UPN 200 S275, galv., M12 resin anchors @ 400 stagg.", "continuous",
                 f"V={wl:.1f} kN/m", "anchor V,Rd ≈ 6.0 kN", f"{wl * 0.4 / 6.0:.2f}", "—"])

    # posts
    pp = rhs_props(120, 120, 6.3)
    N1 = R1 + w3 * Lmax / 2 + 1.35 * 0.25
    Hc = (TOS - PED_TOP) / 1000
    i_r = (pp["I"] / pp["A"]) ** 0.5
    lam = Hc * 1000 / i_r / (93.9 * (235 / 355) ** 0.5)
    phi = 0.5 * (1 + 0.49 * (lam - 0.2) + lam ** 2)
    chi = min(1.0, 1 / (phi + (phi ** 2 - lam ** 2) ** 0.5))
    Nb = chi * pp["A"] * 355 / 1000
    rows.append(["P1/P2 posts", "SHS 120x120x6.3 S355J2H (Ø75 RWP inside P1)", f"pinned, H={Hc:.2f} m",
                 f"N={N1:.1f} kN", f"Nb,Rd={Nb:.0f} kN", f"{N1 / Nb:.2f}", "—"])
    area_p1 = (Lb1 / 2) * trib + Lmax / 2 * 0.4
    upl = -up_area * area_p1
    Wf = (FTG / 1000) ** 2 * (FTG_D / 1000) * 24 + 0.3 * 0.3 * ((PED_TOP - (FTG_BOT + FTG_D)) / 1000) * 24
    Ns = R1s + 1.5
    qb = (Ns + Wf) / (FTG / 1000) ** 2
    rows.append(["F1/F2 pad footings", "800x800x700 C25/30 + 300x300 pedestal", "bearing (SLS)",
                 f"q={qb:.0f} kPa", "allow. ≥ 100 kPa (verify)", f"{qb / 100:.2f}",
                 f"uplift {upl:.1f} kN vs W={Wf:.1f} kN"])
    rows.append(["S1 tail anchor", "PL 250x250x15 + 4 M16 resin anchors to slab soffit, grout pack",
                 "back-span reaction", f"T={T:.1f} kN", "slab check by engineer", "—", "—"])
    rows.append(["S1 wall bearing", "Precast padstone 440x300x215 C32/40 on façade pier", "fulcrum",
                 f"R={Rw:.1f} kN", f"σ={Rw * 1000 / (440 * 300):.2f} MPa", "—", "—"])
    out["rows"] = rows
    out["N1"] = N1
    out["uplift_P1"] = upl
    return out


if __name__ == "__main__":
    c = calcs()
    for r in c["rows"]:
        print(r)
    print(c["uls"], c["sls"], c["uplift"], c["T"], c["Rw"])
