"""Order execution on 1-minute bars.

Entries are market orders filled at the OPEN of the bar after the signal bar.
Exits are a protective stop, a limit target and a time exit (market at the open of
the first bar at/after the exit time). Fills are resolved on 1-minute OHLC:

* price gaps through a level at a bar's open -> filled at that open
* a bar that touches both stop and target -> `policy`:
    "stop_first" (default, conservative) or "ohlc" (MultiCharts' bar-magnifier
    assumption: the extreme nearer the open is visited first)
* a limit target fills only if price trades THROUGH it by one tick (`limit_through`),
  matching MultiCharts' "fill limit orders when price trades through" setting
* no time-exit bar that day (early close) -> out at the close of the day's last bar
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

TICK = 0.25
NQ_PV = 20.0     # $ per NQ point
MNQ_PV = 2.0     # $ per MNQ point


@dataclass
class Costs:
    commission_nq_side: float = 2.09     # $ per NQ contract per side (your MultiCharts setting)
    commission_mnq_side: float = 0.62    # $ per MNQ contract per side
    slip_ticks: float = 1.0              # per side, market and stop fills only

    def trade_cost(self, pv: float, comm_side: float, exit_reason: str) -> float:
        slip_sides = 1 + (0 if exit_reason == "target" else 1)   # entry is always market
        return 2 * comm_side + slip_sides * self.slip_ticks * TICK * pv

    def entry_cost(self, pv: float, comm_side: float) -> float:
        return comm_side + self.slip_ticks * TICK * pv


@dataclass
class Fill:
    policy: str = "stop_first"
    limit_through: bool = True


def resolve_exit(b, i0: int, i_last: int, time_exit_idx: int, side: int,
                 sl, tp, fill: Fill):
    """Scan bars i0..i_last for the first exit. sl/tp are scalars or per-bar arrays.

    Returns (exit_idx, exit_price, reason) with reason in stop/target/time/eod.
    """
    sl_ = np.asarray(sl, float)
    tp_ = np.asarray(tp, float)
    if i_last >= i0:
        sl_k = sl_ if sl_.ndim == 0 else sl_[: i_last - i0 + 1]
        tp_k = tp_ if tp_.ndim == 0 else tp_[: i_last - i0 + 1]
        o = b.o[i0:i_last + 1]
        h = b.h[i0:i_last + 1]
        l = b.l[i0:i_last + 1]
        thr = TICK if fill.limit_through else 0.0
        if side > 0:
            gap_sl, gap_tp = o <= sl_k, o >= tp_k
            hit_sl, hit_tp = l <= sl_k, h >= tp_k + thr
        else:
            gap_sl, gap_tp = o >= sl_k, o <= tp_k
            hit_sl, hit_tp = h >= sl_k, l <= tp_k - thr
        anyhit = gap_sl | gap_tp | hit_sl | hit_tp
        if anyhit.any():
            k = int(np.argmax(anyhit))
            slv = float(sl_k if sl_k.ndim == 0 else sl_k[k])
            tpv = float(tp_k if tp_k.ndim == 0 else tp_k[k])
            if gap_sl[k]:
                return i0 + k, float(o[k]), "stop"
            if gap_tp[k]:
                return i0 + k, float(o[k]), "target"
            if hit_sl[k] and hit_tp[k]:
                if fill.policy == "stop_first":
                    return i0 + k, slv, "stop"
                high_first = (h[k] - o[k]) < (o[k] - l[k])
                tp_first = high_first if side > 0 else not high_first
                return (i0 + k, tpv, "target") if tp_first else (i0 + k, slv, "stop")
            if hit_sl[k]:
                return i0 + k, slv, "stop"
            return i0 + k, tpv, "target"
    if time_exit_idx >= 0:
        return time_exit_idx, float(b.o[time_exit_idx]), "time"
    return i_last, float(b.c[i_last]), "eod"


def make_trade(b, strat: str, side: int, i0: int, exit_idx: int, exit_px: float,
               reason: str, costs: Costs, sl: float, tp: float) -> dict:
    entry = float(b.o[i0])
    pts = side * (exit_px - entry)
    c_nq = costs.trade_cost(NQ_PV, costs.commission_nq_side, reason)
    c_mnq = costs.trade_cost(MNQ_PV, costs.commission_mnq_side, reason)
    return {
        "strat": strat, "day": int(b.day[i0]), "side": side,
        "entry_idx": int(i0), "exit_idx": int(exit_idx),
        "entry_time": b.t[i0], "exit_time": b.t[exit_idx],
        "entry": entry, "exit": float(exit_px), "sl": float(sl), "tp": float(tp),
        "reason": reason, "pts": pts,
        "net_nq": pts * NQ_PV - c_nq, "cost_nq": c_nq,
        "net_mnq": pts * MNQ_PV - c_mnq, "cost_mnq": c_mnq,
    }


def config_dict(costs: Costs, fill: Fill) -> dict:
    return {"costs": asdict(costs), "fill": asdict(fill)}
