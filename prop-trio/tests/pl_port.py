"""Line-by-line Python ports of the three PowerLanguage signals in ../multicharts.

They run bar by bar with MultiCharts' order semantics (script at bar close; market orders fill at
the next bar's open; SetStopLoss/SetProfitTarget and the S2 intrabar limit/stop are live from the
entry bar; the stop wins when one bar touches both; limits need a one-tick trade-through).
The test suite checks that they produce exactly the bench's trades, so the numbers reported by
the bench are the numbers the MultiCharts code should reproduce.
"""
import math

import numpy as np

TICK = 0.25


def _jd(t):
    return int(t.astype("datetime64[D]").astype("int64"))


class Sim:
    """Minimal MultiCharts-like broker: one position, next-bar market orders, intrabar exits."""

    def __init__(self, b):
        self.b = b
        self.mp = 0
        self.entry_px = 0.0
        self.entry_i = -1
        self.pending = None          # ("entry", side) or ("exit",)
        self.trades = []
        self.sl = self.tp = None     # absolute levels while in a position

    def open_bar(self, i):
        b = self.b
        if self.pending is None:
            return
        kind = self.pending
        self.pending = None
        if kind[0] == "entry" and self.mp == 0:
            self.mp, self.entry_px, self.entry_i = kind[1], b.o[i], i
            self.sl = self.tp = None
        elif kind[0] == "exit" and self.mp != 0:
            self._close(i, b.o[i], "time")

    def _close(self, i, px, why):
        self.trades.append((self.entry_i, i, self.mp, self.entry_px, px, why))
        self.mp = 0

    def intrabar(self, i, sl, tp):
        if self.mp == 0 or sl is None:
            return
        b, s = self.b, self.mp
        o, h, l = b.o[i], b.h[i], b.l[i]
        if s > 0:
            if o <= sl:
                return self._close(i, o, "stop")
            if o >= tp:
                return self._close(i, o, "target")
            hs, ht = l <= sl, h >= tp + TICK
        else:
            if o >= sl:
                return self._close(i, o, "stop")
            if o <= tp:
                return self._close(i, o, "target")
            hs, ht = h >= sl, l <= tp - TICK
        if hs:
            return self._close(i, sl, "stop")
        if ht:
            return self._close(i, tp, "target")


def _clock(b, i):
    close_min = (int(b.mod[i]) + 1) % 1440        # MultiCharts Time of a bar = its close
    open_min = (close_min - 1 + 1440) % 1440
    close_jd = _jd(b.t[i] + np.timedelta64(1, 'm'))
    open_jd = close_jd - 1 if close_min == 0 else close_jd
    sess = open_jd + 1 if open_min >= 1020 else open_jd
    return close_min, open_min, open_jd, sess


class _ATR:
    def __init__(self, n):
        self.n, self.buf, self.idx, self.cnt = n, [0.0] * n, 0, 0
        self.hi = self.lo = self.cl = self.last_cl = 0.0
        self.atr = 0.0

    def bar(self, new_sess, first, h, l, c):
        if new_sess and not first:
            tr = (max(self.hi, self.last_cl) - min(self.lo, self.last_cl)) if self.last_cl > 0 else self.hi - self.lo
            self.last_cl = self.cl
            self.buf[self.idx] = tr
            self.idx = (self.idx + 1) % self.n
            self.cnt = min(self.cnt + 1, self.n)
            if self.cnt >= self.n:
                self.atr = sum(self.buf) / self.n
        if new_sess:
            self.hi, self.lo = h, l
        else:
            self.hi, self.lo = max(self.hi, h), min(self.lo, l)
        self.cl = c


class _ADX:
    def __init__(self, n):
        self.n, self.k = n, 0
        self.s_tr = self.s_p = self.s_m = self.adx = 0.0

    def update(self, h, l, ph, pl, pc):
        tr = max(h, pc) - min(l, pc)
        up, dn = h - ph, pl - l
        dp = up if (up > dn and up > 0) else 0.0
        dm = dn if (dn > up and dn > 0) else 0.0
        n = self.n
        if self.k == 0:
            self.s_tr, self.s_p, self.s_m = tr, dp, dm
        else:
            self.s_tr += (tr - self.s_tr) / n
            self.s_p += (dp - self.s_p) / n
            self.s_m += (dm - self.s_m) / n
        if self.s_tr > 0:
            dip, dim = 100 * self.s_p / self.s_tr, 100 * self.s_m / self.s_tr
        else:
            dip = dim = 0.0
        dx = 100 * abs(dip - dim) / (dip + dim) if dip + dim > 0 else 0.0
        prev = self.adx
        self.adx = dx if self.k == 0 else self.adx + (dx - self.adx) / n
        self.k += 1
        return prev


