"""Rev C07 — ONE sheet for client confirmation of the garden edge (client mark-up on V1T-03 + site photo, 07.10.2026).

As the site photo, from the paving outwards: white stone kerb (in line with the door jamb) -> NARROW planter with the
plants -> the LOW WHITE WALL (rounded coping) right behind it. In C06 the wall was drawn ~1 m too far out; the client's
blue line puts it directly behind the planter, next to the column. C1 / C2 stand in the planter at the kerb line,
under the roof edge. Beyond the wall = outside (neighbouring ground, trees in the background).
Once confirmed, the full set (V1, V2, V1T, V2T) is updated to this shape.
"""
import math
from cad import Sheet, View, break_line, PROJECT
from common import shrub
from sheets_b import ladder, paving_cut, upn200, cchan
import preview_c06 as P

KERB = P.KERB                 # (100, 250) white kerb, outer face in line with the door jamb
BED = (-250, 100)             # NARROW planter (soil) between the kerb and the wall
LWN = (-450, -250)            # LOW WHITE WALL — inner face where the client drew the blue line
LWN_H = 1400                  # ≈ 1.40 (rounded coping), as site photo
OUT = -1250                   # outside ground drawn to here


def project():
    p = dict(PROJECT)
    p["rev"] = "C07"
    p["date"] = "07.10.2026"
    p["name"] = "COURTYARD ROOF — GARDEN EDGE"
    p["site"] = ("As site photo + client mark-up: kerb -> narrow planter -> low white wall right behind it; "
                 "C1 / C2 in the planter under the roof edge.")
    p["status"] = "FOR CLIENT CONFIRMATION — shape only; full set follows once confirmed"
    p["revs"] = [["C07", "07.10.2026", "Low white wall moved in, directly behind the narrow planter"]] + P.REVS
    return p


