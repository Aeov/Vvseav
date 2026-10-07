"""Trade statistics, correlation, Monte Carlo drawdown, and Matteo's bench rule."""
from __future__ import annotations

import numpy as np
import pandas as pd


def day_to_date(d) -> pd.Timestamp:
    return pd.Timestamp(int(d) * 86400, unit="s")


def max_drawdown(pnl: np.ndarray) -> float:
    if len(pnl) == 0:
        return 0.0
    eq = np.concatenate([[0.0], np.cumsum(pnl)])
    return float((np.maximum.accumulate(eq) - eq).max())


def trade_stats(tr: pd.DataFrame, col: str = "net_nq") -> dict:
    if tr is None or len(tr) == 0:
        return {"trades": 0}
    x = tr[col].to_numpy()
    wins, losses = x[x > 0], x[x <= 0]
    dd = max_drawdown(x)
    first, last = tr["entry_time"].min(), tr["exit_time"].max()
    years = max((pd.Timestamp(last) - pd.Timestamp(first)).days / 365.25, 1e-9)
    reasons = tr["reason"].value_counts(normalize=True)
    out = {
        "trades": int(len(x)),
        "net": float(x.sum()),
        "win_rate": float((x > 0).mean()),
        "avg_trade": float(x.mean()),
        "avg_win": float(wins.mean()) if len(wins) else 0.0,
        "avg_loss": float(losses.mean()) if len(losses) else 0.0,
        "profit_factor": float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"),
        "max_dd": dd,
        "net_over_dd": float(x.sum() / dd) if dd > 0 else float("inf"),
        "trades_per_year": float(len(x) / years),
        "pct_target": float(reasons.get("target", 0.0)),
        "pct_stop": float(reasons.get("stop", 0.0)),
        "pct_time": float(reasons.get("time", 0.0) + reasons.get("eod", 0.0)),
    }
    if (tr["side"] < 0).any():
        for name, m in (("long", tr["side"] > 0), ("short", tr["side"] < 0)):
            y = tr.loc[m, col].to_numpy()
            out[f"{name}_trades"] = int(len(y))
            out[f"{name}_win_rate"] = float((y > 0).mean()) if len(y) else None
            out[f"{name}_avg"] = float(y.mean()) if len(y) else None
    return out


def yearly(tr: pd.DataFrame, col: str = "net_nq") -> pd.Series:
    if tr is None or len(tr) == 0:
        return pd.Series(dtype=float)
    y = pd.to_datetime(tr["entry_time"]).dt.year
    return tr.groupby(y)[col].sum()


def daily_pnl(tr: pd.DataFrame, days, col: str = "net_nq") -> pd.Series:
    s = pd.Series(0.0, index=pd.Index(days, name="day"))
    if tr is not None and len(tr):
        g = tr.groupby("day")[col].sum()
        s.loc[s.index.intersection(g.index)] = g.loc[s.index.intersection(g.index)]
    return s


def correlations(trades: dict[str, pd.DataFrame], days) -> dict:
    df = pd.DataFrame({k: daily_pnl(v, days) for k, v in trades.items()})
    all_days = df.corr()
    active = df[(df != 0).sum(axis=1) >= 2]
    both = active.corr() if len(active) > 10 else None
    return {"all_days": all_days, "days_two_or_more_traded": both, "n_active": int(len(active))}


def mc_drawdowns(pnl: np.ndarray, sims: int = 2000, length: int | None = None,
                 seed: int = 11) -> np.ndarray:
    """Max drawdown of `sims` resampled (with replacement) trade sequences."""
    rng = np.random.default_rng(seed)
    n = len(pnl)
    length = length or n
    if n == 0:
        return np.zeros(1)
    idx = rng.integers(0, n, size=(sims, length))
    eq = np.cumsum(pnl[idx], axis=1)
    eq = np.concatenate([np.zeros((sims, 1)), eq], axis=1)
    return (np.maximum.accumulate(eq, axis=1) - eq).max(axis=1)


def bench_mask(tr: pd.DataFrame, pct: float = 75.0, min_trades: int = 30,
               col: str = "net_nq", sims: int = 1000) -> np.ndarray:
    """Matteo's rule, walk-forward: bench a strategy when its live drawdown exceeds the
    `pct` percentile of Monte-Carlo max drawdowns of its own past trades; bring it back
    when its (paper) equity makes a new high. Returns True for trades that would be taken.

    The Monte Carlo threshold is re-estimated at each month start from trades closed
    before that month only, so no future information is used.
    """
    if tr is None or len(tr) == 0:
        return np.zeros(0, bool)
    srt = tr.sort_values("entry_time", kind="stable")
    x = srt[col].to_numpy()
    months = pd.to_datetime(srt["entry_time"]).dt.to_period("M").to_numpy()
    take = np.ones(len(x), bool)
    eq = peak = peak_at_bench = 0.0
    benched = False
    thr = np.inf
    cur_month = None
    for k in range(len(x)):
        if months[k] != cur_month:
            cur_month = months[k]
            past = x[:k]
            thr = (np.percentile(mc_drawdowns(past, sims, seed=k), pct)
                   if len(past) >= min_trades else np.inf)
        if benched and eq > peak_at_bench:
            benched = False
        if not benched and (peak - eq) > thr:
            benched = True
            peak_at_bench = peak
        take[k] = not benched
        eq += x[k]
        peak = max(peak, eq)
    return pd.Series(take, index=srt.index).reindex(tr.index).to_numpy()
