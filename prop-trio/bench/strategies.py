"""Matteo's three prop-firm strategies on NQ, faithful defaults plus pre-registered variants.

Every time below is US Central (CME exchange time). Minute-of-day constants:
  510 = 08:30, 525 = 08:45, 540 = 09:00, 600 = 10:00, 870 = 14:30, 900 = 15:00, 955 = 15:55.
See ../SPEC.md for the transcript source of each rule and for each ambiguity.
"""
from __future__ import annotations

from functools import cached_property

import numpy as np
import pandas as pd

from .data import Bars
from .engine import Costs, Fill, make_trade, resolve_exit
from . import indicators as ind


class Ctx:
    """Per-dataset cache of indicators and day boundaries."""

    def __init__(self, b: Bars, costs: Costs | None = None, fill: Fill | None = None):
        self.b = b
        self.costs = costs or Costs()
        self.fill = fill or Fill()
        starts = np.flatnonzero(np.concatenate([[True], b.day[1:] != b.day[:-1]]))
        ends = np.concatenate([starts[1:], [b.n]]) - 1
        self.day_ranges = {int(b.day[s]): (int(s), int(e)) for s, e in zip(starts, ends)}
        self._cache = {}

    # --- cached indicators
    def vwap(self, anchor: int) -> np.ndarray:
        k = ("vwap", anchor)
        if k not in self._cache:
            self._cache[k] = ind.vwap(self.b, anchor)
        return self._cache[k]

    def atr_sess(self, n: int = 15, smooth: str = "sma") -> pd.Series:
        k = ("atr", n, smooth)
        if k not in self._cache:
            self._cache[k] = ind.session_atr(self.b, n, smooth)
        return self._cache[k]

    def atr_at(self, i: int, n: int = 15, smooth: str = "sma") -> float:
        v = self.atr_sess(n, smooth).get(int(self.b.sess[i]), np.nan)
        return float(v)

    def buckets(self, minutes: int) -> pd.DataFrame:
        k = ("bk", minutes)
        if k not in self._cache:
            self._cache[k] = ind.buckets(self.b, minutes)
        return self._cache[k]

    def bucket_adx(self, minutes: int, n: int = 14) -> np.ndarray:
        k = ("bkadx", minutes, n)
        if k not in self._cache:
            bk = self.buckets(minutes)
            self._cache[k] = ind.wilder_adx(bk["h"].to_numpy(), bk["l"].to_numpy(), bk["c"].to_numpy(), n)
        return self._cache[k]

    @cached_property
    def adx1(self) -> np.ndarray:
        return ind.wilder_adx(self.b.h, self.b.l, self.b.c, 14)

    def rolling_hl(self, n_hi: int, n_lo: int):
        k = ("hl", n_hi, n_lo)
        if k not in self._cache:
            hh = pd.Series(self.b.h).rolling(n_hi, min_periods=n_hi).max().to_numpy()
            ll = pd.Series(self.b.l).rolling(n_lo, min_periods=n_lo).min().to_numpy()
            self._cache[k] = (hh, ll)
        return self._cache[k]

    # --- helpers
    def first_at(self, day: int, minute: int) -> int:
        """Index of the first bar of `day` whose open minute >= minute, or -1."""
        s, e = self.day_ranges[day]
        k = int(np.searchsorted(self.b.mod[s:e + 1], minute, side="left"))
        return s + k if s + k <= e else -1

    def exit_bounds(self, day: int, time_exit_min: int):
        """(time_exit_idx or -1, last bar index to scan for stop/target)."""
        s, e = self.day_ranges[day]
        tx = self.first_at(day, time_exit_min)
        # last bar of the regular day before the 16:00 halt
        k = int(np.searchsorted(self.b.mod[s:e + 1], 960, side="left"))
        last_reg = s + k - 1
        if tx >= 0 and tx <= last_reg:
            return tx, tx - 1
        return -1, last_reg


def _entry_ok(ctx: Ctx, j: int, day: int, latest_open_min: int) -> bool:
    b = ctx.b
    i0 = j + 1
    if i0 >= b.n or b.day[i0] != day or b.mod[i0] >= latest_open_min:
        return False
    return (b.t[i0] - b.t[j]).astype(int) <= 5     # no halt between signal and fill


# ============================================================================ S1
S1_DEFAULTS = dict(
    noise_pct=0.30, atr_len=15, atr_smooth="sma",
    tp_pts=40.0, sl_pts=75.0,          # $800 / $1,500 on one NQ contract
    start=600, end=870,                # signal bars closing 10:00 .. before 14:30
    time_exit=870, max_trades=3, tf=30,
    exits="fixed",                     # "fixed" | "atr" (vol-scaled, variant S1-v1)
    tp_atr=None, sl_atr=None,          # ATR multiples for exits="atr"
    noise="atr",                       # "atr" | "tod" (time-of-day band, variant S1-v2)
    tod_lookback=14,
)


