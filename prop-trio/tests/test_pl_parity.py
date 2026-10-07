"""The PowerLanguage logic (ported line by line in pl_port.py) must reproduce the bench's trades."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from bench import synth, strategies as st                  # noqa: E402
from bench.data import Bars                                 # noqa: E402
from bench.engine import Costs                              # noqa: E402
import pl_port                                              # noqa: E402

_B = None


def bars():
    global _B
    if _B is None:
        df = synth.make_bars("2020-01-01", "2021-03-31", seed=11)
        t = df["t"].values.astype("datetime64[m]")
        _B = Bars(t, *(df[k].to_numpy(float) for k in "ohlcv"))
    return _B


def bench_rows(tr):
    if len(tr) == 0:
        return []
    return [(int(a), int(b), int(s), round(e, 2), round(x, 2), r) for a, b, s, e, x, r in
            zip(tr["entry_idx"], tr["exit_idx"], tr["side"], tr["entry"], tr["exit"], tr["reason"])]


def port_rows(tr):
    return [(a, b, s, round(float(e), 2), round(float(x), 2), r) for a, b, s, e, x, r in tr]


class TestParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = bars()
        cls.ctx = st.Ctx(cls.b, Costs(0, 0, 0))

    def check(self, bench_tr, port_tr):
        a, p = bench_rows(bench_tr), port_rows(port_tr)
        self.assertGreater(len(a), 20)
        diff = [(x, y) for x, y in zip(a, p) if x != y]
        self.assertEqual(len(a), len(p), f"trade count {len(a)} vs {len(p)}; first diffs {diff[:3]}")
        self.assertEqual(diff[:3], [])

    def test_s1_faithful(self):
        self.check(st.s1_vault_break(self.ctx), pl_port.port_s1(self.b))

    def test_s1_atr_exits_and_tod_band(self):
        self.check(st.s1_vault_break(self.ctx, exits="atr", tp_atr=0.3, sl_atr=0.55),
                   pl_port.port_s1(self.b, UseATRExits=True, TargetATR=0.3, StopATR=0.55))
        self.check(st.s1_vault_break(self.ctx, noise="tod"), pl_port.port_s1(self.b, UseTODBand=True))

    def test_s2_faithful_and_variants(self):
        self.check(st.s2_vwap_adx_pullback(self.ctx), pl_port.port_s2(self.b))
        self.check(st.s2_vwap_adx_pullback(self.ctx, vwap_anchor=510), pl_port.port_s2(self.b, AnchorMin=510))
        self.check(st.s2_vwap_adx_pullback(self.ctx, exit_mode="dynamic"), pl_port.port_s2(self.b, DynamicExits=True))
        self.check(st.s2_vwap_adx_pullback(self.ctx, max_trades=3), pl_port.port_s2(self.b, MaxTrades=3))

    def test_s3_faithful_and_variants(self):
        self.check(st.s3_overnight_bias_orb(self.ctx), pl_port.port_s3(self.b))
        self.check(st.s3_overnight_bias_orb(self.ctx, on_start=1020), pl_port.port_s3(self.b, ONStartMin=1020))
        self.check(st.s3_overnight_bias_orb(self.ctx, on_start=1380), pl_port.port_s3(self.b, ONStartMin=1380))
        self.check(st.s3_overnight_bias_orb(self.ctx, tp_r=1.5), pl_port.port_s3(self.b, TargetR=1.5))
        self.check(st.s3_overnight_bias_orb(self.ctx, entry_start=570), pl_port.port_s3(self.b, FirstMin=570))


if __name__ == "__main__":
    unittest.main()
