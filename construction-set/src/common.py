"""Shared drawing elements: walls, doors, plants, furniture, schematic symbols."""
import math
import random
from design import *  # noqa
from cad import MAT

GREEN = "#5d8a4a"
GREEN_F = "#dfeed3"
WHITE_F = "#fbfaf7"


# ============================================================ PLAN ELEMENTS
def plan_walls(v, show_rooms=True):
    # façade wall with openings
    segs = [(-BW_T, D01[0]), (D01[1], D02[0]), (D02[1], D03[0]), (D03[1], COURT_W + EW_T)]
    for a, b in segs:
        v.rect(a, 0, b - a, FAC_T, mat="masonry", w=0.5)
    # boundary wall (existing) — continues south
    v.rect(-BW_T, -8800, BW_T, 8800, mat="masonry", w=0.5)
    v.s.rect(*v.P(-BW_T - 40, -8800), (BW_T + 80) / v.scale, 4, lw=0, fill="#fff")
    # east house wall
    v.rect(COURT_W, -EW_LEN, EW_T, EW_LEN, mat="masonry", w=0.5)
    # annex beyond
    v.line(-BW_T, FAC_T + 2700, COURT_W + EW_T, FAC_T + 2700, w=0.13, dash="3,1.5", color="#777")
    for x in (3000, 5200):
        v.line(x, FAC_T, x, FAC_T + 2700, w=0.13, dash="3,1.5", color="#777")
    if show_rooms:
        for x, t in ((1450, "HALL"), (4100, "STORE / WORKSHOP"), (6200, "UTILITY / PLANT")):
            v.text(x, FAC_T + 1500, t, size=1.8, anchor="middle", color="#555")
        v.text(3600, FAC_T + 2200, "EXISTING ANNEX (internal layout indicative)", size=1.6, anchor="middle",
               color="#777", italic=True)
        v.text(COURT_W + EW_T + 300, -2600, "EXISTING HOUSE", size=1.8, rot=90, anchor="middle", color="#555")
        v.text(-BW_T - 250, -4300, "EXISTING BOUNDARY WALL 250, h = 1.80 m", size=1.6, rot=90, anchor="middle",
               color="#555")


def plan_doors(v):
    # D01 glazed door — frame & leaf opening in
    x0, x1 = D01
    v.rect(x0, 110, 50, 80, w=0.2, fill="#999")
    v.rect(x1 - 50, 110, 50, 80, w=0.2, fill="#999")
    v.line(x0 + 50, 150, x0 + 50, 150 + 1000, w=0.25, layer="A-DOOR")
    v.rect(x0 + 50, 150, 1000, 0.01, w=0.1)
    v.arc(x0 + 50, 150, 1000, 0, 90, w=0.13)
    v.tag((x0 + x1) / 2, -380, "D01", shape="rect", r=1.7, size=1.5)
    # D02 roller shutter
    x0, x1 = D02
    v.rect(x0, 60, 80, 120, w=0.2, fill="#999")
    v.rect(x1 - 80, 60, 80, 120, w=0.2, fill="#999")
    v.line(x0 + 80, 120, x1 - 80, 120, w=0.35, dash="2,1")
    v.text((x0 + x1) / 2, 420, "roller shutter — coil box above, inside", size=1.3, anchor="middle", color="#555")
    v.tag((x0 + x1) / 2, -380, "D02", shape="rect", r=1.7, size=1.5)
    # D03 lattice door — opens out
    x0, x1 = D03
    v.rect(x0, 0, 30, 120, w=0.2, fill="#b07a45")
    v.rect(x1 - 30, 0, 30, 120, w=0.2, fill="#b07a45")
    v.line(x1 - 33, 0, x1 - 33, -834, w=0.25, layer="A-DOOR")
    v.arc(x1 - 33, 0, 834, 180, 270, w=0.13)
    v.tag((x0 + x1) / 2, 520, "D03", shape="rect", r=1.7, size=1.5)


