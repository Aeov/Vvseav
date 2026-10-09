# NQ prop-trio: what the OpenAI math release changes, and what it doesn't

Every one of the 372 results in OpenAI's Oct 6, 2026 release was checked against **prop-trio**: Matteo's three NQ prop-firm strategies, the Python bench, and the MultiCharts code, on branch [`claude/affectionate-planck-8z8kpp`](https://github.com/Aeov/Vvseav/tree/claude/affectionate-planck-8z8kpp/prop-trio). Two passes ran. Five reviewers proposed uses, then five skeptics tried to refute each proposal against the papers and the bench code.

## Bottom line

**No result in the release gives prop-trio a new tool.** Every idea that survived rests on classical statistics, and the new theorems at most prompted the question. The review did surface six checks the bench should run **before you pay for challenges on real data**, listed below by importance. None of them needs the new papers.

Two numbers to keep in mind:

- **A strategy with no edge still passes challenges.** A rough simulation under `bench/prop.py`'s rules (zero-mean daily P&L, 60% of days traded) passed about **12–24% of Apex 50K** challenges, depending on daily volatility. Under the 21-day profile it passed anywhere from **almost 0% to about 24%**. Matteo's "about 40% each" means little until it is compared with that baseline.
- **S1's win rate is mostly set by its bracket.** With no drift, price reaches +40 before −75 points about 75 ÷ 115 ≈ **65%** of the time. Matteo's "about 67% winners" is therefore roughly what random entries would give, so only the **average trade** can show S1's edge.

All checks below are reported as **sensitivities** and do not change the pre-registered selection, except check 1. Check 1 should be written into `SPEC.md` as an amendment **before the first real-data run**, because none has happened yet.

---

## 1. A no-edge baseline for every pass rate (most important)

**Why.** Pass rates and win rates are being compared with Matteo's claims in absolute terms. The bench has no baseline for what a strategy with no edge would score under the same rules.

**What to build** (`bench/null.py`, new; called from `run.run()` after the books; shown by `report.render`):
- **Random-timing copies**, which test the signal's timing. On each real trading day with k trades, enter k times at random from the strategy's own entry opens: S1 at the 30-min opens 10:00–14:00 CT, S2 at the 1-min opens 09:01–15:00, S3 at the 15-min opens 09:00–14:15. Keep each trade's side and its stop and target distances. Resolve exits with `Ctx.exit_bounds`, `engine.resolve_exit` and `engine.make_trade`, using the same costs and fills. Build 200 copies.
- **Sign-flip copies**, which test whether there is any edge at all. Draw one random sign per trading day and apply it to every trade of every strategy that day, which keeps the dependence between strategies. When flipping, recompute `net_mnq` with the swapped exit reason, because a long's limit target becomes a short's stop and pays slippage. Build 200 copies.
- Push every copy through `DayPaths` → `combine` → `rolling` for S1, S2 and S3 alone at 5 micros and for 5/5/5, in-sample and out-of-sample, under the Apex and 21-day profiles. Record win rate and average trade too.

**Metric.** Excess pass rate = real − null median, with p = (1 + number of copies ≥ real) ÷ 201.

**Decision rules** (pre-register now):
1. If a strategy's in-sample Apex pass rate at 5 micros doesn't beat the **95th percentile of its sign-flip null**, it has no demonstrated edge. Don't buy challenges on it alone.
2. If it beats the sign-flip null but not the **random-timing** null, the edge is just "long NQ in that time window". The signal's filters earn nothing.
3. Report every out-of-sample pass rate used to check Matteo's 40% claim next to its null median.
4. Don't print textbook gambler's-ruin "floors". None of them matches a coded profile: all three profiles use an end-of-day trailing drawdown, and the formulas ignore the daily loss limit, consistency rule, qualifying days and day caps.

*Prompted by result [222](EXPLAINED.md#r222) (perceptron capacity). The check itself is an ordinary randomization test.*

## 2. Is the sizing search finding noise?

**Why.** `prop.optimize_sizing` scores 728 micro mixes (the 9 × 9 × 9 grid minus all-zero) by in-sample Apex rolling pass rate and keeps the best one. It does this twice, once for the faithful set and once for the improved set. That is the largest search in the protocol, and nothing corrects for it. The variant pick (3–4 versions per strategy) is small and already protected by the single pre-registered out-of-sample run.

**What to do.**
- **Null ceiling:** run `optimize_sizing` on 50 random-timing copies from check 1, on a coarser grid (0, 2, 5, 8) if runtime demands. If the real optimizer's top in-sample pass rate isn't above the 95th percentile of the null optimizers' tops, treat the book as having no demonstrated edge beyond what the search finds in noise. That includes 5/5/5.
- **Probability of backtest overfitting** (combinatorially symmetric cross-validation, Bailey–Borwein–López de Prado–Zhu): store each mix's pass or fail outcome for every in-sample start day once. Split the start days into 8–16 contiguous blocks, dropping starts whose challenge runs into the other half. Rank mixes on half the blocks and see where the winner lands on the other half. Also compare the chosen mix's out-of-sample pass rate with that of a median-ranked mix.
- If a formal test of the variant pick is wanted, use Hansen's SPA on **mean daily P&L differences** against the faithful version. SPA tests means, not a net-to-drawdown ratio.

*Prompted by results [159](EXPLAINED.md#r159)/[160](EXPLAINED.md#r160). The first draft wrongly framed this as a Ramsey-theory effect; it is plain multiple testing.*

## 3. Bench rule: shuffle whole days, not single trades

**Why.** The bench rule's Monte Carlo (`stats.mc_drawdowns`, called by `stats.bench_mask`) draws single trades independently. S1 in every variant, and S2-v3, can take up to three trades along one day's path, so stops can bunch. Outcomes also drift with volatility regimes over months: S1's 40/75-point exits are fixed while NQ's volatility changed. Shuffling single trades then understates typical drawdowns, and the rule benches healthy strategies too often.

**What to build.** Add `mc_drawdowns_days(day_trades, n_days, sims, block)` in `bench/stats.py`, and a `resample='trade'|'day'|'block5'|'block20'` option on `bench_mask`. Keep `'trade'`, Matteo's literal rule, as the default.
- Draw whole trading days, including no-trade days, either independently or in stationary blocks the way `prop.bootstrap` does.
- Concatenate each drawn day's trades in their original order, and take the **trade-level** drawdown. Summing to daily P&L first would hide intraday dips.

**Diagnostics.**
- Share of S1 days with two or more stops, against what independence predicts.
- Ljung-Box (lags 1–10) on daily P&L and on |daily P&L|, Holm-adjusted across strategies.

**Metric.** R = 75th-percentile drawdown (day or block mode) ÷ 75th-percentile drawdown (trade shuffle), per strategy, on each half of the in-sample period.

**Rule.** If R ≥ 1.10 in both halves, report the day or block version as the main bench variant and keep Matteo's literal version alongside it. Note that a higher threshold means fewer benchings, which is less protection. Either way the bench rule stays "tested, not selected on".

*Prompted by result [007](EXPLAINED.md#r007). Uncorrelated isn't independent; the block bootstrap is standard practice (Künsch 1989; Politis–Romano 1994).*

## 4. Does S3's overnight bias actually carry information?

**Why.** S3's stated edge is "overnight price discovery sets the direction". In code that is only the bias step in `s3_overnight_bias_orb`: the open sits in the top third → long, bottom third → short, middle third → no trade. If the thirds carry no information, then choosing S3-v1, which only changes the bias window, is choosing on noise.

**What to build.** Add `force_side=None|1|-1` to `s3_overnight_bias_orb`. When set, use that side every day, middle third included, and store the third on each trade.
1. Run the breakout forced long and forced short on every day. Unit check: forced-long trades in the top third plus forced-short trades in the bottom third must reproduce faithful S3's trade list exactly.
2. Compute R per trade = net ÷ (stop distance × $20).
3. Statistic D = ½ [mean R(long | top third) − mean R(long | middle + bottom)] + ½ [mean R(short | bottom third) − mean R(short | middle + top)]. Measuring within each side keeps NQ's long drift out.
4. Null: shuffle the day-to-third labels across days within each calendar year, with the same shuffle for both sides, 10,000 times. Use a one-sided p.
5. 90% confidence interval from a 10-day block bootstrap.

**Power is low.** The in-sample standard error is roughly 0.06–0.08 R per trade, so a non-significant result is weak evidence.

**Rule (informational).**
- In-sample CI above 0 and out-of-sample D of the same sign → premise supported.
- All-data CI entirely below 0.05 R → premise rejected. Flag that the S3-v1 vs faithful pick is between equally useless filters.
- Otherwise → "inconclusive".

*Prompted by result [115](EXPLAINED.md#r115). Its new uniform table sampler would be the **wrong** null here; the right one is this label shuffle.*

## 5. Could state-dependent sizing beat fixed micros?

**Why.** Sizing is one fixed mix for the whole challenge. A challenge is a small one-player problem against chance, so ordinary dynamic programming can tell you whether varying size with your cushion could help at all, before you tune any rule.

**What to build.** `dp_screen` in `bench/prop.py`:
- **Actions:** the chosen in-sample mix, ¾ of it and ½ of it, built with `paths.combine(mix, prof.dll)`.
- **States:** balance −$2,000…$5,000 on a $50 grid, peak, cushion, qualifying days 0–5, and days left for the 21-day profile.
- **Method:** value iteration, drawing days independently from the in-sample rows. This ignores the consistency rule, so the Apex result is approximate.

**Metric.** Gap = optimal pass probability − best fixed action's pass probability.

**Rule.**
- If the gap is under 2 points for Apex and Lucid, stop and record "not worth it". Still report the 21-day profile.
- Otherwise test one threshold rule of the shape the DP suggests, such as a smaller mix when cushion < C. Adopt it only if the in-sample Apex rolling and bootstrap pass rates both rise ≥ 3 points without a rise in unresolved challenges, and out-of-sample isn't lower.

**Expect little on Apex and Lucid.** With a positive edge and no day limit, classical theory (Dubins–Savage) favours small size at every cushion. State dependence matters more under the 21-day limit and around Apex's five qualifying days. `rolling()` and `bootstrap()` drop unresolved challenges, so report that share alongside, because smaller size lengthens challenges.

*Prompted by result [104](EXPLAINED.md#r104) (mean-payoff games). Those two-player algorithms aren't needed: this is ordinary dynamic programming.*

## 6. Honest error bars on pass rates

**Why.** `prop.rolling` starts a challenge on every day. Neighbouring starts share most of their days, so the pass rate has far fewer independent observations than starts, and it is reported with no error bar. `prop.bootstrap` uses a mean block of 5 days, which may be too short if outcomes depend on longer regimes.

**What to do.**
- Give the rolling pass rate a Newey–West (HAC) effective sample size and confidence interval.
- Rerun `prop.bootstrap` with mean blocks of 5, 10, 20 and 40 days. If the pass rate moves materially as the block grows, report the longest-block number.

*Prompted by result [145](EXPLAINED.md#r145). That theorem gives no rate and can't set a block length; these classical tools can.*

---

## Considered and dropped

- **Signal selection under the 3-entry cap ([111](EXPLAINED.md#r111), prophet inequalities).** The theorem needs each value to be visible before you decide, and a trade's P&L isn't. Prop-trio's binding limits (one position per chart, a shared daily loss limit) aren't the kind the theorem covers. A "skip the trade if the daily-loss headroom is too small" gate would be a new, non-pre-registered rule with an unclear effect. One generic report line is still worth adding: how often the daily loss limit cuts a day short at the chosen mix, and how often S3's dollar stop at the chosen micros exceeds the limit.
- **Everything else.** Each result's entry in [EXPLAINED.md](EXPLAINED.md) says why it has no trading use. The most common reasons:
  - The speed-ups are galactic.
  - The theorem assumes independent coin-flip inputs, log-concave shapes or sparse random graphs that markets don't have.
  - The useful part was already classical.

## BTC

Nothing here is specific to BTC. Two notes carry over:
- If you ever build a **multivariate** scenario map with optimal transport (for example, joint BTC/NQ daily returns), refit it on resampled data and measure how much the scenarios move. Result [374](EXPLAINED.md#r374) shows such maps can be far less stable than the data in the worst case.
- Result [279](EXPLAINED.md#r279) (exact quantum factoring) is **not** a new threat to Bitcoin's keys.

## Running it

`prop-trio` has no real-data results yet. The bench reads the NQ 1-minute export from `Desktop\NQ Section` on your laptop; see that branch's [README](https://github.com/Aeov/Vvseav/blob/claude/affectionate-planck-8z8kpp/prop-trio/README.md). These checks can be added to the bench on the same branch and run on that data by a Claude session on the laptop.
