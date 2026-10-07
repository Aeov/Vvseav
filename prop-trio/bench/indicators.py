"""Indicators, each computed exactly as the PowerLanguage signals in ../multicharts compute them.

* VWAP: typical price (H+L+C)/3 weighted by volume, reset at an anchor minute each day.
* ADX: Wilder. Smoothed TR, +DM, -DM and ADX all use x += (new - x) / n, seeded with the
  first value (identical to pandas ewm(alpha=1/n, adjust=False)).
* Session ATR: simple average of the last N completed Globex sessions' true range
  (17:00-16:00 CT), i.e. MultiCharts AvgTrueRange(N) on daily bars, known at the start
  of the session it is used in.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import Bars


def vwap(b: Bars, anchor_min: int = 0) -> np.ndarray:
    """VWAP reset at `anchor_min` (minutes after midnight CT) each calendar day.

    Bars before the anchor get NaN (for anchor 0 every bar has a value).
    """
    tp = (b.h + b.l + b.c) / 3.0
    vol = np.where(b.v > 0, b.v, 0.0)
    active = b.mod >= anchor_min
    key = np.where(active, b.day, -1)
    df = pd.DataFrame({"k": key, "pv": np.where(active, tp * vol, 0.0), "v": np.where(active, vol, 0.0)})
    cpv = df.groupby("k")["pv"].cumsum().to_numpy()
    cv = df.groupby("k")["v"].cumsum().to_numpy()
    # No volume yet today: fall back to the bar close (as the PowerLanguage code does).
    out = np.where(cv > 0, cpv / np.where(cv > 0, cv, 1.0), b.c)
    out[~active] = np.nan
    return out


def wilder_adx(h: np.ndarray, l: np.ndarray, c: np.ndarray, n: int = 14) -> np.ndarray:
    """Wilder ADX on a bar series (first bar has no previous close -> NaN)."""
    m = len(c)
    out = np.full(m, np.nan)
    if m < 2:
        return out
    pc, ph, pl = c[:-1], h[:-1], l[:-1]
    hh, ll = h[1:], l[1:]
    tr = np.maximum(hh, pc) - np.minimum(ll, pc)
    up = hh - ph
    dn = pl - ll
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    a = 1.0 / n
    s_tr = pd.Series(tr).ewm(alpha=a, adjust=False).mean().to_numpy()
    s_p = pd.Series(pdm).ewm(alpha=a, adjust=False).mean().to_numpy()
    s_m = pd.Series(mdm).ewm(alpha=a, adjust=False).mean().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        pdi = np.where(s_tr > 0, 100 * s_p / s_tr, 0.0)
        mdi = np.where(s_tr > 0, 100 * s_m / s_tr, 0.0)
        dx = np.where(pdi + mdi > 0, 100 * np.abs(pdi - mdi) / (pdi + mdi), 0.0)
    adx = pd.Series(dx).ewm(alpha=a, adjust=False).mean().to_numpy()
    out[1:] = adx
    return out


def session_table(b: Bars) -> pd.DataFrame:
    """One row per Globex session (17:00 prior day -> 16:00 CT), indexed by session day number."""
    df = pd.DataFrame({"s": b.sess, "h": b.h, "l": b.l, "c": b.c})
    g = df.groupby("s")
    t = pd.DataFrame({"h": g["h"].max(), "l": g["l"].min(), "c": g["c"].last()})
    pc = t["c"].shift(1)
    t["tr"] = np.where(pc.notna(), np.maximum(t["h"], pc) - np.minimum(t["l"], pc), t["h"] - t["l"])
    return t


def session_atr(b: Bars, n: int = 15, smooth: str = "sma") -> pd.Series:
    """ATR known at the START of each session (uses only completed sessions).

    smooth="sma":     mean of the last n session true ranges (MultiCharts AvgTrueRange(n)).
    smooth="sma_of_atr14": mean over n sessions of a 14-session SMA ATR (the "moving average
                       of the ATR" reading of the interview) - kept as a sensitivity check.
    """
    t = session_table(b)
    if smooth == "sma":
        atr = t["tr"].rolling(n, min_periods=n).mean()
    elif smooth == "sma_of_atr14":
        atr = t["tr"].rolling(14, min_periods=14).mean().rolling(n, min_periods=n).mean()
    else:
        raise ValueError(smooth)
    return atr.shift(1)   # value usable during session s


def buckets(b: Bars, minutes: int) -> pd.DataFrame:
    """Aggregate 1-minute bars into clock-aligned buckets of `minutes` (by bar open time).

    Columns: first, last (1-min indices), h, l, c, close_mod (minute the bucket's last bar
    closes), boundary (True when that last bar closes exactly on the bucket boundary,
    the only moment the PowerLanguage code evaluates a signal), day.
    """
    key = b.t.astype("int64") // minutes
    starts = np.flatnonzero(np.concatenate([[True], key[1:] != key[:-1]]))
    ends = np.concatenate([starts[1:], [b.n]]) - 1
    h = np.maximum.reduceat(b.h, starts)
    l = np.minimum.reduceat(b.l, starts)
    c = b.c[ends]
    close_mod = (b.mod[ends] + 1) % 1440
    boundary = (close_mod % minutes) == 0
    return pd.DataFrame({"first": starts, "last": ends, "h": h, "l": l, "c": c,
                         "close_mod": close_mod, "boundary": boundary, "day": b.day[ends],
                         "key": key[starts]})
