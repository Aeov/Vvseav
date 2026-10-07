"""Run the whole pre-registered test (see ../SPEC.md) and write a report.

    python -m bench.run --data "C:/Users/<you>/Desktop/NQ Section"            (laptop)
    python -m bench.run --data data/                                          (pushed files)
    python -m bench.run --synthetic                                           (plumbing check)

Options: --tz America/New_York  --stamp close|open  --split 2023-01-01  --out results/<name>
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np
import pandas as pd

from . import data, prop, report, stats, synth
from . import strategies as st
from .engine import Costs, Fill, config_dict

EPOCH = pd.Timestamp("1970-01-01")


def day_num(ts) -> int:
    return int((pd.Timestamp(ts) - EPOCH).days)


def candidates(ctx: st.Ctx, split_day: int) -> dict:
    """Pre-registered candidates per strategy: (label, params, is_candidate)."""
    atr = ctx.atr_sess(15)
    med = float(atr[(atr.index < split_day)].median())
    return {
        "S1": [("faithful", {}, True),
               ("S1-v1 ATR-scaled exits", {"exits": "atr", "tp_atr": 40.0 / med, "sl_atr": 75.0 / med}, True),
               ("S1-v2 time-of-day noise band", {"noise": "tod"}, True),
               ("sens: ATR = mean of ATR(14)", {"atr_smooth": "sma_of_atr14"}, False)],
        "S2": [("faithful", {}, True),
               ("S2-v1 session VWAP (08:30)", {"vwap_anchor": 510}, True),
               ("S2-v2 exits recalculated each bar", {"exit_mode": "dynamic"}, True),
               ("S2-v3 up to 3 trades a day", {"max_trades": 3}, True),
               ("sens: entries until 15:54", {"entry_cutoff": 955}, False)],
        "S3": [("faithful", {}, True),
               ("S3-v1 overnight from 17:00", {"on_start": 1020}, True),
               ("S3-v2 target 1.5x stop", {"tp_r": 1.5}, True),
               ("sens: overnight from 23:00", {"on_start": 1380}, False),
               ("sens: first signal 09:15", {"entry_start": 555}, False),
               ("sens: first signal 09:30", {"entry_start": 570}, False),
               ("sens: ATR = mean of ATR(14)", {"atr_smooth": "sma_of_atr14"}, False)],
    }, med


def trading_days(ctx: st.Ctx) -> np.ndarray:
    out = []
    for d in ctx.day_ranges:
        i = ctx.first_at(d, 510)
        if i >= 0 and ctx.b.mod[i] <= 515 and pd.Timestamp(int(d) * 86400, unit="s").dayofweek < 5:
            out.append(d)
    return np.array(sorted(out), np.int64)


def split(tr: pd.DataFrame, split_day: int):
    if tr is None or len(tr) == 0:
        return tr, tr
    return tr[tr["day"] < split_day], tr[tr["day"] >= split_day]


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, pd.DataFrame):
        return jsonable(x.to_dict(orient="split"))
    return x


def run(b, out_dir: str, split_ts="2023-01-01", synthetic=False, quick=False, fee=0.0):
    t0 = time.time()
    os.makedirs(out_dir, exist_ok=True)
    split_day = day_num(split_ts)
    costs, fill = Costs(), Fill()
    ctx = st.Ctx(b, costs, fill)
    cands, med_atr = candidates(ctx, split_day)
    res = {"meta": {**{k: v for k, v in b.info.items() if k != "detected"},
                    "clock_detection": b.info.get("detected"),
                    "split": split_ts, "synthetic": synthetic,
                    "is_median_atr15": med_atr, **config_dict(costs, fill),
                    "generated": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")},
           "strategies": {}, "sensitivity": [], "books": []}

    # ---------------------------------------------------------------- strategies & variants
    trades = {}
    for sname, lst in cands.items():
        rows = []
        for label, params, is_cand in lst:
            tr = st.RUNNERS[sname](ctx, **params)
            tr = tr.assign(variant=label) if len(tr) else tr
            trades[(sname, label)] = tr
            tis, toos = split(tr, split_day)
            rows.append({"label": label, "candidate": is_cand, "params": params,
                         "IS": stats.trade_stats(tis), "OOS": stats.trade_stats(toos),
                         "ALL": stats.trade_stats(tr),
                         "yearly": stats.yearly(tr).to_dict()})
            print(f"[{sname}] {label:38s} trades {len(tr):5d}  IS n/DD "
                  f"{rows[-1]['IS'].get('net_over_dd', float('nan')):6.2f}  OOS n/DD "
                  f"{rows[-1]['OOS'].get('net_over_dd', float('nan')):6.2f}")
        # pre-registered selection: best IS net/DD among candidates with >= 100 IS trades
        pool = [r for r in rows if r["candidate"] and r["IS"].get("trades", 0) >= 100]
        sel = max(pool, key=lambda r: r["IS"]["net_over_dd"])["label"] if pool else "faithful"
        res["strategies"][sname] = {"variants": rows, "selected": sel}

    # fill / cost sensitivity on the faithful versions
    for label, c2, f2 in (("fills: bar-magnifier ordering", costs, Fill("ohlc")),
                          ("fills: limit fills on touch", costs, Fill(limit_through=False)),
                          ("costs: 2 ticks slippage", Costs(slip_ticks=2.0), fill)):
        ctx2 = st.Ctx(b, c2, f2)
        ctx2._cache = ctx._cache                      # same indicators
        for sname in ("S1", "S2", "S3"):
            tr = st.RUNNERS[sname](ctx2)
            tis, toos = split(tr, split_day)
            res["sensitivity"].append({"strategy": sname, "label": label,
                                       "IS": stats.trade_stats(tis), "OOS": stats.trade_stats(toos)})

    faithful = {s: trades[(s, "faithful")] for s in ("S1", "S2", "S3")}
    chosen = {s: trades[(s, res["strategies"][s]["selected"])] for s in ("S1", "S2", "S3")}

    # ---------------------------------------------------------------- correlation
    days = trading_days(ctx)
    d_is, d_oos = days[days < split_day], days[days >= split_day]
    res["correlation"] = {}
    for per, dd in (("IS", d_is), ("OOS", d_oos), ("ALL", days)):
        c = stats.correlations({k: v[v["day"].isin(dd)] if len(v) else v for k, v in faithful.items()}, dd)
        res["correlation"][per] = {"all_days": c["all_days"].round(3).to_dict(),
                                   "active": None if c["days_two_or_more_traded"] is None
                                   else c["days_two_or_more_traded"].round(3).to_dict(),
                                   "n_active": c["n_active"]}

    # ---------------------------------------------------------------- bench rule (walk-forward)
    gated = {}
    for tag, src in (("", faithful), ("*", chosen)):
        for s, tr in src.items():
            gated[s + tag + "b"] = tr[stats.bench_mask(tr)] if len(tr) else tr
    res["bench_rule"] = {k: {"kept": int(len(v)), "of": int(len(faithful[k[:2]]) if "*" not in k
                                                             else len(chosen[k[:2]]))}
                         for k, v in gated.items()}

    # ---------------------------------------------------------------- prop-firm books
    series = {**faithful, **{s + "*": tr for s, tr in chosen.items()}, **gated}
    paths = {"IS": prop.DayPaths(b, {k: v[v["day"].isin(d_is)] if len(v) else v for k, v in series.items()}, d_is, costs),
             "OOS": prop.DayPaths(b, {k: v[v["day"].isin(d_oos)] if len(v) else v for k, v in series.items()}, d_oos, costs)}
    apex = prop.PROFILES["apex50"]
    grid = (0, 2, 5, 8) if quick else (0, 1, 2, 3, 4, 5, 6, 8, 10)
    opt_f = prop.optimize_sizing(paths["IS"], apex, grid, ["S1", "S2", "S3"])
    opt_c = prop.optimize_sizing(paths["IS"], apex, grid, ["S1*", "S2*", "S3*"])
    mix_f = {k: int(opt_f.iloc[0][k]) for k in ("S1", "S2", "S3")}
    mix_c = {k: int(opt_c.iloc[0][k]) for k in ("S1*", "S2*", "S3*")}
    res["sizing"] = {"faithful": {"mix": mix_f, "top": opt_f.head(10).to_dict(orient="records")},
                     "improved": {"mix": mix_c, "top": opt_c.head(10).to_dict(orient="records")}}

    books = [
        ("S1 alone, 5 micros", {"S1": 5}),
        ("S2 alone, 5 micros", {"S2": 5}),
        ("S3 alone, 5 micros", {"S3": 5}),
        ("Matteo: all three, 5 micros each", {"S1": 5, "S2": 5, "S3": 5}),
        ("Matteo 5/5/5 + bench rule", {"S1b": 5, "S2b": 5, "S3b": 5}),
        ("Faithful, sizes chosen in-sample", mix_f),
        ("Improved, sizes chosen in-sample", mix_c),
        ("Improved + bench rule", {k[:2] + "*b": v for k, v in mix_c.items()}),
    ]
    sims = 1000 if quick else 4000
    for name, mix in books:
        for per in ("IS", "OOS"):
            for pk, pf in prop.PROFILES.items():
                close, dmin, traded = paths[per].combine(mix, pf.dll)
                res["books"].append({
                    "book": name, "mix": mix, "period": per, "profile": pf.name,
                    "rolling": prop.rolling(close, dmin, traded, pf),
                    "back_to_back": prop.back_to_back(close, dmin, traded, pf, fee),
                    "bootstrap": prop.bootstrap(close, dmin, traded, pf, sims=sims, horizon=250),
                    "day_net_over_dd": float(close.sum() / max(stats.max_drawdown(close), 1e-9)),
                    "net": float(close.sum()),
                })
        print(f"[book] {name}: OOS Apex pass "
              f"{next(x for x in res['books'] if x['book'] == name and x['period'] == 'OOS' and x['profile'] == apex.name)['rolling']['pass_rate']}")

    # ---------------------------------------------------------------- Matteo's claims
    res["claims"] = claims(res, faithful, split_day)

    # ---------------------------------------------------------------- curves for the report
    res["curves"] = {}
    for s in ("S1", "S2", "S3"):
        for lab, tr in (("faithful", faithful[s]), ("selected", chosen[s])):
            if len(tr):
                tt = tr.sort_values("exit_time")
                res["curves"][f"{s} {lab}"] = {
                    "t": [str(x)[:10] for x in tt["exit_time"]],
                    "eq": np.cumsum(tt["net_nq"].to_numpy()).round(1).tolist()}
    res["meta"]["runtime_s"] = round(time.time() - t0, 1)

    all_tr = pd.concat([t.assign(strategy=k[0]) for k, t in trades.items() if len(t)], ignore_index=True)
    all_tr.drop(columns=["entry_idx", "exit_idx"]).to_csv(os.path.join(out_dir, "trades_all.csv.gz"), index=False)
    with open(os.path.join(out_dir, "summary.json"), "w") as fh:
        json.dump(jsonable(res), fh, indent=1, default=str)
    html = report.render(jsonable(res))
    with open(os.path.join(out_dir, "report.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"[done] {out_dir}/report.html  ({res['meta']['runtime_s']} s)")
    return res


def claims(res, faithful, split_day) -> list:
    def var(s, lab="faithful"):
        return next(v for v in res["strategies"][s]["variants"] if v["label"] == lab)

    def book(name, profile, per="OOS"):
        return next(x for x in res["books"] if x["book"] == name and x["profile"] == profile and x["period"] == per)

    s3_22 = faithful["S3"][faithful["S3"]["day"] >= day_num("2022-01-01")]
    s3s = stats.trade_stats(s3_22)
    gen = prop.PROFILES["matteo21"].name
    corr = res["correlation"]["OOS"]["all_days"]
    pairs = [corr[a][b] for a, b in (("S1", "S2"), ("S1", "S3"), ("S2", "S3"))
             if corr.get(a, {}).get(b) is not None]
    out = [
        {"claim": "S1 average trade about $112 per NQ", "source": "[00:57:44]",
         "measured": var("S1")["OOS"].get("avg_trade"), "unit": "$ per NQ, 2023+"},
        {"claim": "S1 wins about 67% of trades", "source": "[00:57:44]",
         "measured": var("S1")["OOS"].get("win_rate"), "unit": "share, 2023+"},
        {"claim": "S3 profit factor about 1.4", "source": "[01:13:15]",
         "measured": s3s.get("profit_factor"), "unit": "2022+"},
        {"claim": "S3 wins about 53%", "source": "[01:13:15]",
         "measured": s3s.get("win_rate"), "unit": "share, 2022+"},
        {"claim": "S3 made about $200,000 per NQ 2022-2026", "source": "[01:13:15]",
         "measured": s3s.get("net"), "unit": "$ per NQ, 2022+"},
        {"claim": "Each strategy alone passes about 40%", "source": "[01:07:19]",
         "measured": [book(f"{s} alone, 5 micros", gen)["rolling"]["pass_rate"] for s in ("S1", "S2", "S3")],
         "unit": f"pass rate, {gen}, 2023+"},
        {"claim": "Daily correlation between strategies below 0.25", "source": "[01:11:00]",
         "measured": max(pairs) if pairs else None, "unit": "highest pair, 2023+"},
        {"claim": "Together at 5 micros each: pass in about 5 trading days", "source": "[01:19:15]",
         "measured": book("Matteo: all three, 5 micros each", gen)["rolling"]["median_days_to_pass"],
         "unit": "median trading days, 2023+"},
        {"claim": "Running all three passes more often than one alone", "source": "[01:18:38]",
         "measured": book("Matteo: all three, 5 micros each", gen)["rolling"]["pass_rate"],
         "unit": f"pass rate together, {gen}, 2023+"},
    ]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", help="folder or file with NQ 1-minute bars")
    ap.add_argument("--tz", help="clock the file was written in, e.g. America/New_York (default: detect)")
    ap.add_argument("--stamp", choices=["open", "close"], help="bar time is its open or close (default: detect)")
    ap.add_argument("--split", default="2023-01-01", help="first out-of-sample day")
    ap.add_argument("--start", help="ignore bars before this date")
    ap.add_argument("--out", help="output folder (default results/<data-name>)")
    ap.add_argument("--fee", type=float, default=0.0, help="challenge fee, for cost per pass")
    ap.add_argument("--synthetic", action="store_true", help="run on generated fake data")
    ap.add_argument("--quick", action="store_true", help="coarser sizing grid, fewer bootstrap runs")
    a = ap.parse_args(argv)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if a.synthetic:
        df = synth.make_bars("2019-01-01", "2024-06-28", seed=3)
        t = df["t"].values.astype("datetime64[m]")
        b = data.Bars(t, *(df[k].to_numpy(float) for k in "ohlcv"),
                      info={"files": ["synthetic"], "tz_source": "America/Chicago", "stamp": "open",
                            "bars": len(df), "first": str(t[0]), "last": str(t[-1])})
        out = a.out or os.path.join(here, "results", "synthetic")
        return run(b, out, a.split, synthetic=True, quick=a.quick, fee=a.fee)
    if not a.data:
        ap.error("--data is required (or --synthetic)")
    b = data.load_bars(a.data, tz=a.tz, stamp=a.stamp)
    if a.start:
        b = b.slice_dates(start=a.start)
    name = os.path.basename(os.path.normpath(a.data)).replace(" ", "_") or "run"
    out = a.out or os.path.join(here, "results", name)
    return run(b, out, a.split, quick=a.quick, fee=a.fee)


if __name__ == "__main__":
    main()