def coping(v, u0, u1, z):
    r = (u1 - u0) / 2
    cx = (u0 + u1) / 2
    pts = [(cx - r * math.cos(math.radians(a)), z + r * 0.6 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    v.pl([(u0, z)] + pts + [(u1, z)], w=0.35, fill="#ffffff")


def sheet():
    c = P.VAR["V1T"]
    RD = c["roof_d"]
    s = Sheet("C07-01", "GARDEN EDGE — corrected shape\nsection, key plan & 3D", "1:25 / 1:100", project=project())
    s.frame()
    s.text(16, 14, "GARDEN EDGE — CORRECTED SHAPE (site photo + your blue mark-up)", size=3.0, weight="bold",
           color=P.RED)

    def u(y):
        return P.WALL_Y0 + P.TW_T - y

    # ---------------- 1: section across at C1, 1:25 (tall wall LEFT, garden RIGHT)
    v = View(s, 30, 214, 25)
    paving_cut(v, [(u(P.WALL_Y0), -15), (u(KERB[1]), -15)], z_bottom_extra=200)
    v.rect(u(P.WALL_Y0 + P.TW_T), -600, P.TW_T, 4200, w=0.45, mat="masonry")
    break_line(v, u(P.WALL_Y0 + P.TW_T), 3600, u(P.WALL_Y0), 3600)
    # outside, beyond the wall (existing ground, background trees)
    v.rect(u(LWN[0]), -500, LWN[0] - OUT, 500, w=0.15, mat="earth")
    v.line(u(LWN[0]), 0, u(OUT), 0, w=0.4)
    break_line(v, u(OUT), -500, u(OUT), 300)
    v.text(u(-1000), 150, "outside (exist.)", size=1.3, anchor="middle", color="#777")
    # where C06 had the wall (removed)
    v.rect(u(-1000), 0, 200, P.LW_H, w=0.25, dash="2,1.2", color="#c0392b")
    v.text(u(-1100), P.LW_H + 140, "C06 wall position", size=1.25, anchor="middle", color="#c0392b")
    v.text(u(-1100), P.LW_H + 300, "(wrong — removed)", size=1.25, anchor="middle", color="#c0392b")
    # narrow planter + plants (growing up against / over the wall)
    v.rect(u(BED[1]), -400, BED[1] - BED[0], P.KERB_H - 30 + 400, w=0.15, mat="soil")
    shrub(v, u(-60), P.KERB_H, 330, 1750, seed=140, flowers=5)
    shrub(v, u(-170), P.KERB_H, 300, 1350, seed=141, flowers=5)
    # white kerb
    v.rect(u(KERB[1]), -200, KERB[1] - KERB[0], P.KERB_H + 200, w=0.4, fill="#f4f1ea")
    # LOW WHITE WALL — directly behind the planter (client's blue line)
    v.rect(u(LWN[1]), -600, LWN[1] - LWN[0], LWN_H + 600, w=0.5, mat="masonry")
    coping(v, u(LWN[1]) - 10, u(LWN[0]) + 10, LWN_H)
    # column C1 in the planter at the kerb line + eccentric pad clear of the wall footing
    v.rect(u(P.CLAD), 0, P.CLAD, P.COL_TOP, w=0.35, mat="timber")
    v.rect(u(100 + P.POST / 2), -60, P.POST, P.COL_TOP - 10 + 60, w=0.3, fill="#5c6670")
    v.rect(u(P.CLAD) - 30, P.COL_TOP - 10, P.CLAD + 60, 10, w=0.25, fill="#888")
    v.rect(u(650), -900, 800, 700, w=0.3, mat="rc")
    v.rect(u(100 + 150), -200, 300, 140, w=0.3, mat="rc")
    # roof (to the tall wall, as V1 / V1T)
    for i in range(1, 5):
        cchan(v, u(150 + (RD - 300) * i / 5), P.BOS, facing=-1)
    P.roof_layers_y(v, u(RD - 50), u(P.CLAD))
    P.bracket(v, u(P.CLAD), P.SOFFIT, -1)
    upn200(v, u(P.WALL_Y0), P.BOS, facing=1)
    P.bracket(v, u(P.WALL_Y0), P.SOFFIT + 50, 1, r=180)
    v.pl([(u(0) - 3, P.SOFFIT), (u(0), P.SOFFIT), (u(0), P.FTOP), (u(0) - 45, P.FTOP - 6)], w=0.45, closed=False)
    ladder(v, u(P.WALL_Y0 + P.TW_T), [(0, "±0.000"), (LWN_H, "+1.40 wall"), (P.SOFFIT, "+2.360 u/s"),
                                       (P.FTOP, "+2.790"), (P.COL_TOP, "+2.920 col.")], 27, size=1.35, inside=False)
    v.chain([u(P.WALL_Y0), u(KERB[1]), u(KERB[0]), u(BED[0]), u(LWN[0])], "x", -900, -4, size=1.35, overall=True)
    rows = [((u(1200), P.TOS + 50), 128, ["roof 3.44 to the tall wall (V1 / V1T)"]),
            ((u(100), 1300), 142, ["C1 stands in the planter at the kerb line"]),
            ((u(-350), 1150), 156, ["LOW WHITE WALL (exist.) — right behind the planter, h ≈ 1.40"]),
            ((u(-100), 700), 168, ["narrow planter ≈ 0.35 + plants (as photo)"]),
            ((u(175), P.KERB_H - 20), 180, ["white kerb, in line with the door jamb"]),
            ((u(1500), 0), 196, ["paving runs up to the kerb"]),
            ((u(250), -700), 246, ["Pad 800x800x700, eccentric — clear of the wall footing (verify)"])]
    for tgt, py, lines in rows:
        px = 125 if py == 128 else (160 if py < 190 else 112)
        P.lab(v, tgt, px, py, lines, size=1.45)
    s.text(16, 26, "1  SECTION ACROSS AT C1 — 1:25 (corrected)", size=2.2, weight="bold")
    s.text(16, 31, "tall house wall LEFT — garden RIGHT, as your mark-up", size=1.5)
    s.scale_bar(30, 282, 25, 2)
    s.text(30, 280, "SCALE BAR 1:25 (section 1)", size=1.3)

    # ---------------- 2: key plan 1:100
    k = View(s, 236 - 7000 / 100, 84, 100)
    XR = P.TIP + 700
    k.rect(7000, OUT, XR - 7000, P.WALL_Y0 - OUT, w=0, fill="#f3eee4")
    k.rect(7000, OUT, XR - 7000, LWN[0] - OUT, w=0.1, fill="#e7efdc", color="#9bb98a")      # outside
    k.rect(7000, 0, P.HOUSE_L - 7000, P.HOUSE_W, mat="masonry", w=0.35)
    k.rect(7000 + 200, 200, P.HOUSE_L - 7000 - 400, P.HOUSE_W - 400, w=0.2, fill="#fbfaf7")
    break_line(k, 7000, -100, 7000, P.HOUSE_W + 100)
    for (a, b, tr) in P.SLIDES:
        k.rect(P.HOUSE_L + 10 + tr * 45, a, 35, b - a, w=0.15, fill="#6e5544")
    k.rect(7000, P.WALL_Y0, XR - 7000, P.TW_T, mat="masonry", w=0.35)
    k.rect(P.HOUSE_L - 120, P.LATTICE[0], 60, P.LATTICE[1] - P.LATTICE[0], w=0.2, fill="#b07a45")
    k.rect(P.HOUSE_L, BED[0], P.GARDEN_X1 - P.HOUSE_L, BED[1] - BED[0], w=0.15, fill="#cdb79a")  # planter
    k.rect(P.HOUSE_L, KERB[0], P.GARDEN_X1 - P.HOUSE_L, KERB[1] - KERB[0], w=0.2, fill="#ffffff")  # kerb
    k.rect(P.HOUSE_L - P.WALL, LWN[0], P.WALL, 0 - LWN[0], w=0.2, fill="#555")                   # return
    k.rect(P.HOUSE_L, LWN[0], XR - P.HOUSE_L, LWN[1] - LWN[0], w=0.3, fill="#555")               # low wall
    k.pl(P.roof_poly(c), w=0, fill="#dfe5ea", opacity=0.7)
    k.pl(P.roof_poly(c), w=0.4, dash="3,1.2")
    for (lb, x, y) in c["cols"]:
        k.rect(x - 100, 0, 200, 200, w=0.2, fill="#c99a62")
        k.text(x, 350, lb, size=1.3, anchor="middle", weight="bold")
    k.line(P.COLS_T[0][1], P.WALL_Y0 + 150, P.COLS_T[0][1], OUT + 100, w=0.3, dash="6,1.5,1,1.5")
    k.text(P.COLS_T[0][1] + 80, OUT + 150, "1", size=1.4, weight="bold")
    k.text(P.HOUSE_L - 150, P.HOUSE_W / 2, "ANNEX", size=1.3, anchor="end", color="#555")
    k.text(XR - 100, -1150, "outside", size=1.2, anchor="end", color="#5a7a4a")
    P.lab(k, (P.HOUSE_L + 3000, -350), 302, 98, ["low white wall"], size=1.25)
    P.lab(k, (P.HOUSE_L + 3800, -80), 302, 103, ["narrow planter + kerb"], size=1.25)
    k.chain([P.HOUSE_L, P.RX1, P.TIP], "x", P.WALL_Y0 + P.TW_T, 4, size=1.25)
    s.text(236, 26, "2  KEY PLAN — 1:100 (triangle shown; same edge for all)", size=1.8, weight="bold")

    # ---------------- 3: 3D at eye level, same direction as the site photo
    saved = (P.PL, P.LW)
    P.PL, P.LW = BED, LWN
    s.text(236, 116, "3  3D — SAME DIRECTION AS THE SITE PHOTO", size=1.8, weight="bold")
    P.axo_view(s, c, 236, 119, 340, 205, beta=70, elev=12, eye=True)
    P.PL, P.LW = saved

    s.textblock(236, 214, 104, [
        ("B", "WHAT CHANGED"),
        "As the photo: kerb → narrow planter → low white wall right behind it (your blue line). "
        "In C06 the wall was ~1 m too far out — removed.",
        "C1 / C2 stand in the planter at the kerb line, under the roof edge.",
        "Same edge for V1, V2, V1T, V2T — confirm and all 12 sheets follow.",
        ("B", "PLEASE CONFIRM / MEASURE"),
        "Planter width kerb-to-wall (drawn ≈ 0.50 incl. kerb), wall height (≈ 1.40) and thickness (0.20).",
    ], size=1.5, gap=0.35)
    return s


if __name__ == "__main__":
    import build
    sh = sheet()
    print(build.to_pdf([sh], "Rev-C07_Garden-Edge_1-sheet"))