def _s1_tod_sigma(ctx: Ctx, p: dict) -> pd.DataFrame:
    """Mean |close/midnight - 1| at each signal minute over the previous N days."""
    b = ctx.b
    bk = ctx.buckets(p["tf"])
    sel = bk[bk["boundary"] & (bk["close_mod"] >= p["start"]) & (bk["close_mod"] < p["end"])]
    refs = {d: b.o[s] for d, (s, e) in ctx.day_ranges.items()}
    move = np.abs(sel["c"].to_numpy() / sel["day"].map(refs).to_numpy() - 1.0)
    piv = pd.DataFrame({"day": sel["day"].to_numpy(), "m": sel["close_mod"].to_numpy(), "x": move}) \
        .pivot_table(index="day", columns="m", values="x")
    return piv.rolling(p["tod_lookback"], min_periods=p["tod_lookback"]).mean().shift(1)


def s1_vault_break(ctx: Ctx, **kw) -> pd.DataFrame:
    p = {**S1_DEFAULTS, **kw}
    b = ctx.b
    vw = ctx.vwap(0)
    bk = ctx.buckets(p["tf"])
    sig = bk[bk["boundary"] & (bk["close_mod"] >= p["start"]) & (bk["close_mod"] < p["end"])]
    sig_by_day = {d: g for d, g in sig.groupby("day")}
    sigma = _s1_tod_sigma(ctx, p) if p["noise"] == "tod" else None
    trades = []
    for day, g in sig_by_day.items():
        s, e = ctx.day_ranges[day]
        ref = b.o[s]
        atr = ctx.atr_at(s, p["atr_len"], p["atr_smooth"])
        if not np.isfinite(atr):
            continue
        tx, last = ctx.exit_bounds(day, p["time_exit"])
        n_tr, free_from = 0, s
        for j, cm, close in zip(g["last"].to_numpy(), g["close_mod"].to_numpy(), g["c"].to_numpy()):
            if n_tr >= p["max_trades"]:
                break
            if j < free_from:
                continue
            if p["noise"] == "tod":
                if sigma is None or day not in sigma.index or cm not in sigma.columns:
                    continue
                sg = sigma.at[day, cm]
                if not np.isfinite(sg):
                    continue
                barrier = ref * (1 + sg)
            else:
                barrier = ref + p["noise_pct"] * atr
            if not (close > barrier and close > vw[j]):
                continue
            if not _entry_ok(ctx, j, day, p["end"]):
                continue
            i0 = j + 1
            entry = b.o[i0]
            if p["exits"] == "atr":
                tp_d, sl_d = p["tp_atr"] * atr, p["sl_atr"] * atr
            else:
                tp_d, sl_d = p["tp_pts"], p["sl_pts"]
            sl, tp = entry - sl_d, entry + tp_d
            xi, xp, why = resolve_exit(b, i0, last, tx, 1, sl, tp, ctx.fill)
            trades.append(make_trade(b, "S1", 1, i0, xi, xp, why, ctx.costs, sl, tp))
            n_tr += 1
            free_from = xi
    return pd.DataFrame(trades)


# ============================================================================ S2
S2_DEFAULTS = dict(
    or_start=510, or_end=540,          # opening range 08:30-09:00 CT (not 08:45)
    vwap_anchor=0,                     # 0 = midnight CT; 510 = regular session (variant S2-v1)
    adx_min=20.0,
    tp_lookback=5, sl_lookback=20,
    exit_mode="static",                # "static" levels from the signal bar | "dynamic" (S2-v2)
    time_exit=955,                     # 15:55 CT
    entry_cutoff=900,                  # no signal bars closing after 15:00 CT (assumption)
    max_trades=1,                      # not stated in the interview (assumption; S2-v3 = 3)
)