def port_s1(b, NoisePct=0.30, ATRLen=15, TargetPts=40.0, StopPts=75.0, UseATRExits=False,
            TargetATR=0.0, StopATR=0.0, UseTODBand=False, TODDays=14,
            FirstMin=600, LastMin=840, ExitMin=870, MaxTrades=3, SigMins=30):
    sim, atr = Sim(b), _ATR(ATRLen)
    prev_day = prev_sess = None
    cum_pv = cum_v = 0.0
    ref = 0.0
    trades_today = 0
    ring, day_rec = 0, False
    mv = [[0.0] * 60 for _ in range(40)]
    mvset = [[False] * 60 for _ in range(40)]
    band_ok, sigma = False, 0.0
    for i in range(b.n):
        sim.open_bar(i)
        if sim.mp != 0:
            d_tp = (TargetATR * atr.atr if (UseATRExits and TargetATR > 0) else TargetPts)
            d_sl = (StopATR * atr.atr if (UseATRExits and StopATR > 0) else StopPts)
            if sim.sl is None:
                sim.sl, sim.tp = sim.entry_px - d_sl, sim.entry_px + d_tp
            sim.intrabar(i, sim.sl, sim.tp)
        cm, om, day, sess = _clock(b, i)
        new_day, new_sess = (i == 0 or day != prev_day), (i == 0 or sess != prev_sess)
        prev_day, prev_sess = day, sess
        atr.bar(new_sess, i == 0, b.h[i], b.l[i], b.c[i])
        if new_day:
            ref, trades_today, day_rec, cum_pv, cum_v = b.o[i], 0, False, 0.0, 0.0
        cum_pv += (b.h[i] + b.l[i] + b.c[i]) / 3 * b.v[i]
        cum_v += b.v[i]
        vw = cum_pv / cum_v if cum_v > 0 else b.c[i]
        noise_up = ref + NoisePct * atr.atr
        is_sig = cm % SigMins == 0 and FirstMin <= cm <= LastMin
        if UseTODBand and is_sig and ref > 0:
            slot = (cm - FirstMin) // SigMins
            if not day_rec:
                ring = (ring + 1) % 40
                mvset[ring] = [False] * 60
                day_rec = True
            vals = [mv[(ring - d) % 40][slot] for d in range(1, TODDays + 1) if mvset[(ring - d) % 40][slot]]
            band_ok = len(vals) == TODDays
            if band_ok:
                sigma = sum(vals) / TODDays
            mv[ring][slot] = abs(b.c[i] / ref - 1)
            mvset[ring][slot] = True
        if is_sig and sim.mp == 0 and trades_today < MaxTrades and atr.atr > 0 and ref > 0:
            barrier = (ref * (1 + sigma) if band_ok else math.inf) if UseTODBand else noise_up
            if b.c[i] > barrier and b.c[i] > vw:
                sim.pending = ("entry", 1)
                trades_today += 1
        if sim.mp == 1 and ExitMin <= cm <= 960:
            sim.pending = ("exit",)
    return sim.trades


def port_s2(b, ORStartMin=510, OREndMin=540, AnchorMin=0, ADXLen=14, ADXMin=20.0, TPBars=5,
            SLBars=20, DynamicExits=False, CutoffMin=900, ExitMin=955, MaxTrades=1):
    sim, adx = Sim(b), _ADX(ADXLen)
    prev_day = None
    orh = 0.0
    or_bars = 0
    armed = touched = anchor_done = False
    trades_today = 0
    cum_pv = cum_v = vw = 0.0
    tp = sl = 0.0
    prev_adx = 0.0
    for i in range(b.n):
        sim.open_bar(i)
        if sim.mp == 1:
            sim.intrabar(i, sl, tp)
        cm, om, day, _ = _clock(b, i)
        new_day = i == 0 or day != prev_day
        prev_day = day
        if new_day:
            orh, or_bars, armed, touched, trades_today, anchor_done = 0.0, 0, False, False, 0, False
            cum_pv = cum_v = 0.0
        if not anchor_done and om >= AnchorMin:
            anchor_done, cum_pv, cum_v = True, 0.0, 0.0
        if anchor_done:
            cum_pv += (b.h[i] + b.l[i] + b.c[i]) / 3 * b.v[i]
            cum_v += b.v[i]
            vw = cum_pv / cum_v if cum_v > 0 else b.c[i]
        if i > 0:
            prev_adx = adx.update(b.h[i], b.l[i], b.h[i - 1], b.l[i - 1], b.c[i - 1])
        if ORStartMin <= om < OREndMin:
            orh = b.h[i] if or_bars == 0 else max(orh, b.h[i])
            or_bars += 1
        if sim.mp == 0 and or_bars >= 10 and om >= OREndMin and om < CutoffMin and trades_today < MaxTrades:
            if not armed and b.c[i] > orh:
                armed = True
            if armed:
                if b.l[i] <= vw:
                    touched = True
                if touched and b.c[i] > vw and adx.k > 1 and adx.adx > ADXMin and adx.adx <= prev_adx:
                    tp = max(b.h[i - TPBars + 1:i + 1])
                    sl = min(b.l[i - SLBars + 1:i + 1])
                    sim.pending = ("entry", 1)
                    trades_today += 1
                    touched = False
        if sim.mp == 1 and DynamicExits:
            tp = max(b.h[i - TPBars + 1:i + 1])
            sl = min(b.l[i - SLBars + 1:i + 1])
        if sim.mp == 1 and ExitMin <= cm <= 960:
            sim.pending = ("exit",)
    return sim.trades


