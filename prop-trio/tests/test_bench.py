"""Rule-by-rule tests on hand-built bars.  Run:  python -m unittest discover -s tests -v"""
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bench import data, indicators as ind, prop, stats, synth          # noqa: E402
from bench import strategies as st                                      # noqa: E402
from bench.data import Bars                                             # noqa: E402
from bench.engine import Costs, Fill, resolve_exit                      # noqa: E402

ZERO = Costs(0.0, 0.0, 0.0)


def flat_sessions(first_day="2024-01-02", n=16, px=10000.0, rng_pts=100.0):
    """n weekday sessions of quiet 1-min bars whose session range is exactly rng_pts."""
    rows = []
    for d in pd.bdate_range(first_day, periods=n):
        t0 = pd.Timestamp(d) - pd.Timedelta(hours=7)          # 17:00 prior day
        mins = pd.date_range(t0, periods=23 * 60, freq="min")
        o = np.full(len(mins), px)
        h, l = o + 1.0, o - 1.0
        h[100] = px + rng_pts / 2                              # one spike each way
        l[200] = px - rng_pts / 2
        rows.append(pd.DataFrame({"t": mins, "o": o, "h": h, "l": l, "c": o, "v": 100.0}))
    return pd.concat(rows, ignore_index=True)


def day_frame(day, px=10000.0, start="00:00", end="15:59"):
    t = pd.date_range(f"{day} {start}", f"{day} {end}", freq="min")
    o = np.full(len(t), px)
    return pd.DataFrame({"t": t, "o": o, "h": o + 0.25, "l": o - 0.25, "c": o.copy(), "v": 100.0})


def set_bar(df, ts, o=None, h=None, l=None, c=None, v=None):
    k = df.index[df["t"] == pd.Timestamp(ts)][0]
    for col, val in (("o", o), ("h", h), ("l", l), ("c", c), ("v", v)):
        if val is not None:
            df.at[k, col] = val
    df.at[k, "h"] = max(df.at[k, "h"], df.at[k, "o"], df.at[k, "c"])
    df.at[k, "l"] = min(df.at[k, "l"], df.at[k, "o"], df.at[k, "c"])
    return k


def to_bars(df):
    df = df.sort_values("t").drop_duplicates("t", keep="last")
    t = df["t"].values.astype("datetime64[m]")
    return Bars(t, *(df[k].to_numpy(float) for k in "ohlcv"))


def idx_of(b, ts):
    return int(np.flatnonzero(b.t == np.datetime64(pd.Timestamp(ts), "m"))[0])


class TestEngine(unittest.TestCase):
    def setUp(self):
        df = day_frame("2024-03-04", start="09:00", end="09:09")
        self.df = df

    def bars(self):
        return to_bars(self.df)

    def test_target_needs_trade_through(self):
        set_bar(self.df, "2024-03-04 09:02", h=10010.0)       # touches 10010 exactly
        set_bar(self.df, "2024-03-04 09:04", h=10010.25)      # one tick through
        b = self.bars()
        xi, px, why = resolve_exit(b, 0, b.n - 1, -1, 1, 9900.0, 10010.0, Fill())
        self.assertEqual((xi, px, why), (4, 10010.0, "target"))
        xi, px, why = resolve_exit(b, 0, b.n - 1, -1, 1, 9900.0, 10010.0, Fill(limit_through=False))
        self.assertEqual(xi, 2)

    def test_both_hit_is_stop_first_by_default(self):
        set_bar(self.df, "2024-03-04 09:03", h=10020.0, l=9980.0)
        b = self.bars()
        self.assertEqual(resolve_exit(b, 0, b.n - 1, -1, 1, 9990.0, 10010.0, Fill())[2], "stop")
        # bar-magnifier ordering: open 10000 is nearer the low (9980 is 20 away, high 20 away) ->
        # tie goes O-L-H-C, stop first for a long
        self.assertEqual(resolve_exit(b, 0, b.n - 1, -1, 1, 9990.0, 10010.0, Fill("ohlc"))[2], "stop")
        set_bar(self.df, "2024-03-04 09:03", h=10012.0, l=9980.0)
        b = self.bars()
        self.assertEqual(resolve_exit(b, 0, b.n - 1, -1, 1, 9990.0, 10010.0, Fill("ohlc"))[2], "target")

    def test_gap_through_stop_fills_at_open(self):
        set_bar(self.df, "2024-03-04 09:05", o=9950.0, h=9955.0, l=9940.0, c=9950.0)
        b = self.bars()
        xi, px, why = resolve_exit(b, 0, b.n - 1, -1, 1, 9990.0, 10050.0, Fill())
        self.assertEqual((xi, px, why), (5, 9950.0, "stop"))

    def test_short_side_and_time_exit(self):
        b = self.bars()
        xi, px, why = resolve_exit(b, 0, 6, 7, -1, 10050.0, 9950.0, Fill())
        self.assertEqual((xi, px, why), (7, 10000.0, "time"))
        set_bar(self.df, "2024-03-04 09:02", l=9949.75)
        b = self.bars()
        self.assertEqual(resolve_exit(b, 0, 6, 7, -1, 10050.0, 9950.0, Fill())[:3], (2, 9950.0, "target"))


