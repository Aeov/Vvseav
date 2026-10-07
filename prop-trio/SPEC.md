# The three prop-firm strategies — exact rules

Source: the interview transcript with Matteo (ex-market maker, CIO at a quant fund),
timestamps in `[hh:mm:ss]`. All times are **US Central (CME exchange time)**.
Instrument: **NQ** (Nasdaq-100 E-mini, $20/point). For challenges Matteo sizes each
strategy at **5 MNQ** (micro, $2/point), so 5 micros = half an NQ.

Every rule below is implemented identically in `bench/strategies.py` (Python) and in
`multicharts/*.txt` (PowerLanguage). Each ambiguity names the default chosen and the
variant that tests the other reading.

---

## S1 — Vault Break (NQ, 30-minute signals, long only)

**Why it should work** [00:10:37]: positive drift in NQ; only trade a clear
directional push that escapes the overnight "noise area" and is backed by volume (VWAP).

| Rule | Value | Source |
|---|---|---|
| Reference price | price of NQ at **00:00 CT** (open of the first bar after midnight) | [00:11:15] |
| Volatility | average true range of the **past 15 sessions** (simple average, daily sessions 17:00→16:00) | [00:12:28], [00:18:30] |
| Noise-up barrier | reference + **30% × ATR15** — fixed for the whole day | [00:13:05], [00:18:30] |
| VWAP | volume-weighted average price **anchored at 00:00 CT** | [00:54:07] |
| Entry | a 30-min bar **closes above the barrier AND above VWAP** → buy at the **open of the next bar** | [00:15:16], [00:17:08] |
| Entry window | signal bars closing **10:00 → before 14:30 CT** | [00:16:17] |
| Max entries | **3 per day**; after a target or stop, a new signal re-enters while the conditions hold | [00:16:17], [00:19:54] |
| Take profit | **+$800 per NQ = 40 points** | [00:19:07] |
| Stop loss | **−$1,500 per NQ = 75 points** | [00:19:07] |
| Time exit | **14:30 CT**, at market | [00:19:07] |

Matteo's stated results [00:57:44]: average trade **$112** per NQ, about **67% winners**.

## S2 — VWAP Pullback with ADX gate (NQ, 1-minute, long only)

**Why it should work** [00:27:21]: most institutional flow is executed by VWAP algorithms;
a pullback to VWAP in an up-move, followed by a close back above VWAP while the pullback's
momentum fades, is where those algos push price back up.

| Step | Rule | Source |
|---|---|---|
| Opening range | high/low of **08:30–09:00 CT** (30 minutes) | [00:28:19] |
| 1. Arm | a 1-min bar **closes above the opening-range high** | [00:31:53] |
| 2. Pullback | price **touches VWAP** (bar low ≤ VWAP) | [00:31:53] |
| 3. Trigger | a bar **closes back above VWAP** | [00:31:53] |
| 4. ADX gate | ADX(14) **> 20 and not increasing** (ADX ≤ previous bar's ADX). If only the ADX is missing, wait for it | [00:32:51], [00:33:56] |
| Same bar | steps 1, 2 and 3 may all happen on one bar | [00:33:27] |
| Entry | buy at the **open of the next bar** | [00:33:27] |
| Take profit | **high of the past 5 bars** | [00:34:44] |
| Stop loss | **low of the past 20 bars** | [00:34:44] |
| Time exit | **15:55 CT** | [00:34:44] |

Matteo's stated results [01:01:26]: fewer trades than S1, higher average trade, similar win rate.
He notes the target can coincide with the entry candle's high "less than 5% of the time" [00:35:22].

## S3 — Overnight Bias Opening-Range Breakout (NQ, 15-minute, long and short)

**Why it should work** [00:36:44]: overnight price discovery by participants who trade
before the cash open sets a direction; a break of the first 15 minutes confirms it.

| Rule | Value | Source |
|---|---|---|
| Overnight range | high/low **00:00 → 08:30 CT** as coded on his chart (whiteboard said 23:00) | [01:04:29], [00:37:31] |
| Bias | where the **08:30 open** sits in the overnight range: **top third → long only**, **bottom third → short only**, middle third → **no trade** | [00:38:30] |
| Opening range | the first 15-min bar, **08:30–08:45** | [00:38:30] |
| Entry | a 15-min bar **closes above the OR high** (long bias) or **below the OR low** (short bias), with **ADX(14) > 20** (rising or falling is irrelevant) → enter at the **next bar's open** | [00:40:41], [00:41:27] |
| Still valid | price dipping into the middle third during the OR, or breaking the opposite side first | [00:40:41], [00:46:31] |
| Trades | **one per day** | [00:42:24] |
| Stop loss | **30% of ATR15** (same 15-session average as S1) | [00:43:16], [00:44:07] |
| Take profit | **3 × the stop distance** | [00:44:07] |
| Time exit | **14:30 CT** (most trades end here) | [00:45:50] |

Matteo's stated results [01:13:15]: profit factor **1.4**, **53% winners**, about **$200,000 per NQ
2022–2026**, $88,000 of it from outliers. He sees S3 as a funded-account strategy more than a
challenge strategy.

## How he runs them together

* Each strategy on its own chart, all three live at once, automated [01:17:23].
* **About 5 micros each**, average time to pass **about 5 trading days** [01:19:15].
* Each alone passes about **40%** of challenges [01:07:19]; together their daily P&L correlation is
  **below 0.25** [01:11:00].
* Developed on 2018–2022, **out of sample from 2023** [00:56:23].
* **Bench rule** [01:11:38]: Monte Carlo the trade list; if the live drawdown is beyond the
  **75th percentile** of simulated drawdowns, stop trading the strategy until its equity makes a
  **new high** [01:09:00].

---

## What DeepSeek's "corrected" version gets wrong

DeepSeek's spelling and terminology fixes (VWOP→VWAP, ENQ→NQ, ADX "not increasing", 14:30,
3× stop) are right. These are not:

