"""Rev C11 — ONE sheet: the annex side wall and the low garden wall are ONE LINE (client). The roof edge is on that
line (roof back to the sketch 3.44 / 2.54), the entrance opening runs to the side wall (no pier), the 1.00 planter
sits in front of the left part of the facade inside the wall, reached through the 1.00 paved entry space.
Rev C10 — ONE sheet: C09 with the paved entry space at the left doorway widened to 1.00 m (was 0.60).
Rev C09 — ONE sheet (C08 + paved entry space at the left doorway, as the site photo).
Rev C08 — ONE sheet for client confirmation of the garden edge (client, 07.10.2026, after C07):
  * the garden (planter) is DOUBLE the C07 width: kerb (in line with the door jamb) to low white wall = 1.00 m;
  * the support columns (timber-clad) stand against the low white wall and are CONNECTED to it.
So the roof's plants-side edge comes out to the low wall: the whole planter is under the roof.
Shown on the rectangular V1 (roof to the tall wall); the same edge applies to V2 / V1T / V2T.
"""
import math
from cad import Sheet, View, break_line, PROJECT
from common import shrub
from sheets_b import ladder, paving_cut, upn200, cchan, rhs
import preview_c06 as P

LWN = (0, 200)                     # low white wall IN LINE with the annex side wall (same line, same 0.20)
WI = LWN[1]                        # wall inner face
GARDEN_W = 1000                    # wall inner face -> kerb outer face
KERB = (WI + GARDEN_W - 150, WI + GARDEN_W)   # (1050, 1200) white kerb
LWN_H = 1400
BED = (WI, KERB[0])                # planter soil (200, 1050)
EDGE = 0                           # roof plants-side edge = the annex side / garden wall line (sketch 3.44)
CY = WI + 100                      # column centre: against the wall inner face (300)
OUT = -600
ENTR_C11 = (WI, P.ENTR[1])         # entrance opening runs to the side wall (no pier)
COLS = [("C1", P.XM, CY), ("C2", P.RX1 - 100, CY)]
ENTRY = 1000                        # paved entry space between the facade and the planter's near-end kerb
GX0 = P.HOUSE_L + ENTRY            # planter starts here (site photo: kerb turns ~0.5-0.6 m in front of the door)
LEFT_DOOR = (ENTR_C11[0], P.SLIDES[1][0])
GX1 = P.RX1 + 1500                 # planter CONTINUES along the low wall (client) — drawn to the plan edge   # open (glass) part of the entrance, left of the brown slider


def project():
    p = dict(PROJECT)
    p["rev"] = "C11"
    p["date"] = "07.10.2026"
    p["name"] = "COURTYARD ROOF — GARDEN EDGE"
    p["site"] = ("Annex side wall + low garden wall in ONE line; roof edge on that line (3.44 as sketch); "
                 "entrance to the side wall; 1.00 planter + 1.00 entry space.")
    p["status"] = "FOR CLIENT CONFIRMATION — shape only; full set follows once confirmed"
    p["revs"] = [["C11", "07.10.2026", "Annex side wall + garden wall in one line; roof 3.44 as sketch"],
                 ["C10", "07.10.2026", "Entry space at the left doorway widened: 0.60 -> 1.00 m"],
                 ["C09", "07.10.2026", "Paved entry space 0.60 at the left doorway; planter starts after it"],
                 ["C08", "07.10.2026", "Planter 1.00 wide; columns against + fixed to the low wall; roof to wall"],
                 ["C07", "07.10.2026", "Low white wall moved in, directly behind the planter"]] + P.REVS[:2]
    return p