def plan_planter(v, soil=True, label=True):
    if soil:
        v.pl([(0, 0), (KERB_X0, 0), (KERB_X0, PL_END_Y), (0, PL_END_Y)], w=0, mat="soil", opacity=0.55)
    # coping / kerb (seen below cut plane)
    v.rect(COP_X0, PL_SOUTH, COP_X1 - COP_X0, -PL_SOUTH, w=0.3, fill="#f3efe6")
    v.line(KERB_X0, 0, KERB_X0, PL_SOUTH, w=0.13, dash="2,1", color="#777")
    v.line(KERB_X1, 0, KERB_X1, PL_SOUTH, w=0.13, dash="2,1", color="#777")
    v.rect(0, PL_SOUTH, COP_X1, 230, w=0.3, fill="#f3efe6")
    if label:
        v.text(420, -7900, "RAISED PLANTER", size=1.6, anchor="middle", rot=90, color="#5a3d1e")


def plan_pb2(v, label=False):
    """Raised planter box PB2 (700x700, h 400) around the east post P2."""
    x0, x1, y0, y1 = PB2
    v.rect(x0, y0, x1 - x0, y1 - y0, w=0.3, fill="#f3efe6")
    v.rect(x0 + 100, y0 + 100, x1 - x0 - 200, y1 - y0 - 200, w=0.15, mat="soil", opacity=0.6)
    if label:
        v.text((x0 + x1) / 2, y0 - 180, "PB2", size=1.4, anchor="middle", weight="bold")


def plan_posts(v, alt=False, clad=True, pb2=True):
    if pb2:
        plan_pb2(v)
    for (x, y) in (P1, P2):
        if clad:
            v.rect(x - POST_CLAD / 2, y - POST_CLAD / 2, POST_CLAD, POST_CLAD, w=0.2, fill="#e7c79a")
        v.rect(x - POST / 2, y - POST / 2, POST, POST, w=0.3, fill="#222", layer="S-STEEL")


def plan_canopy_outline(v, color="#000", w=0.3):
    v.rect(CAN_X0, CAN_Y1, CAN_X1 - CAN_X0, -CAN_Y1, w=w, dash="4,1.5", color=color, fill="none")


def plan_paving_outline(v, grid=True):
    v.rect(PAV_X0, PAV_Y1, PAV_X1 - PAV_X0, -PAV_Y1, w=0.25)
    if grid:
        for x in range(PAV_X0 + PAVER, PAV_X1, PAVER):
            v.line(x, PAV_Y1, x, -150 if SD1[0] <= x <= SD1[1] else 0, w=0.05, color="#bbb", layer="A-PAVING")
        for y in range(PAV_Y0 - PAVER, PAV_Y1, -PAVER):
            v.line(PAV_X0, y, PAV_X1, y, w=0.05, color="#bbb", layer="A-PAVING")


def plan_drainage(v, labels=True):
    x0, x1, y0, y1 = SD1
    v.rect(x0, y1, x1 - x0, y0 - y1, w=0.25, fill="#d0d5da", layer="C-DRAIN")
    v.line(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, w=0.35, layer="C-DRAIN")
    for g in (G1, G2):
        v.rect(g[0] - 150, g[1] - 150, 300, 300, w=0.3, fill="#d0d5da", layer="C-DRAIN")
        for i in range(1, 6):
            v.line(g[0] - 150 + i * 50, g[1] - 130, g[0] - 150 + i * 50, g[1] + 130, w=0.08)
    if labels:
        v.leader([(x0 + 300, (y0 + y1) / 2), (x0 + 300, -650), (x0 + 1500, -650)],
                 ["SD1 slot drain 100 wide, 5 x 1.0 m", "units, invert falls E"], size=1.5)
        v.leader([(G1[0] - 100, G1[1] + 100), (G1[0] - 900, G1[1] + 700)], ["G1 yard gully", "300x300 grate"],
                 size=1.5, anchor="end")
        v.leader([(G2[0] - 100, G2[1] + 100), (G2[0] - 900, G2[1] + 700)], ["G2 yard gully", "300x300 grate"],
                 size=1.5, anchor="end")


def plan_screen(v):
    x0, x1 = SCR_X
    for a, b in SCR_POSTS:
        v.rect(x0, b, x1 - x0, a - b, w=0.25, fill="#8a5a2b")
    # fixed lattice panels
    for a, b in ((-5500, -6400), (-7600, -8300)):
        v.rect(x0 + 30, b, 45, a - b, w=0.2, fill="#e7c79a")
    # gate leaf (swings in)
    ga, gb = GATE
    v.line(x0 + 50, ga - 10, x0 + 50 - 980, ga - 10, w=0.25)
    v.arc(x0 + 50, ga - 10, 980, 180, 270, w=0.13)
    v.tag(x1 + 350, (ga + gb) / 2, "G01", shape="rect", r=1.7, size=1.5)


