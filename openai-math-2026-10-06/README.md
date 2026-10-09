# OpenAI's October 6, 2026 math release, explained

On **October 6, 2026**, OpenAI published [`openai/math`](https://github.com/openai/math): mathematical manuscripts written by an unreleased internal model, with Lean formal proofs for some of them. This folder explains **every result in plain language**, and checks each one for real uses in **quant trading** and in **Politeia**, our citizen UI.

| File | What it is |
|---|---|
| [`EXPLAINED.md`](EXPLAINED.md) | All 372 results, one plain-language entry each, grouped by subject, with links to every paper |
| [`results.csv`](results.csv) | The same data in a table (filter by subject, Lean status, quant rating, Politeia rating) |
| [`NQ-PROP-TRIO.md`](NQ-PROP-TRIO.md) | What the release means for your NQ prop-firm strategies: six concrete checks for the prop-trio bench |

## "377 problems": what the numbers actually are

| Count | Meaning |
|---|---|
| **377** | The highest catalogue number. Numbers **045, 061, 070, 123 and 163 are unused**, so there are… |
| **372** | …result families: one main theorem, plus companion and follow-up papers. This guide covers all 372. |
| **722** | Manuscripts in the original Oct 6 release. |
| **719** | Manuscripts now. On Oct 7 OpenAI **withdrew 3** (a sign error in the K3 and abelian-eightfold companions of result [032](EXPLAINED.md#r032)) and **repaired 14** others. |
| **235 → 242** | Families with a Lean formalization page, at release and after the Oct 7 update. OpenAI counts 300 of 719 manuscripts (about 42%) as having their top-line result formalized. |
| **~4,000** | Problems the model was given in total. OpenAI kept the results it judged significant, using about 3 hours of ChatGPT Pro thinking per result on average. |

## How much to trust it

- **Nothing here is peer reviewed.** Read each entry as "OpenAI's model claims to prove…".
- **📐 Lean-checked** means a computer verified a formal version of the main statement. Each Lean page lists exactly what is covered, and side results are often left out (for example, [017](EXPLAINED.md#r017) checks the π exponent but not the Flint Hills series).
- **Not formally verified** means only a model-written proof exists. Within a day of release, a sign error broke the proofs in 3 such papers (now withdrawn) and 14 others needed repairs. Expect more corrections.
- OpenAI says results [003](EXPLAINED.md#r003) (zeta zero-free region) and [032](EXPLAINED.md#r032) (Hodge for CM abelian varieties) were **not** produced by its standard fixed procedure, and that the 11/12 zeta write-up was edited by humans.
- Some headline claims, if they hold up, would be among the biggest results of the century: the Unique Games Conjecture, a 7/8 zero-free region for ζ, Hadwiger's conjecture being false, Hilbert's 10th problem over ℚ. Treat them with matching caution until experts weigh in.

## Bottom line

**This is overwhelmingly pure mathematics.** Of 372 results:

| | 🟢 Testable idea | 🟡 Background | ⚪ No practical link |
|---|---:|---:|---:|
| **Quant trading** | 0 | 14 | 358 |
| **Politeia** | 2 | 20 | 350 |

None of these theorems is a trading edge by itself. For your NQ work, the value is in the classical checks they prompted (below).

## Quant trading: what's actually useful

**Short answer: nothing in the release is a new trading tool.** Every result was checked against your actual NQ setup, `prop-trio`: Matteo's three strategies, the challenge simulator and the pre-registered test plan. That check ran in two passes. Five reviewers proposed uses, then five skeptics tried to refute each one against the papers and the bench code. No proposal survived as "testable", and 20 of my first-draft quant notes were corrected or downgraded (see [How this was checked](#how-this-was-checked)).

The review did surface **six classical checks the prop-trio bench should run before you pay for challenges on real data**. They are written up as concrete bench changes in **[NQ-PROP-TRIO.md](NQ-PROP-TRIO.md)**:

1. **A no-edge baseline for every pass rate.** A zero-edge book still passes roughly 12–24% of Apex challenges, and S1's +40/−75 bracket alone produces about 65% winners from random entries. Matteo's "40% pass" and "67% winners" mean little until compared with that.
2. **Is the 728-mix sizing search finding noise?** Use a null-optimizer ceiling and a probability-of-backtest-overfitting check.
3. **Bench rule:** resample whole days, not single trades, because S1 can take three trades on one path.
4. **Does S3's overnight bias carry information?** Run a permutation test of the thirds.
5. **Could state-dependent sizing help?** Answer it with a dynamic-programming screen before tuning any rule.
6. **Honest error bars on pass rates.** Overlapping start days are not independent.

**🟡 Background worth knowing** (each entry says exactly what is new and what was already classical):

- **Overfitting capacity ([222](EXPLAINED.md#r222)).** A linear rule with N weights can fit about 2N random labels (Cover 1965). These papers sharpen the theory but don't change that rule.
- **Uncorrelated ≠ independent ([007](EXPLAINED.md#r007)).** This is why the bench rule's single-trade shuffle needs checking.
- **Pattern-vs-regime tests ([115](EXPLAINED.md#r115)).** The new uniform table sampler is the *wrong* null; shuffle the labels instead.
- **Optimal-transport scenario maps can be unstable ([374](EXPLAINED.md#r374)).** This only bites in two or more dimensions, for example joint BTC/NQ scenario maps.
- **Long/short book splitting is Max-Cut ([102](EXPLAINED.md#r102)).** Goemans–Williamson rounding is now provably the best general method (unless P = NP).
- Also: [097](EXPLAINED.md#r097), [104](EXPLAINED.md#r104), [111](EXPLAINED.md#r111), [117](EXPLAINED.md#r117), [121](EXPLAINED.md#r121), [125](EXPLAINED.md#r125), [229](EXPLAINED.md#r229), [279](EXPLAINED.md#r279), [281](EXPLAINED.md#r281).

**Looks useful, isn't (yet)**

- Faster matrix multiplication ([107](EXPLAINED.md#r107)), integer multiplication ([109](EXPLAINED.md#r109)) and FFT ([130](EXPLAINED.md#r130)) are "galactic": the speed-up only appears at astronomically large sizes. Your covariance or FFT code will not get faster.
- Quantum optimization ([281](EXPLAINED.md#r281)) matches a spin-glass optimum only in an asymptotic limit. It is no evidence for quantum portfolio optimization.
- Exact quantum factoring ([279](EXPLAINED.md#r279)) is not a new threat to BTC. It concerns RSA-style factoring, and Shor's algorithm already broke both RSA and elliptic-curve keys in theory. The practical risk timeline still depends on quantum hardware.

## Politeia: what's actually useful

> **Note:** I couldn't open the Politeia Atlas UI files from this session. They aren't in the one connected repo (`Aeov/Vvseav`) or in your claude.ai artifacts. So these notes target the features a citizen platform like Politeia typically has: a **map/atlas** of services, **proposals and voting**, **budgets and priorities**, **community discussion networks**, and **privacy of citizen data**. Share the repo or link and I'll tie each idea to specific screens.

**🟢 Worth building**

1. **"Where should the next k services go?" on the map ([125](EXPLAINED.md#r125)).** This is k-median facility location; ≈1.74× optimal is now the proven best possible guarantee. Use a standard local-search or integer-programming solver, and show citizens the total and average travel distance for each candidate plan side by side.
2. **Privacy-safe and auditable tables ([115](EXPLAINED.md#r115)).** Publish synthetic district × group tables that match every official total exactly but contain no real records. Run the same machinery as an audit: "is this district × option table surprising given its totals?"

**🟡 Good framing for explainers and design choices**

- **"How much does my vote matter?" ([127](EXPLAINED.md#r127)).** In any weighted vote over n people, on average at most about 8√n are pivotal, so one person's chance of being decisive is roughly 1/√n or less. A crisp, honest civic-education fact.
- **One-number summaries lose information ([119](EXPLAINED.md#r119)).** Majority is the most stable summary, but not the most informative. Show distributions, not just the winner.
- **Don't over-claim communities ([229](EXPLAINED.md#r229), [131](EXPLAINED.md#r131), [117](EXPLAINED.md#r117), [102](EXPLAINED.md#r102)).** Check the detection threshold and a rewired-network baseline before labelling "camps" or "influencers".
- **Fair random pairing and matching ([113](EXPLAINED.md#r113), [120](EXPLAINED.md#r120)).** Deliberation pairs, volunteers to tasks, residents to slots.
- **Map and network visuals ([090](EXPLAINED.md#r090), [165](EXPLAINED.md#r165), [089](EXPLAINED.md#r089)).** Hexagon bins are provably the most even spatial tiling. Dense networks should be drawn as matrices rather than node-link diagrams. Planar road networks support bottleneck analysis.
- **Allocation and operations ([097](EXPLAINED.md#r097), [111](EXPLAINED.md#r111), [138](EXPLAINED.md#r138), [110](EXPLAINED.md#r110)).** Keep running allocations balanced across districts, set rolling-approval thresholds from last cycle's data, size budget selection correctly, and dispatch mobile services.
- **Rollouts and networks ([186](EXPLAINED.md#r186), [178](EXPLAINED.md#r178)).** Participation features tip sharply rather than growing linearly. Ramanujan graphs are the best design for sparse delegate or communication networks.
- **Security ([238](EXPLAINED.md#r238), [279](EXPLAINED.md#r279)).** Format-preserving pseudonymisation of IDs (use a vetted standard), and no new quantum threat beyond the normal post-quantum migration.
- **Data claims ([159](EXPLAINED.md#r159)).** Big civic datasets always contain striking patterns, so add a "could this be chance?" check before highlighting one.

## Headline results (if they hold up)

| # | Claim | Lean |
|---|---|:-:|
| [002](EXPLAINED.md#r002) / [006](EXPLAINED.md#r006) | Full Birch–Swinnerton-Dyer formula in ranks 0 and 1; Goldfeld's conjecture (half of twists rank 0, half rank 1) | |
| [003](EXPLAINED.md#r003) | No zeta or Dirichlet L-function zeros with Re s > 7/8; no Landau–Siegel zeros | 📐 |
| [004](EXPLAINED.md#r004) | Hilbert's 10th problem over the rationals is undecidable | |
| [005](EXPLAINED.md#r005) / [017](EXPLAINED.md#r017) | Catalan's constant is irrational; π's irrationality exponent is 2 | 📐 |
| [029](EXPLAINED.md#r029) | Artin's primitive root conjecture, unconditionally | |
| [032](EXPLAINED.md#r032) | Hodge conjecture for CM abelian varieties (3 companion papers withdrawn) | |
| [038](EXPLAINED.md#r038) / [039](EXPLAINED.md#r039) | Fujita's freeness conjecture; Nagata's conjecture | 39: 📐 |
| [102](EXPLAINED.md#r102) | The Unique Games Conjecture | 📐 |
| [103](EXPLAINED.md#r103) | L = BPL (randomness doesn't help low-memory computation) | 📐 |
| [107](EXPLAINED.md#r107) | Matrix multiplication exponent ω ≤ 9/4 | 📐 |
| [143](EXPLAINED.md#r143) | Hilbert's 16th problem: limit cycles bounded by degree | 📐 |
| [157](EXPLAINED.md#r157) / [158](EXPLAINED.md#r158) | Hadwiger's conjecture is false; the plane needs at least 6 colours | 📐 |
| [159](EXPLAINED.md#r159) | Erdős's conjecture on arithmetic progressions | 📐 |
| [196](EXPLAINED.md#r196) / [197](EXPLAINED.md#r197) | Kaplansky's zero-divisor and direct-finiteness conjectures are false; non-sofic groups exist | 📐 |
| [213](EXPLAINED.md#r213) | No percolation at criticality on ℤ³ | 📐 |
| [246](EXPLAINED.md#r246) / [248](EXPLAINED.md#r248) | Cannon's conjecture; Thompson's group F is non-amenable | 📐 |
| [267](EXPLAINED.md#r267) / [271](EXPLAINED.md#r271) | Bose–Einstein condensation at positive temperature; spontaneous magnetization of the quantum Heisenberg ferromagnet | 📐 |
| [287](EXPLAINED.md#r287) / [288](EXPLAINED.md#r288) | Free group factors are isomorphic; Kadison's similarity problem | 📐 |
| [304](EXPLAINED.md#r304) / [320](EXPLAINED.md#r320) | Hilbert–Smith conjecture; the Borel conjecture fails in dimension 4 | |
| [325](EXPLAINED.md#r325) | Crouzeix's conjecture (constant 2) | 📐 |
| [362](EXPLAINED.md#r362) | Global smooth solutions of relativistic Vlasov–Maxwell | 📐 |

## Results by subject

| Subject | Results | Lean pages |
|---|---:|---:|
| Number theory | 31 | 17 |
| Algebraic and complex geometry | 36 | 8 |
| Real and complex analysis | 16 | 10 |
| Convex and metric geometry | 15 | 13 |
| Theoretical computer science | 40 | 34 |
| Dynamical systems and ergodic theory | 12 | 9 |
| Combinatorics | 37 | 33 |
| Algebra | 18 | 10 |
| Probability and statistical mechanics | 29 | 19 |
| Mathematical logic | 6 | 6 |
| Group theory | 14 | 12 |
| Mathematical physics | 25 | 17 |
| Operator algebras | 19 | 15 |
| Topology | 18 | 3 |
| Functional analysis | 11 | 10 |
| Differential geometry | 29 | 15 |
| Partial differential equations | 16 | 11 |
| **Total** | **372** | **242** |

## Sources

- [openai/math](https://github.com/openai/math): README, [CONTENTS.md](https://github.com/openai/math/blob/main/CONTENTS.md), [overview.pdf](https://github.com/openai/math/blob/main/overview.pdf), [history.md](https://github.com/openai/math/blob/main/history.md) and [lean/docs](https://github.com/openai/math/tree/main/lean/docs). The initial commit `adc7f12` (Oct 6, 2026) and update `fd4aeeb` (Oct 7, 2026) were both read in full for this guide.
- News coverage of the release: [WinBuzzer](https://winbuzzer.com/2026/10/09/openai-shares-hundreds-of-math-results-from-an-unreleased-ai-xcxwbn/), [Unite.ai](https://www.unite.ai/openai-releases-722-math-manuscripts-from-an-unreleased-ai-model/).