class TestIndicators(unittest.TestCase):
    def test_vwap_typical_price(self):
        df = day_frame("2024-03-04", start="00:00", end="00:02")
        df.loc[:, ["o", "h", "l", "c", "v"]] = [[10, 12, 8, 10, 1], [10, 13, 10, 13, 3], [13, 14, 12, 13, 0]]
        b = to_bars(df)
        vw = ind.vwap(b, 0)
        self.assertAlmostEqual(vw[0], 10.0)
        self.assertAlmostEqual(vw[1], (10 * 1 + 12 * 3) / 4)
        self.assertAlmostEqual(vw[2], vw[1])                  # zero volume -> unchanged

    def test_adx_matches_hand_recursion(self):
        rng = np.random.default_rng(3)
        c = 100 + np.cumsum(rng.standard_normal(60))
        h, l = c + rng.random(60), c - rng.random(60)
        got = ind.wilder_adx(h, l, c, 14)
        str_ = sp = sm = adx = None
        for i in range(1, 60):
            tr = max(h[i], c[i - 1]) - min(l[i], c[i - 1])
            up, dn = h[i] - h[i - 1], l[i - 1] - l[i]
            pdm = up if (up > dn and up > 0) else 0.0
            mdm = dn if (dn > up and dn > 0) else 0.0
            if str_ is None:
                str_, sp, sm = tr, pdm, mdm
            else:
                str_ += (tr - str_) / 14
                sp += (pdm - sp) / 14
                sm += (mdm - sm) / 14
            pdi, mdi = 100 * sp / str_, 100 * sm / str_
            dx = 100 * abs(pdi - mdi) / (pdi + mdi) if pdi + mdi > 0 else 0.0
            adx = dx if adx is None else adx + (dx - adx) / 14
            self.assertAlmostEqual(got[i], adx, places=9)

    def test_session_atr_simple_average_known_next_session(self):
        b = to_bars(flat_sessions(n=16, rng_pts=100.0))
        atr = ind.session_atr(b, 15)
        sess = sorted(set(b.sess))
        self.assertTrue(np.isnan(atr[sess[14]]))              # only 14 completed sessions
        self.assertAlmostEqual(atr[sess[15]], 100.0)          # 15 completed, each TR = 100