def coping(v, u0, u1, z):
    r = (u1 - u0) / 2
    cx = (u0 + u1) / 2
    pts = [(cx - r * math.cos(math.radians(a)), z + r * 0.6 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    v.pl([(u0, z)] + pts + [(u1, z)], w=0.35, fill="#ffffff")


def sheet():
    c = dict(P.VAR["V1"])
    c["cols"] = COLS
    RD = c["roof_d"]
    s = Sheet("C11-01", "GARDEN EDGE — corrected shape\nsection, key plan & 3D", "1:25 / 1:75", project=project())
    s.frame()
    s.text(16, 14, "GARDEN EDGE — BUILDING WALL + GARDEN WALL IN ONE LINE", size=3.0, weight="bold", color=P.RED)

    def u(y):
        return P.WALL_Y0 + P.TW_T - y

    # ---------------- 1: section across at C1, 1:25 (tall wall LEFT, garden RIGHT)
    v = View(s, 30, 214, 25)
    paving_cut(v, [(u(P.WALL_Y0), -15), (u(KERB[1]), -15)], z_bottom_extra=200)
    v.rect(u(P.WALL_Y0 + P.TW_T), -600, P.TW_T, 4200, w=0.45, mat="masonry")
    break_line(v, u(P.WALL_Y0 + P.TW_T), 3600, u(P.WALL_Y0), 3600)
    # outside, beyond the low wall
    v.rect(u(LWN[0]), -500, LWN[0] - OUT, 500, w=0.15, mat="earth")
    v.line(u(LWN[0]), 0, u(OUT), 0, w=0.4)
    break_line(v, u(OUT), -500, u(OUT), 300)
    v.text(u(-350), 150, "outside", size=1.25, anchor="middle", color="#777")
    # planter 1.00 wide (soil) + plants
    v.rect(u(BED[1]), -400, BED[1] - BED[0], P.KERB_H - 30 + 400, w=0.15, mat="soil")
    for i, (yy, h, wd) in enumerate(((900, 1500, 380), (640, 1850, 420), (390, 1300, 300))):
        shrub(v, u(yy), P.KERB_H, wd, h, seed=150 + i, flowers=5)
    v.rect(u(KERB[1]), -200, KERB[1] - KERB[0], P.KERB_H + 200, w=0.4, fill="#f4f1ea")            # white kerb
    # low white wall + footing
    v.rect(u(LWN[1]), -600, LWN[1] - LWN[0], LWN_H + 600, w=0.5, mat="masonry")
    coping(v, u(LWN[1]) - 10, u(LWN[0]) + 10, LWN_H)
    # column C1 AGAINST the wall, fixed to it (2 x SS angle brackets + resin anchors)
    v.rect(u(CY + 100), 0, P.CLAD, P.COL_TOP, w=0.35, mat="timber")
    v.rect(u(CY + P.POST / 2), -60, P.POST, P.COL_TOP - 10 + 60, w=0.3, fill="#5c6670")
    v.rect(u(CY + 100) - 30, P.COL_TOP - 10, P.CLAD + 60, 10, w=0.25, fill="#888")
    for z in (450, 1150):
        v.rect(u(CY - P.POST / 2), z - 40, (P.CLAD - P.POST) / 2 + 60, 80, w=0.25, fill="#9aa3ab")   # angle
        v.rect(u(WI) - 5, z - 8, 130, 16, w=0.15, fill="#666")                                   # anchor into wall
    # pad: eccentric toward the courtyard, tied to the wall footing
    v.rect(u(CY + 650), -900, 900, 700, w=0.3, mat="rc")
    v.rect(u(CY + 150), -200, 300, 140, w=0.3, mat="rc")
    # roof: tall wall -> out to the low wall (edge beam over C1)
    for i in range(1, 6):
        cchan(v, u(EDGE + 150 + (RD - EDGE - 300) * i / 6), P.BOS, facing=-1)
    rhs(v, u(CY + 50), P.BOS, 100, 200, 6.3)
    P.roof_layers_y(v, u(RD - 50), u(CY + 100))
    P.bracket(v, u(CY + 100), P.SOFFIT, -1)
    upn200(v, u(P.WALL_Y0), P.BOS, facing=1)
    P.bracket(v, u(P.WALL_Y0), P.SOFFIT + 50, 1, r=180)
    v.pl([(u(EDGE) - 3, P.SOFFIT), (u(EDGE), P.SOFFIT), (u(EDGE), P.FTOP), (u(EDGE) - 45, P.FTOP - 6)], w=0.5,
         closed=False)
    ladder(v, u(P.WALL_Y0 + P.TW_T), [(0, "±0.000"), (LWN_H, "+1.40 wall"), (P.SOFFIT, "+2.360 u/s"),
                                       (P.FTOP, "+2.790"), (P.COL_TOP, "+2.920 col.")], 27, size=1.35, inside=False)
    v.chain([u(P.WALL_Y0), u(KERB[1]), u(WI), u(LWN[0])], "x", -900, -4, size=1.4, overall=True,
            texts=[f"{P.WALL_Y0 - KERB[1]:.0f}", "1000 garden", "200"])
    v.dim((u(P.WALL_Y0), P.FTOP), (u(EDGE), P.FTOP), 6, text="3440 roof (as your sketch)", size=1.35)
    rows = [((u(1500), P.TOS + 50), 126, ["roof 3.44 as your sketch — edge on the wall line"]),
            ((u(CY), 2000), 140, ["C1 timber-clad column AGAINST the low wall"]),
            ((u(WI) + 2, 1150), 152, ["fixed to the wall: 2 x SS angle brackets + M12 resin anchors"]),
            ((u(640), 700), 164, ["garden / planter 1.00 wide — under the roof"]),
            ((u(LWN[0] + 100), 1250), 176, ["LOW WHITE WALL, in line with the annex side wall"]),
            ((u(KERB[0] + 75), P.KERB_H - 20), 188, ["white kerb"]),
            ((u(2000), 0), 200, ["paving runs up to the kerb"]),
            ((u(CY + 300), -700), 246, ["Pad 900x800x700 eccentric, tied to the wall footing (engineer to verify)"])]
    for tgt, py, lines in rows:
        px = 112 if (py in (126, 200) or py > 210) else 150
        P.lab(v, tgt, px, py, lines, size=1.45)
    s.text(16, 26, "1  SECTION ACROSS AT C1 — 1:25", size=2.2, weight="bold")
    s.text(16, 31, "tall house wall LEFT — garden RIGHT", size=1.5)
    s.scale_bar(30, 282, 25, 2)
    s.text(30, 280, "SCALE BAR 1:25 (section 1)", size=1.3)

    # ---------------- 2: key plan 1:100
    P.EDGE_Y = EDGE
    k = View(s, 236 - 7000 / 75, 92, 75)
    XR = P.RX1 + 1500
    k.rect(7000, OUT, XR - 7000, P.WALL_Y0 - OUT, w=0, fill="#f3eee4")
    k.rect(7000, OUT, XR - 7000, LWN[0] - OUT, w=0.1, fill="#e7efdc", color="#9bb98a")
    k.rect(7000, 0, P.HOUSE_L - 7000, P.HOUSE_W, mat="masonry", w=0.35)
    k.rect(7000 + 200, 200, P.HOUSE_L - 7000 - 400, P.HOUSE_W - 400, w=0.2, fill="#fbfaf7")
    break_line(k, 7000, -100, 7000, P.HOUSE_W + 100)
    for (a, b, tr) in P.SLIDES:
        k.rect(P.HOUSE_L + 10 + tr * 45, a, 35, b - a, w=0.15, fill="#6e5544")
    k.rect(7000, P.WALL_Y0, XR - 7000, P.TW_T, mat="masonry", w=0.35)
    k.rect(P.HOUSE_L - 120, P.LATTICE[0], 60, P.LATTICE[1] - P.LATTICE[0], w=0.2, fill="#b07a45")
    k.rect(GX0, BED[0], GX1 - GX0, BED[1] - BED[0], w=0.15, fill="#cdb79a")
    P.plants(k, GX0 + 150, GX1 - 50, BED[0] + 100, BED[1] - 100, seed=6, rmin=140, rmax=210)
    k.rect(GX0, KERB[0], GX1 - GX0, KERB[1] - KERB[0], w=0.2, fill="#ffffff")
    k.text(GX1 - 100, KERB[1] + 120, "garden continues →", size=1.25, anchor="end", color="#3f6b2e",
           weight="bold")
    k.rect(GX0, BED[0], 150, KERB[1] - BED[0], w=0.2, fill="#ffffff")                     # near-end kerb
    k.rect(P.HOUSE_L, BED[0], ENTRY, KERB[1] - BED[0], w=0.3, fill="#efe2c8", color="#c0392b")  # entry space
    k.rect(P.HOUSE_L - P.WALL, LEFT_DOOR[0], P.WALL, LEFT_DOOR[1] - LEFT_DOOR[0], w=0.3, fill="#cfe3ef")
    k.dim((P.HOUSE_L, BED[0]), (GX0, BED[0]), -3, text=f"{ENTRY}", size=1.2)
    k.rect(P.HOUSE_L, LWN[0], XR - P.HOUSE_L, LWN[1] - LWN[0], w=0.3, fill="#555")      # garden wall = annex line
    k.line(7000, 0, XR, 0, w=0.25, dash="5,1.2,1,1.2", color="#c0392b")
    k.text(7100, -250, "ONE LINE: annex side wall = garden wall = roof edge", size=1.15, color="#c0392b",
           weight="bold")
    k.pl(P.roof_poly(c), w=0, fill="#dfe5ea", opacity=0.6)
    k.pl(P.roof_poly(c), w=0.45, dash="3,1.2")
    for (lb, x, y) in COLS:
        k.rect(x - 100, y - 100, 200, 200, w=0.25, fill="#c99a62")
        k.text(x, y + 230, lb, size=1.3, anchor="middle", weight="bold")
    k.line(P.XM, P.WALL_Y0 + 150, P.XM, OUT + 100, w=0.3, dash="6,1.5,1,1.5")
    k.text(P.XM + 80, OUT + 150, "1", size=1.4, weight="bold")
    k.text(P.HOUSE_L - 150, P.HOUSE_W / 2, "ANNEX", size=1.3, anchor="end", color="#555")
    k.chain([P.HOUSE_L, P.RX1], "x", P.WALL_Y0 + P.TW_T, 4, size=1.25)
    k.chain([LWN[0], WI, KERB[1], P.HOUSE_W, P.WALL_Y0], "y", XR, -4, size=1.1, overall=False)
    P.lab(k, (P.RX1 + 700, (LWN[0] + LWN[1]) / 2), 318, 104, ["low white wall"], size=1.25)
    P.lab(k, (P.RX1 + 900, 600), 318, 99, ["garden 1.00, continues"], size=1.25)
    P.lab(k, (P.HOUSE_L + 300, 700), 245, 112, ["PAVED ENTRY SPACE 1.00 —", "walk in to the left doorway"],
          size=1.3)
    P.lab(k, (P.HOUSE_L - 100, (LEFT_DOOR[0] + LEFT_DOOR[1]) / 2), 236, 34, ["left doorway (glass)"], size=1.2)
    s.text(236, 26, "2  KEY PLAN — 1:75 (V1 shown; same edge for all)", size=1.8, weight="bold")

    # ---------------- 3: 3D at eye level, as the site photo
    saved = (P.PL, P.LW, P.GARDEN_X0, P.GARDEN_X1, P.GARDEN_OPEN_END, P.KERB, P.ENTR)
    P.PL, P.LW, P.GARDEN_X0, P.GARDEN_X1, P.GARDEN_OPEN_END, P.KERB, P.ENTR = BED, LWN, GX0, GX1, True, KERB, ENTR_C11
    s.text(236, 122, "3  3D — SAME DIRECTION AS THE SITE PHOTO", size=1.8, weight="bold")
    P.axo_view(s, c, 236, 125, 340, 207, beta=70, elev=12, eye=True)
    P.PL, P.LW, P.GARDEN_X0, P.GARDEN_X1, P.GARDEN_OPEN_END, P.KERB, P.ENTR = saved
    P.EDGE_Y = 0

    s.textblock(236, 214, 104, [
        ("B", "WHAT CHANGED (C11)"),
        "The annex side wall and the low garden wall are ONE straight line (it was 0.75 more inside).",
        "Entrance opening runs to the side wall (no pier); glass door left, brown slider right.",
        "Roof edge on that line → roof 3.44 (V2 2.54) exactly as your sketch.",
        "Planter 1.00 wide inside the wall, continues; paved entry space 1.00 at the door; "
        "columns against + fixed to the wall.",
        ("B", "PLEASE CONFIRM"),
        "Garden 1.00 + columns at the wall + roof to the wall: confirmed by you (C08). All 12 sheets follow.",
    ], size=1.5, gap=0.35)
    return s


if __name__ == "__main__":
    import build
    sh = sheet()
    print(build.to_pdf([sh], "Rev-C11_Garden-Edge_1-sheet"))