| # | DeepSeek says | Correct | Why it matters |
|---|---|---|---|
| 1 | S2 opening range **08:30–08:45** ("8:30 to 9" listed as an error) | **08:30–09:00** | Matteo says "8:30 central time and 9 we record the opening range" [00:28:19]. Only S3 uses the 15-minute range. A 15-minute range is narrower, so S2 arms on different days |
| 2 | S3 overnight range **23:00–08:30** | Strategy Matteo backtested used **00:00–08:30** | On the chart: "the overnight range that starts at midnight central time" [01:04:29]. 23:00 is the whiteboard version; both are tested |
| 3 | S3 can enter on the bar right after the OR | His chart entry came **later than the breakout candle**: "we wait like the first one after 9" [01:05:06] | Default: first signal bar closes 09:00; 09:15 and 09:30 tested |
| 4 | S2 "max 1 trade/day (implied)" | **Never stated** | An assumption, labelled as one; 3/day tested |
| 5 | S2 VWAP from midnight | Midnight anchor is only stated for **S1's** chart | S2's own rationale (execution algos) points to the **08:30 session VWAP**; both tested |
| 6 | Silent on S2 exits | "High of past 5 / low of past 20" can be **fixed at entry** or **recalculated every bar** | These are different strategies; both tested |
| 7 | "$800 / $1,500 per contract" | **40 / 75 NQ points** | On 5 MNQ ($2/pt) a dollar stop typed as $1,500 per contract becomes a 750-point stop. Code must use points × BigPointValue |
| 8 | Stops via strategy properties | MultiCharts `SetStopLoss` / `SetProfitTarget` are **per position unless `SetStopContract`** is called | Your own September finding: Kun's stop sat at 750 instead of 1,500 points at 2 MNQ for exactly this reason |
| 9 | Run S1 on a 30-min chart | Without Bar Magnifier MultiCharts guesses the path inside a 30-min bar for a 40-point target | Here every strategy runs on a **1-minute chart**; the 30/15-min signals are built in code |
| 10 | "Single combined signal possible" | MultiCharts holds **one net position per chart**; S1 and S2 are both long NQ | They would net into one position. Run three charts (as Matteo does) or Portfolio Trader |
| 11 | ATR as "15-day MA of daily ATR" via Data2 | Same number as MultiCharts `AvgTrueRange(15)` on daily bars (already a simple average) — fine, but Data2's session template must be **17:00–16:00 CT** | The code here builds the sessions itself, so no Data2 is needed. The double-smoothed reading (average of an ATR(14)) is a sensitivity test |
| 12 | Time zone "Central Time" setting | MultiCharts: Format Instrument → Settings → Time Zone → **Exchange** | Same effect for CME, different menu item |

