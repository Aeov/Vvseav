"""Prop-firm evaluation simulator.

Each strategy's trades are turned into a minute-by-minute path per trading day
(08:30-16:00 CT): realized P&L plus the WORST open P&L inside each minute (bar low for
longs, bar high for shorts). Paths are per one micro (MNQ) and scale linearly, so any
sizing mix is a weighted sum.

A challenge walks those days:
  * daily loss limit (soft): the moment the day's worst equity reaches -DLL the account
    is flattened for the rest of the day (Apex/Lucid behaviour)
  * trailing drawdown (end-of-day): threshold = highest end-of-day balance - DD; touching
    it intraday (worst open equity) fails the account
  * pass is judged at the end of a day: profit >= target, best day <= consistency x total
    profit, and enough qualifying trading days
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

from .engine import MNQ_PV

W0, W1 = 510, 960           # path window 08:30 -> 16:00 CT
W = W1 - W0


@dataclass(frozen=True)
class Profile:
    name: str
    target: float = 3000.0
    trail_dd: float = 2000.0
    dll: float | None = 1000.0
    consistency: float | None = None     # best day <= this share of total profit
    min_days: int = 0                    # qualifying trading days required
    min_day_profit: float = 0.0          # a day qualifies if it traded and made >= this
    max_days: int | None = None          # trading days allowed (None = no limit)
    max_micros: int = 60


PROFILES = {
    # Your 13 Aug 2026 sheet ("Prop Firm Screen + Revival Plan"); verify against your account.
    "apex50": Profile("Apex 50K EOD", dll=1000.0, consistency=0.50, min_days=5,
                      min_day_profit=250.0, max_micros=60),
    "lucid50": Profile("LucidPro 50K", dll=1200.0, max_micros=40),
    # The interview's framing: hit +$3,000 before the drawdown, within 21 trading days.
    "matteo21": Profile("Generic 50K, 21 days", dll=1000.0, max_days=21, max_micros=60),
}


# ----------------------------------------------------------------------------- day paths
class DayPaths:
    """Per-strategy [day, minute] arrays of realized and worst-open P&L for one micro."""

    def __init__(self, b, trades: dict[str, pd.DataFrame], days: np.ndarray, costs):
        self.days = np.asarray(days)
        self.day_pos = {int(d): k for k, d in enumerate(self.days)}
        self.names = list(trades)
        nd = len(self.days)
        self.real = {}
        self.worst = {}
        self.traded = {}
        for name, tr in trades.items():
            real = np.zeros((nd, W), np.float32)
            unreal = np.zeros((nd, W), np.float32)
            traded = np.zeros(nd, bool)
            if tr is not None and len(tr):
                for r in tr.itertuples(index=False):
                    k = self.day_pos.get(int(r.day))
                    if k is None:
                        continue
                    traded[k] = True
                    i0, i1, side = int(r.entry_idx), int(r.exit_idx), int(r.side)
                    m0 = int(b.mod[i0]) - W0
                    m1 = int(b.mod[i1]) - W0
                    if m0 < 0 or m0 >= W:
                        continue
                    m1 = min(max(m1, m0), W - 1)
                    entry_cost = costs.entry_cost(MNQ_PV, costs.commission_mnq_side)
                    if i1 > i0:
                        idx = np.arange(i0, i1)
                        worst_px = b.l[idx] if side > 0 else b.h[idx]
                        val = side * (worst_px - r.entry) * MNQ_PV - entry_cost
                        mm = b.mod[idx] - W0
                        ok = (mm >= 0) & (mm < W)
                        seg = np.full(m1 - m0 + 1, np.nan)
                        seg[mm[ok] - m0] = val[ok]
                        seg = pd.Series(seg).ffill().fillna(-entry_cost).to_numpy()
                    else:
                        seg = np.full(m1 - m0 + 1, -entry_cost)
                    # exit minute: realized, plus any dip inside that bar below the exit price
                    worst_exit_bar = b.l[i1] if side > 0 else b.h[i1]
                    seg[-1] = min(0.0, side * (worst_exit_bar - r.exit) * MNQ_PV)
                    unreal[k, m0:m1 + 1] += seg.astype(np.float32)
                    real[k, m1:] += np.float32(r.net_mnq)
            self.real[name] = real
            self.worst[name] = real + unreal
            self.traded[name] = traded

    def combine(self, micros: dict[str, int], dll: float | None):
        """Day summaries for a sizing mix: (day_close, day_min, traded)."""
        nd = len(self.days)
        worst = np.zeros((nd, W), np.float64)
        real = np.zeros((nd, W), np.float64)
        traded = np.zeros(nd, bool)
        for name, n in micros.items():
            if n:
                worst += n * self.worst[name]
                real += n * self.real[name]
                traded |= self.traded[name]
        close = real[:, -1].copy()
        dmin = np.minimum(worst.min(axis=1), 0.0)
        if dll is not None:
            hit = worst <= -dll
            any_hit = hit.any(axis=1)
            close[any_hit] = -dll
            dmin[any_hit] = -dll
        return close, dmin, traded


# ----------------------------------------------------------------------------- challenge
def run_challenge(close, dmin, traded, start: int, prof: Profile):
    """Walk one challenge from day index `start`. Returns (outcome, trading days used)."""
    bal = 0.0
    peak = 0.0
    best_day = 0.0
    qual = 0
    n = len(close)
    for k in range(start, n):
        used = k - start + 1
        thr = peak - prof.trail_dd
        if bal + dmin[k] <= thr:
            return "fail", used
        bal += close[k]
        peak = max(peak, bal)
        best_day = max(best_day, close[k])
        if traded[k] and close[k] >= prof.min_day_profit:
            qual += 1
        if (bal >= prof.target and qual >= prof.min_days and
                (prof.consistency is None or best_day <= prof.consistency * bal)):
            return "pass", used
        if prof.max_days is not None and used >= prof.max_days:
            return "expired", used
    return "open", n - start


def rolling(close, dmin, traded, prof: Profile, starts=None) -> dict:
    """A challenge started on every trading day; overlapping, so not independent."""
    starts = range(len(close)) if starts is None else starts
    res = [run_challenge(close, dmin, traded, s, prof) for s in starts]
    return summarize(res)


def back_to_back(close, dmin, traded, prof: Profile, fee: float = 0.0) -> dict:
    """Buy a challenge, run it to the end, buy the next one the following day."""
    res = []
    k = 0
    while k < len(close):
        out, used = run_challenge(close, dmin, traded, k, prof)
        res.append((out, used))
        k += used
    s = summarize(res)
    s["attempts"] = sum(1 for o, _ in res if o != "open")
    s["fees_per_pass"] = (fee * s["attempts"] / s["passes"]) if s["passes"] else None
    return s


def bootstrap(close, dmin, traded, prof: Profile, sims: int = 4000, block: float = 5.0,
              horizon: int = 80, seed: int = 7) -> dict:
    """Stationary block bootstrap of trading days -> independent synthetic challenges."""
    rng = np.random.default_rng(seed)
    n = len(close)
    res = []
    for _ in range(sims):
        idx = np.empty(horizon, int)
        k = rng.integers(n)
        for t in range(horizon):
            idx[t] = k
            k = rng.integers(n) if rng.random() < 1.0 / block else (k + 1) % n
        out, used = run_challenge(close[idx], dmin[idx], traded[idx], 0, prof)
        res.append((out, used))
    return summarize(res)


def summarize(res) -> dict:
    outs = [o for o, _ in res]
    done = [r for r in res if r[0] != "open"]
    passes = [u for o, u in res if o == "pass"]
    n_done = len(done)
    return {
        "starts": len(res), "resolved": n_done,
        "passes": len(passes),
        "pass_rate": (len(passes) / n_done) if n_done else None,
        "fail_rate": (outs.count("fail") / n_done) if n_done else None,
        "expired_rate": (outs.count("expired") / n_done) if n_done else None,
        "median_days_to_pass": float(np.median(passes)) if passes else None,
        "mean_days_to_pass": float(np.mean(passes)) if passes else None,
    }


def optimize_sizing(paths: DayPaths, prof: Profile, grid=(0, 1, 2, 3, 4, 5, 6, 8, 10),
                    names=None, min_total: int = 1) -> pd.DataFrame:
    """Every sizing mix on the grid, scored by rolling-start pass rate."""
    names = names or paths.names
    rows = []
    import itertools
    for combo in itertools.product(grid, repeat=len(names)):
        if sum(combo) < min_total or sum(combo) > prof.max_micros:
            continue
        mix = dict(zip(names, combo))
        close, dmin, traded = paths.combine(mix, prof.dll)
        r = rolling(close, dmin, traded, prof)
        rows.append({**mix, **r})
    return pd.DataFrame(rows).sort_values(["pass_rate", "median_days_to_pass"],
                                          ascending=[False, True]).reset_index(drop=True)


def profile_dict(p: Profile) -> dict:
    return asdict(p)
