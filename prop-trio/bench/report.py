"""Self-contained HTML report (no external files, opens offline)."""
from __future__ import annotations

import html
from datetime import date

CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#16181d;--dim:#5b616e;--line:#e3e1da;--acc:#0f6e66;
--good:#1b7a46;--bad:#a8322d;--warn:#8a5a10;--s1:#2f6fb0;--s2:#b5651d;--s3:#6a4fb3;--sel:#e9f4f2}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#111317;--card:#181b21;--ink:#e7e9ee;
--dim:#9aa1ad;--line:#2b303a;--acc:#4cc2b5;--good:#5ccf8c;--bad:#ef7d77;--warn:#e0b060;--s1:#6aa8ec;
--s2:#e69a55;--s3:#a58ef0;--sel:#16302d}}
:root[data-theme=dark]{--bg:#111317;--card:#181b21;--ink:#e7e9ee;--dim:#9aa1ad;--line:#2b303a;--acc:#4cc2b5;
--good:#5ccf8c;--bad:#ef7d77;--warn:#e0b060;--s1:#6aa8ec;--s2:#e69a55;--s3:#a58ef0;--sel:#16302d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1120px;margin:0 auto;padding:32px 16px 80px}
h1{font-size:28px;margin:0 0 6px;letter-spacing:-.01em}h2{font-size:19px;margin:36px 0 8px}
h3{font-size:14px;margin:18px 0 6px;color:var(--dim);text-transform:uppercase;letter-spacing:.08em}
p{max-width:78ch;margin:6px 0}.dim{color:var(--dim)}.good{color:var(--good)}.bad{color:var(--bad)}
.banner{border:2px solid var(--bad);color:var(--bad);padding:10px 14px;border-radius:6px;margin:14px 0;font-weight:600}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--card);margin:8px 0}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:13px}
th,td{padding:7px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim);background:var(--bg)}
th.l,td.l{text-align:left;white-space:normal}tr.sel td{background:var(--sel)}tr:last-child td{border-bottom:0}
.tag{font-size:11px;padding:1px 6px;border-radius:3px;border:1px solid var(--line);color:var(--dim)}
.chart{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:10px;margin:8px 0}
.chart svg{width:100%;height:auto;display:block}.key{font-size:12px;color:var(--dim)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}
"""


def e(x):
    return html.escape(str(x))


def money(x):
    if x is None:
        return "–"
    return ("−$" if x < 0 else "$") + f"{abs(x):,.0f}"


def pct(x, d=0):
    return "–" if x is None else f"{100 * x:.{d}f}%"


def num(x, d=2):
    return "–" if x is None else f"{x:,.{d}f}"


def stat_cells(s):
    if not s or not s.get("trades"):
        return "<td>0</td>" + "<td>–</td>" * 8
    return (f"<td>{s['trades']}</td><td>{pct(s['win_rate'])}</td><td>{money(s['avg_trade'])}</td>"
            f"<td>{num(s['profit_factor'])}</td><td>{money(s['net'])}</td><td>{money(s['max_dd'])}</td>"
            f"<td><b>{num(s['net_over_dd'])}</b></td>"
            f"<td>{pct(s['pct_target'])} / {pct(s['pct_stop'])} / {pct(s['pct_time'])}</td>"
            f"<td>{num(s['trades_per_year'], 0)}</td>")


STAT_HEAD = ("<th>Trades</th><th>Win</th><th>Avg</th><th>PF</th><th>Net</th><th>Max DD</th>"
             "<th>Net/DD</th><th>Target/stop/time</th><th>/yr</th>")


def curve_svg(curves: dict, keys, split: str, colors) -> str:
    pts = {k: curves[k] for k in keys if k in curves and curves[k]["t"]}
    if not pts:
        return "<p class='dim'>No trades.</p>"
    def x_of(s):
        return date.fromisoformat(s).toordinal()
    xs = [x_of(t) for c in pts.values() for t in c["t"]]
    ys = [y for c in pts.values() for y in c["eq"]] + [0.0]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    W, H, L, B = 1000, 250, 64, 22
    sx = lambda x: L + (W - L - 8) * (x - x0) / max(x1 - x0, 1)
    sy = lambda y: 8 + (H - B - 8) * (1 - (y - y0) / max(y1 - y0, 1e-9))
    out = [f"<svg viewBox='0 0 {W} {H}' role='img'>"]
    for frac in (0, .5, 1):
        yv = y0 + frac * (y1 - y0)
        out.append(f"<line x1='{L}' x2='{W - 8}' y1='{sy(yv):.1f}' y2='{sy(yv):.1f}' stroke='var(--line)'/>"
                   f"<text x='{L - 6}' y='{sy(yv) + 4:.1f}' font-size='10' text-anchor='end' fill='var(--dim)'>{money(yv)}</text>")
    try:
        xs_ = sx(x_of(split))
        if L <= xs_ <= W:
            out.append(f"<line x1='{xs_:.1f}' x2='{xs_:.1f}' y1='8' y2='{H - B}' stroke='var(--dim)' stroke-dasharray='3 3'/>"
                       f"<text x='{xs_ + 4:.1f}' y='18' font-size='10' fill='var(--dim)'>out-of-sample →</text>")
    except ValueError:
        pass
    for yr in range(date.fromordinal(x0).year + 1, date.fromordinal(x1).year + 1):
        xv = sx(date(yr, 1, 1).toordinal())
        out.append(f"<text x='{xv:.1f}' y='{H - 6}' font-size='10' text-anchor='middle' fill='var(--dim)'>{yr}</text>")
    for k, c in pts.items():
        step = max(1, len(c["t"]) // 1500)
        p = " ".join(f"{sx(x_of(t)):.1f},{sy(y):.1f}" for t, y in list(zip(c["t"], c["eq"]))[::step])
        dash = " stroke-dasharray='5 3'" if "selected" in k else ""
        out.append(f"<polyline fill='none' stroke='{colors[k]}' stroke-width='1.6'{dash} points='{p}'/>")
    out.append("</svg>")
    return "".join(out)


def render(r: dict) -> str:
    m = r["meta"]
    h = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' "
         f"content='width=device-width,initial-scale=1'><title>Prop Trio Backtest</title><style>{CSS}</style>"
         "</head><body><div class='wrap'>"]
    h.append("<h1>Prop Trio — Matteo's three NQ strategies, tested</h1>")
    h.append(f"<p class='dim'>{e(', '.join(m.get('files', [])))} · {e(m.get('first'))} → {e(m.get('last'))} CT · "
             f"clock {e(m.get('tz_source'))}, bars stamped at {e(m.get('stamp'))} · out-of-sample from "
             f"<b>{e(m['split'])}</b> · generated {e(m['generated'])}</p>")
    if m.get("synthetic"):
        h.append("<div class='banner'>SYNTHETIC DATA — this run only checks the plumbing. "
                 "Every number below is meaningless for trading.</div>")
    c = m["costs"]
    h.append(f"<p class='dim'>Costs ${c['commission_nq_side']}/NQ/side, ${c['commission_mnq_side']}/MNQ/side, "
             f"{c['slip_ticks']} tick slippage on market and stop fills. Fills on 1-minute bars, "
             f"{e(m['fill']['policy'])}, limit targets {'need a trade-through' if m['fill']['limit_through'] else 'fill on touch'}. "
             f"Dollar figures per one NQ contract unless marked.</p>")

    # claims
    h.append("<h2>Matteo's claims against the data</h2><div class='tw'><table><tr><th class='l'>Claim</th>"
             "<th class='l'>Where</th><th>Measured</th><th class='l'>On</th></tr>")
    for cl in r["claims"]:
        v = cl["measured"]
        if isinstance(v, list):
            vs = " / ".join(pct(x) for x in v)
        elif v is None:
            vs = "–"
        elif "share" in cl["unit"] or "pass rate" in cl["unit"]:
            vs = pct(v)
        elif "$" in cl["unit"]:
            vs = money(v)
        else:
            vs = num(v)
        h.append(f"<tr><td class='l'>{e(cl['claim'])}</td><td class='l dim'>{e(cl['source'])}</td>"
                 f"<td><b>{vs}</b></td><td class='l dim'>{e(cl['unit'])}</td></tr>")
    h.append("</table></div>")

    # strategies
    colors = {"S1 faithful": "var(--s1)", "S1 selected": "var(--s1)", "S2 faithful": "var(--s2)",
              "S2 selected": "var(--s2)", "S3 faithful": "var(--s3)", "S3 selected": "var(--s3)"}
    names = {"S1": "S1 Vault Break", "S2": "S2 VWAP pullback + ADX", "S3": "S3 Overnight bias ORB"}
    h.append("<h2>Each strategy, faithful and pre-registered variants</h2>"
             "<p>Shaded row = the version the in-sample rule picked (highest in-sample net ÷ drawdown, "
             "≥ 100 trades). Rows marked <span class='tag'>sens</span> are readings of an ambiguous rule, "
             "never eligible for selection.</p>")
    for s, block in r["strategies"].items():
        h.append(f"<h3>{e(names[s])}</h3><div class='tw'><table><tr><th class='l'>Version</th><th></th>"
                 + STAT_HEAD + "</tr>")
        for v in block["variants"]:
            cls = " class='sel'" if v["label"] == block["selected"] else ""
            for per in ("IS", "OOS"):
                lab = (f"{e(v['label'])}" + ("" if v["candidate"] else " <span class='tag'>sens</span>")) if per == "IS" else ""
                h.append(f"<tr{cls}><td class='l'>{lab}</td><td class='dim'>{per}</td>{stat_cells(v[per])}</tr>")
        h.append("</table></div>")
        h.append(f"<div class='chart'>{curve_svg(r['curves'], [f'{s} faithful', f'{s} selected'], m['split'], colors)}"
                 f"<div class='key'>Cumulative net per NQ. Solid: faithful. Dashed: selected "
                 f"({e(block['selected'])}).</div></div>")
        years = sorted({y for v in block["variants"][:1] for y in v["yearly"]})
        if years:
            h.append("<div class='tw'><table><tr><th class='l'>Net per NQ by year</th>"
                     + "".join(f"<th>{y}</th>" for y in years) + "</tr>")
            for v in block["variants"]:
                if v["label"] in ("faithful", block["selected"]):
                    h.append(f"<tr><td class='l'>{e(v['label'])}</td>" + "".join(
                        f"<td class='{'bad' if v['yearly'].get(y, 0) < 0 else ''}'>{money(v['yearly'].get(y, 0))}</td>"
                        for y in years) + "</tr>")
            h.append("</table></div>")

    # correlation
    h.append("<h2>Daily P&amp;L correlation (faithful versions)</h2><div class='grid'>")
    for per in ("IS", "OOS"):
        cm = r["correlation"][per]["all_days"]
        ks = list(cm)
        h.append(f"<div class='tw'><table><tr><th class='l'>{per}, all days</th>"
                 + "".join(f"<th>{k}</th>" for k in ks) + "</tr>")
        for a in ks:
            h.append(f"<tr><td class='l'>{a}</td>" + "".join(f"<td>{num(cm[a][b])}</td>" for b in ks) + "</tr>")
        h.append("</table></div>")
    h.append("</div><p class='dim'>Matteo's claim is below 0.25 between every pair.</p>")

    # prop books
    h.append("<h2>Prop-firm challenges</h2><p>Rolling: a challenge started on every trading day "
             "(overlapping, so not independent). Bootstrap: 5-day blocks of real days reshuffled into "
             "independent challenges. Back-to-back: buy one, run it out, buy the next. Sizes in micros.</p>")
    profiles = []
    for x in r["books"]:
        if x["profile"] not in profiles:
            profiles.append(x["profile"])
    for pf in profiles:
        h.append(f"<h3>{e(pf)}</h3><div class='tw'><table><tr><th class='l'>Book</th><th class='l'>Micros</th>"
                 "<th>IS pass</th><th>OOS pass</th><th>OOS bootstrap</th><th>OOS fail</th>"
                 "<th>OOS median days</th><th>OOS tries per pass</th></tr>")
        for name in dict.fromkeys(x["book"] for x in r["books"]):
            row = {x["period"]: x for x in r["books"] if x["book"] == name and x["profile"] == pf}
            if "OOS" not in row:
                continue
            o, i = row["OOS"], row.get("IS")
            bb = o["back_to_back"]
            tries = (bb["attempts"] / bb["passes"]) if bb.get("passes") else None
            mix = ", ".join(f"{k} {v}" for k, v in o["mix"].items() if v)
            h.append(f"<tr><td class='l'>{e(name)}</td><td class='l dim'>{e(mix)}</td>"
                     f"<td>{pct(i['rolling']['pass_rate']) if i else '–'}</td>"
                     f"<td><b>{pct(o['rolling']['pass_rate'])}</b></td><td>{pct(o['bootstrap']['pass_rate'])}</td>"
                     f"<td>{pct(o['rolling']['fail_rate'])}</td><td>{num(o['rolling']['median_days_to_pass'], 0)}</td>"
                     f"<td>{num(tries, 1)}</td></tr>")
        h.append("</table></div>")

    sz = r["sizing"]
    h.append("<h3>In-sample sizing search (Apex 50K), top mixes</h3><div class='tw'><table>"
             "<tr><th class='l'>Set</th><th class='l'>Micros</th><th>IS pass</th><th>IS median days</th></tr>")
    for setname in ("faithful", "improved"):
        for row in sz[setname]["top"][:5]:
            mix = ", ".join(f"{k} {int(row[k])}" for k in row
                            if k in ("S1", "S2", "S3", "S1*", "S2*", "S3*") and row[k])
            h.append(f"<tr><td class='l'>{setname}</td><td class='l'>{e(mix)}</td><td>{pct(row['pass_rate'])}</td>"
                     f"<td>{num(row['median_days_to_pass'], 0)}</td></tr>")
    h.append("</table></div>")

    br = r["bench_rule"]
    h.append("<h3>Bench rule (75th-percentile Monte Carlo drawdown, back at a new high)</h3><p>"
             + "; ".join(f"{e(k)}: kept {v['kept']} of {v['of']} trades" for k, v in br.items()) + "</p>")

    # sensitivity
    h.append("<h2>Fill and cost sensitivity (faithful versions)</h2><div class='tw'><table>"
             "<tr><th class='l'>Change</th><th class='l'>Strategy</th><th></th>" + STAT_HEAD + "</tr>")
    for sv in r["sensitivity"]:
        for per in ("IS", "OOS"):
            h.append(f"<tr><td class='l'>{e(sv['label']) if per == 'IS' else ''}</td>"
                     f"<td class='l'>{e(sv['strategy']) if per == 'IS' else ''}</td><td class='dim'>{per}</td>"
                     f"{stat_cells(sv[per])}</tr>")
    h.append("</table></div>")
    h.append("<p class='dim'>Rules, sources and the pre-registered test plan: SPEC.md. "
             f"Run time {m.get('runtime_s')} s.</p></div></body></html>")
    return "".join(h)
