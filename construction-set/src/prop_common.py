"""Shared context (existing courtyard) for alternative proposals B, C, D."""
from cad import Sheet, View, break_line, PROJECT, MAT
from common import *  # noqa
from design import *  # noqa
from sheets_b import ladder, paving_cut


def project(code, name):
    p = dict(PROJECT)
    p["name"] = f"COURTYARD — PROPOSAL {code}"
    p["site"] = name + " — alternative to Design A (same courtyard, existing doors retained)"
    p["status"] = "DESIGN PROPOSAL — developed design, buildable; confirm by survey & engineer before construction"
    return p


def ctx_plan(v, planter=True, screen=True, doors=True, rooms=False, soil=True):
    plan_walls(v, show_rooms=rooms)
    if doors:
        plan_doors(v)
    if planter:
        plan_planter(v, soil=soil, label=False)
    if screen:
        plan_screen(v)


def porcelain_grid(v, x0, x1, y0, y1, m=600, col="#d9d4cc"):
    v.rect(x0, y1, x1 - x0, y0 - y1, w=0.25, fill=col)
    x = x0 + m
    while x < x1:
        v.line(x, y1, x, y0, w=0.06, color="#9a948b")
        x += m
    y = y0 - m
    while y > y1:
        v.line(x0, y, x1, y, w=0.06, color="#9a948b")
        y -= m


def ctx_elev(v, planter=True, ac=True, solar=True, east_wall=True, levels=True, px_ladder=14.5, extra_levels=()):
    ground(v, -250, 7350, -5, depth=250)
    v.rect(0, -5, COURT_W, FAC_PARAPET + 5, w=0.35, fill="#f7f3ea")
    v.rect(0, FAC_PARAPET - 50, COURT_W, 50, w=0.25, fill="#efe9dd")
    if solar:
        v.rect(SOLAR[0], FAC_PARAPET + 150, SOLAR[1] - SOLAR[0], 450, w=0.2, dash="2,1", color="#777")
    door_elev(v, "D01", *D01)
    door_elev(v, "D02", *D02)
    door_elev(v, "D03", *D03)
    if ac:
        ac_unit(v, *AC1)
    v.rect(-BW_T, -5, BW_T, BW_TOP + 5, mat="masonry", w=0.45)
    v.rect(-BW_T - 25, BW_TOP, BW_T + 50, 50, w=0.3, fill="#e8e3d8")
    if planter:
        v.rect(0, -5, KERB_X1, COP_TOP - COP_T + 5, w=0.3, mat="render")
        v.rect(0, COP_TOP - COP_T, COP_X1, COP_T, w=0.3, fill="#efe9dd")
    if east_wall:
        v.rect(COURT_W, -65, 150, 4200, w=0.35, fill="#f2eee6")
        break_line(v, COURT_W, 4135, COURT_W + 150, 4135)
    if levels:
        lv = [(0, "±0.000 FFL"), (HEAD, "+2.400 heads"), (FAC_PARAPET, "+3.400 parapet")] + list(extra_levels)
        ladder(v, -BW_T, sorted(lv), px_ladder)


def ctx_section_ns(v, y_min=-4400, y_max=1200, zt=-25, door=True):
    """N-S section context at a door (looking west): façade, slab, internal floor, paving."""
    paving_cut(v, [(y_min, zt), (-200, zt), (-130, -15)], z_bottom_extra=320)
    sx0, sx1 = SD1[3], SD1[2]
    v.rect(sx0 - 100, -345, 300, 330, w=0.2, mat="conc")
    v.rect(sx0, -245, sx1 - sx0, 230, w=0.25, mat="alu")
    v.rect(sx0 + 8, -237, sx1 - sx0 - 16, 200, w=0.1, fill="#fff")
    v.rect(FAC_T, -70, y_max - FAC_T, 70, w=0.2, mat="sand")
    v.rect(FAC_T, -220, y_max - FAC_T, 150, w=0.25, mat="rc")
    v.rect(0, -900, FAC_T, 900, w=0.2, mat="masonry")
    if door:
        v.rect(90, -15, 120, 35, w=0.2, fill="#888")
        v.rect(120, 20, 60, HEAD - 90, w=0.15, fill="#5a4a3c")
        v.rect(90, HEAD - 70, 120, 70, w=0.2, fill="#5a4a3c")
        v.rect(0, HEAD, FAC_T, SLAB_SOFFIT - HEAD, w=0.3, mat="rc")
    else:
        v.rect(0, 0, FAC_T, SLAB_SOFFIT, w=0.3, mat="masonry")
    v.rect(0, SLAB_SOFFIT, y_max, SLAB_TOP - SLAB_SOFFIT, w=0.3, mat="rc")
    v.rect(0, SLAB_TOP, FAC_T, FAC_PARAPET - SLAB_TOP - 40, w=0.3, mat="masonry")
    v.rect(-30, FAC_PARAPET - 40, FAC_T + 60, 40, w=0.25, fill="#e8e3d8")
    break_line(v, y_max, -250, y_max, 50)
    break_line(v, y_max, SLAB_SOFFIT - 80, y_max, SLAB_TOP + 80)


def cover(code, title, tagline, axo_fn, concept, features, compare, register, scale=60, ox=88, oy=118):
    s = Sheet(f"{code}-000", f"Proposal {code} — cover, concept & drawing register", "NTS",
              project=project(code, title))
    s.frame()
    s.text(16, 20, f"PROPOSAL {code} — {title.upper()}", size=6.2, weight="bold")
    s.text(16, 28, tagline, size=2.5)
    s.line(16, 31, 336, 31, w=0.6)
    s.text(16, 38, "AXONOMETRIC FROM SOUTH-EAST (east wall cut away at 1.0 m) — NTS", size=1.8, weight="bold")
    axo_fn(s, ox, oy, scale)
    s.text(222, 40, "DRAWING REGISTER", size=2.2, weight="bold")
    s.table(222, 42, [("No.", 16), ("Title", 100)], [[a, b] for a, b in register], size=1.5)
    y = 42 + 6 + len(register) * 3.6 + 6
    s.text(222, y, "COMPARISON WITH DESIGN A", size=2.0, weight="bold")
    s.table(222, y + 2, [("Criterion", 40), ("Design A", 38), (f"Prop. {code}", 38)], compare, size=1.4)
    s.textblock(16, 212, 200, [("B", "CONCEPT")] + concept + [("B", "KEY FEATURES")] + features, size=1.5,
                gap=0.3)
    return s


def boq_sheet(code, title, rows, notes=""):
    s = Sheet(f"{code}-600", f"Proposal {code} — schedules & bill of quantities", "NTS", series="QUANTITIES",
              project=project(code, title))
    s.frame()
    half = (len(rows) + 1) // 2
    for k, part in enumerate((rows[:half], rows[half:])):
        fills = {i: "#efece6" for i, r in enumerate(part) if r[0].isdigit() and "." not in r[0]}
        s.table(16 + k * 162, 14, [("Item", 11), ("Description", 92), ("Unit", 12), ("Qty", 22), ("Rate", 22)],
                part, size=1.45, fills=fills)
    if notes:
        s.textblock(16, 262, 320, [notes], size=1.5)
    return s
