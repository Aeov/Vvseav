"""FINAL — V2T technical design, minimal set (client: "make it minimal").

Sheets: V2T-01 top view & roof framing · V2T-02 views, section & 3D · V2T-03 roof section & details
(from the agreed client-check module, re-issued as FINAL T01) + V2T-04 3D views & schedules.
"""
import base64
import io
import os
from PIL import Image
from cad import Sheet
import build
import fin_base as F

try:
    import preview_c14 as P
except ImportError:          # planting round not available
    import preview_c13 as P

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
NAME = "V2T_FINAL_Technical-Design"
REFS = {"B1": "V2T-03 sect. 1 — M12 A4 resin @ 400", "B2": "V2T-03 D2 — FP 12 + 2 M16",
        "B3": "V2T-03 D1 — 10 mm fork lugs", "B4": "V2T-03 D3 — mitred, 12 mm end plate",
        "J1-J3": "cleats, 2 M12 each end", "C1, C2": "V2T-03 sect. 1 + D2", "BR": "V2T-03 D2 — welded / 2 M16",
        "H1, H2": "V2T-03 D1", "WP": "V2T-03 D1 — 4 M12 A4 resin each", "WA": "V2T-03 sect. 1 — 2 M12 A4 resin",
        "BP": "4 M16 HD anchors into F1/F2", "F1, F2": "V2T-03 sect. 1 (verify wall footing)"}
REVS = [["T01", "07.10.2026", "FINAL technical design V2T (minimal set) — for tender & construction"],
        ["C14", "07.10.2026", "Planting per client reference: jasmine, low shrubs, uplights"],
        ["C13", "07.10.2026", "Planter 0.70, soil + low planting; garden wall continues"]]
_base_project = P.project


def project(vk):
    p = _base_project(vk)
    p["rev"] = "T01"
    p["status"] = ("FINAL TECHNICAL DESIGN — for tender & construction. Structure subject to licensed engineer's "
                   "sign-off; verify all dimensions on site")
    p["revs"] = REVS
    return p


P.project = project          # every sheet function looks it up at call time


def img(s, path, x, y, w, h, caption):
    im = Image.open(path).convert("RGB")
    im.thumbnail((1500, 1000))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84)
    b64 = base64.b64encode(buf.getvalue()).decode()
    s.add(f'<image href="data:image/jpeg;base64,{b64}" x="{x}" y="{y}" width="{w}" height="{h}" '
          f'preserveAspectRatio="xMidYMid slice"/>')
    s.rect(x, y, w, h, lw=0.3)
    s.text(x, y + h + 3.2, caption, size=1.7, weight="bold")


def render(view, light):
    for p in (f"Render_C14/V2T_{view}_{light}.png", f"Render_C14/V2T_{view}.png", f"Render_C13/V2T_{view}.png"):
        f = os.path.join(OUT, p)
        if os.path.exists(f):
            return f
    raise FileNotFoundError(view + " " + light)


def sheet_3d():
    s = Sheet("V2T-04", "V2T TRIANGLE + RODS\n3D views & schedules", "NTS", project=project("V2T"))
    s.frame()
    s.text(16, 14, "VERSION 2T — TRIANGLE, 0.90 m VOID + 2 RODS — FINAL", size=3.2, weight="bold", color=P.RED)
    img(s, render("eye", "dusk"), 16, 20, 158, 105.3, "1  EVENING — LED soffit + uplights (as client reference)")
    img(s, render("eye", "day"), 180, 20, 158, 105.3, "2  DAY — same view as the site photo")
    y0 = 136
    s.text(16, y0, "STEEL & MEMBER SCHEDULE", size=2.1, weight="bold")
    s.table(16, y0 + 2, [("Mark", 13), ("Member", 47), ("Section", 33), ("Material / finish", 30),
                         ("Length · qty", 27), ("Connection", 50)],
            [list(m[:5]) + [REFS[m[0]]] for m in F.MEMBERS], size=1.35)
    x2 = 225
    s.text(x2, y0, "FINISHES", size=2.1, weight="bold")
    s.table(x2, y0 + 2, [("Item", 22), ("Specification", 91)], [list(r) for r in F.FINISHES], size=1.3)
    s.text(x2, 172, "ROOF BUILD-UP (top → bottom)", size=2.1, weight="bold")
    s.textblock(x2, 174, 113, [f"{i + 1}. {t}" for i, t in enumerate(F.ROOF_BUILDUP)], size=1.35, gap=0.2)
    y1 = 200
    s.text(16, y1, "PLANTING & LIGHTING SCHEDULE (planter 0.70: 50 bark mulch / 400 topsoil / geotextile / "
                   "100 gravel drainage; drip line 16 mm, 2 L/h @ 0.30)", size=2.1, weight="bold")
    s.table(16, y1 + 2, [("Code", 10), ("Botanical name", 58), ("Common name", 34), ("Size", 22),
                         ("Spacing", 40), ("Mature h", 18), ("Notes", 68)],
            [list(r) for r in F.PLANTING], size=1.35)
    s.textblock(16, 232, 320, [
        "Key data: roof 9.78 m² — plants edge 3.22 + 1.26 = 4.48, void edge 3.22, raked edge 2.84 (63.6°), depth 2.54 "
        "(edges in line with the annex walls); 0.90 m void open to the tall wall; hangers H1/H2 Ø16 SS ≈ 1.14 m @ 28°; "
        "underside +2.36, fascia 0.43 (top +2.79); falls 1:70 to the box gutter on the raked edge, outlet into C2.",
        "Design basis (preliminary, engineer to verify): G 0.50 kN/m² + fascia 0.10 kN/m; Q 0.40 kN/m² (roof not "
        "accessible); snow 0.32 kN/m²; wind uplift ≈ 0.7 kN/m² net — hangers act in tension only, under uplift the "
        "frame spans unaided (rods slack); seismic: light roof, check anchors."], size=1.4, gap=0.3)
    return s


def sheets():
    ss = P.sheets() + [sheet_3d()]
    return ss


if __name__ == "__main__":
    import subprocess
    pdf = build.to_pdf(sheets(), NAME)
    d = os.path.join(OUT, NAME + "_png")
    os.makedirs(d, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(d, "V2T")], check=True)
    print(pdf)