class TestS1(unittest.TestCase):
    """ATR = 100 -> barrier = midnight + 30. Target 40, stop 75 points."""

    def build(self, modify):
        hist = flat_sessions("2024-02-05", n=16)              # through 2024-02-26
        day = "2024-02-27"
        eve = day_frame("2024-02-26", start="17:00", end="23:59")
        df = day_frame(day)
        modify(df)
        return to_bars(pd.concat([hist, eve, df], ignore_index=True)), day

    def test_entries_reentries_cap_and_time_exit(self):
        def mod(df):
            # VWAP stays near 10000; close above 10030 from 09:59 on
            df.loc[df["t"] >= "2024-02-27 09:59", ["o", "h", "l", "c"]] = [10035, 10035.25, 10034.75, 10035]
            set_bar(df, "2024-02-27 10:05", h=10080.0)        # first trade (in at 10:00) -> target
            set_bar(df, "2024-02-27 10:40", h=10080.0)        # second (in at 10:30) -> target
            set_bar(df, "2024-02-27 11:10", l=9950.0)         # third (in at 11:00) -> stop at 10035-75
        b, day = self.build(mod)
        ctx = st.Ctx(b, ZERO)
        tr = st.s1_vault_break(ctx)
        self.assertEqual(len(tr), 3)                          # capped at 3
        self.assertEqual([str(x)[11:16] for x in tr["entry_time"]], ["10:00", "10:30", "11:00"])
        self.assertEqual(list(tr["reason"]), ["target", "target", "stop"])
        self.assertAlmostEqual(tr["pts"].iloc[0], 40.0)
        self.assertAlmostEqual(tr["pts"].iloc[2], -75.0)

    def test_no_entry_below_vwap_and_time_exit(self):
        def mod(df):
            # big volume at a high price early -> VWAP far above the barrier
            set_bar(df, "2024-02-27 03:00", o=10200, h=10200, l=10200, c=10200, v=1e7)
            df.loc[df["t"] >= "2024-02-27 09:59", ["o", "h", "l", "c"]] = [10035, 10035.25, 10034.75, 10035]
        b, day = self.build(mod)
        self.assertEqual(len(st.s1_vault_break(st.Ctx(b, ZERO))), 0)

        def mod2(df):
            df.loc[df["t"] >= "2024-02-27 13:59", ["o", "h", "l", "c"]] = [10035, 10035.25, 10034.75, 10035]
        b, day = self.build(mod2)
        tr = st.s1_vault_break(st.Ctx(b, ZERO))
        self.assertEqual(len(tr), 1)                          # 14:00 signal only, then 14:30 exit
        self.assertEqual(str(tr["entry_time"].iloc[0])[11:16], "14:00")
        self.assertEqual(str(tr["exit_time"].iloc[0])[11:16], "14:30")
        self.assertEqual(tr["reason"].iloc[0], "time")


class TestS2(unittest.TestCase):
    def build(self, modify, adx_fn):
        df = day_frame("2024-03-05", start="00:00", end="15:59")
        modify(df)
        b = to_bars(df)
        ctx = st.Ctx(b, ZERO)
        ctx.__dict__["adx1"] = adx_fn(b)                      # control the ADX directly
        return b, ctx

    def test_arm_touch_close_above_then_wait_for_adx(self):
        def mod(df):
            set_bar(df, "2024-03-05 08:40", h=10010.0)        # OR high 10010 (08:30-08:59)
            set_bar(df, "2024-03-05 09:10", o=10000, h=10012, l=10000, c=10011)   # arm
            set_bar(df, "2024-03-05 09:20", o=10011, h=10011, l=9990, c=10003)    # touch + close above
            df.loc[(df["t"] > "2024-03-05 09:20") & (df["t"] < "2024-03-05 09:40"),
                   ["o", "h", "l", "c"]] = [10004, 10004.25, 10003.75, 10004]
            set_bar(df, "2024-03-05 09:40", h=10030.0)        # target touched later

        def adx(b):
            a = np.full(b.n, 25.0)
            k = idx_of(b, "2024-03-05 09:00")
            a[k:] = 25.0 + np.arange(b.n - k) * 0.1              # rising -> blocked
            j = idx_of(b, "2024-03-05 09:25")
            a[j] = a[j - 1] - 0.5                                 # stops rising at 09:25
            return a

        b, ctx = self.build(mod, adx)
        tr = st.s2_vwap_adx_pullback(ctx)
        self.assertEqual(len(tr), 1)
        self.assertEqual(str(tr["entry_time"].iloc[0])[11:16], "09:26")
        # target = highest high of the 5 bars ending 09:25; stop = lowest low of 20 bars
        self.assertEqual(tr["tp"].iloc[0], 10004.25)
        self.assertEqual(tr["sl"].iloc[0], 9990.0)

    def test_no_arm_no_trade_and_opening_range_is_30_minutes(self):
        def mod(df):
            set_bar(df, "2024-03-05 08:50", h=10020.0)        # in the 08:30-09:00 range
            set_bar(df, "2024-03-05 09:10", o=10000, h=10016, l=9990, c=10015)  # below ORH 10020

        b, ctx = self.build(mod, lambda b: np.full(b.n, 25.0))
        self.assertEqual(len(st.s2_vwap_adx_pullback(ctx)), 0)


