"""Shadow study — where the roof's shadow falls in MAY / JUNE / JULY / AUGUST, triangle (option C2) and square
(option D, 2.20 x 3.44), both supported by the tall wall.

Sun position: NOAA solar-position equations, Athens 37.98 N / 23.73 E, 21st of each month, 09:00 / 12:00 / 15:00 / 18:00
local summer time (EEST = UTC+3). Assumed orientation: plan north = up (tall wall on the north side, garden wall on the
south side — the solar water heaters on the annex face the garden side); verify on site.
Shadows are real 3D shadows (three.js renderer, top-down view; the roof is hidden from the camera but casts its shadow);
roof, annex, tall wall, low garden wall, posts and planting cast shadows, the existing trees are left out.
"""
import base64
import io
import json
import math
import os
import subprocess
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
from cad import Sheet, PROJECT
import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")
REN = os.path.join(HERE, "..", "render")
IMG = os.path.join(OUT, "Shadow_Study")
LAT, LON = 37.98, 23.73
MONTHS = [(5, "21 MAY"), (6, "21 JUNE"), (7, "21 JULY"), (8, "21 AUGUST")]
TIMES = [(9, "09:00"), (12, "12:00"), (15, "15:00"), (18, "18:00")]
X0, X1, Y0, Y1, W, H = 6.6, 14.6, -1.2, 3.9, 1600, 1020          # plan window (m) and image size (px)
HOUSE_L, WALL_Y0 = 8.0, 3.44
TRI_WALL = 1.754                                                 # option C2: edge at the tall wall (m)
VERSIONS = {
    "C2": dict(v="V1T", L=TRI_WALL, T=round(3.06 - TRI_WALL, 3), title="TRIANGLE — option C2 (tip at the AC line)",
               poly=[(8.0, 0.0), (11.06, 0.0), (8.0 + TRI_WALL, 3.44), (8.0, 3.44)], cols=[9.53, 10.46]),
    "D": dict(v="V1", L=2.2, T=None, title="SQUARE — option D (2.20 x 3.44)",
              poly=[(8.0, 0.0), (10.2, 0.0), (10.2, 3.44), (8.0, 3.44)], cols=[9.3, 10.1]),
}


def sun_position(dt_utc, lat=LAT, lon=LON):
    """NOAA solar position. Returns (altitude, azimuth from north clockwise), degrees."""
    jd = (dt_utc - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400 + 2451545.0
    T = (jd - 2451545.0) / 36525
    r = math.radians
    L0 = (280.46646 + T * (36000.76983 + T * 0.0003032)) % 360
    Ma = 357.52911 + T * (35999.05029 - 0.0001537 * T)
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    C = (math.sin(r(Ma)) * (1.914602 - T * (0.004817 + 0.000014 * T)) + math.sin(r(2 * Ma)) * (0.019993 - 0.000101 * T)
         + math.sin(r(3 * Ma)) * 0.000289)
    om = 125.04 - 1934.136 * T
    lam = L0 + C - 0.00569 - 0.00478 * math.sin(r(om))
    eps = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60 + 0.00256 * math.cos(r(om))
    dec = math.asin(math.sin(r(eps)) * math.sin(r(lam)))
    y = math.tan(r(eps) / 2) ** 2
    eqt = 4 * math.degrees(y * math.sin(2 * r(L0)) - 2 * e * math.sin(r(Ma)) + 4 * e * y * math.sin(r(Ma)) *
                           math.cos(2 * r(L0)) - 0.5 * y * y * math.sin(4 * r(L0)) - 1.25 * e * e * math.sin(2 * r(Ma)))
    tst = dt_utc.hour * 60 + dt_utc.minute + dt_utc.second / 60 + eqt + 4 * lon
    ha = tst / 4 - 180
    cz = math.sin(r(lat)) * math.sin(dec) + math.cos(r(lat)) * math.cos(dec) * math.cos(r(ha))
    zen = math.acos(max(-1, min(1, cz)))
    ca = (math.sin(r(lat)) * math.cos(zen) - math.sin(dec)) / (math.cos(r(lat)) * math.sin(zen))
    a = math.degrees(math.acos(max(-1, min(1, ca))))
    az = (a + 180) % 360 if ha > 0 else (540 - a) % 360
    return 90 - math.degrees(zen), az


def sun_table():
    rows = {}
    for m, _ in MONTHS:
        for h, _ in TIMES:
            dt = datetime(2026, m, 21, h, 0, tzinfo=timezone(timedelta(hours=3))).astimezone(timezone.utc)
            rows[(m, h)] = sun_position(dt)
    return rows


def px(x, y):
    return ((x - X0) / (X1 - X0) * W, (Y1 - y) / (Y1 - Y0) * H)


def dashed(d, pts, fill, width=4, dash=22, gap=12):
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        (x1, y1), (x2, y2) = px(*a), px(*b)
        L = math.hypot(x2 - x1, y2 - y1)
        t = 0
        while t < L:
            t2 = min(L, t + dash)
            d.line([(x1 + (x2 - x1) * t / L, y1 + (y2 - y1) * t / L), (x1 + (x2 - x1) * t2 / L, y1 + (y2 - y1) * t2 / L)],
                   fill=fill, width=width)
            t += dash + gap


def overlay(path, ver, alt, az):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 34)
    pts = [px(*q) for q in ver["poly"]]
    d.line(pts + pts[:1], fill=(200, 30, 30), width=6, joint="curve")
    cxr = sum(p[0] for p in pts) / len(pts)
    cyr = sum(p[1] for p in pts) / len(pts) - 120
    fb = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 44)
    tw = d.textlength("ROOF", font=fb)
    d.rectangle([cxr - tw / 2 - 10, cyr - 6, cxr + tw / 2 + 10, cyr + 50], fill=(255, 255, 255), outline=(200, 30, 30), width=3)
    d.text((cxr - tw / 2, cyr), "ROOF", fill=(200, 30, 30), font=fb)
    # sun direction arrow (towards the sun) in the corner
    cx, cy, R = W - 95, 95, 62
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(255, 255, 255), outline=(60, 60, 60), width=3)
    d.text((cx - 9, cy - R - 2), "N", fill=(0, 0, 0), font=ImageFont.truetype(
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 22))
    sx, sy = cx + math.sin(math.radians(az)) * (R - 12), cy - math.cos(math.radians(az)) * (R - 12)
    d.line([(cx, cy), (sx, sy)], fill=(230, 150, 0), width=6)
    d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=(255, 190, 0), outline=(180, 110, 0), width=2)
    im.save(path.replace(".png", "_ov.jpg"), quality=86)
    os.remove(path)


