"""Shadow study — OPTION E (rectangle 3.06 x 3.44 to the end of the AC line, AC above the roof, columns flush under
the roof) through ALL SEASONS: 21 March (spring), 21 June (summer), 21 September (autumn), 21 December (winter),
09:00 / 12:00 / 15:00 / 18:00 local clock time (EET UTC+2 in March and December, EEST UTC+3 in June and September).
Same method and layout as SH-02 (shadow_study.py): Athens, north towards the upper-left corner of the plan.
"""
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
from cad import Sheet, PROJECT
import build
import shadow_study as S

S.IMG = os.path.join(S.OUT, "Shadow_Study_E_seasons")
KEY = "E"
VER = dict(v="V1", L=3.06, T=None, title="OPTION E — rectangle 3.06 x 3.44 to the end of the AC line",
           poly=[(8.0, 0.0), (11.06, 0.0), (11.06, 3.44), (8.0, 3.44)], cols=[9.53, 10.96])
EXTRA = "&acz=3.0&coltop=flush"                    # AC above the roof, columns flush under the roof (as C22-E)
SEASONS = [(3, "21 MARCH", "SPRING", 2), (6, "21 JUNE", "SUMMER", 3), (9, "21 SEPTEMBER", "AUTUMN", 3),
           (12, "21 DECEMBER", "WINTER", 2)]
TIMES = S.TIMES
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def sun_table():
    out = {}
    for m, _, _, tz in SEASONS:
        for h, _ in TIMES:
            dt = datetime(2026, m, 21, h, 0, tzinfo=timezone(timedelta(hours=tz))).astimezone(timezone.utc)
            out[(m, h)] = S.sun_position(dt)
    return out


def night(path):
    im = Image.new("RGB", (S.W, S.H), (40, 44, 58))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 64)
    t = "sun below the horizon"
    d.text(((S.W - d.textlength(t, font=f)) / 2, S.H / 2 - 40), t, fill=(235, 235, 240), font=f)
    im.save(path, quality=86)


def render(sun):
    os.makedirs(S.IMG, exist_ok=True)
    jobs = []
    for m, *_ in SEASONS:
        for h, _ in TIMES:
            alt, az = sun[(m, h)]
            out = os.path.join(S.IMG, f"{KEY}_{m:02d}_{h:02d}.png")
            if alt <= 0.5:
                night(out.replace(".png", "_ov.jpg"))
                continue
            jobs.append(dict(out=out, v=VER["v"], L=VER["L"], T=VER["T"], az=round((az - S.PLAN_UP) % 360, 2),
                             alt=round(alt, 2), extra=EXTRA))
    jp = os.path.join(S.IMG, "jobs.json")
    json.dump(jobs, open(jp, "w"))
    subprocess.run(["node", os.path.join(S.REN, "shadow.js"), jp], check=True, cwd=S.REN)
    os.remove(jp)
    for j in jobs:
        m, h = int(os.path.basename(j["out"])[2:4]), int(os.path.basename(j["out"])[5:7])
        alt, az = sun[(m, h)]
        S.overlay(j["out"], VER, alt, az)


def project():
    p = dict(PROJECT)
    p.update(rev="C23", date="09.10.2026", name="COURTYARD ROOF — SHADOW STUDY",
             site="Sun & shadow through the seasons (21 Mar / Jun / Sep / Dec), Athens 37.98 N; " + VER["title"] +
                  "; roof supported by the tall wall, AC above the roof",
             status="SHADOW STUDY — orientation per client: NORTH towards the upper-left corner of the plan (tall wall "
                    "faces NE)",
             revs=[["C23", "09.10.2026", "Shadow study, all seasons, option E (3.06 x 3.44)"],
                   ["C22", "08.10.2026", "Options E / F, columns flush under the roof"],
                   ["C19", "08.10.2026", "Shadow study May-Aug, north towards the upper-left"]])
    return p


def sheet(sun):
    s = Sheet("SH-E1", "SHADOW STUDY\nOPTION E — all seasons", "NTS (plan views)", series="SUN / SHADOW",
              project=project())
    s.frame()
    s.text(16, 14, "WHERE THE SHADOW FALLS — ALL SEASONS — OPTION E (rectangle 3.06 x 3.44)", size=3.2, weight="bold",
           color="#c0392b")
    s.text(16, 19.5, "Top views as the drawings — NORTH = upper-left (dial). ROOF = see-through white with red outline; "
                     "dark = shade on the ground (roof + annex + walls); dial top-right = where the sun is.", size=1.7)
    cw, ch, gx, gy = 76, 76 * S.H / S.W, 2, 7.5
    xs = [30 + i * (cw + gx) for i in range(4)]
    y0 = 30
    for i, (_, tl) in enumerate(TIMES):
        s.text(xs[i] + cw / 2, y0 - 2.5, tl + (" (morning)" if i == 0 else " (evening)" if i == 3 else ""), size=2.2,
               anchor="middle", weight="bold")
    for r, (m, dl, season, tz) in enumerate(SEASONS):
        y = y0 + r * (ch + gy)
        s.text(19.5, y + ch / 2 + 1, season, size=2.4, anchor="middle", weight="bold", rot=-90)
        s.text(24.5, y + ch / 2 + 1, dl, size=1.8, anchor="middle", rot=-90)
        for i, (h, _) in enumerate(TIMES):
            S.embed(s, os.path.join(S.IMG, f"{KEY}_{m:02d}_{h:02d}_ov.jpg"), xs[i], y, cw, ch)
            alt, az = sun[(m, h)]
            cap = (f"sun height {alt:.0f}°, from {S.compass(az)} ({az:.0f}°)" if alt > 0.5 else "night — no sun")
            s.text(xs[i], y + ch + 3.2, cap + f"   [{'EET' if tz == 2 else 'EEST'}]", size=1.45)
    s.textblock(16, 262, 322, [
        ("B", "HOW TO READ — OPTION E through the year"),
        "SUMMER (21 June): sun very high at midday (~70°): the roof's shade sits close under the roof; mornings are shaded "
        "by the tall wall (sun in the east, over the wall); evenings the annex and the garden wall shade most of the "
        "courtyard.",
        "SPRING / AUTUMN (21 March / 21 September): sun at ~50° at midday; the roof's shade reaches further out (about "
        "2 m) from under the roof, towards the tall wall and the annex door; the tall wall shades the courtyard in the "
        "morning.",
        "WINTER (21 December): sun low all day (12-28°), from the south-east to the south-west: in the morning and at "
        "midday it reaches in under the roof (the roof hardly blocks the winter sun — warm corner); by 15:00 the low "
        "garden wall shades most of the courtyard; after ~17:10 the sun has set (18:00 shown as night).",
        "Assumptions: Athens 37.98 N, 21st of the month, local clock time (EET / EEST); NORTH towards the upper-left of the "
        "plan (client); existing trees not included (they add shade)."], size=1.45, gap=0.25)
    return s


if __name__ == "__main__":
    sun = sun_table()
    if not os.environ.get("SKIP_RENDER"):
        render(sun)
    pdf = build.to_pdf([sheet(sun)], "Rev-C23_Shadow-Study_Option-E_All-Seasons")
    d = os.path.join(S.OUT, "Rev-C23_png")
    os.makedirs(d, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(d, "SH-E1")], check=True)
    for (m, h), (alt, az) in sorted(sun.items()):
        print(m, h, f"alt {alt:.1f} az {az:.1f}")
    print(pdf)