class TestS3(unittest.TestCase):
    def build(self, open830, breakout_close, adx_val=25.0, side=1):
        hist = flat_sessions("2024-02-05", n=16, rng_pts=100.0)          # ATR15 = 100
        eve = day_frame("2024-02-26", start="17:00", end="23:59")
        df = day_frame("2024-02-27")
        set_bar(df, "2024-02-27 02:00", h=10060.0)            # overnight range 9940..10060
        set_bar(df, "2024-02-27 03:00", l=9940.0)
        df.loc[df["t"] >= "2024-02-27 08:30", ["o", "h", "l", "c"]] = [open830, open830 + .25, open830 - .25, open830]
        set_bar(df, "2024-02-27 08:35", h=open830 + 5, l=open830 - 5)     # OR = open830 +/- 5
        set_bar(df, "2024-02-27 09:14", c=breakout_close)     # 15-min bar 09:00-09:15 closes there
        b = to_bars(pd.concat([hist, eve, df], ignore_index=True))
        ctx = st.Ctx(b, ZERO)
        ctx._cache[("bkadx", 15, 14)] = np.full(len(ctx.buckets(15)), adx_val)
        return b, ctx

    def test_long_bias_top_third(self):
        b, ctx = self.build(open830=10050.0, breakout_close=10060.0)
        tr = st.s3_overnight_bias_orb(ctx)
        self.assertEqual(len(tr), 1)
        self.assertEqual(int(tr["side"].iloc[0]), 1)
        self.assertEqual(str(tr["entry_time"].iloc[0])[11:16], "09:15")
        e = tr["entry"].iloc[0]
        self.assertAlmostEqual(e - tr["sl"].iloc[0], 30.0)    # 0.30 x ATR 100
        self.assertAlmostEqual(tr["tp"].iloc[0] - e, 90.0)    # 3 x stop

    def test_middle_third_and_low_adx_do_not_trade(self):
        b, ctx = self.build(open830=10000.0, breakout_close=10010.0)
        self.assertEqual(len(st.s3_overnight_bias_orb(ctx)), 0)
        b, ctx = self.build(open830=10050.0, breakout_close=10060.0, adx_val=19.0)
        self.assertEqual(len(st.s3_overnight_bias_orb(ctx)), 0)

    def test_short_bias_bottom_third(self):
        b, ctx = self.build(open830=9950.0, breakout_close=9940.0)
        tr = st.s3_overnight_bias_orb(ctx)
        self.assertEqual(int(tr["side"].iloc[0]), -1)
        self.assertAlmostEqual(tr["sl"].iloc[0] - tr["entry"].iloc[0], 30.0)