def render_all():
    sun = sun_table()
    jobs = []
    for key, ver in VERSIONS.items():
        for m, _ in MONTHS:
            for h, _ in TIMES:
                alt, az = sun[(m, h)]
                jobs.append(dict(out=os.path.join(IMG, f"{key}_{m:02d}_{h:02d}.png"), v=ver["v"], L=ver["L"], T=ver["T"],
                                 az=round(az, 2), alt=round(alt, 2)))
    jp = os.path.join(IMG, "jobs.json")
    os.makedirs(IMG, exist_ok=True)
    json.dump(jobs, open(jp, "w"))
    subprocess.run(["node", os.path.join(REN, "shadow.js"), jp], check=True, cwd=REN)
    os.remove(jp)
    for key, ver in VERSIONS.items():
        for m, _ in MONTHS:
            for h, _ in TIMES:
                alt, az = sun[(m, h)]
                overlay(os.path.join(IMG, f"{key}_{m:02d}_{h:02d}.png"), ver, alt, az)
    return sun


def render_3d(sun):
    """3D views of BOTH roofs with the sun of 21 June at the four times."""
    jobs = []
    for key, ver in VERSIONS.items():
        for h, _ in TIMES:
            alt, az = sun[(6, h)]
            jobs.append(dict(out=os.path.join(IMG, f"3D_{key}_06_{h:02d}.png"), v=ver["v"], L=ver["L"], T=ver["T"],
                             az=round(az, 2), alt=round(alt, 2), view="close"))
    jp = os.path.join(IMG, "jobs3d.json")
    json.dump(jobs, open(jp, "w"))
    subprocess.run(["node", os.path.join(REN, "shadow.js"), jp], check=True, cwd=REN)
    os.remove(jp)
    for j in jobs:
        Image.open(j["out"]).convert("RGB").save(j["out"].replace(".png", ".jpg"), quality=86)
        os.remove(j["out"])


def sheet_3d(sun, num):
    s = Sheet(num, "SHADOW STUDY\nboth roofs in 3D (21 June)", "NTS", series="SUN / SHADOW", project=project("C2"))
    s.frame()
    s.text(16, 14, "THE TWO ROOFS — TRIANGLE (C2) and SQUARE (D) — with their shadow on 21 JUNE", size=3.2,
           weight="bold", color="#c0392b")
    s.text(16, 19.5, "Same 3D model as the drawings (roof to the tall wall, no void); sun of 21 June, Athens; view from "
                     "the garden side over the low wall. Month-by-month top views: next two sheets.", size=1.7)
    cw, ch, gx = 76, 76 * H / W, 2
    xs = [30 + i * (cw + gx) for i in range(4)]
    for i, (h, tl) in enumerate(TIMES):
        s.text(xs[i] + cw / 2, 33, tl, size=2.4, anchor="middle", weight="bold")
    for r, key in enumerate(("C2", "D")):
        y = 37 + r * (ch + 22)
        s.text(22, y + ch / 2 + 1, ("TRIANGLE C2" if key == "C2" else "SQUARE D"), size=2.3, anchor="middle",
               weight="bold", rot=-90)
        for i, (h, _) in enumerate(TIMES):
            embed(s, os.path.join(IMG, f"3D_{key}_06_{h:02d}.jpg"), xs[i], y, cw, ch)
            alt, az = sun[(6, h)]
            s.text(xs[i], y + ch + 3.2, f"sun height {alt:.0f}°, from {compass(az)}", size=1.45)
        s.text(30, y + ch + 8.5, VERSIONS[key]["title"] + (": plants edge 3.06, 1.75 at the tall wall" if key == "C2"
               else ": 2.20 along the planter, 2.20 at the tall wall"), size=1.8, weight="bold")
    return s