def port_s3(b, ONStartMin=0, ORMins=15, FirstMin=540, LastMin=855, ExitMin=870, ADXLen=14,
            ADXMin=20.0, StopATR=0.30, ATRLen=15, TargetR=3.0, SigMins=15):
    sim, atr, adx = Sim(b), _ATR(ATRLen), _ADX(ADXLen)
    prev_day = prev_sess = prev_bkey = None
    in_on_prev = False
    onh = onl = 0.0
    on_valid = bias_done = traded = False
    bias = 0
    orh = orl = 0.0
    or_bars = 0
    bh = bl = bc = ph = pl = pc = 0.0
    nb, b_closed = 0, True
    for i in range(b.n):
        sim.open_bar(i)
        if sim.mp != 0:
            if sim.sl is None:
                sd = StopATR * atr.atr
                sim.sl = sim.entry_px - sim.mp * sd
                sim.tp = sim.entry_px + sim.mp * TargetR * sd
            sim.intrabar(i, sim.sl, sim.tp)
        cm, om, day, sess = _clock(b, i)
        new_day, new_sess = (i == 0 or day != prev_day), (i == 0 or sess != prev_sess)
        prev_day, prev_sess = day, sess
        atr.bar(new_sess, i == 0, b.h[i], b.l[i], b.c[i])
        if new_day:
            bias_done, bias, or_bars, traded = False, 0, 0, False
        in_on = (om < 510) if ONStartMin == 0 else (om >= ONStartMin or om < 510)
        if in_on and not in_on_prev:
            onh, onl, on_valid = b.h[i], b.l[i], True
        elif in_on:
            onh, onl = max(onh, b.h[i]), min(onl, b.l[i])
        in_on_prev = in_on
        if 510 <= om < 1020 and not bias_done:
            bias_done, bias = True, 0
            if on_valid and om <= 515 and onh > onl:
                pos = (b.o[i] - onl) / (onh - onl)
                bias = 1 if pos >= 2 / 3 else (-1 if pos <= 1 / 3 else 0)
            on_valid = False
        if 510 <= om < 510 + ORMins:
            if or_bars == 0:
                orh, orl = b.h[i], b.l[i]
            else:
                orh, orl = max(orh, b.h[i]), min(orl, b.l[i])
            or_bars += 1
        bkey = day * 1440 + om - om % SigMins
        new_b = i == 0 or bkey != prev_bkey
        prev_bkey = bkey

        def close_bucket():
            nonlocal ph, pl, pc, nb
            if nb > 0:
                adx.update(bh, bl, ph, pl, pc)
            ph, pl, pc, nb = bh, bl, bc, nb + 1

        if new_b and i > 0 and not b_closed:
            close_bucket()
            b_closed = True
        if new_b:
            bh, bl, b_closed = b.h[i], b.l[i], False
        else:
            bh, bl = max(bh, b.h[i]), min(bl, b.l[i])
        bc = b.c[i]
        if cm % SigMins == 0:
            close_bucket()
            b_closed = True
            if (FirstMin <= cm <= LastMin and sim.mp == 0 and not traded and bias != 0 and or_bars > 0
                    and atr.atr > 0 and nb > 2 and adx.adx > ADXMin):
                if bias == 1 and b.c[i] > orh:
                    sim.pending, traded = ("entry", 1), True
                elif bias == -1 and b.c[i] < orl:
                    sim.pending, traded = ("entry", -1), True
        if ExitMin <= cm <= 960 and sim.mp != 0:
            sim.pending = ("exit",)
    return sim.trades