class TestProp(unittest.TestCase):
    def test_pass_fail_consistency_and_expiry(self):
        p = prop.Profile("t", target=3000, trail_dd=2000, dll=None)
        close = np.array([1000, 1000, 1000.0]); dmin = np.zeros(3); traded = np.ones(3, bool)
        self.assertEqual(prop.run_challenge(close, dmin, traded, 0, p), ("pass", 3))
        # EOD trailing: a +1500 day lifts the threshold from -2000 to -500, so from a
        # balance of 1500 a 1999 intraday dip survives and a 2000 dip fails
        close = np.array([1500, -100.0, 0])
        self.assertEqual(prop.run_challenge(close, np.array([0, -1999.0, 0]), traded, 0, p)[0], "open")
        self.assertEqual(prop.run_challenge(close, np.array([0, -2000.0, 0]), traded, 0, p), ("fail", 2))
        # consistency 50%: a single +3000 day can't pass until total reaches 6000
        pc = prop.Profile("c", consistency=0.5, dll=None)
        close = np.array([3000.0, 1000, 1000, 1000]); dmin = np.zeros(4); traded = np.ones(4, bool)
        self.assertEqual(prop.run_challenge(close, dmin, traded, 0, pc), ("pass", 4))
        pe = prop.Profile("e", max_days=2, dll=None)
        self.assertEqual(prop.run_challenge(np.array([100.0, 100, 5000]), np.zeros(3),
                                            np.ones(3, bool), 0, pe), ("expired", 2))

    def test_vectorised_rolling_equals_scalar(self):
        rng = np.random.default_rng(0)
        n = 400
        close = np.round(rng.normal(60, 450, n), 2)
        dmin = np.minimum(0, close - np.abs(rng.normal(0, 300, n)))
        traded = rng.random(n) < 0.8
        for prof_ in prop.PROFILES.values():
            want = prop.summarize([prop.run_challenge(close, dmin, traded, s, prof_) for s in range(n)])
            self.assertEqual(prop.rolling(close, dmin, traded, prof_), want)

    def test_day_paths_worst_and_dll(self):
        df = day_frame("2024-03-05", start="08:30", end="15:59")
        set_bar(df, "2024-03-05 09:05", l=9950.0)
        b = to_bars(df)
        tr = pd.DataFrame([{"day": int(b.day[0]), "entry_idx": 30, "exit_idx": 60, "side": 1,
                            "entry": 10000.0, "exit": 10010.0, "net_mnq": 20.0}])
        paths = prop.DayPaths(b, {"A": tr}, np.array([int(b.day[0])]), ZERO)
        self.assertAlmostEqual(paths.worst["A"][0].min(), -100.0)   # 50 pts x $2
        self.assertAlmostEqual(paths.real["A"][0, -1], 20.0)
        close, dmin, _ = paths.combine({"A": 10}, dll=500.0)        # -1000 intraday at 10 micros
        self.assertEqual((close[0], dmin[0]), (-500.0, -500.0))


class TestLoader(unittest.TestCase):
    def roundtrip(self, tz, stamp, fmt):
        df = synth.make_bars("2021-01-04", "2021-08-31", seed=5)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "NQ_test.txt")
            synth.write_multicharts(df, p, tz=tz, stamp=stamp, date_fmt=fmt)
            b = data.load_bars(d, verbose=False)
        self.assertEqual(b.info["tz_source"], tz)
        self.assertEqual(b.info["stamp"], stamp)
        src = df["t"].values.astype("datetime64[m]")
        self.assertGreater(np.isin(b.t, src).mean(), 0.9999)
        self.assertGreater(len(b.t) / len(src), 0.999)

    def test_eastern_close_stamped_greek_dates(self):
        self.roundtrip("America/New_York", "close", "%d/%m/%Y")

    def test_central_open_stamped_iso(self):
        self.roundtrip("America/Chicago", "open", "%Y-%m-%d")

    def test_athens_clock(self):
        self.roundtrip("Europe/Athens", "close", "%d.%m.%Y")


class TestBenchRule(unittest.TestCase):
    def test_benches_in_deep_drawdown_and_returns_at_new_high(self):
        t = pd.date_range("2020-01-01", periods=400, freq="D")
        x = np.r_[np.tile([100.0, -50.0], 150), np.full(40, -200.0), np.full(60, 300.0)]
        tr = pd.DataFrame({"entry_time": t, "net_nq": x})
        take = stats.bench_mask(tr)
        self.assertTrue(take[:300].all())
        self.assertFalse(take[330:345].any())                 # benched inside the slide
        self.assertTrue(take[-1])                             # back after a new high


if __name__ == "__main__":
    unittest.main()