def plan_furniture(v):
    # lounge chair + side table + potted olive (FF&E, by owner)
    cx, cy = 1450, -1350
    pts = [(-380, -400), (380, -400), (380, 400), (-380, 400)]
    a = math.radians(-20)
    rp = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    v.pl(rp, w=0.15, color="#777", dash="1.5,0.8")
    v.circle(1400, -650, 300, w=0.2, color="#777", fill="#fbfbfb")
    v.text(1400, -680, "OL", size=1.4, anchor="middle", color="#555")


# ============================================================ ELEVATION ELEMENTS
def shrub(v, cx, z0, w, h, seed=1, fill=GREEN_F, color=GREEN, flowers=0):
    rnd = random.Random(seed)
    n = 14
    pts = []
    for i in range(n + 1):
        t = math.pi * i / n
        rr = 1 + rnd.uniform(-0.12, 0.1)
        pts.append((cx - math.cos(t) * w / 2 * rr, z0 + math.sin(t) * h * rr))
    v.pl(pts, w=0.18, color=color, fill=fill, closed=True, layer="L-PLANT")
    # inner leaf strokes
    for i in range(int(w * h / 60000) + 3):
        x = cx + rnd.uniform(-w / 2.6, w / 2.6)
        z = z0 + rnd.uniform(h * 0.15, h * 0.8)
        v.line(x, z, x + rnd.uniform(-60, 60), z + rnd.uniform(40, 90), w=0.08, color=color, layer="L-PLANT")
    for i in range(flowers):
        x = cx + rnd.uniform(-w / 2.5, w / 2.5)
        z = z0 + rnd.uniform(h * 0.3, h * 0.92)
        v.circle(x, z, 18, w=0.06, color="#999", fill="#fff")


def vine(v, x, z0, z1, seed=3, amp=60, width=1.0):
    rnd = random.Random(seed)
    pts = []
    z = z0
    while z < z1:
        pts.append((x + math.sin(z / 180 + seed) * amp * width, z))
        z += 40
    v.pl(pts, w=0.12, color=GREEN, closed=False, layer="L-PLANT")
    for i in range(int((z1 - z0) / 110)):
        zz = z0 + rnd.uniform(0, z1 - z0)
        xx = x + math.sin(zz / 180 + seed) * amp * width + rnd.choice((-1, 1)) * rnd.uniform(20, 70)
        v.circle(xx, zz, rnd.uniform(14, 26), w=0.08, color=GREEN, fill=GREEN_F, layer="L-PLANT")
        if rnd.random() < 0.25:
            v.circle(xx + 25, zz + 20, 12, w=0.05, color="#999", fill="#fff")


def olive_elev(v, cx, z0, pot_d=600, pot_h=550, h=2000, seed=5):
    v.pl([(cx - pot_d / 2, z0 + pot_h), (cx + pot_d / 2, z0 + pot_h), (cx + pot_d * 0.38, z0),
          (cx - pot_d * 0.38, z0)], w=0.2, fill="#f7f7f4")
    v.line(cx - 20, z0 + pot_h, cx - 60, z0 + h * 0.55, w=0.25, color="#6b5a45")
    v.line(cx + 20, z0 + pot_h, cx + 70, z0 + h * 0.6, w=0.25, color="#6b5a45")
    shrub(v, cx, z0 + h * 0.45, pot_d * 1.5, h * 0.55, seed=seed, fill="#e4ecd8", color="#6f8a55")


