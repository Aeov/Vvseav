"""Synthetic NQ-like 1-minute bars, ONLY for testing the plumbing. Not market data.

Globex week Sunday 17:00 -> Friday 16:00 CT with the daily 16:00-17:00 halt, a volume
jump at the 08:30 CT open, U-shaped regular-session volume, intraday volatility profile,
and a mild upward drift. Optionally written as a MultiCharts-style file in another
clock (e.g. Eastern, close-stamped) to exercise the loader's detection.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def make_bars(start="2019-01-01", end="2021-12-31", seed=1, price0=7000.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    days = pd.bdate_range(start, end)
    rows = []
    px = price0
    for d in days:
        # session = previous calendar day 17:00 -> this day 16:00 (CT)
        t0 = pd.Timestamp(d) - pd.Timedelta(hours=7)
        mins = pd.date_range(t0, periods=23 * 60, freq="min")
        mod = mins.hour * 60 + mins.minute
        rth = (mod >= 510) & (mod < 900)
        vol_sigma = np.where(rth, 0.00045, 0.00018)
        vol_sigma = np.where((mod >= 510) & (mod < 540), 0.0008, vol_sigma)
        drift = 0.0000012
        r = rng.standard_normal(len(mins)) * vol_sigma + drift
        # occasional trending days
        if rng.random() < 0.25:
            r = r + np.where(rth, rng.choice([-1, 1]) * 0.00006, 0)
        closes = px * np.exp(np.cumsum(r))
        opens = np.concatenate([[px], closes[:-1]])
        wig = np.abs(rng.standard_normal(len(mins))) * vol_sigma * px * 0.6
        highs = np.maximum(opens, closes) + wig
        lows = np.minimum(opens, closes) - np.abs(rng.standard_normal(len(mins))) * vol_sigma * px * 0.6
        base = np.where(rth, 900, 120)
        base = np.where(mod == 510, 9000, base)
        base = np.where((mod > 510) & (mod < 540), 2500, base)
        base = np.where((mod >= 840) & (mod < 900), 1800, base)
        vol = rng.poisson(base)
        q = 0.25
        o = np.round(opens / q) * q
        c = np.round(closes / q) * q
        h = np.maximum(np.round(highs / q) * q, np.maximum(o, c))
        l = np.minimum(np.round(lows / q) * q, np.minimum(o, c))
        rows.append(pd.DataFrame({"t": mins, "o": o, "h": h, "l": l, "c": c, "v": vol}))
        px = closes[-1]
    df = pd.concat(rows, ignore_index=True)
    return df


def write_multicharts(df: pd.DataFrame, path: str, tz: str = "America/New_York",
                      stamp: str = "close", date_fmt: str = "%m/%d/%Y"):
    """Write bars (CT, open-stamped) the way a MultiCharts export would look."""
    t = df["t"]
    if stamp == "close":
        t = t + pd.Timedelta(minutes=1)
    if tz != "America/Chicago":
        t = t.dt.tz_localize("America/Chicago", ambiguous="NaT", nonexistent="NaT") \
             .dt.tz_convert(tz).dt.tz_localize(None)
    out = pd.DataFrame({"Date": t.dt.strftime(date_fmt), "Time": t.dt.strftime("%H:%M"),
                        "Open": df["o"], "High": df["h"], "Low": df["l"], "Close": df["c"],
                        "Up": df["v"] // 2, "Down": df["v"] - df["v"] // 2})
    out = out.dropna()
    out.to_csv(path, index=False)