def embed(s, path, x, y, w, h):
    im = Image.open(path)
    im.thumbnail((1100, 800))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84)
    s.add(f'<image href="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}" x="{x}" y="{y}" '
          f'width="{w}" height="{h}" preserveAspectRatio="none"/>')
    s.rect(x, y, w, h, lw=0.25)


def project(key):
    p = dict(PROJECT)
    p.update(rev="C18", date="08.10.2026", name="COURTYARD ROOF — SHADOW STUDY",
             site=f"Sun & shadow, 21 May - 21 August, Athens 37.98 N; {VERSIONS[key]['title']}; roof supported by the tall "
                  "wall, no void",
             status="SHADOW STUDY — assumed orientation: north = up (tall wall north, garden wall south); verify on site",
             revs=[["C18", "08.10.2026", "Shadow study May-Aug: triangle C2 / square D"],
                   ["C17", "08.10.2026", "Option C2: tip at the AC line"],
                   ["C16", "08.10.2026", "Roof supported by the tall wall (C / D)"]])
    return p


def sheet(key, sun, num):
    ver = VERSIONS[key]
    s = Sheet(num, f"SHADOW STUDY\n{ver['title'].split(' — ')[0]} roof", "NTS (plan views)", series="SUN / SHADOW",
              project=project(key))
    s.frame()
    s.text(16, 14, f"WHERE THE SHADOW FALLS — {ver['title']}", size=3.2, weight="bold", color="#c0392b")
    s.text(16, 19.5, "Top views (north up). ROOF = see-through white with red outline; dark = shade on the ground (roof + annex + walls); "
                     "sun dial top-right of each view shows where the sun is.", size=1.7)
    cw, ch, gx, gy = 76, 76 * H / W, 2, 7.5
    xs = [30 + i * (cw + gx) for i in range(4)]
    y0 = 30
    for i, (_, tl) in enumerate(TIMES):
        s.text(xs[i] + cw / 2, y0 - 2.5, tl + (" (morning)" if i == 0 else " (evening)" if i == 3 else ""), size=2.2,
               anchor="middle", weight="bold")
    for r, (m, ml) in enumerate(MONTHS):
        y = y0 + r * (ch + gy)
        s.text(22, y + ch / 2 + 1, ml, size=2.3, anchor="middle", weight="bold", rot=-90)
        for i, (h, _) in enumerate(TIMES):
            embed(s, os.path.join(IMG, f"{key}_{m:02d}_{h:02d}_ov.jpg"), xs[i], y, cw, ch)
            alt, az = sun[(m, h)]
            s.text(xs[i], y + ch + 3.2, f"sun height {alt:.0f}°, from {compass(az)} ({az:.0f}°)", size=1.45)
    s.textblock(16, 262, 322, [
        ("B", "HOW TO READ (both versions behave the same way; only the size of the shaded patch changes)"),
        "09:00 — sun low in the EAST (25-32°): it shines in under the roof; the roof's shade lands on the annex facade, "
        "so the paving under the roof is mostly in sun (only a strip at the facade is shaded).",
        "12:00 — sun high in the SOUTH-EAST (57-66°): the shade lies under the roof, shifted ~1 m towards the annex and "
        "the tall wall; the planter strip along the garden wall stays in sun.   15:00 — sun high in the SOUTH-WEST: the "
        "shade shifts towards the tall wall and further along the courtyard; the annex shades the door area too.",
        "18:00 — sun low in the WEST: the annex and the tall wall shade almost the whole courtyard; the roof adds little.  "
        f"{'Triangle C2: 3.06 along the planter, 1.75 at the wall — longer shade along the planter side.' if key == 'C2' else 'Square D: 2.20 along the planter and 2.20 at the wall — more shade at the tall-wall side, less along the planter.'}",
        "Assumptions: Athens 37.98 N, 21st of each month, summer time (EEST); plan north = up (tall wall north) — if the "
        "real orientation differs, the pattern rotates with it. Existing trees not included (they add shade)."], size=1.45,
        gap=0.25)
    return s


def compass(az):
    return ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][int((az + 22.5) // 45) % 8]


if __name__ == "__main__":
    sun = sun_table() if os.environ.get("SKIP_RENDER") else render_all()
    if not os.environ.get("SKIP_RENDER"):
        render_3d(sun)
    ss = [sheet_3d(sun, "SH-01"), sheet("C2", sun, "SH-02"), sheet("D", sun, "SH-03")]
    pdf = build.to_pdf(ss, "Rev-C18_Shadow-Study_May-Aug")
    d = os.path.join(OUT, "Rev-C18_png")
    os.makedirs(d, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(d, "SH")], check=True)
    for (m, h), (alt, az) in sorted(sun.items()):
        print(m, h, f"alt {alt:.1f} az {az:.1f}")
    print(pdf)