def door_elev(v, kind, x0, x1, z0=0, z1=HEAD, detail=True):
    """Elevation of opening infill as seen from courtyard. Model coords (x, z)."""
    W = x1 - x0
    if kind == "D01":
        v.rect(x0, z0, W, z1 - z0, w=0.35, fill="#5a4a3c", layer="A-DOOR")
        f = 60
        v.rect(x0 + f, z0 + 25, W - 2 * f, z1 - z0 - 25 - f, w=0.2, mat="glass", layer="A-DOOR")
        # leaf frame (slim)
        v.rect(x0 + f, z0 + 25, W - 2 * f, z1 - z0 - 25 - f, w=0.25, fill="none", layer="A-DOOR")
        if detail:
            v.rect(x0 + f + 40, z0 + 950, 20, 300, w=0.15, fill="#999")  # pull handle
            v.line(x0 + f, z0 + 25, x1 - f, (z0 + z1) * 0.5, w=0.08, dash="2,1", color="#666")
            v.line(x0 + f, z1 - f, x1 - f, (z0 + z1) * 0.5, w=0.08, dash="2,1", color="#666")
    elif kind == "D02":
        g = 80
        v.rect(x0, z0, W, z1 - z0, w=0.35, fill="#5b4636", layer="A-DOOR")
        v.rect(x0 + g, z0, W - 2 * g, z1 - z0, w=0.2, fill="#6e5544", layer="A-DOOR")
        if detail:
            z = z0 + 60
            while z < z1:
                v.line(x0 + g, z, x1 - g, z, w=0.08, color="#2e2219", layer="A-DOOR")
                z += 77
            v.rect(x0 + g, z0, W - 2 * g, 60, w=0.15, fill="#4a382b")
    elif kind == "D03":
        lin = 30
        v.rect(x0, z0, W, z1 - z0, w=0.35, fill="#9a6a3c", layer="A-DOOR")
        lx0, lx1 = x0 + lin + 3, x1 - lin - 3
        lz0, lz1 = z0 + 10, z1 - lin - 3
        v.rect(lx0, lz0, lx1 - lx0, lz1 - lz0, w=0.25, fill="#b98552", layer="A-DOOR")
        st, tr, br = 90, 110, 200
        fx0, fx1, fz0, fz1 = lx0 + st, lx1 - st, lz0 + br, lz1 - tr
        ncol, nrow = 6, 18
        bar = 36
        a = (fx1 - fx0 - (ncol - 1) * bar) / ncol
        b = (fz1 - fz0 - (nrow - 1) * bar) / nrow
        if detail:
            for i in range(ncol):
                for j in range(nrow):
                    xx = fx0 + i * (a + bar)
                    zz = fz0 + j * (b + bar)
                    v.rect(xx, zz, a, b, w=0.06, fill="#3b2a1d", layer="A-DOOR")
        else:
            v.rect(fx0, fz0, fx1 - fx0, fz1 - fz0, w=0.1, fill="#6d4c2f")
        return {"leaf": (lx1 - lx0, lz1 - lz0), "open": (a, b), "bar": bar, "field": (fx1 - fx0, fz1 - fz0)}


def lattice_panel(v, u0, u1, z0, z1, pitch=120, bar=40, fill="#b98552", hole="#3b2a1d"):
    v.rect(u0, z0, u1 - u0, z1 - z0, w=0.25, fill=fill, layer="A-TIMBER")
    n = int((u1 - u0 - bar) // pitch)
    m = int((z1 - z0 - bar) // pitch)
    if n < 1 or m < 1:
        return
    sx = (u1 - u0 - bar) / n
    sz = (z1 - z0 - bar) / m
    for i in range(n):
        for j in range(m):
            v.rect(u0 + bar + i * sx, z0 + bar + j * sz, sx - bar, sz - bar, w=0.05, fill=hole, layer="A-TIMBER")


def ac_unit(v, u0, u1, z0, z1):
    v.rect(u0, z0, u1 - u0, z1 - z0, w=0.25, fill="#f2f2f2", dash=None)
    cx = u0 + (u1 - u0) * 0.62
    cz = (z0 + z1) / 2
    r = min(u1 - u0, z1 - z0) * 0.36
    v.circle(cx, cz, r, w=0.15, color="#777")
    v.circle(cx, cz, r * 0.2, w=0.1, color="#777")
    v.text(u0 + 40, z1 - 120, "AC (exist.)", size=1.2, color="#666")


def ground(v, u0, u1, z, depth=300, mat="earth"):
    v.pl([(u0, z), (u1, z), (u1, z - depth), (u0, z - depth)], w=0, mat=mat)
    v.line(u0, z, u1, z, w=0.5)


def paving_level(x):
    """Finished paving level (m) at plan x (cross fall)."""
    if x <= DRAIN_X:
        return LV_KERB + (LV_VALLEY - LV_KERB) * (x - PAV_X0) / (DRAIN_X - PAV_X0)
    return LV_VALLEY + (LV_EASTWALL - LV_VALLEY) * (x - DRAIN_X) / (PAV_X1 - DRAIN_X)