I have not seen DeepSeek's PowerLanguage code (it wasn't in the message), so I can't confirm
which of 1–10 it carries. The code in `multicharts/` is written from this spec.

---

## Ambiguities — default and the variant that tests the other reading

| Strategy | Question | Default | Variant(s) |
|---|---|---|---|
| S1 | ATR smoothing | simple mean of 15 session true ranges | mean of 15 values of ATR(14) |
| S2 | Exit levels | fixed at the signal bar | recalculated every bar (**S2-v2**) |
| S2 | Trades per day | 1 | 3, each needing a new VWAP touch (**S2-v3**) |
| S2 | Last entry | signal bars closing by 15:00 CT (cash close) | up to 15:54 |
| S2 | VWAP anchor | 00:00 CT | 08:30 CT (**S2-v1**) |
| S3 | Overnight start | 00:00 CT | 23:00, 17:00 (**S3-v1**) |
| S3 | First signal bar | closes 09:00 CT | 09:15, 09:30 |
| all | Early-close days (12:15 halt) | flat at the last bar before the halt | — |

## Execution model (both implementations)

* Signals on bar close, entries **at market on the next bar's open**.
* Stops, targets and time exits are resolved on **1-minute bars**. A minute that touches both
  stop and target counts as a **stop** (conservative; MultiCharts' bar-magnifier ordering is a
  switch). Limit targets fill only when price **trades through** by a tick.
* Costs: **$2.09 per NQ per side** (your MultiCharts setting), **$0.62 per MNQ per side**,
  **1 tick slippage** on every market or stop fill, none on limit fills.

---

## Pre-registered tests (fixed before any run on your real data)

**Split.** In-sample = start of data → 2022-12-31. Out-of-sample = 2023-01-01 → end.
Matches Matteo's own split [00:56:23].

**Improvement candidates** — each is one hypothesis, not a parameter sweep:

| ID | Change | Hypothesis |
|---|---|---|
| S1-v1 | Target/stop in ATR units, calibrated so they equal 40/75 points at the **in-sample median ATR** | NQ roughly tripled in price over the decade; fixed 40/75 points shrink relative to volatility, so the trade shape drifts over time |
| S1-v2 | Time-of-day noise band: barrier = midnight price × (1 + mean of \|close/midnight − 1\| at that same minute over the previous 14 days) | The "noise area" research (Zarattini, Aziz & Barbon 2024) widens the band through the day; a flat 30% of ATR is too loose at 10:00 and too tight at 14:00 |
| S2-v1 | VWAP anchored at 08:30 | Matteo's own reason — execution algorithms benchmark to the regular-session VWAP |
| S2-v2 | Exit levels recalculated each bar | Tests the other reading of the exit rule |
| S2-v3 | Up to 3 trades a day | More trades per day help a time-limited challenge |
| S3-v1 | Overnight range from 17:00 | Overnight price discovery starts when Globex opens, not at midnight |
| S3-v2 | Target 1.5 × stop | Most 3R trades end at 14:30; a nearer target raises the hit rate, which challenges reward |

**Selection rule (in-sample only).** For each strategy, keep the candidate with the highest
in-sample **net ÷ max drawdown** among those with at least 100 in-sample trades; otherwise keep
the faithful version.

**Sizing rule (in-sample only).** Micros per strategy from {0,1,2,3,4,5,6,8,10}, chosen by the
highest **Apex 50K** rolling-start pass rate in-sample.

**Then, once:** the chosen versions and sizes run out-of-sample. Every variant's out-of-sample
numbers are printed too, but the pick is not changed after seeing them.

**Also tested, not selected on:** Matteo's 5/5/5 sizing; each strategy alone at 5 micros (his
"about 40%" claim); the 75th-percentile bench rule walk-forward; fills with bar-magnifier
ordering, limits filling on touch, and double slippage.

**Challenge profiles** (`bench/prop.py`):

| Profile | Target | Trailing DD (EOD) | Daily loss | Other |
|---|---|---|---|---|
| Apex 50K EOD | $3,000 | $2,000 | $1,000 (stop for day) | best day ≤ 50% of profit; 5 days ≥ $250 (as on your 13 Aug sheet) |
| LucidPro 50K | $3,000 | $2,000 | $1,200 | — |
| Generic 50K, 21 days | $3,000 | $2,000 | $1,000 | must pass within 21 trading days (the interview's framing) |

Firm rules change; check them against your own account before trusting a pass rate.