def s2_vwap_adx_pullback(ctx: Ctx, **kw) -> pd.DataFrame:
    p = {**S2_DEFAULTS, **kw}
    b = ctx.b
    vw = ctx.vwap(p["vwap_anchor"])
    adx = ctx.adx1
    hh, ll = ctx.rolling_hl(p["tp_lookback"], p["sl_lookback"])
    trades = []
    for day, (s, e) in ctx.day_ranges.items():
        i_or = ctx.first_at(day, p["or_start"])
        i_go = ctx.first_at(day, p["or_end"])
        if i_or < 0 or i_go < 0 or i_go - i_or < 10:
            continue
        orh = b.h[i_or:i_go].max()
        tx, last = ctx.exit_bounds(day, p["time_exit"])
        armed = touched = False
        n_tr = 0
        j = i_go
        end_j = min(last, e)
        while j <= end_j:
            close_min = b.mod[j] + 1
            if close_min > p["entry_cutoff"]:
                break
            if not armed and b.c[j] > orh:
                armed = True
            if armed:
                if b.l[j] <= vw[j]:
                    touched = True
                if (touched and b.c[j] > vw[j] and adx[j] > p["adx_min"] and adx[j] <= adx[j - 1]
                        and np.isfinite(hh[j]) and np.isfinite(ll[j])
                        and _entry_ok(ctx, j, day, p["time_exit"])):
                    i0 = j + 1
                    tp0, sl0 = hh[j], ll[j]
                    if p["exit_mode"] == "dynamic":
                        m = last - i0 + 1
                        tp_arr = np.empty(m)
                        sl_arr = np.empty(m)
                        tp_arr[0], sl_arr[0] = tp0, sl0
                        if m > 1:
                            tp_arr[1:] = hh[i0:last]
                            sl_arr[1:] = ll[i0:last]
                        xi, xp, why = resolve_exit(b, i0, last, tx, 1, sl_arr, tp_arr, ctx.fill)
                    else:
                        xi, xp, why = resolve_exit(b, i0, last, tx, 1, sl0, tp0, ctx.fill)
                    trades.append(make_trade(b, "S2", 1, i0, xi, xp, why, ctx.costs, sl0, tp0))
                    n_tr += 1
                    touched = False
                    if n_tr >= p["max_trades"] or why in ("time", "eod"):
                        break
                    j = xi          # flat again at the close of the exit bar
                    continue
            j += 1
    return pd.DataFrame(trades)


# ============================================================================ S3
S3_DEFAULTS = dict(
    on_start=0,                        # overnight range from 00:00 CT (as coded on his chart);
                                       # 1380 = 23:00 prior day (whiteboard), 1020 = 17:00 (S3-v1)
    or_minutes=15,                     # opening range = first 15-min bar 08:30-08:45
    entry_start=540,                   # first signal bar closes 09:00 CT
    entry_end=870,                     # last signal bar closes before 14:30
    time_exit=870,
    adx_min=20.0, tf=15,
    stop_atr=0.30, atr_len=15, atr_smooth="sma",
    tp_r=3.0,                          # target = 3 x stop distance (S3-v2: 1.5)
)


def s3_overnight_bias_orb(ctx: Ctx, **kw) -> pd.DataFrame:
    p = {**S3_DEFAULTS, **kw}
    b = ctx.b
    bk = ctx.buckets(p["tf"])
    adx = ctx.bucket_adx(p["tf"])
    bk = bk.assign(adx=adx)
    sig = bk[bk["boundary"] & (bk["close_mod"] >= p["entry_start"]) & (bk["close_mod"] < p["entry_end"])]
    sig_by_day = {d: g for d, g in sig.groupby("day")}
    mins_abs = b.t.astype("int64")
    trades = []
    for day, g in sig_by_day.items():
        s, e = ctx.day_ranges[day]
        i830 = ctx.first_at(day, 510)
        if i830 < 0 or b.mod[i830] > 515:
            continue
        if p["on_start"] == 0:
            a0 = s
        else:
            a0 = int(np.searchsorted(mins_abs, (day - 1) * 1440 + p["on_start"], side="left"))
        if a0 >= i830:
            continue
        onh, onl = b.h[a0:i830].max(), b.l[a0:i830].min()
        if onh <= onl:
            continue
        pos = (b.o[i830] - onl) / (onh - onl)
        bias = 1 if pos >= 2 / 3 else (-1 if pos <= 1 / 3 else 0)
        if bias == 0:
            continue
        i_or_end = ctx.first_at(day, 510 + p["or_minutes"])
        if i_or_end <= i830:
            continue
        orh, orl = b.h[i830:i_or_end].max(), b.l[i830:i_or_end].min()
        atr = ctx.atr_at(i830, p["atr_len"], p["atr_smooth"])
        if not np.isfinite(atr):
            continue
        tx, last = ctx.exit_bounds(day, p["time_exit"])
        for j, close, a in zip(g["last"].to_numpy(), g["c"].to_numpy(), g["adx"].to_numpy()):
            if not (a > p["adx_min"]):
                continue
            if not ((bias == 1 and close > orh) or (bias == -1 and close < orl)):
                continue
            if not _entry_ok(ctx, j, day, p["entry_end"]):
                continue
            i0 = j + 1
            entry = b.o[i0]
            sd = p["stop_atr"] * atr
            sl, tp = entry - bias * sd, entry + bias * p["tp_r"] * sd
            xi, xp, why = resolve_exit(b, i0, last, tx, bias, sl, tp, ctx.fill)
            trades.append(make_trade(b, "S3", bias, i0, xi, xp, why, ctx.costs, sl, tp))
            break                       # one trade per day
    return pd.DataFrame(trades)


RUNNERS = {"S1": s1_vault_break, "S2": s2_vwap_adx_pullback, "S3": s3_overnight_bias_orb}
