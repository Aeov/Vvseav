# OpenAI's October 6, 2026 math release: every result, explained simply

A plain-language guide to all **372 result families** in OpenAI's public [`openai/math`](https://github.com/openai/math) collection (catalogue numbers 001–377; 045, 061, 070, 123 and 163 are unused). Each entry says what was claimed, then whether it has any use for **quant trading** or for **Politeia**, our citizen UI. See the [README](README.md) for the summary, the best ideas, and caveats.

> **Treat every entry as a claim, not a settled fact.** None of this has been peer reviewed. "Lean" means a formal statement of the main result was machine-checked (each Lean page says exactly what it covers). Everything else is a model-written proof. OpenAI withdrew 3 papers and repaired 14 within a day of release.

**How to read the ratings**

| Rating | Meaning |
|---|---|
| 🟢 Testable idea | A concrete experiment or feature you could build or backtest now |
| 🟡 Background | A real connection that sharpens thinking or flags a pitfall; nothing to plug in directly |
| ⚪ No practical link | Pure mathematics; no honest use for trading or civic UI |

## Contents

| Subject | Results | Quant 🟢/🟡 | Politeia 🟢/🟡 |
|---|---:|---:|---:|
| [Number theory](#s-number-theory) (001–031) | 31 | 0/1 | 0/0 |
| [Algebraic and complex geometry](#s-algebraic-and-complex-geometry) (032–069) | 36 | 0/0 | 0/0 |
| [Real and complex analysis](#s-real-and-complex-analysis) (071–086) | 16 | 0/0 | 0/0 |
| [Convex and metric geometry](#s-convex-and-metric-geometry) (087–101) | 15 | 0/1 | 0/3 |
| [Theoretical computer science](#s-theoretical-computer-science) (102–142) | 40 | 0/7 | 2/10 |
| [Dynamical systems and ergodic theory](#s-dynamical-systems-and-ergodic-theory) (143–154) | 12 | 0/0 | 0/0 |
| [Combinatorics](#s-combinatorics) (155–192) | 37 | 0/0 | 0/4 |
| [Algebra](#s-algebra) (193–210) | 18 | 0/0 | 0/0 |
| [Probability and statistical mechanics](#s-probability-and-statistical-mechanics) (211–239) | 29 | 0/2 | 0/2 |
| [Mathematical logic](#s-mathematical-logic) (240–245) | 6 | 0/0 | 0/0 |
| [Group theory](#s-group-theory) (246–259) | 14 | 0/0 | 0/0 |
| [Mathematical physics](#s-mathematical-physics) (260–284) | 25 | 0/2 | 0/1 |
| [Operator algebras](#s-operator-algebras) (285–303) | 19 | 0/0 | 0/0 |
| [Topology](#s-topology) (304–321) | 18 | 0/0 | 0/0 |
| [Functional analysis](#s-functional-analysis) (322–332) | 11 | 0/0 | 0/0 |
| [Differential geometry](#s-differential-geometry) (333–361) | 29 | 0/0 | 0/0 |
| [Partial differential equations](#s-partial-differential-equations) (362–377) | 16 | 0/1 | 0/0 |

<a name="s-number-theory"></a>

## Number theory

<a name="r001"></a>

### 001 · Milne’s rationality conjecture and algebraic specialization

Not formally verified · 1 paper

Abelian varieties are higher-dimensional cousins of the doughnut, cut out by polynomial equations. They carry special "Hodge classes" that should come from real algebraic shapes inside them. Milne predicted that if you reduce the equations modulo a prime and measure these classes with any of the standard measuring tools (cohomology theories), you always get the same rational number. This proves it, and with result [032](#r032) shows each such class is one genuine algebraic shape in all those settings at once.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Milne's rationality conjecture for abelian varieties](https://github.com/openai/math/blob/main/preprints/Milnes-rationality-conjecture-for-abelian-varieties-October-7-2026/paper.pdf)

</details>

<a name="r002"></a>

### 002 · The full BSD formula from low Selmer corank

Not formally verified · 3 papers

Elliptic curves are equations like y² = x³ + ax + b. The Birch–Swinnerton-Dyer (BSD) conjecture, a Millennium Prize problem, predicts how many rational solutions a curve has (its "rank") and gives an exact formula linking them to an L-function. This proves the full exact formula whenever a computable approximation (the Selmer group) says the rank is 0 or 1, and, with result [006](#r006), for "almost all" twisted versions of every curve. Bonus: every prime ℓ ≡ 4, 7, 8 (mod 9) is a sum of two rational cubes (Sylvester's old question). Ranks 2 and higher are not covered, so the Millennium problem itself is still open.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Exact Birch–Swinnerton-Dyer Formula from Low Selmer Corank](https://github.com/openai/math/blob/main/preprints/Exact-Birch-Swinnerton-Dyer-Formula-from-Low-Selmer-Corank-October-7-2026/exact-bsd-low-selmer-corank.pdf)
- [The Selmer converse for elliptic curves at every prime](https://github.com/openai/math/blob/main/preprints/The-Selmer-converse-for-elliptic-curves-at-every-prime-October-7-2026/main.pdf)
- [The two-primary Birch–Swinnerton-Dyer formula in Selmer corank at most one](https://github.com/openai/math/blob/main/preprints/The-two-primary-Birch-Swinnerton-Dyer-formula-in-Selmer-corank-at-most-one-October-6-2026/paper.pdf)

</details>

<a name="r003"></a>

### 003 · The quasi-Riemann hypothesis

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/003.md) · 3 papers · produced outside OpenAI's standard procedure

The Riemann Hypothesis says the important zeros of the zeta function all lie on the line Re s = 1/2. Until now nobody could even prove that a strip like Re s > 0.99 is free of zeros. This claims no zero has real part above 7/8 (for zeta and every Dirichlet L-function), which would sharply improve how precisely we can count primes. It also rules out "Landau–Siegel zeros", a long-feared kind of exceptional zero. Not the full Riemann Hypothesis, but by far the largest step toward it. OpenAI says this work did not follow its standard fixed procedure, and the 11/12 write-up was edited by humans.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane $`\Re s\gt 7/8`$ ](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf)
- [The Quasi-Riemann Hypothesis (alternate 11/12 proof)](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-October-5-2026/paper2.pdf)
- [Uniform exclusion of Landau–Siegel zeros](https://github.com/openai/math/blob/main/preprints/Uniform-exclusion-of-Landau-Siegel-zeros-October-1-2026/paper.pdf)

</details>

<a name="r004"></a>

### 004 · Hilbert’s tenth problem over ℚ

Not formally verified · 2 papers

Hilbert's 10th problem asked for an algorithm that decides whether a polynomial equation has whole-number solutions; in 1970 that was shown to be impossible. The same question for fractions (rational solutions) stayed open for over 50 years. This proves no such algorithm exists for rational solutions either.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Hilbert’s tenth problem over the rational numbers](https://github.com/openai/math/blob/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026/main.pdf)
- [A pointwise 2-converse for elliptic curves with rational two-torsion](https://github.com/openai/math/blob/main/preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-October-7-2026/paper.pdf)

</details>

<a name="r005"></a>

### 005 · Irrationality of Catalan’s constant

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/005.md) · 1 paper

Catalan's constant G = 1 − 1/9 + 1/25 − 1/49 + … ≈ 0.91597. This proves G is irrational (not a fraction), a famous open question about one of the most natural constants in analysis.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Catalan's constant is irrational](https://github.com/openai/math/blob/main/preprints/Catalans-constant-is-irrational-September-24-2026/paper.pdf)

</details>

<a name="r006"></a>

### 006 · Goldfeld’s conjecture: densities and mean analytic rank

Not formally verified · 2 papers

Take one elliptic curve and "twist" it by every square-free number d. Goldfeld conjectured that half of the twists have rank 0, half have rank 1, and higher ranks are negligible, so the average rank is 1/2. This proves it for every elliptic curve over the rationals.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Goldfeld's analytic density conjecture and the 2-converse for elliptic curves](https://github.com/openai/math/blob/main/preprints/Goldfelds-analytic-density-conjecture-and-the-2-converse-for-elliptic-curves-October-7-2026/paper.pdf)
- [The mean analytic rank of quadratic twists of elliptic curves](https://github.com/openai/math/blob/main/preprints/The-mean-analytic-rank-of-quadratic-twists-of-elliptic-curves-October-6-2026/paper.pdf)

</details>

<a name="r007"></a>

### 007 · Ordinary two-point correlations and the corrected Elliott conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/007.md) · 1 paper · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/ordinary-two-point-correlations.pdf)

The Liouville function λ(n) is +1 or −1 depending on whether n has an even or odd number of prime factors, and it is believed to behave like fair coin flips. Chowla's conjecture says it has no correlations: knowing λ(n) tells you nothing about λ(n+h). This proves the two-point version (pairs of values) with an explicit rate, and a more general version for other multiplicative functions.

- **Quant trading:** 🟡 *Background.* The trading lesson is classical, not new: a lag-correlation test can show outcomes are uncorrelated, not that they are independent (volatility clustering is the standard counterexample). The theorem itself covers only pairs of values of one deterministic number-theory sequence. In prop-trio this matters for the bench rule, whose Monte Carlo shuffles single trades as if they were independent; see check 3 in the [NQ playbook](NQ-PROP-TRIO.md).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Ordinary two-point correlations of multiplicative functions](https://github.com/openai/math/blob/main/preprints/Ordinary-two-point-correlations-of-multiplicative-functions-September-24-2026/final.pdf)

</details>

<a name="r008"></a>

### 008 · The Deligne–Drinfeld conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/008.md) · 1 paper

The Grothendieck–Teichmüller Lie algebra is a symmetry structure tied to multiple zeta values, the sums that link number theory, knot theory and quantum algebra. Deligne and Drinfeld predicted it is "free", with exactly one building block in each odd weight 3, 5, 7, …. This proves it, giving a clean description of a central object.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Deligne-Drinfeld conjecture](https://github.com/openai/math/blob/main/preprints/The-Deligne-Drinfeld-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r009"></a>

### 009 · Function-field reconstruction from Milnor K-theory and Galois data

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/009.md) · 3 papers

A field of functions in two or more variables can be rebuilt completely from a small algebraic "fingerprint": its Milnor K-theory mod ℓ, or certain Galois-symmetry data (Bogomolov–Pop). It is like reconstructing an object from a few of its shadows.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Reconstruction of Function Fields from Mod-ℓ Milnor K-Theory](https://github.com/openai/math/blob/main/preprints/Reconstruction-of-Function-Fields-from-Mod-ell-Milnor-K-Theory-October-5-2026/mod-ell-bogomolov-pop.pdf)
- [Reconstruction from Milnor K-theory modulo the characteristic](https://github.com/openai/math/blob/main/preprints/Reconstruction-from-Milnor-K-theory-modulo-the-characteristic-October-5-2026/paper.pdf)
- [The Bogomolov-Pop reconstruction theorem](https://github.com/openai/math/blob/main/preprints/The-Bogomolov-Pop-reconstruction-theorem-September-23-2026/paper.pdf)

</details>

<a name="r010"></a>

### 010 · Unrestricted pro-modularity at the prime two

Not formally verified · 3 papers

Galois representations encode the hidden symmetries of solutions to polynomial equations. "Modularity" means they come from modular forms, which are extremely symmetric functions; this is the bridge used to prove Fermat's Last Theorem. The prime 2 has always been the hardest case. This proves every suitable 2-adic two-dimensional representation is (pro-)modular, and the 2-adic Fontaine–Mazur conjecture without the usual extra conditions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Unrestricted pro-modularity at the prime two](https://github.com/openai/math/blob/main/preprints/Unrestricted-pro-modularity-at-the-prime-two-October-6-2026/two-adic-promodularity.pdf)
- [The Dimension of the Two-Adic Hecke Algebra at Odd Level](https://github.com/openai/math/blob/main/preprints/The-Dimension-of-the-Two-Adic-Hecke-Algebra-at-Odd-Level-October-5-2026/two-adic-hecke.pdf)
- [Fontaine–Mazur modularity at the prime 2](https://github.com/openai/math/blob/main/preprints/Fontaine-Mazur-modularity-at-the-prime-2-October-6-2026/paper.pdf)

</details>

<a name="r011"></a>

### 011 · Prime-factor statistics of $`p-1`$

Not formally verified · 3 papers

Take a random prime p and look at the prime factors of p − 1. This proves their relative sizes follow the same random "stick-breaking" law (Poisson–Dirichlet) as the factors of a random whole number, settling the Ford–Konyagin–Luca conjecture. It also shows that some numbers are the totient φ(m) of more than n^(1−ε) different integers m.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Weighted dilation graphs, smooth shifted primes and totient fibers](https://github.com/openai/math/blob/main/preprints/Weighted-Dilation-Graphs-Smooth-Shifted-Primes-and-Totient-Fibers-September-24-2026/paper.pdf)
- [The Poisson-Dirichlet law for prime predecessors](https://github.com/openai/math/blob/main/preprints/The-Poisson-Dirichlet-Law-for-Prime-Predecessors-September-24-2026/paper.pdf)
- [Prime Predecessors with an Even Number of Prime Factors](https://github.com/openai/math/blob/main/preprints/Prime-Predecessors-with-an-Even-Number-of-Prime-Factors-September-17-2026/paper.pdf)

</details>

<a name="r012"></a>

### 012 · Independent largest prime factors of consecutive integers

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/012.md) · 1 paper

Erdős and Pomerance asked whether the largest prime factors of n and n + 1 are independent of each other. This proves they are in the limit, so the largest prime factor of n + 1 is bigger than that of n exactly half the time.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The joint Dickman law for consecutive integers](https://github.com/openai/math/blob/main/preprints/The-joint-Dickman-law-for-consecutive-integers-September-24-2026/paper.pdf)

</details>

<a name="r013"></a>

### 013 · Ostmann’s inverse Goldbach conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/013.md) · 1 paper

Could the primes, after changing finitely many of them, be written as all sums a + b from two sets A and B that each have at least two elements? Ostmann conjectured not. This proves the primes are "additively indecomposable".

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The additive indecomposability of the primes](https://github.com/openai/math/blob/main/preprints/the-additive-indecomposability-of-the-primes-September-24-2026/paper.pdf)

</details>

<a name="r014"></a>

### 014 · Restricted geometric Langlands, global Arthur enhancements, and generic Ramanujan

Not formally verified · 8 papers

Geometric Langlands is a grand dictionary linking geometry over curves to representation theory. This family proves the "restricted" version over curves in positive characteristic (under stated conditions), proves Ramanujan-type bounds (eigenvalues as small as theory allows) for certain automorphic forms over function fields, and builds "Arthur enhancements" assuming a stated decomposition. With 8 papers it is one of the largest families.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (8)</summary>

- [Global Arthur Enhancements of Cuspidal Excursion Parameters](https://github.com/openai/math/blob/main/preprints/Global-Arthur-Enhancements-of-Cuspidal-Excursion-Parameters-October-5-2026/manuscript.pdf)
- [Rationality of the Canonical Unramified Arthur Filtration](https://github.com/openai/math/blob/main/preprints/Rationality-of-the-Canonical-Unramified-Arthur-Filtration-September-24-2026/paper.pdf)
- [Ramanujan-Arthur Decompositions of Cuspidal Functions at Full Finite Level](https://github.com/openai/math/blob/main/preprints/Ramanujan-Arthur-Decompositions-of-Cuspidal-Functions-at-Full-Finite-Level-September-24-2026/paper.pdf)
- [Temperedness at ramified places for globally generic exceptional groups](https://github.com/openai/math/blob/main/preprints/Temperedness-at-ramified-places-for-globally-generic-exceptional-groups-October-5-2026/ramified-ramanujan.pdf)
- [The Restricted Geometric Langlands Equivalence in Positive Characteristic](https://github.com/openai/math/blob/main/preprints/The-Restricted-Geometric-Langlands-Equivalence-in-Positive-Characteristic-September-24-2026/paper.pdf)
- [Constructible tame Hecke eigensheaves in positive characteristic](https://github.com/openai/math/blob/main/preprints/Constructible-tame-Hecke-eigensheaves-in-positive-characteristic-October-5-2026/constructible-tame-hecke-eigensheaves-positive-characteristic.pdf)
- [Tame Hecke Eigensheaves with Several Marked Points](https://github.com/openai/math/blob/main/preprints/Tame-Hecke-Eigensheaves-with-Several-Marked-Points-October-5-2026/Tame-Hecke-Eigensheaves-with-Several-Marked-Points.pdf)
- [Frobenius Structures on Tame Hecke Eigensheaves](https://github.com/openai/math/blob/main/preprints/Frobenius-Structures-on-Tame-Hecke-Eigensheaves-October-5-2026/tame-hecke-frobenius.pdf)

</details>

<a name="r015"></a>

### 015 · Torus-packet equidistribution in prime, quartic, and sextic degrees

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/015.md) · 3 papers

Certain arithmetic orbits ("torus packets") built from number fields are shown to spread out perfectly evenly in their space as the field grows, with no mass escaping to infinity. This covers prime degree at least five, and quartic and sextic fields.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Equidistribution of Prime-Degree Torus Packets with Arbitrary Local Type](https://github.com/openai/math/blob/main/preprints/Equidistribution-of-Prime-Degree-Torus-Packets-with-Arbitrary-Local-Type-September-24-2026/paper.pdf)
- [Equidistribution of primitive quartic torus packets for arbitrary orders](https://github.com/openai/math/blob/main/preprints/Equidistribution-of-Primitive-Quartic-Torus-Packets-for-Arbitrary-Orders-October-5-2026/quartic-torus-packets.pdf)
- [Equidistribution of Primitive Sextic Torus Packets](https://github.com/openai/math/blob/main/preprints/Equidistribution-of-Primitive-Sextic-Torus-Packets-October-5-2026/primitive-sextic-torus-packets.pdf)

</details>

<a name="r016"></a>

### 016 · Zilber–Pink in abelian varieties and the Siegel threefold

Not formally verified · 4 papers

Zilber–Pink is about "unlikely intersections": a shape should meet special sub-shapes more often than dimension-counting predicts only in finitely many structured ways. This proves the full abelian-variety version over algebraic numbers, and the curve case in the Siegel modular threefold A₂.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [The abelian Zilber–Pink conjecture](https://github.com/openai/math/blob/main/preprints/The-Abelian-Zilber-Pink-Conjecture-September-24-2026/paper.pdf)
- [The E×CM component of Zilber–Pink for curves in A2](https://github.com/openai/math/blob/main/preprints/The-E-times-CM-Component-of-Zilber-Pink-for-Curves-in-A2-September-24-2026/paper.pdf)
- [Quaternionic division points on curves in the Siegel threefold](https://github.com/openai/math/blob/main/preprints/Quaternionic-Division-Points-on-Curves-in-the-Siegel-Threefold-September-24-2026/paper.pdf)
- [Elliptic squares and Zilber–Pink for curves in A2](https://github.com/openai/math/blob/main/preprints/Elliptic-Squares-and-Zilber-Pink-for-Curves-in-A2-September-24-2026/paper.pdf)

</details>

<a name="r017"></a>

### 017 · The irrationality exponent of <i>π</i> is 2

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/017.md) · 1 paper · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/irrationality-exponent-of-pi.pdf)

How well can π be approximated by fractions? This proves "no better than a typical number": for any ε > 0, |π − p/q| ≥ q^(−2−ε) once q is large. It also proves that the Flint Hills series Σ 1/(n³ sin² n) converges, a notorious open problem. The Lean check covers the exponent statement but not the series.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The irrationality exponent of pi is 2](https://github.com/openai/math/blob/main/preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/paper.pdf)

</details>

<a name="r018"></a>

### 018 · The Margulis–Platonov conjecture over global fields

Not formally verified · 2 papers

For arithmetic groups (for example matrix groups over number fields), the Margulis–Platonov conjecture describes all of their normal subgroups: they are controlled by finitely many local pieces. This proves it over every global field, including characteristic-2 function fields.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The Margulis–Platonov conjecture over global function fields](https://github.com/openai/math/blob/main/preprints/The-Margulis-Platonov-conjecture-over-global-function-fields-October-5-2026/margulis-platonov-global-function-fields.pdf)
- [The Margulis–Platonov conjecture over number fields](https://github.com/openai/math/blob/main/preprints/The-Margulis-Platonov-conjecture-over-number-fields-September-23-2026/paper.pdf)

</details>

<a name="r019"></a>

### 019 · The local <i>p</i>-adic section conjecture and global consequences

Not formally verified · 2 papers

Grothendieck's section conjecture says the rational points on a curve of genus at least two can be read off from the symmetries of its fundamental group. This proves the local p-adic version for all such curves, and the global version over ℚ for the modular curves X₀(N) and X₁(N).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Étale covers with a prescribed exterior sheet](https://github.com/openai/math/blob/main/preprints/Etale-covers-with-a-prescribed-exterior-sheet-September-24-2026/main.pdf)
- [The p-adic section conjecture](https://github.com/openai/math/blob/main/preprints/The-p-adic-section-conjecture-October-6-2026/main.pdf)

</details>

<a name="r020"></a>

### 020 · Squarefree quartics and power-free polynomial values

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/020.md) · 1 paper

For an irreducible degree-4 polynomial f with integer coefficients, how often is f(n) squarefree (not divisible by any square bigger than 1)? This proves it happens with exactly the predicted positive frequency. Similar results hold up to degree 8, so with earlier work every degree from 4 up is now covered.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Squarefree values of quartics and power-free values of polynomials](https://github.com/openai/math/blob/main/preprints/Squarefree-values-of-quartics-and-power-free-values-of-polynomials-September-24-2026/manuscript.pdf)

</details>

<a name="r021"></a>

### 021 · A quadratic bound for Jacobsthal’s function

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/021.md) · 1 paper

How long can a run of consecutive integers be if every one of them shares a factor with a number that has k prime factors? This proves every run of C·k² consecutive integers contains one that shares no factor, a clean quadratic bound with no logarithmic loss.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A quadratic bound for Jacobsthal's function](https://github.com/openai/math/blob/main/preprints/A-quadratic-bound-for-Jacobsthals-function-September-25-2026/paper.pdf)

</details>

<a name="r022"></a>

### 022 · The weak inhomogeneous Duffin–Schaeffer conjecture

Not formally verified · 1 paper

This result is about approximating numbers by fractions when the target is shifted by a fixed amount γ. It proves the weak inhomogeneous Duffin–Schaeffer conjecture: if a natural series diverges, then almost every number has infinitely many good shifted approximations.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Weak Inhomogeneous Duffin–Schaeffer Conjecture](https://github.com/openai/math/blob/main/preprints/The-weak-inhomogeneous-Duffin-Schaeffer-conjecture-September-25-2026/paper.pdf)

</details>

<a name="r023"></a>

### 023 · Patterson's first moment for cubic Gauss sums

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/023.md) · 1 paper

Cubic Gauss sums are special sums built from cube roots of unity. Patterson predicted their average over primes has a main term of size X^(5/6)/log X. This proves it without any unproven assumptions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An unconditional first moment for cubic Gauss sums](https://github.com/openai/math/blob/main/preprints/An-unconditional-first-moment-for-cubic-Gauss-sums-September-25-2026/paper.pdf)

</details>

<a name="r024"></a>

### 024 · An asymptotic formula for the number of totients

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/024.md) · 1 paper

How many different values does Euler's totient function φ take up to x? This gives a precise asymptotic formula, and answers Erdős and Hall's question by showing V(cx)/V(x) → c.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An asymptotic formula for the number of totients](https://github.com/openai/math/blob/main/preprints/An-asymptotic-formula-for-the-number-of-totients-September-25-2026/An-asymptotic-formula-for-the-number-of-totients-September-25-2026.pdf)

</details>

<a name="r025"></a>

### 025 · Short Egyptian fractions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/025.md) · 1 paper

Every fraction a/b can be written as a sum of distinct unit fractions (1/n), the Egyptian way. Erdős asked how few are needed. The answer is on the order of log log b, and that is the best possible.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Short Egyptian fractions](https://github.com/openai/math/blob/main/preprints/Short-Egyptian-fractions-September-25-2026/Short-Egyptian-fractions-September-25-2026.pdf)

</details>

<a name="r026"></a>

### 026 · Positive lower density of large prime gaps

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/026.md) · 1 paper

Gaps between consecutive primes are about log p on average. This proves that, for any fixed C, a positive proportion of gaps are bigger than C·log p, answering a question of Erdős and Prachar.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Positive lower density of large prime gaps](https://github.com/openai/math/blob/main/preprints/Positive-lower-density-of-large-prime-gaps-September-25-2026/main.pdf)

</details>

<a name="r027"></a>

### 027 · Potential integral density on curve character varieties

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/027.md) · 1 paper

"Character varieties" list all the ways to represent a curve's fundamental group by matrices. This proves that points with integer-like coordinates (from one number field) fill them densely, answering Litt's question in the SL_r curve case.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Integral points on character varieties of curves](https://github.com/openai/math/blob/main/preprints/Integral-points-on-character-varieties-of-curves-September-25-2026/paper.pdf)

</details>

<a name="r028"></a>

### 028 · Uniformly bounded components of Gaussian-prime graphs

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/028.md) · 1 paper

Gaussian primes are the primes in the grid of complex integers a + bi. The "Gaussian moat" problem asks whether you can walk off to infinity stepping only on Gaussian primes, with every step shorter than some fixed length. This proves you cannot: for every step size you are trapped on a finite island.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Bounded-Step Walks on Gaussian Primes](https://github.com/openai/math/blob/main/preprints/Bounded-Step-Walks-on-Gaussian-Primes-September-26-2026/paper.pdf)

</details>

<a name="r029"></a>

### 029 · Primitive roots for every admissible integer base

Not formally verified · 2 papers

Artin's 1927 conjecture says any integer a that is not −1 or a perfect square is a primitive root (it generates every nonzero remainder) modulo infinitely many primes. Until now this was known only assuming the Generalized Riemann Hypothesis. This proves it unconditionally, with a lower bound on how many such primes exist.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Primitive roots for every admissible integer base](https://github.com/openai/math/blob/main/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/primitive-roots-all-integer-bases.pdf)
- [Simultaneous primitive roots: a conditional lower bound for prime bases](https://github.com/openai/math/blob/main/preprints/Simultaneous-primitive-roots-a-conditional-lower-bound-for-prime-bases-October-4-2026/simultaneous-primitive-roots-conditional-lower-bound-prime-bases.pdf)

</details>

<a name="r030"></a>

### 030 · Modularity of elliptic curves over imaginary quadratic fields

Not formally verified · 1 paper

Modularity, the key ingredient in the proof of Fermat's Last Theorem, is proven for every elliptic curve over every imaginary quadratic field, such as ℚ(i).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Modularity of elliptic curves over imaginary quadratic fields](https://github.com/openai/math/blob/main/preprints/Modularity-of-elliptic-curves-over-imaginary-quadratic-fields-October-4-2026/paper.pdf)

</details>

<a name="r031"></a>

### 031 · Uchida’s conjecture for open homomorphisms of Galois groups

Not formally verified · 1 paper

Uchida's conjecture says maps between certain Galois groups of number fields always come from actual embeddings of the fields. This proves it with no extra restrictions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Open Homomorphisms of Global Solvably Closed Galois Groups](https://github.com/openai/math/blob/main/preprints/Open-Homomorphisms-of-Global-Solvably-Closed-Galois-Groups-October-5-2026/open-homomorphisms-solvably-closed-galois-groups.pdf)

</details>

<a name="s-algebraic-and-complex-geometry"></a>

## Algebraic and complex geometry

<a name="r032"></a>

### 032 · The rational Hodge conjecture for CM abelian varieties

Not formally verified · 5 papers · ⚠️ 3 companion papers withdrawn Oct 7 · produced outside OpenAI's standard procedure

The Hodge conjecture, a Millennium Prize problem, says certain topological classes on algebraic varieties come from actual algebraic sub-shapes. This proves it for CM abelian varieties (a highly symmetric family) in every dimension. Through Milne's theorems, it also gives the Tate conjecture for abelian varieties over finite fields. It is not the full Hodge conjecture. On Oct 7 OpenAI withdrew three companion papers (on K3 surfaces and abelian eightfolds) after a sign error was found.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5 + 3 withdrawn)</summary>

- [The rational Hodge conjecture for CM abelian varieties](https://github.com/openai/math/blob/main/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-October-6-2026/paper.pdf)
- [Algebraic Kuga–Satake correspondences and Hodge conjectures on a K3 quadratic locus](https://github.com/openai/math/blob/main/preprints/Algebraic-Kuga-Satake-correspondences-and-Hodge-conjectures-on-a-K3-quadratic-locus-September-30-2026/paper.pdf)
- [Weil classes and Hodge classes on abelian powers](https://github.com/openai/math/blob/main/preprints/Weil-classes-and-Hodge-classes-on-abelian-powers-October-6-2026/paper.pdf)
- [Abelian covers, Gale correspondences, and the Hodge conjecture for powers](https://github.com/openai/math/blob/main/preprints/Abelian-covers-Gale-correspondences-and-the-Hodge-conjecture-for-powers-October-6-2026/paper.pdf)
- [A Conditional Reduction for Algebraic Kuga–Satake Correspondences](https://github.com/openai/math/blob/main/preprints/A-Conditional-Reduction-for-Algebraic-Kuga-Satake-Correspondences-September-10-2026/paper.pdf)
- ~~The rational Hodge conjecture for products of K3 surfaces~~ (withdrawn: [notice](https://github.com/openai/math/blob/main/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/README.md), [archived PDF](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/hodge-conjecture-products-k3.pdf))
- ~~Algebraicity of Kuga–Satake Correspondences for K3 Surfaces~~ (withdrawn: [notice](https://github.com/openai/math/blob/main/preprints/Algebraicity-of-Kuga-Satake-Correspondences-for-K3-Surfaces-October-3-2026/README.md), [archived PDF](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Algebraicity-of-Kuga-Satake-Correspondences-for-K3-Surfaces-October-3-2026/manuscript.pdf))
- ~~Algebraicity of Weil classes on split abelian eightfolds~~ (withdrawn: [notice](https://github.com/openai/math/blob/main/preprints/Algebraicity-of-Weil-classes-on-split-abelian-eightfolds-September-18-2026/README.md), [archived PDF](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Algebraicity-of-Weil-classes-on-split-abelian-eightfolds-September-18-2026/paper.pdf))

</details>

<a name="r033"></a>

### 033 · Iitaka subadditivity, variation, and logarithmic additivity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/033.md) · 5 papers

Kodaira dimension measures how "rich" a geometric space is in functions and forms. Iitaka's subadditivity says that when a space is fibred over a base, its richness is at least that of the fibre plus the base. This proves the orbifold and logarithmic versions conjectured by Campana and Popa.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5)</summary>

- [Orbifold and logarithmic Iitaka subadditivity](https://github.com/openai/math/blob/main/preprints/Orbifold-and-logarithmic-Iitaka-subadditivity-September-26-2026/paper.pdf)
- [Logarithmic Kodaira dimension and whole-fiber variation](https://github.com/openai/math/blob/main/preprints/Logarithmic-Kodaira-dimension-and-whole-fiber-variation-September-26-2026/paper.pdf)
- [The reverse logarithmic Kodaira inequality and additivity](https://github.com/openai/math/blob/main/preprints/The-reverse-logarithmic-Kodaira-inequality-and-additivity-September-26-2026/paper.pdf)
- [Projective Hodge lines and ordinary Iitaka subadditivity](https://github.com/openai/math/blob/main/preprints/Projective-Hodge-lines-and-ordinary-Iitaka-subadditivity-September-27-2026/paper.pdf)
- [B-semiampleness for compact log-smooth Kähler fibrations](https://github.com/openai/math/blob/main/preprints/B-semiampleness-for-compact-log-smooth-Kahler-fibrations-September-10-2026/paper.pdf)

</details>

<a name="r034"></a>

### 034 · Log abundance for compact Kähler spaces under logarithmic Iitaka subadditivity

Not formally verified · 14 papers · 🔧 proof repaired Oct 7

Abundance is a central conjecture of the minimal model program, the long project of classifying algebraic shapes. Using result [033](#r033), this proves log abundance for compact Kähler spaces and in characteristic zero, plus effective and uniform versions (14 papers). Several papers were revised on Oct 7 to repair positivity and contraction arguments.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (14)</summary>

- [Log abundance for compact Kähler spaces under logarithmic Iitaka subadditivity](https://github.com/openai/math/blob/main/preprints/Log-abundance-for-compact-Kahler-spaces-under-logarithmic-Iitaka-subadditivity-October-6-2026/main.pdf)
- [Uniform indices for semi-log-canonical log Calabi–Yau pairs](https://github.com/openai/math/blob/main/preprints/Uniform-indices-for-semi-log-canonical-log-Calabi-Yau-pairs-October-5-2026/uniform-slc-index.pdf)
- [Conditional good minimal models for compact Kähler fourfolds](https://github.com/openai/math/blob/main/preprints/Conditional-good-minimal-models-for-compact-Kahler-fourfolds-October-6-2026/paper.pdf)
- [Log abundance in characteristic zero](https://github.com/openai/math/blob/main/preprints/Log-abundance-in-characteristic-zero-September-24-2026/paper.pdf)
- [Minimal metrics and interior injectivity for nef adjoints](https://github.com/openai/math/blob/main/preprints/Minimal-metrics-and-interior-injectivity-for-nef-adjoints-September-27-2026/paper.pdf)
- [Fourfold nonvanishing by minimal metrics and moving jets](https://github.com/openai/math/blob/main/preprints/Fourfold-nonvanishing-by-minimal-metrics-and-moving-jets-September-27-2026/paper.pdf)
- [Lifting sections from the reduced support of an adjoint](https://github.com/openai/math/blob/main/preprints/Lifting-sections-from-the-reduced-support-of-an-adjoint-September-27-2026/paper.pdf)
- [Schnell fiber spaces and good canonical models](https://github.com/openai/math/blob/main/preprints/Schnell-fiber-spaces-and-good-canonical-models-September-24-2026/paper.pdf)
- [Uniform log Iitaka fibrations and bounded moduli denominators](https://github.com/openai/math/blob/main/preprints/Uniform-log-Iitaka-fibrations-and-bounded-moduli-denominators-October-4-2026/uniform-log-iitaka.pdf)
- [Uniform Pluricanonical Iitaka Fibrations](https://github.com/openai/math/blob/main/preprints/Uniform-Pluricanonical-Iitaka-Fibrations-October-3-2026/paper.pdf)
- [Relative denominators and effective systems for log Calabi-Yau fibrations](https://github.com/openai/math/blob/main/preprints/Relative-denominators-and-effective-systems-for-log-Calabi-Yau-fibrations-September-27-2026/paper.pdf)
- [Arithmetic Stein-degree bounds for log Calabi–Yau pairs](https://github.com/openai/math/blob/main/preprints/Arithmetic-Stein-degree-bounds-for-log-Calabi-Yau-pairs-September-25-2026/paper.pdf)
- [Uniform effective log Iitaka fibrations for fourfolds](https://github.com/openai/math/blob/main/preprints/Uniform-effective-log-Iitaka-fibrations-for-fourfolds-September-26-2026/paper.pdf)
- [Abundance after nonvanishing for compact Kähler fourfolds](https://github.com/openai/math/blob/main/preprints/Abundance-after-nonvanishing-for-compact-Kahler-fourfolds-September-27-2026/paper.pdf)

</details>

<a name="r035"></a>

### 035 · Log-canonical threefold abundance in numerical dimension one

Not formally verified · 2 papers

This proves abundance for three-dimensional log canonical pairs in characteristic p > 3 when the "numerical dimension" is one. It is part of the shape-classification program in positive characteristic.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Log abundance in numerical dimension one for threefolds in positive characteristic](https://github.com/openai/math/blob/main/preprints/Log-abundance-in-numerical-dimension-one-for-threefolds-in-positive-characteristic-October-5-2026/paper.pdf)
- [Abundance in numerical dimension one for terminal threefolds in positive characteristic](https://github.com/openai/math/blob/main/preprints/Abundance-in-numerical-dimension-one-for-terminal-threefolds-in-positive-characteristic-September-24-2026/paper.pdf)

</details>

<a name="r036"></a>

### 036 · Numerical semiampleness and generalized minimal models

Not formally verified · 4 papers · 🔧 proof repaired Oct 7

These are technical pillars of the classification program: numerical semiampleness of nef adjoint classes, and existence of minimal models or Mori fibre spaces for generalized log canonical pairs. One paper was revised on Oct 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Numerical semiampleness of nef adjoint classes on compact Kähler manifolds](https://github.com/openai/math/blob/main/preprints/Numerical-semiampleness-of-nef-adjoint-classes-on-compact-Kahler-manifolds-October-6-2026/numerical-generalized-abundance.pdf)
- [Numerical Semiampleness of Nef Adjoint Divisors](https://github.com/openai/math/blob/main/preprints/Numerical-Semiampleness-of-Nef-Adjoint-Divisors-October-3-2026/paper.pdf)
- [Minimal models and Mori fibre spaces for generalized log canonical Q-pairs](https://github.com/openai/math/blob/main/preprints/Minimal-models-and-Mori-fibre-spaces-for-generalized-log-canonical-Q-pairs-September-24-2026/paper.pdf)
- [Minimal models in numerical dimension one](https://github.com/openai/math/blob/main/preprints/Minimal-models-in-numerical-dimension-one-September-24-2026/paper.pdf)

</details>

<a name="r037"></a>

### 037 · The ordinary-double-point volume gap

Not formally verified · 2 papers

Singular points can be scored by a "normalized volume". This proves that the simplest singularity, the ordinary double point (like the tip of the cone x² + y² + z² = 0), has the largest volume among all singular points: a sharp gap in every dimension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The ordinary-double-point gap in every dimension](https://github.com/openai/math/blob/main/preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/paper.pdf)
- [The normalized-volume gap in dimension four](https://github.com/openai/math/blob/main/preprints/The-normalized-volume-gap-in-dimension-four-September-24-2026/paper.pdf)

</details>

<a name="r038"></a>

### 038 · Fujita’s freeness conjecture

Not formally verified · 1 paper

Fujita's 1985 freeness conjecture says that on an n-dimensional smooth projective variety, K_X + mL has enough sections to be "globally generated" once m ≥ n + 1. It was known only in low dimensions. This proves it in every dimension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Fujita's freeness conjecture](https://github.com/openai/math/blob/main/preprints/Fujitas-freeness-conjecture-September-23-2026/Fujitas-freeness-conjecture-September-23-2026.pdf)

</details>

<a name="r039"></a>

### 039 · Nagata’s conjecture and maximal Seshadri constants

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/039.md) · 4 papers

Nagata's 1959 conjecture says a plane curve of degree d passing through r ≥ 10 general points with multiplicities m_i must satisfy Σ m_i < d·√r. This proves it, together with "maximal Seshadri constants" in higher dimensions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Nagata's conjecture for plane curves](https://github.com/openai/math/blob/main/preprints/Nagatas-Conjecture-for-Plane-Curves-September-23-2026/main.pdf)
- [Maximal Seshadri constants on arbitrary polarized surfaces](https://github.com/openai/math/blob/main/preprints/Maximal-Seshadri-Constants-on-Arbitrary-Polarized-Surfaces-September-23-2026/main.pdf)
- [Maximal Multipoint Seshadri Constants in Higher Dimensions](https://github.com/openai/math/blob/main/preprints/Maximal-Multipoint-Seshadri-Constants-in-Higher-Dimensions-October-5-2026/main.pdf)
- [Maximal multipoint Seshadri constants in positive characteristic](https://github.com/openai/math/blob/main/preprints/Maximal-multipoint-Seshadri-constants-in-positive-characteristic-October-5-2026/seshadri-positive-characteristic.pdf)

</details>

<a name="r040"></a>

### 040 · Bloch’s conjecture for complex surfaces

Not formally verified · 1 paper

Bloch's conjecture says that on a surface with no holomorphic 2-forms (p_g = 0), the group of 0-cycles (formal combinations of points) is as small as possible. This proves it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Bloch’s conjecture for surfaces with p_g=0](https://github.com/openai/math/blob/main/preprints/Blochs-Conjecture-for-Surfaces-with-pg-equals-q-equals-0-September-24-2026/paper.pdf)

</details>

<a name="r041"></a>

### 041 · Hyperkähler SYZ and projective-space bases

Not formally verified · 2 papers

Hyperkähler manifolds are rigid, highly symmetric spaces that appear in geometry and string theory. This proves the strong SYZ conjecture (certain line bundles produce fibrations) and shows the base of every projective Lagrangian fibration is a projective space.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Projective-space bases of Lagrangian fibrations](https://github.com/openai/math/blob/main/preprints/Projective-Space-Bases-of-Lagrangian-Fibrations-September-23-2026/main.pdf)
- [The strong hyperkähler SYZ conjecture](https://github.com/openai/math/blob/main/preprints/The-Strong-Hyperkahler-SYZ-Conjecture-September-23-2026/main.pdf)

</details>

<a name="r042"></a>

### 042 · Oka classification for minimal compact complex surfaces: Kodaira dimension zero and class VII

Not formally verified · 1 paper

Oka manifolds are complex spaces that admit lots of holomorphic maps from ℂⁿ. This proves every K3 surface is Oka, and classifies which minimal surfaces of Kodaira dimension 0 and of class VII are Oka.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Every complex K3 surface is Oka](https://github.com/openai/math/blob/main/preprints/Every-complex-K3-surface-is-Oka-September-23-2026/paper.pdf)

</details>

<a name="r043"></a>

### 043 · <i>P</i> = <i>W</i> for fixed-determinant SL<sub><i>n</i></sub> moduli spaces

Not formally verified · 1 paper

"P = W" says two different filtrations on the cohomology of Higgs-bundle moduli spaces, one from topology and one from algebraic geometry, are the same. This proves the fixed-determinant SL_n version in composite rank, which completes all coprime ranks.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [P=W in composite rank for fixed determinant](https://github.com/openai/math/blob/main/preprints/P-equals-W-in-composite-rank-for-fixed-determinant-September-24-2026/P-equals-W-in-composite-rank-for-fixed-determinant-September-24-2026.pdf)

</details>

<a name="r044"></a>

### 044 · The equivariant cohomological Hikita conjecture

Not formally verified · 1 paper

The Hikita conjecture links the two sides of 3D mirror symmetry: the cohomology of a quiver variety equals the coordinate ring of a fixed locus on the dual "Coulomb branch". This proves the equivariant version for every quiver.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The equivariant cohomological Hikita conjecture for arbitrary quivers](https://github.com/openai/math/blob/main/preprints/The-equivariant-cohomological-Hikita-conjecture-for-arbitrary-quivers-September-24-2026/main.pdf)

</details>

<a name="r046"></a>

### 046 · Shafarevich counterexamples in dimension two and with large fundamental group

Not formally verified · 2 papers

Shafarevich conjectured that universal covers of projective varieties are "holomorphically convex". This gives counterexamples: a fourfold with large fundamental group, and a separate surface.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A projective fourfold with large fundamental group and non-Stein universal cover](https://github.com/openai/math/blob/main/preprints/A-projective-fourfold-with-large-fundamental-group-and-non-Stein-universal-cover-October-5-2026/large-fundamental-group-non-stein.pdf)
- [A surface counterexample to Shafarevich holomorphic convexity](https://github.com/openai/math/blob/main/preprints/A-surface-counterexample-to-Shafarevich-holomorphic-convexity-September-23-2026/paper.pdf)

</details>

<a name="r047"></a>

### 047 · Zariski cancellation and affine fibrations over the complex numbers

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/047.md) · 1 paper

Zariski cancellation asks: if X times a line is ordinary 5-dimensional space, must X be ordinary 4-space? This disproves it over ℂ in dimension 4 by building an "impostor" 4-space that becomes ordinary once one dimension is added. It also disproves the Dolgachev–Weisfeiler fibration conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An explicit failure of complex affine-space cancellation](https://github.com/openai/math/blob/main/preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026/paper.pdf)

</details>

<a name="r048"></a>

### 048 · A characteristic-zero counterexample to Lipman–Zariski

Not formally verified · 1 paper

The Lipman–Zariski conjecture says that if a surface's tangent sheaf is free, the surface must be smooth. This gives a counterexample in characteristic zero.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A singular normal affine surface with free tangent sheaf](https://github.com/openai/math/blob/main/preprints/A-singular-normal-affine-surface-with-free-tangent-sheaf-September-23-2026/paper.pdf)

</details>

<a name="r049"></a>

### 049 · A stable-coordinate counterexample in four variables

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/049.md) · 2 papers

This builds a polynomial in 4 variables that is not a "coordinate" but becomes one after adding a single extra variable. That disproves the Stable Coordinate and Abhyankar–Sathaye conjectures in this setting.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A stable coordinate that is not a coordinate in four variables](https://github.com/openai/math/blob/main/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/stable-coordinate-four-variables.pdf)
- [An explicit noncoordinate polynomial with affine three-space zero fibre](https://github.com/openai/math/blob/main/preprints/An-explicit-noncoordinate-polynomial-with-affine-three-space-zero-fibre-September-24-2026/paper.pdf)

</details>

<a name="r050"></a>

### 050 · A counterexample to Griffiths’ positivity conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/050.md) · 1 paper

Griffiths conjectured that every ample vector bundle admits a metric with positive (Griffiths) curvature. This gives a counterexample already on the simple surface P¹ × P¹.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Ample rank-two bundles on the quadric surface without Griffiths-positive metrics](https://github.com/openai/math/blob/main/preprints/ample-rank-two-bundles-on-the-quadric-surface-without-griffiths-positive-metrics-September-24-2026/paper.pdf)

</details>

<a name="r051"></a>

### 051 · Kobayashi’s canonical-ampleness conjecture

Not formally verified · 1 paper

Kobayashi conjectured that compact Kähler manifolds with no entire curves (they are "hyperbolic") must have an ample canonical bundle, which makes them projective. This proves it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Canonical ampleness of compact hyperbolic Kähler manifolds](https://github.com/openai/math/blob/main/preprints/Canonical-ampleness-of-compact-hyperbolic-Kahler-manifolds-September-23-2026/canonical-ampleness.pdf)

</details>

<a name="r052"></a>

### 052 · Tangent splittings and product decompositions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/052.md) · 2 papers

If the tangent bundle of a compact Kähler manifold splits into two well-behaved pieces, this proves the universal cover splits as a product (Beauville's conjecture, two-piece case). It also proves Höring's conjecture for rationally connected manifolds.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Universal-cover splitting for compact Kähler manifolds](https://github.com/openai/math/blob/main/preprints/Universal-cover-splitting-for-compact-Kahler-manifolds-September-23-2026/paper.pdf)
- [Integrability of split tangent bundles on rationally connected manifolds](https://github.com/openai/math/blob/main/preprints/Integrability-of-split-tangent-bundles-on-rationally-connected-manifolds-September-23-2026/main.pdf)

</details>

<a name="r053"></a>

### 053 · A counterexample to Pixton completeness in Chow

Not formally verified · 1 paper

Pixton conjectured that his relations generate every "tautological" relation on moduli spaces of curves. This gives a counterexample in Chow groups and in cohomology.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A high-arity counterexample to Pixton completeness in Chow](https://github.com/openai/math/blob/main/preprints/A-high-arity-counterexample-to-Pixton-completeness-in-Chow-September-24-2026/paper.pdf)

</details>

<a name="r054"></a>

### 054 · Irrational cubic fourfolds with Hodge-theoretic and categorical K3 associations

Not formally verified · 1 paper

Kuznetsov conjectured that a cubic fourfold is rational exactly when it has an associated K3 category. This disproves it: some cubic fourfolds have K3 associations yet are irrational (for large enough discriminant; the threshold is not explicit).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Irrational cubic fourfolds with geometric K3 categories](https://github.com/openai/math/blob/main/preprints/Irrational-cubic-fourfolds-with-geometric-K3-categories-September-24-2026/Irrational-cubic-fourfolds-with-geometric-K3-categories-September-24-2026.pdf)

</details>

<a name="r055"></a>

### 055 · Gepner symmetry and large-volume stability on threefolds

Not formally verified · 2 papers

Bridgeland stability conditions, an idea that came from string theory, organize the geometry of threefolds. This constructs the special "Gepner point" stability condition on every quintic threefold (Toda's conjecture), and large-volume stability conditions on all Calabi–Yau threefolds.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A Gepner stability condition on every smooth quintic threefold](https://github.com/openai/math/blob/main/preprints/A-Gepner-stability-condition-on-every-smooth-quintic-threefold-September-24-2026/paper.pdf)
- [Prescribed large-volume charges on threefolds with trivial canonical bundle](https://github.com/openai/math/blob/main/preprints/Prescribed-large-volume-charges-on-threefolds-with-trivial-canonical-bundle-September-24-2026/paper.pdf)

</details>

<a name="r056"></a>

### 056 · Termination of projective and Kähler fourfold minimal model programs

Not formally verified · 5 papers · 🔧 proof repaired Oct 7

This proves the minimal model program terminates (there is no infinite chain of surgeries called "flips") for projective log canonical fourfolds and Kähler fourfolds. Papers were revised on Oct 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5)</summary>

- [Termination of generalized log canonical flips on compact Kähler fourfolds](https://github.com/openai/math/blob/main/preprints/Termination-of-generalized-log-canonical-flips-on-compact-Kahler-fourfolds-October-7-2026/termination-generalized-lc-kahler-fourfolds.pdf)
- [Termination of generalized-canonical flips on compact Kähler fourfolds](https://github.com/openai/math/blob/main/preprints/Termination-of-generalized-canonical-flips-on-compact-Kahler-fourfolds-October-6-2026/termination-generalized-terminal-flips-compact-kahler-fourfolds.pdf)
- [Termination for projective log canonical fourfolds with rational boundary](https://github.com/openai/math/blob/main/preprints/Termination-for-projective-log-canonical-fourfolds-with-rational-boundary-September-24-2026/paper.pdf)
- [Finite ordinary minimal model programs on compact Kähler fourfolds](https://github.com/openai/math/blob/main/preprints/Finite-ordinary-minimal-model-programs-on-compact-Kahler-fourfolds-October-6-2026/paper.pdf)
- [Finite ordinary minimal model programs on compact Kähler fourfolds](https://github.com/openai/math/blob/main/preprints/Finite-ordinary-minimal-model-programs-on-compact-Kahler-fourfolds-September-24-2026/paper.pdf)

</details>

<a name="r057"></a>

### 057 · Fundamental groups of special complex varieties and root orbifolds

Not formally verified · 3 papers

Campana's abelianity conjecture says that "special" varieties have virtually abelian fundamental groups (their loops commute, up to finite index). This proves it for compact Kähler manifolds, with related results for quasi-projective ones.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [The abelianity conjecture for special compact Kähler manifolds](https://github.com/openai/math/blob/main/preprints/The-abelianity-conjecture-for-special-compact-Kahler-manifolds-September-23-2026/paper.pdf)
- [Two-step monodromy of special quasi-projective varieties](https://github.com/openai/math/blob/main/preprints/Two-step-monodromy-of-special-quasi-projective-varieties-September-24-2026/paper.pdf)
- [A conditional abelianity theorem for special fourfold pairs with a half-weight divisor](https://github.com/openai/math/blob/main/preprints/A-conditional-abelianity-theorem-for-special-fourfold-pairs-with-a-half-weight-divisor-October-5-2026/main.pdf)

</details>

<a name="r058"></a>

### 058 · Semialgebraic universal covers and bounded domains

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/058.md) · 2 papers

Kollár–Pardon: classify the projective varieties whose universal covers are semialgebraic. They are exactly products of a bounded symmetric domain, ℂ^m and a compact factor. A corollary: a smooth projective variety covered by ℂⁿ is, up to a finite cover, an abelian variety.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Semialgebraic universal covers of normal projective varieties](https://github.com/openai/math/blob/main/preprints/Semialgebraic-universal-covers-of-normal-projective-varieties-September-24-2026/paper.pdf)
- [Symmetry of semialgebraic bounded domains with compact quotient](https://github.com/openai/math/blob/main/preprints/Symmetry-of-semialgebraic-bounded-domains-with-compact-quotient-September-24-2026/paper.pdf)

</details>

<a name="r059"></a>

### 059 · Counterexamples to Zariski’s multiplicity conjecture

Not formally verified · 2 papers

Zariski's 1971 multiplicity conjecture says two hypersurface singularities that look identical topologically must have the same multiplicity. This disproves it with explicit counterexamples (multiplicities 2 vs 3, and 4 vs 5 in ℂ⁴).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Ambiently homeomorphic isolated hypersurfaces of multiplicities two and three](https://github.com/openai/math/blob/main/preprints/Ambiently-homeomorphic-isolated-hypersurfaces-of-multiplicities-two-and-three-September-24-2026/paper.pdf)
- [Ambiently homeomorphic isolated hypersurface germs in ℂ⁴ with multiplicities four and five](https://github.com/openai/math/blob/main/preprints/Ambiently-homeomorphic-isolated-hypersurface-germs-in-C4-with-multiplicities-four-and-five-September-27-2026/paper.pdf)

</details>

<a name="r060"></a>

### 060 · The Global Spherical Shell conjecture

Not formally verified · 1 paper

Class VII surfaces are the last poorly understood family of compact complex surfaces. This proves the Global Spherical Shell conjecture for b₂ > 0, a decisive step toward classifying them completely.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Global Spherical Shells on Minimal Surfaces of Class VII](https://github.com/openai/math/blob/main/preprints/Global-Spherical-Shells-on-Minimal-Surfaces-of-Class-VII-September-24-2026/paper.pdf)

</details>

<a name="r062"></a>

### 062 · Projective contact classification and the LeBrun–Salamon conjecture

Not formally verified · 1 paper

The LeBrun–Salamon conjecture says positive quaternion-Kähler manifolds must be the standard symmetric "Wolf spaces". This proves it, and classifies projective contact manifolds.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Contact Fano manifolds and the LeBrun–Salamon conjecture](https://github.com/openai/math/blob/main/preprints/Contact-Fano-manifolds-and-the-LeBrun-Salamon-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r063"></a>

### 063 · The generalized Mukai conjecture

Not formally verified · 1 paper

The generalized Mukai conjecture bounds the shape of Fano manifolds: ρ(ι − 1) ≤ n, with equality only for products of projective spaces. This proves it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The generalized Mukai conjecture](https://github.com/openai/math/blob/main/preprints/The-Generalized-Mukai-Conjecture-September-24-2026/article.pdf)

</details>

<a name="r064"></a>

### 064 · Topological triviality of <i>μ</i>-constant surface singularities

Not formally verified · 1 paper

The μ-constant problem: if a family of surface singularities keeps the same Milnor number, is the family topologically trivial? This proves yes for surfaces in ℂ³.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Topological triviality of mu-constant families of surface singularities](https://github.com/openai/math/blob/main/preprints/Topological-triviality-of-mu-constant-families-of-surface-singularities-September-24-2026/main.pdf)

</details>

<a name="r065"></a>

### 065 · Virasoro constraints for complete intersections and projective-bundle towers

Not formally verified · 2 papers

Virasoro constraints are symmetries that string theory predicts for curve-counting invariants. This proves them for complete intersections in projective space and for towers of projective bundles.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Virasoro Constraints under Projectivization](https://github.com/openai/math/blob/main/preprints/Virasoro-Constraints-under-Projectivization-October-5-2026/virasoro-constraints-under-projectivization.pdf)
- [Virasoro Constraints for Projective Complete Intersections](https://github.com/openai/math/blob/main/preprints/Virasoro-Constraints-for-Projective-Complete-Intersections-September-24-2026/article.pdf)

</details>

<a name="r066"></a>

### 066 · Bounded klt complements for Fano contractions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/066.md) · 2 papers

This proves Shokurov's bounded-complements conjecture for Fano contractions (finite-coefficient version), a key boundedness tool in classifying shapes.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Bounded klt complements for Fano contractions](https://github.com/openai/math/blob/main/preprints/Bounded-klt-complements-for-Fano-contractions-September-25-2026/Bounded-klt-complements-for-Fano-contractions-September-25-2026.pdf)
- [Uniform Cartier sections for Fano type contractions](https://github.com/openai/math/blob/main/preprints/Uniform-Cartier-sections-for-Fano-type-contractions-September-25-2026/Uniform-Cartier-sections-for-Fano-type-contractions-September-25-2026.pdf)

</details>

<a name="r067"></a>

### 067 · The Campana–Peternell conjecture in dimension six

Not formally verified · 1 paper

This proves the Campana–Peternell conjecture in dimension 6: Fano manifolds whose tangent bundle is nef are rational homogeneous spaces.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Campana–Peternell conjecture in dimension six](https://github.com/openai/math/blob/main/preprints/The-Campana-Peternell-conjecture-in-dimension-six-September-25-2026/main.pdf)

</details>

<a name="r068"></a>

### 068 · Anticanonical nonvanishing in every dimension

Not formally verified · 7 papers

If −K_X carries a smooth metric of nonnegative curvature, this proves some power of the anticanonical bundle has a nonzero section, in every dimension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (7)</summary>

- [Anticanonical nonvanishing from smooth semipositivity](https://github.com/openai/math/blob/main/preprints/Anticanonical-nonvanishing-from-smooth-semipositivity-September-26-2026/main.pdf)
- [Invariant anticanonical indices and conversion of twisted differentials](https://github.com/openai/math/blob/main/preprints/Invariant-anticanonical-indices-and-conversion-of-twisted-differentials-September-26-2026/main.pdf)
- [Bounded anticanonical metrics on klt pairs and torus quotients](https://github.com/openai/math/blob/main/preprints/Bounded-anticanonical-metrics-on-klt-pairs-and-torus-quotients-September-26-2026/main.pdf)
- [Cohomological transfer and equivariant anticanonical sections](https://github.com/openai/math/blob/main/preprints/Cohomological-transfer-and-equivariant-anticanonical-sections-September-26-2026/main.pdf)
- [Metric descent and rank-preserving contractions](https://github.com/openai/math/blob/main/preprints/Metric-descent-and-rank-preserving-contractions-September-26-2026/main.pdf)
- [Integrable metrics and effectivity with controlled boundary](https://github.com/openai/math/blob/main/preprints/Integrable-metrics-and-effectivity-with-controlled-boundary-September-26-2026/main.pdf)
- [Exact orders and invariant anticanonical linear systems](https://github.com/openai/math/blob/main/preprints/Exact-orders-and-invariant-anticanonical-linear-systems-September-26-2026/main.pdf)

</details>

<a name="r069"></a>

### 069 · Global quantum geometric Langlands at irrational level

Not formally verified · 1 paper

This proves quantum geometric Langlands at irrational level, in the unramified de Rham setting: an equivalence between categories of twisted D-modules for a group and for its Langlands dual.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Global quantum geometric Langlands at irrational level](https://github.com/openai/math/blob/main/preprints/Global-quantum-geometric-Langlands-at-irrational-level-October-4-2026/quantum-langlands.pdf)

</details>

<a name="s-real-and-complex-analysis"></a>

## Real and complex analysis

<a name="r071"></a>

### 071 · Koebe’s circle-domain conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/071.md) · 2 papers

Koebe's 1908 conjecture: any region of the plane or sphere, however many holes it has, can be reshaped without distorting angles (conformally) into a region whose holes are perfect round disks or points. This proves the existence part, and shows the round-hole picture is rigid when the boundary is "removable" (one direction of the He–Schramm conjecture).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Removable Boundaries and Rigidity of Circle Domains](https://github.com/openai/math/blob/main/preprints/Removable-Boundaries-and-Rigidity-of-Circle-Domains-September-23-2026/paper.pdf)
- [Koebe's Circle-Domain Conjecture](https://github.com/openai/math/blob/main/preprints/Koebes-Circle-Domain-Conjecture-September-23-2026/paper.pdf)

</details>

<a name="r072"></a>

### 072 · Brennan's conjecture and the integral-means spectrum

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/072.md) · 2 papers

Brennan's conjecture: for any angle-preserving map from a simply connected region onto the disk, |φ′|^s is area-integrable for 4/3 < s < 4. This proves it with a sharp "integral means" identity, and disproves a prediction of Kraetzer.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Brennan's conjecture and sharp inverse-square integral means](https://github.com/openai/math/blob/main/preprints/Brennans-conjecture-and-sharp-inverse-square-integral-means-September-24-2026/paper.pdf)
- [A strict inverse-first-power bound for univalent functions](https://github.com/openai/math/blob/main/preprints/A-strict-inverse-first-power-bound-for-univalent-functions-September-24-2026/paper.pdf)

</details>

<a name="r073"></a>

### 073 · The Falconer distance conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/073.md) · 1 paper

Falconer's distance conjecture: any set in ℝ^d of fractal dimension greater than d/2 produces a "large" set of distances (positive length). This proves it in every dimension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Falconer distance conjecture in all dimensions](https://github.com/openai/math/blob/main/preprints/The-Falconer-distance-conjecture-in-all-dimensions-September-23-2026/paper.pdf)

</details>

<a name="r074"></a>

### 074 · Kakeya in three and four dimensions

Not formally verified · 2 papers

The Kakeya problem asks how small a set can be if it contains a unit line segment pointing in every direction. This proves such sets in 4D have full dimension, and proves the stronger "maximal function" version in 3D.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The Kakeya maximal conjecture in three dimensions](https://github.com/openai/math/blob/main/preprints/The-Kakeya-maximal-conjecture-in-three-dimensions-September-23-2026/paper.pdf)
- [Every four-dimensional Kakeya set has full Hausdorff dimension](https://github.com/openai/math/blob/main/preprints/Every-four-dimensional-Kakeya-set-has-full-Hausdorff-dimension-September-24-2026/paper.pdf)

</details>

<a name="r075"></a>

### 075 · The $`L\log L`$ Fourier-convergence conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/075.md) · 1 paper

When does a function's Fourier series add back up to the function? Carleson proved it happens almost everywhere for square-integrable functions, and Kolmogorov showed it can fail for merely integrable ones. This proves convergence for the in-between class L log L, the conjectured boundary.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Almost-everywhere Fourier convergence in L log L](https://github.com/openai/math/blob/main/preprints/Almost-everywhere-Fourier-convergence-in-L-log-L-September-23-2026/paper.pdf)

</details>

<a name="r076"></a>

### 076 · Real ultraflat Littlewood polynomials and unbounded binary merit factors

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/076.md) · 3 papers

Littlewood polynomials have every coefficient equal to +1 or −1. Can one be "ultraflat", with the same size (about √N) everywhere on the unit circle? This proves yes, even with real coefficients. As a result, binary ±1 sequences can have arbitrarily low autocorrelation (unbounded "merit factor"), disproving Turyn's conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Ultraflat real Littlewood polynomials](https://github.com/openai/math/blob/main/preprints/Ultraflat-real-Littlewood-polynomials-October-5-2026/ultraflat-real-littlewood-polynomials.pdf)
- [Nearly minimal maxima and positive minima of Littlewood polynomials](https://github.com/openai/math/blob/main/preprints/Nearly-minimal-maxima-and-positive-minima-of-Littlewood-polynomials-October-5-2026/littlewood-lower-envelope.pdf)
- [Asymptotically minimal maxima of real Littlewood polynomials](https://github.com/openai/math/blob/main/preprints/Asymptotically-minimal-maxima-of-real-Littlewood-polynomials-September-23-2026/paper.pdf)

</details>

<a name="r077"></a>

### 077 · Fourier restriction for positively curved surfaces

Not formally verified · 2 papers

Fourier restriction asks how well the Fourier transform of something living on a curved surface spreads into space. This proves the conjectured bound (p > 3) for every positively curved surface in 3D, including the sphere: the famous restriction conjecture in three dimensions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Elliptic capacity propagation and Fourier restriction to the sphere](https://github.com/openai/math/blob/main/preprints/Elliptic-capacity-propagation-and-Fourier-restriction-to-the-sphere-September-24-2026/Elliptic-capacity-propagation-and-Fourier-restriction-to-the-sphere-September-24-2026.pdf)
- [Diagonal Fourier extension for positively curved surfaces in three dimensions](https://github.com/openai/math/blob/main/preprints/Diagonal-Fourier-extension-for-positively-curved-surfaces-in-three-dimensions-September-24-2026/Diagonal-Fourier-extension-for-positively-curved-surfaces-in-three-dimensions-September-24-2026.pdf)

</details>

<a name="r078"></a>

### 078 · The three-dimensional Bochner–Riesz conjecture

Not formally verified · 1 paper

Bochner–Riesz means smooth out a sharp Fourier cut-off to a ball. The conjecture predicts exactly which smoothing orders keep the operator bounded on L^p. This resolves it in 3D.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Bochner–Riesz multipliers in three dimensions](https://github.com/openai/math/blob/main/preprints/Bochner-Riesz-Multipliers-in-Three-Dimensions-September-24-2026/Bochner-Riesz-Multipliers-in-Three-Dimensions-September-24-2026.pdf)

</details>

<a name="r079"></a>

### 079 · Local smoothing in three dimensions

Not formally verified · 1 paper

Sogge's local smoothing conjecture says waves become smoother when you average over a short time window rather than look at a single moment. This proves it in 3D over the full range of exponents.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Critical local smoothing for the three-dimensional wave equation](https://github.com/openai/math/blob/main/preprints/Critical-local-smoothing-for-the-three-dimensional-wave-equation-September-24-2026/paper.pdf)

</details>

<a name="r080"></a>

### 080 · The exact Sobolev endpoint for Schrödinger convergence

Not formally verified · 2 papers

Carleson's problem: if you start the free Schrödinger equation from data f, does the solution return to f point by point as time goes to 0? This was known to need f in H^s with s ≥ n/(2(n+1)). This proves convergence exactly at that endpoint.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Endpoint convergence for the planar Schrodinger equation](https://github.com/openai/math/blob/main/preprints/Endpoint-convergence-for-the-planar-Schrodinger-equation-September-24-2026/paper.pdf)
- [Endpoint pointwise convergence for the Schrodinger equation in higher dimensions](https://github.com/openai/math/blob/main/preprints/Endpoint-pointwise-convergence-for-the-Schrodinger-equation-in-higher-dimensions-September-24-2026/paper.pdf)

</details>

<a name="r081"></a>

### 081 · Riesz transforms and rectifiability in higher codimension

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/081.md) · 1 paper

If a measure's Riesz transform is bounded, must the measure be made of smooth pieces ("rectifiable")? This resolves the remaining higher-codimension cases.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Riesz transforms and uniform rectifiability in higher codimension](https://github.com/openai/math/blob/main/preprints/Riesz-transforms-and-uniform-rectifiability-in-higher-codimension-September-24-2026/paper.pdf)

</details>

<a name="r082"></a>

### 082 · Annular variation and dyadic absolute bounds for the triangular Hilbert transform

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/082.md) · 3 papers

The triangular Hilbert transform is a notoriously hard multilinear singular integral. This proves bounds for it at the symmetric L³ point, with variation and maximal versions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Annular variation of the triangular Hilbert transform at the symmetric point](https://github.com/openai/math/blob/main/preprints/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/annular-variation.pdf)
- [An L³ bound for the dyadic triangular Hilbert form](https://github.com/openai/math/blob/main/preprints/An-L3-bound-for-the-dyadic-triangular-Hilbert-form-October-5-2026/dyadic-triangular-hilbert.pdf)
- [The maximal triangular Hilbert transform at the symmetric point](https://github.com/openai/math/blob/main/preprints/The-maximal-triangular-Hilbert-transform-at-the-symmetric-point-September-24-2026/paper.pdf)

</details>

<a name="r083"></a>

### 083 · Hilbert transforms along Lipschitz directions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/083.md) · 1 paper

This gives a uniform L² bound for the Hilbert transform taken along a Lipschitz field of directions at short scales, establishing Stein's weak-type conjecture in that regime.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A uniform Hilbert transform estimate for Lipschitz directions](https://github.com/openai/math/blob/main/preprints/A-uniform-Hilbert-transform-estimate-for-Lipschitz-directions-September-25-2026/main.pdf)

</details>

<a name="r084"></a>

### 084 · The geometric case of the Erdős similarity conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/084.md) · 2 papers

Erdős's similarity conjecture says that for every infinite set of numbers, some set of positive measure contains no shifted, rescaled copy of it. This proves it for every geometric progression {qⁿ}.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The geometric case of the Erdős similarity conjecture](https://github.com/openai/math/blob/main/preprints/The-geometric-case-of-the-Erdos-similarity-conjecture-October-5-2026/geometric-erdos-similarity.pdf)
- [The dyadic case of the Erdős similarity conjecture](https://github.com/openai/math/blob/main/preprints/The-dyadic-case-of-the-Erdos-similarity-conjecture-September-25-2026/paper.pdf)

</details>

<a name="r085"></a>

### 085 · Endpoint Sobolev regularity of centered disk averages

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/085.md) · 1 paper

Averaging a function over disks and taking the largest average (the maximal function) does not increase its total variation (W^{1,1} norm) in 2D. This resolves the centered-disk case of the Hajłasz–Onninen problem.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An Endpoint Gradient Bound for the Centered Disk Maximal Operator](https://github.com/openai/math/blob/main/preprints/An-Endpoint-Gradient-Bound-for-the-Centered-Disk-Maximal-Operator-September-26-2026/article.pdf)

</details>

<a name="r086"></a>

### 086 · An <i>L</i><sup>3</sup> bound for the trilinear Hilbert transform

Not formally verified · 1 paper

The trilinear Hilbert transform with shifts t, 2t, 3t is shown to be bounded from L³ × L³ × L³ to L¹, a long-sought case.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An <i>L</i><sup>3</sup> bound for the trilinear Hilbert transform](https://github.com/openai/math/blob/main/preprints/An-L3-bound-for-the-trilinear-Hilbert-transform-October-5-2026/paper.pdf)

</details>

<a name="s-convex-and-metric-geometry"></a>

## Convex and metric geometry

<a name="r087"></a>

### 087 · The Mahler conjectures, functional inequalities and polar-product symplectic width

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/087.md) · 3 papers · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/symmetric-and-general-mahler-conjectures.pdf)

Mahler's conjecture: for a convex body K and its "polar" dual K°, the product vol(K)·vol(K°) is smallest for the cube (symmetric case) and the simplex (general case). This proves both in every dimension, with all equality cases, and computes a related symplectic width. It is one of the best-known problems in convex geometry.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [The symmetric Mahler conjecture and its equality cases](https://github.com/openai/math/blob/main/preprints/The-symmetric-Mahler-conjecture-and-its-equality-cases-September-22-2026/paper.pdf)
- [The Mahler Conjecture for General Convex Bodies](https://github.com/openai/math/blob/main/preprints/The-Mahler-Conjecture-for-General-Convex-Bodies-September-22-2026/paper.pdf)
- [Symplectic Balls in Symmetric Polar Products](https://github.com/openai/math/blob/main/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/paper.pdf)

</details>

<a name="r088"></a>

### 088 · Sharp projection-body inequalities and a counterexample to simplex maximization

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/088.md) · 2 papers

A projection body records the shadow areas of a convex body in every direction. Petty's conjecture (ellipsoids minimize projection-body volume at fixed volume) is proven for n ≥ 4, completing it. It also shows simplices are not the maximizers, because products of simplices beat them.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Petty’s projection-volume conjecture in dimensions at least four](https://github.com/openai/math/blob/main/preprints/Pettys-projection-volume-conjecture-in-dimensions-at-least-four-September-24-2026/paper.pdf)
- [A product counterexample to the simplex maximum for projection-body volume](https://github.com/openai/math/blob/main/preprints/A-product-counterexample-to-the-simplex-maximum-for-projection-body-volume-September-24-2026/paper.pdf)

</details>

<a name="r089"></a>

### 089 · Bounded-distortion <i>L</i><sub>1</sub> embeddings of planar and bounded-treewidth graphs

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/089.md) · 2 papers

Can shortest-path distances in a planar network be represented faithfully as L1 ("Manhattan-style") distances? This proves yes, with bounded distortion, for planar graphs and for graphs of bounded treewidth. Consequence: in such networks, the maximum multi-route flow and the minimum cut differ by at most a constant factor.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* Road and transit networks are nearly planar. This guarantees that cut-based bottleneck analysis ("which few links, if closed, split the city?") is within a constant factor of true multi-route capacity. It is background for any capacity or bottleneck layer on a map; existing tools already compute this.

<details><summary>Papers (2)</summary>

- [Planar Graph Metrics Embed into L1 with Constant Distortion](https://github.com/openai/math/blob/main/preprints/Planar-Graph-Metrics-Embed-into-L1-with-Constant-Distortion-September-23-2026/paper.pdf)
- [L1 Embeddings of Graphs of Bounded Treewidth](https://github.com/openai/math/blob/main/preprints/L1-Embeddings-of-Graphs-of-Bounded-Treewidth-September-23-2026/paper.pdf)

</details>

<a name="r090"></a>

### 090 · Triangular-lattice optimality, long-range Riesz and Coulomb energies, and spherical logarithmic energy

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/090.md) · 4 papers

Among all ways to spread points in the plane at a given density, the triangular (honeycomb) lattice minimizes energy for a very wide class of repulsive interactions ("universal optimality" in 2D). This also settles the Coulomb and Riesz versions (Sandier–Serfaty) and logarithmic energy on the sphere.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* Hexagonal arrangements are provably the most even way to spread points over a plane for any repulsive cost. That backs using hexagon bins for map aggregation and evenly spaced placement (sensors, kiosks, sample points). This is already common practice; the result is the strongest theoretical support for it.

<details><summary>Papers (4)</summary>

- [An atomic certificate for triangular-lattice universal optimality](https://github.com/openai/math/blob/main/preprints/An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026/paper.pdf)
- [Universal optimality of the triangular lattice](https://github.com/openai/math/blob/main/preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/paper.pdf)
- [A sharp Fourier certificate for planar circle packing](https://github.com/openai/math/blob/main/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/paper.pdf)
- [Triangular minimality for planar Coulomb renormalized energy](https://github.com/openai/math/blob/main/preprints/Triangular-minimality-for-planar-Coulomb-renormalized-energy-September-23-2026/paper.pdf)

</details>

<a name="r091"></a>

### 091 · Logarithmic and <i>L</i><sub><i>p</i></sub> Brunn–Minkowski inequalities and the B-conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/091.md) · 1 paper

The log Brunn–Minkowski inequality is a strengthened "volume of a blend" inequality for symmetric convex bodies. This proves it in every dimension, along with the B-conjecture for even log-concave measures.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The logarithmic Brunn–Minkowski conjecture](https://github.com/openai/math/blob/main/preprints/The-logarithmic-Brunn-Minkowski-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r092"></a>

### 092 · The optimal order of convex-body covering density

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/092.md) · 2 papers

How efficiently can you cover space with translated copies of one convex shape? This proves the worst-case covering density is on the order of n·log n in dimension n, and that lattice coverings achieve it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A single-lattice covering bound of order n log n](https://github.com/openai/math/blob/main/preprints/A-single-lattice-covering-bound-of-order-n-log-n-September-23-2026/paper.pdf)
- [Translative covering densities of order n log n](https://github.com/openai/math/blob/main/preprints/Translative-covering-densities-of-order-n-log-n-September-23-2026/paper.pdf)

</details>

<a name="r093"></a>

### 093 · Dimension-free logarithmic Sobolev inequality for subgaussian log-concave measures

Not formally verified · 1 paper

Logarithmic Sobolev inequalities control how tightly random quantities concentrate around their averages. This proves a version whose constant does not grow with dimension for log-concave distributions whose one-dimensional views are sub-Gaussian.

- **Quant trading:** ⚪ *No practical link:* Dimension-free concentration was already known for independent coordinates and for linear combinations; the new case is log-concave laws with no curvature bound. NQ returns are fat-tailed and stop/target trade P&L is two-peaked, so neither has this shape.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [A dimension-free logarithmic Sobolev inequality for subgaussian log-concave measures](https://github.com/openai/math/blob/main/preprints/A-dimension-free-logarithmic-Sobolev-inequality-for-subgaussian-log-concave-measures-September-23-2026/paper.pdf)

</details>

<a name="r094"></a>

### 094 · Subpolynomial dimension reduction in <i>L</i><sub><i>p</i></sub>

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/094.md) · 1 paper

Dimension reduction: can n points be squeezed into few dimensions while keeping all distances within a factor D? For ordinary Euclidean distance about log n dimensions suffice (Johnson–Lindenstrauss). For other L_p distances it was unclear. This shows n^{o(1)} dimensions suffice for every 1 < p < ∞.

- **Quant trading:** ⚪ *No practical link:* The theorem is existential (the paper gives no efficient embedding), its constants are unspecified, and it excludes the L1 case. Nothing usable at trading-data sizes.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Subpolynomial dimension reduction in Lp](https://github.com/openai/math/blob/main/preprints/Subpolynomial-dimension-reduction-in-Lp-September-23-2026/paper.pdf)

</details>

<a name="r095"></a>

### 095 · Hyperbolicity cones without semidefinite lifts

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/095.md) · 3 papers

Hyperbolicity cones are convex shapes that come from optimization. The generalized Lax conjecture said they can all be written as slices of semidefinite cones, which would make them solvable by standard SDP software. This disproves it: some of them cannot be written that way at all.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Hyperbolicity Cones Without Semidefinite Lifts](https://github.com/openai/math/blob/main/preprints/Hyperbolicity-Cones-Without-Semidefinite-Lifts-October-5-2026/nonliftable-hyperbolicity.pdf)
- [A nonspectrahedral hyperbolicity cone](https://github.com/openai/math/blob/main/preprints/A-Nonspectrahedral-Hyperbolicity-Cone-September-24-2026/nonspectrahedral-hyperbolicity-cone.pdf)
- [An Exact Semidefinite Lift of a Nonspectrahedral Hyperbolicity Cone](https://github.com/openai/math/blob/main/preprints/An-Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone-October-5-2026/Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone.pdf)

</details>

<a name="r096"></a>

### 096 · The Gaussian propeller conjecture in every dimension

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/096.md) · 1 paper

Split space into pieces and measure each piece's Gaussian "centre of mass". The sum of their squares is at most 9/(8π), achieved by three 120° wedges (the "propeller"). One consequence is a hardness result for approximate kernel clustering.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Gaussian propeller bound in every dimension](https://github.com/openai/math/blob/main/preprints/The-Gaussian-Propeller-Bound-in-Every-Dimension-September-24-2026/main.pdf)

</details>

<a name="r097"></a>

### 097 · The Euclidean Steinitz–Bergström bound

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/097.md) · 1 paper

Take any sequence of arrows (vectors) of length at most 1 in d dimensions. You can pick a + or − for each one, in order, so that every running total stays within C·√d, however long the sequence is. Equivalently, any set of arrows that sums to zero can be put in an order whose running totals all stay within C·√d. The √d size is optimal.

- **Quant trading:** 🟡 *Background.* If indivisible trades whose factor exposures net exactly to zero must go out one at a time, some order keeps running exposure within C·√d trade sizes. But the construction is existential (no algorithm), comparable usable bounds already existed (Banaszczyk; Dutta–Jha–Jiang), and real rebalances are sliced and traded in parallel. No use for a single-instrument NQ book.
- **Politeia:** 🟡 *Background.* For sequential fairness: when approving items one at a time (projects, budget lines) that affect d groups or districts, some order (or choice of which side to fund) keeps every group's running balance within C·√d. Useful framing for a "keep it balanced as we go" allocation view.

<details><summary>Papers (1)</summary>

- [The Euclidean Steinitz–Bergström theorem](https://github.com/openai/math/blob/main/preprints/The-Euclidean-Steinitz-Bergstrom-theorem-September-24-2026/The-Euclidean-Steinitz-Bergstrom-theorem-September-24-2026.pdf)

</details>

<a name="r098"></a>

### 098 · Compact counterexamples to bi-Lipschitz dimension reduction

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/098.md) · 1 paper

Sets that look finite-dimensional at every scale ("doubling" sets) still need not fit into any finite-dimensional space without distortion, even compact pieces of Hilbert space. This answers the Lang–Plaut problem negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A doubling Hilbert subset with no finite-dimensional bi-Lipschitz embedding](https://github.com/openai/math/blob/main/preprints/A-doubling-Hilbert-subset-with-no-finite-dimensional-bi-Lipschitz-embedding-September-25-2026/main.pdf)

</details>

<a name="r099"></a>

### 099 · The sharp exponential scale of edit-distance distortion

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/099.md) · 3 papers

Edit distance (the fewest insertions, deletions and substitutions that turn one string into another) cannot be represented faithfully as an L1 distance. This finds the best possible distortion exactly: exp(Θ(√(log d · log log d))).

- **Quant trading:** ⚪ *No practical link:* This pins down the worst-case distortion exactly, but the fact that it must grow was already known, and the lower bound uses specially built strings. Nothing changes for comparing real bar patterns.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (3)</summary>

- [Edit Distance in l1: Matching Bounds up to Constants in the Exponent](https://github.com/openai/math/blob/main/preprints/Edit-Distance-in-l1-Matching-Bounds-up-to-Constants-in-the-Exponent-September-27-2026/paper.pdf)
- [Finite-Circle Obstructions, Binary Codes, and Histogram Embeddings for Edit Distance](https://github.com/openai/math/blob/main/preprints/Finite-Circle-Obstructions-Binary-Codes-and-Histogram-Embeddings-for-Edit-Distance-September-27-2026/paper.pdf)
- [Tree Constructions for the l1 Distortion of Binary Edit Distance](https://github.com/openai/math/blob/main/preprints/Tree-Constructions-for-the-l1-Distortion-of-Binary-Edit-Distance-September-27-2026/paper.pdf)

</details>

<a name="r100"></a>

### 100 · Cylinder coverings below the half-area bound

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/100.md) · 4 papers

This covers a regular tetrahedron with finitely many cylinders whose total cross-section area is less than half its smallest shadow, disproving Bang-type "half-area" covering bounds in 3D.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Finite angular cylinder covers below the half-area bound](https://github.com/openai/math/blob/main/preprints/Finite-angular-cylinder-covers-below-the-half-area-bound-September-27-2026/main.pdf)
- [Finite cylinder approximation of ruled sets](https://github.com/openai/math/blob/main/preprints/Finite-cylinder-approximation-of-ruled-sets-September-27-2026/main.pdf)
- [Slope-field perturbations of the two-cylinder covering](https://github.com/openai/math/blob/main/preprints/Slope-field-perturbations-of-the-two-cylinder-covering-September-27-2026/main.pdf)
- [Finite triangular approximation of radial sweeps](https://github.com/openai/math/blob/main/preprints/Finite-triangular-approximation-of-radial-sweeps-September-27-2026/main.pdf)

</details>

<a name="r101"></a>

### 101 · The sharp simplex conjecture for isotropic constants

Not formally verified · 1 paper

Among all convex bodies, the simplex has the most "lopsided" spread of volume (the largest isotropic constant), resolving the strong isotropic constant conjecture. This also proves a sharp lower bound on the entropy of log-concave densities.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A sharp entropy bound and the simplex inequality for isotropic constants](https://github.com/openai/math/blob/main/preprints/A-sharp-entropy-bound-and-the-simplex-inequality-for-isotropic-constants-October-5-2026/isotropic-simplex.pdf)

</details>

<a name="s-theoretical-computer-science"></a>

## Theoretical computer science

<a name="r102"></a>

### 102 · The Unique Games Conjecture and optimal approximation thresholds

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/102.md) · 5 papers · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/basic-semidefinite-threshold-np-hardness.pdf)

The Unique Games Conjecture (Khot, 2002) is the central open problem about approximation algorithms, and this proves it. As a consequence, many simple approximation algorithms are the best possible unless P = NP. For example, Goemans–Williamson's 0.878 for Max-Cut and factor 2 for Vertex Cover cannot be beaten. The family also gives direct proofs of these consequences.

- **Quant trading:** 🟡 *Background.* Splitting assets into two books so the most anti-correlated pairs land on opposite sides is a Max-Cut problem. The Goemans–Williamson semidefinite rounding is now proven to be the best possible general guarantee (unless P = NP). For a few hundred assets use that method or an exact solver; don't expect a cleverer general algorithm.
- **Politeia:** 🟡 *Background.* Splitting a disagreement network (who votes against whom) into two camps is also Max-Cut. If Politeia ever shows a "polarization split", the same method is provably the best general approach, and exact solvers are fine for small groups.

<details><summary>Papers (5)</summary>

- [The Unique Games Theorem](https://github.com/openai/math/blob/main/preprints/The-Unique-Games-Theorem-September-23-2026/paper.pdf)
- [A Direct Proof of Optimal Max-Cut Hardness](https://github.com/openai/math/blob/main/preprints/A-Direct-Proof-of-Optimal-Max-Cut-Hardness-September-23-2026/paper.pdf)
- [The Factor-Two Hardness Threshold for Vertex Cover](https://github.com/openai/math/blob/main/preprints/The-Factor-Two-Hardness-Threshold-for-Vertex-Cover-September-23-2026/paper.pdf)
- [Constant-factor hardness of Min-UnCut](https://github.com/openai/math/blob/main/preprints/Constant-factor-hardness-of-Min-UnCut-September-23-2026/paper.pdf)
- [Constant-factor hardness of directed feedback vertex set](https://github.com/openai/math/blob/main/preprints/Constant-factor-hardness-of-directed-feedback-vertex-set-September-23-2026/paper.pdf)

</details>

<a name="r103"></a>

### 103 · Exact derandomization of logarithmic space: $`\mathsf L=\mathsf{RL}=\mathsf{BPL}`$

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/103.md) · 1 paper

L = BPL: anything a computer can solve with randomness and very little memory (logarithmic space) can be solved with the same memory and no randomness at all. A landmark in derandomization.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Exact derandomization of logarithmic space: L = RL = BPL](https://github.com/openai/math/blob/main/preprints/Exact-Derandomization-of-Logarithmic-Space-L-equals-RL-equals-BPL-September-23-2026/paper.pdf)

</details>

<a name="r104"></a>

### 104 · Quasipolynomial algorithms for mean-payoff, stochastic and parity games

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/104.md) · 4 papers

In mean-payoff games, two players push a token around a graph collecting rewards, and the question is who can guarantee a positive long-run average. Whether this can be solved in polynomial time is a famous open question. This gives quasipolynomial algorithms (2^{O(log² L)} steps) for plain, stochastic, and parity versions, including optimal stationary strategies.

- **Quant trading:** 🟡 *Background.* A prop challenge is a one-player problem against chance (reach +$3,000 before the trailing drawdown), which ordinary dynamic programming solves exactly; these two-player mean-payoff algorithms are not needed. Checking whether state-dependent sizing could help is check 5 in the [NQ playbook](NQ-PROP-TRIO.md).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (4)</summary>

- [Turn-Based Stochastic Mean-Payoff Games in Deterministic Quasipolynomial Time](https://github.com/openai/math/blob/main/preprints/Turn-Based-Stochastic-Mean-Payoff-Games-in-Deterministic-Quasipolynomial-Time-October-5-2026/stochastic-mean-payoff-games.pdf)
- [Mean-payoff parity games in quasipolynomial time](https://github.com/openai/math/blob/main/preprints/Mean-payoff-parity-games-in-quasipolynomial-time-October-5-2026/mean-payoff-parity.pdf)
- [Deterministic quasipolynomial-time mean-payoff games](https://github.com/openai/math/blob/main/preprints/Deterministic-quasipolynomial-time-mean-payoff-games-September-25-2026/paper.pdf)
- [Randomized quasipolynomial-time mean-payoff games](https://github.com/openai/math/blob/main/preprints/Randomized-quasipolynomial-time-mean-payoff-games-September-25-2026/paper.pdf)

</details>

<a name="r105"></a>

### 105 · Perfect completeness for 2-to-1 games

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/105.md) · 1 paper

This proves Khot's 2-to-1 Games Conjecture with perfect completeness: it is NP-hard to tell fully satisfiable instances of these constraint games from ones where almost nothing can be satisfied.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Perfect completeness for 2-to-1 games](https://github.com/openai/math/blob/main/preprints/Perfect-completeness-for-2-to-1-games-September-23-2026/paper.pdf)

</details>

<a name="r106"></a>

### 106 · Hardness of coloring three-colorable graphs

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/106.md) · 1 paper

Even when a graph is known to be colourable with 3 colours, finding a colouring with any fixed number of colours (say 1,000) is NP-hard. This settles a classic hardness question.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Hardness of finding large independent sets in three-colorable graphs](https://github.com/openai/math/blob/main/preprints/Hardness-of-finding-large-independent-sets-in-three-colorable-graphs-September-24-2026/Hardness-of-finding-large-independent-sets-in-three-colorable-graphs-September-24-2026.pdf)

</details>

<a name="r107"></a>

### 107 · Matrix multiplication with exponent at most 9/4

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/107.md) · 3 papers

The matrix multiplication exponent ω is pushed from about 2.371 down to at most 9/4 = 2.25 over ℂ. In theory, n×n matrices can be multiplied in about n^2.25 steps. These are "galactic" algorithms with astronomically large hidden constants.

- **Quant trading:** ⚪ *No practical link:* Covariance, regression and PCA will not get faster from this at real sizes.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (3)</summary>

- [An Upper Bound of 9/4 for the Matrix Multiplication Exponent](https://github.com/openai/math/blob/main/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/paper.pdf)
- [Complex Matrix Multiplication Below 2.258 and Rectangular Bounds](https://github.com/openai/math/blob/main/preprints/Complex-Matrix-Multiplication-Below-2.258-and-Rectangular-Bounds-September-24-2026/Complex-Matrix-Multiplication-Below-2.258-and-Rectangular-Bounds-September-24-2026.pdf)
- [Staggered extraction for exact matrix multiplication over every field](https://github.com/openai/math/blob/main/preprints/Staggered-extraction-for-exact-matrix-multiplication-over-every-field-September-24-2026/Staggered-extraction-for-exact-matrix-multiplication-over-every-field-September-24-2026.pdf)

</details>

<a name="r108"></a>

### 108 · A cubic permanent–determinant lower bound

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/108.md) · 1 paper

The permanent-versus-determinant problem is the algebraic version of P vs NP. This proves that writing the n×n permanent as a determinant, even approximately, needs a matrix of size at least c·n³, the first cubic lower bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A cubic lower bound for border determinantal complexity of the permanent](https://github.com/openai/math/blob/main/preprints/A-cubic-lower-bound-for-border-determinantal-complexity-of-the-permanent-September-24-2026/A-cubic-lower-bound-for-border-determinantal-complexity-of-the-permanent-September-24-2026.pdf)

</details>

<a name="r109"></a>

### 109 · Integer multiplication below $`n\log n`$

Not formally verified · 1 paper

This multiplies two n-bit integers in slightly less than n·log n time, disproving the Schönhage–Strassen optimality conjecture in the multitape Turing machine model. The saving factor (log n)^κ with κ = 2^−182 is purely theoretical.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Integer multiplication below n log n](https://github.com/openai/math/blob/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/paper.pdf)

</details>

<a name="r110"></a>

### 110 · Optimal-order randomized <i>k</i>-server on arbitrary metrics

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/110.md) · 2 papers

In the k-server problem, k servers (think repair trucks) must move to serve requests that arrive one at a time at points of a space, keeping total travel close to the best plan made in hindsight. This proves randomized strategies within O(log² k) of hindsight exist on every space, the optimal order. The extra additive travel cost can be enormous.

- **Quant trading:** ⚪ *No practical link:* Moving a resting order costs nothing like travel distance, and you do not have to fill at every price, so k-server gives no benchmark for order ladders or grids.
- **Politeia:** 🟡 *Background.* Dispatching k mobile units (inspectors, repair crews, mobile service vans) to requests that appear over time is literally k-server. Background for any live dispatch view; real dispatch uses simple heuristics such as nearest-available plus rebalancing.

<details><summary>Papers (2)</summary>

- [Squared-logarithmic randomized k-server on arbitrary metrics](https://github.com/openai/math/blob/main/preprints/Squared-logarithmic-randomized-k-server-on-arbitrary-metrics-September-24-2026/Squared-logarithmic-randomized-k-server-on-arbitrary-metrics-September-24-2026.pdf)
- [Uniform computation of the squared-logarithmic k-server bound](https://github.com/openai/math/blob/main/preprints/Uniform-computation-of-the-squared-logarithmic-k-server-bound-September-24-2026/Uniform-computation-of-the-squared-logarithmic-k-server-bound-September-24-2026.pdf)

</details>

<a name="r111"></a>

### 111 · One-sample matroid prophet inequalities against an almighty adversary

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/111.md) · 1 paper

In a prophet inequality, values arrive one at a time and you must accept or reject each on the spot, subject to limits on what combination you may keep (a "matroid": for example at most k items, or at most one per category). This shows that seeing just one past sample per item is enough to guarantee a constant fraction of the hindsight optimum, even against an adversary who knows everything. The constant is 2^−310, so it proves possibility rather than giving a usable guarantee.

- **Quant trading:** 🟡 *Background.* The setting needs each value to be visible at decision time, independent and non-negative, under a "matroid" limit. A trade's P&L is unknown at entry and can be negative, and prop-trio's binding limits (one position per chart, a shared daily loss limit) are not matroids. For a plain "at most k" cap, usable single-sample rules already existed; the 2^−310 constant only proves existence.
- **Politeia:** 🟡 *Background.* Proposals or volunteer offers that arrive over time, with caps (budget slots, one per district) and on-the-spot decisions: set thresholds from last cycle's data. Framing for "rolling approval" flows.

<details><summary>Papers (1)</summary>

- [One Sample Suffices for Matroid Prophet Inequalities against an Almighty Adversary](https://github.com/openai/math/blob/main/preprints/One-Sample-Suffices-for-Matroid-Prophet-Inequalities-against-an-Almighty-Adversary-September-23-2026/final.pdf)

</details>

<a name="r112"></a>

### 112 · Beyond the square-root exponent for depth-three circuits

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/112.md) · 1 paper

This gives an explicit function that needs more than 2^{ω(√n)} gates in depth-3 OR–AND–OR circuits, breaking a long-standing barrier for circuit lower bounds.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Beyond the Square-Root Exponent for Depth-Three Boolean Circuits](https://github.com/openai/math/blob/main/preprints/Beyond-the-Square-Root-Exponent-for-Depth-Three-Boolean-Circuits-September-23-2026/main.pdf)

</details>

<a name="r113"></a>

### 113 · Approximate counting and entropy of perfect matchings

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/113.md) · 2 papers

Counting perfect matchings (ways to pair up all vertices of a graph) exactly is #P-hard. This gives the first efficient randomized approximate counter (an FPRAS) for every graph, a decades-old open problem, plus a sharp entropy bound.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* Fair random pairing (citizens for deliberation pairs, mentors, reviewers) when only some pairings are allowed. Efficient approximate counting implies near-uniform random sampling of valid pairings, so every allowed pairing is almost equally likely, a fairness promise you can state publicly. A practical version would need engineering.

<details><summary>Papers (2)</summary>

- [A Fully Polynomial Randomized Approximation Scheme for Perfect Matchings in General Graphs](https://github.com/openai/math/blob/main/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/main.pdf)
- [Entropy and Face Dimension of the Perfect-Matching Polytope](https://github.com/openai/math/blob/main/preprints/Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026/main.pdf)

</details>

<a name="r114"></a>

### 114 · Approximate counting of common integer polymatroid bases

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/114.md) · 2 papers

This gives an efficient randomized approximate counter for the common "bases" of two matroids or polymatroids (for example, structures that are valid in two systems at once).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An FPRAS for Common Integer Polymatroid Bases with Binary Capacities](https://github.com/openai/math/blob/main/preprints/An-FPRAS-for-Common-Integer-Polymatroid-Bases-with-Binary-Capacities-October-5-2026/polymatroid-fpras.pdf)
- [Approximate counting of common bases of two matroids](https://github.com/openai/math/blob/main/preprints/Approximate-counting-of-common-bases-of-two-matroids-September-23-2026/main.pdf)

</details>

<a name="r115"></a>

### 115 · Sampling and counting contingency tables with arbitrary margins

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/115.md) · 2 papers

A contingency table here is a grid of non-negative whole numbers with fixed row totals and fixed column totals. This gives an exact uniformly random sampler, and an efficient approximate counter, for any sizes and any totals.

- **Quant trading:** 🟡 *Background.* Careful: the new sampler is uniform over tables with fixed totals, which is not the right null for "does this pattern cluster in this regime?". That null is hypergeometric (shuffle the labels, or use Patefield's sampler). The classical label-shuffle test is worth running on S3's overnight-bias thirds; see check 4 in the [NQ playbook](NQ-PROP-TRIO.md).
- **Politeia:** 🟢 *Testable idea.* Two strong uses. (1) Privacy: release synthetic tables (say, service use by district × age band) that match the published totals exactly without exposing real records. (2) Audits: test whether a district × option table of votes or usage is surprising given its totals.

<details><summary>Papers (2)</summary>

- [Exact Uniform Sampling of Contingency Tables with Arbitrary Margins](https://github.com/openai/math/blob/main/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/main.pdf)
- [An FPRAS for Cell-Bounded Contingency Tables](https://github.com/openai/math/blob/main/preprints/An-FPRAS-for-Cell-Bounded-Contingency-Tables-September-24-2026/main.pdf)

</details>

<a name="r116"></a>

### 116 · Uniform black-box noncommutative identity testing across characteristics

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/116.md) · 3 papers

This gives deterministic black-box tests for whether a noncommutative formula is secretly zero, uniformly across all field characteristics.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Uniform Matrix Hitting Points in Every Positive Characteristic](https://github.com/openai/math/blob/main/preprints/Uniform-Matrix-Hitting-Points-in-Every-Positive-Characteristic-October-4-2026/uniform-matrix-hitting-points-positive-characteristic.pdf)
- [One Rational Matrix Hitting Point for Noncommutative Formulas](https://github.com/openai/math/blob/main/preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026.pdf)
- [Polynomial Hitting Lists for Noncommutative Rational Formulas](https://github.com/openai/math/blob/main/preprints/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026.pdf)

</details>

<a name="r117"></a>

### 117 · Uniform sparsest cut: hardness and semidefinite gaps

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/117.md) · 2 papers

Sparsest cut asks for the weakest bottleneck that splits a network into two parts, relative to their sizes. This proves even constant-factor approximation is NP-hard, and that the standard semidefinite relaxation can be off by about √(log n).

- **Quant trading:** 🟡 *Background.* Clustering assets by cutting a correlation network at its weakest bottleneck is a sparsest-cut problem. There is no constant-factor guarantee in general, so treat spectral or semidefinite cluster splits as heuristics and check them with stability tests.
- **Politeia:** 🟡 *Background.* The same goes for community maps: "where does this community split?" has no guaranteed near-optimal answer. Show such splits as suggestions, not facts.

<details><summary>Papers (2)</summary>

- [Constant-factor hardness of uniform sparsest cut](https://github.com/openai/math/blob/main/preprints/Constant-factor-hardness-of-uniform-sparsest-cut-September-24-2026/Constant-factor-hardness-of-uniform-sparsest-cut-September-24-2026.pdf)
- [Near-square-root logarithmic integrality gaps for uniform sparsest cut](https://github.com/openai/math/blob/main/preprints/Near-square-root-logarithmic-integrality-gaps-for-uniform-sparsest-cut-September-24-2026/Near-square-root-logarithmic-integrality-gaps-for-uniform-sparsest-cut-September-24-2026.pdf)

</details>

<a name="r118"></a>

### 118 · Bin packing and unbounded configuration-LP gaps

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/118.md) · 1 paper

Bin packing means fitting items into as few bins as possible. This shows the popular linear-programming lower bound can be off by any fixed additive amount, and that approximating within a fixed additive amount is NP-hard.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Additive hardness and unbounded configuration gaps in bin packing](https://github.com/openai/math/blob/main/preprints/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026.pdf)

</details>

<a name="r119"></a>

### 119 · The Courtade–Kumar and Hellinger conjectures

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/119.md) · 2 papers

If you compress n random bits into a single yes/no bit, which compression keeps the most information about a noisy copy of the input? Courtade and Kumar conjectured the answer is to just copy one bit (a "dictator"). This proves it, along with the related Hellinger conjecture.

- **Quant trading:** ⚪ *No practical link:* Combining noisy indicators of one hidden direction is a different setting (Condorcet): a majority of independent, equally accurate, better-than-chance indicators beats any single one, and with unequal accuracy you weight by log-odds. If a combined signal fails, look at correlation between indicators, unequal accuracy and overfitting.
- **Politeia:** 🟡 *Background.* This connects to a classic tension in voting theory: majority vote is the most stable summary under noise, yet the summary carrying the most information about individual inputs is the "dictator". Good material for a civic explainer on why one-number summaries of public opinion lose information, and why to show the full distribution.

<details><summary>Papers (2)</summary>

- [Sharp binary-information contraction on the discrete cube](https://github.com/openai/math/blob/main/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/main.pdf)
- [Hellinger contraction with arbitrary Boolean output bias](https://github.com/openai/math/blob/main/preprints/Hellinger-contraction-with-arbitrary-Boolean-output-bias-September-24-2026/main.pdf)

</details>

<a name="r120"></a>

### 120 · Almost-linear-time exact matching and prescribed-degree factors in general graphs

Not formally verified · 1 paper

Maximum matching (pairing up as many vertices as possible) in any graph is solved in almost-linear time, a landmark speed-up over the classic m·√n bound.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* Fast exact matching at city scale (volunteers to tasks, residents to appointment slots) when compatibility is yes or no. Existing algorithms already handle realistic sizes; this mostly removes worst-case worries.

<details><summary>Papers (1)</summary>

- [Almost-Linear-Time Maximum-Cardinality Matching in General Graphs](https://github.com/openai/math/blob/main/preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-September-24-2026/main.pdf)

</details>

<a name="r121"></a>

### 121 · Almost-linear approximation of edit distance

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/121.md) · 1 paper

Edit distance (the fewest single-character edits that turn one string into another) is approximated within 1 + ε in almost-linear time. Exact edit distance is believed to need about quadratic time, so this is close to the best possible.

- **Quant trading:** 🟡 *Background.* If you turn sessions into symbol strings (for example a 64-state regime code), edit distance finds historical analogues that match up to shifts and insertions. This says approximate edit distance can scale to very long histories in principle. At normal data sizes, ordinary dynamic programming is fine.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [An Almost-Linear Approximation Scheme for Edit Distance](https://github.com/openai/math/blob/main/preprints/An-Almost-Linear-Approximation-Scheme-for-Edit-Distance-September-24-2026/paper.pdf)

</details>

<a name="r122"></a>

### 122 · Quantitative trace-reconstruction bounds with a uniform decoder

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/122.md) · 3 papers

Trace reconstruction: recover a hidden binary string from many copies, each with random deletions. This proves n^{Ω(log log n)} copies are needed (so no polynomial number suffices), and gives quasipolynomial algorithms.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Uniform quasipolynomial-time trace reconstruction](https://github.com/openai/math/blob/main/preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/uniform-trace-reconstruction.pdf)
- [A latest-anchor induction with spectrally compact masks for worst-case trace reconstruction](https://github.com/openai/math/blob/main/preprints/A-latest-anchor-induction-with-spectrally-compact-masks-for-worst-case-trace-reconstruction-October-5-2026/paper.pdf)
- [Quantitative lower bounds for trace reconstruction](https://github.com/openai/math/blob/main/preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/paper.pdf)

</details>

<a name="r124"></a>

### 124 · Polynomial-time scheduling on three identical machines

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/124.md) · 1 paper

Scheduling unit-length jobs with "this before that" constraints on 3 identical machines to finish as early as possible has been open since Garey and Johnson (1979). This solves it in polynomial time.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Polynomial-Time Algorithm for Three-Machine Unit-Job Scheduling](https://github.com/openai/math/blob/main/preprints/A-polynomial-time-algorithm-for-three-machine-unit-job-scheduling-September-24-2026/paper.pdf)

</details>

<a name="r125"></a>

### 125 · The metric <i>k</i>-median approximation threshold and recovery

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/125.md) · 2 papers

In k-median you open k facilities among candidate sites so that the total distance from every client to its nearest open facility is as small as possible. This gives a (1 + 2/e + ε) ≈ 1.736 approximation, and shows that is the best possible unless P = NP.

- **Quant trading:** 🟡 *Background.* k-medoids clustering of market days (pick k representative days) is the same problem. Useful for choosing "representative regimes" for scenario tests.
- **Politeia:** 🟢 *Testable idea.* This is the "where should the next k clinics, libraries or polling stations go?" question on a map. The result fixes the gold-standard guarantee (about 1.74× optimal). In practice, use local-search or integer-programming solvers at city scale, and show citizens the total travel distance each option implies: a simple, honest comparison view.

<details><summary>Papers (2)</summary>

- [Single-exponential recovery and bounded-price strictness for metric k-median](https://github.com/openai/math/blob/main/preprints/Single-Exponential-Recovery-and-Bounded-Price-Strictness-for-Metric-k-Median-September-24-2026/paper.pdf)
- [The approximation threshold for metric k-median](https://github.com/openai/math/blob/main/preprints/The-Approximation-Threshold-for-Metric-k-Median-September-24-2026/main.pdf)

</details>

<a name="r126"></a>

### 126 · Exponential semidefinite complexity of perfect matching

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/126.md) · 1 paper

This proves every exact semidefinite description of the perfect-matching polytope must be exponentially large, answering Rothvoss's question negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Exponential PSD rank of positively shifted matching matrices](https://github.com/openai/math/blob/main/preprints/Exponential-PSD-rank-of-positively-shifted-matching-matrices-October-5-2026/shifted-matching-psd.pdf)

</details>

<a name="r127"></a>

### 127 · Average sensitivity of polynomial threshold functions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/127.md) · 1 paper

A polynomial threshold function decides yes or no from the sign of a degree-d polynomial in n inputs that are each ±1; a weighted vote is the degree-1 case. This proves that, on average, at most 8d·√n of the n inputs are "pivotal" (flipping that one input changes the outcome). This is the Gotsman–Linial conjecture.

- **Quant trading:** ⚪ *No practical link:* The linear-rule (degree 1) case was already known (Gotsman–Linial 1994), and the bound assumes inputs are independent fair coin flips, which market features are not. To see how much one condition in a rule matters, drop it and re-run the backtest.
- **Politeia:** 🟡 *Background.* For any weighted-vote rule over n voters, the expected number of pivotal voters is at most 8√n. So an individual's chance of being decisive in a large vote is typically about 1/√n or less. A crisp, honest fact for civic-education screens.

<details><summary>Papers (1)</summary>

- [Average sensitivity of polynomial threshold functions](https://github.com/openai/math/blob/main/preprints/Average-Sensitivity-of-Polynomial-Threshold-Functions-September-25-2026/main.pdf)

</details>

<a name="r128"></a>

### 128 · A factor-two approximation for shortest common superstring

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/128.md) · 1 paper

The shortest common superstring problem asks for the shortest string containing every given string. This gives a long-conjectured factor-2 approximation in polynomial time.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Polynomial-Time 2-Approximation for Shortest Common Superstring](https://github.com/openai/math/blob/main/preprints/A-Polynomial-Time-2-Approximation-for-Shortest-Common-Superstring-September-24-2026/paper.pdf)

</details>

<a name="r129"></a>

### 129 · Exponential state costs for two-way automata

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/129.md) · 2 papers

This proves exponential lower bounds on the number of states two-way finite automata need for certain tasks, resolving the Sakoda–Sipser conjecture over growing alphabets.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An exponential state lower bound for two-way nondeterministic complementation](https://github.com/openai/math/blob/main/preprints/An-exponential-state-lower-bound-for-two-way-nondeterministic-complementation-September-25-2026/paper.pdf)
- [An exponential two-way deterministic state lower bound for one-way liveness](https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/main.pdf)

</details>

<a name="r130"></a>

### 130 · Exact Fourier transforms below $`n\log n`$

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/130.md) · 2 papers

This computes the exact discrete Fourier transform in fewer than n·log n operations. The saving factor is (log n)^(10^−13), so it is purely theoretical.

- **Quant trading:** ⚪ *No practical link:* FFT-based filters and spectral analysis will not get faster from this.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (2)</summary>

- [An explicit power saving for the exact discrete Fourier transform](https://github.com/openai/math/blob/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/main.pdf)
- [Finite tensor savings and exact Fourier circuits](https://github.com/openai/math/blob/main/preprints/Finite-tensor-savings-and-exact-Fourier-circuits-September-25-2026/main.pdf)

</details>

<a name="r131"></a>

### 131 · Rapid mixing of graph switches for every degree sequence

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/131.md) · 1 paper

Random networks with a prescribed degree sequence (everyone keeps their number of links) can be generated by repeatedly swapping pairs of edges. This proves the swapping process mixes in polynomial time for every degree sequence (the Kannan–Tetali–Vempala conjecture), and gives an exact uniform sampler.

- **Quant trading:** ⚪ *No practical link:* Degree-preserving rewiring is a poor null for thresholded correlation networks: they are more clustered than random graphs with the same degrees (Zalesky, Fornito & Bullmore 2012). Compare against null correlation matrices (for example a one-factor model) and check that clusters are stable across time instead.
- **Politeia:** 🟡 *Background.* Use the same check for civic networks (who co-signs whose proposals): before showing "communities" or "influencers", compare against degree-preserving random rewiring.

<details><summary>Papers (1)</summary>

- [Polynomial mixing of the switch chain for every graphical degree sequence](https://github.com/openai/math/blob/main/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/main.pdf)

</details>

<a name="r132"></a>

### 132 · A superquadratic separation of sensitivity and block sensitivity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/132.md) · 1 paper

This builds Boolean functions whose block sensitivity grows faster than the square of their sensitivity, disproving the quadratic strengthening of the Sensitivity Conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A superquadratic separation between sensitivity and block sensitivity](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/paper.pdf)

</details>

<a name="r133"></a>

### 133 · The computational complexity of Weisfeiler–Leman refinement

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/133.md) · 4 papers

Weisfeiler–Leman refinement underlies graph-isomorphism heuristics and limits what graph neural networks can tell apart. This proves unconditional n^{Ω(k)} time lower bounds for it, and EXPTIME-completeness when k is part of the input.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Parity lifts and bounded-treewidth witnesses for Weisfeiler–Leman equivalence](https://github.com/openai/math/blob/main/preprints/Parity-lifts-and-bounded-treewidth-witnesses-for-Weisfeiler-Leman-equivalence-September-25-2026/paper.pdf)
- [The complexity of identifying a graph by Weisfeiler–Leman refinement](https://github.com/openai/math/blob/main/preprints/The-complexity-of-identifying-a-graph-by-Weisfeiler-Leman-refinement-September-25-2026/paper.pdf)
- [Unconditional time lower bounds for Weisfeiler–Leman equivalence](https://github.com/openai/math/blob/main/preprints/Unconditional-time-lower-bounds-for-Weisfeiler-Leman-equivalence-September-25-2026/paper.pdf)
- [Variable-dimension Weisfeiler–Leman equivalence on general and subcubic graphs](https://github.com/openai/math/blob/main/preprints/Variable-dimension-Weisfeiler-Leman-equivalence-on-general-and-subcubic-graphs-September-25-2026/paper.pdf)

</details>

<a name="r134"></a>

### 134 · Generalized star height at most three

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/134.md) · 3 papers

Every regular language can be written as a generalized regular expression (with complement allowed) using at most three nested Kleene stars, an absolute bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Finite Monoid Computations and a Uniform Generalized Star-Height Bound](https://github.com/openai/math/blob/main/preprints/Finite-Monoid-Computations-and-a-Uniform-Generalized-Star-Height-Bound-September-25-2026/Finite-Monoid-Computations-and-a-Uniform-Generalized-Star-Height-Bound-September-25-2026.pdf)
- [Generalized Star Height at Most Four](https://github.com/openai/math/blob/main/preprints/Generalized-Star-Height-at-Most-Four-September-25-2026/Generalized-Star-Height-at-Most-Four-September-25-2026.pdf)
- [Generalized Star Height at Most Three](https://github.com/openai/math/blob/main/preprints/Generalized-Star-Height-at-Most-Three-September-25-2026/article.pdf)

</details>

<a name="r135"></a>

### 135 · Homogeneous depth-five lower bounds for iterated matrix multiplication

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/135.md) · 1 paper

The (1,1) entry of a product of n matrices of variables needs n^{Θ(√n)} gates in homogeneous depth-5 arithmetic circuits, a sharp lower bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Homogeneous depth-five lower bounds for iterated matrix multiplication](https://github.com/openai/math/blob/main/preprints/Homogeneous-depth-five-lower-bounds-for-iterated-matrix-multiplication-September-25-2026/Homogeneous-depth-five-lower-bounds-for-iterated-matrix-multiplication-September-25-2026.pdf)

</details>

<a name="r136"></a>

### 136 · A quasilinear PCP theorem for PPAD

Not formally verified · 1 paper

This proves a quasilinear-size PCP theorem for PPAD, the complexity class behind finding Nash equilibria and fixed points: approximate solutions can be checked robustly and locally.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The PCP-for-PPAD conjecture: a quasilinear reduction](https://github.com/openai/math/blob/main/preprints/The-PCP-for-PPAD-conjecture-a-quasilinear-reduction-September-25-2026/paper.pdf)

</details>

<a name="r137"></a>

### 137 · One-tape time simulation in two-fifths-power space

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/137.md) · 1 paper

Any time-T computation of a one-tape machine can be simulated in about T^{2/5} memory, improving the previous square-root bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Simulating One-Tape Time in Two-Fifths-Power Space](https://github.com/openai/math/blob/main/preprints/Simulating-One-Tape-Time-in-Two-Fifths-Power-Space-September-25-2026/article.pdf)

</details>

<a name="r138"></a>

### 138 · Subset Sum in $`O(2^{0.49n})`$ time

Not formally verified · 2 papers

Subset Sum (choose numbers from a list that add up to a target) is solved in 2^{0.49n} time in the worst case. This is the first improvement on the 2^{n/2} "meet in the middle" barrier from 1974.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* Choosing projects whose costs add up exactly to a budget is a Subset Sum problem. Worst-case cost drops to 2^{0.49n}, which is still exponential. At realistic participatory-budget sizes, standard knapsack or integer-programming solvers are what you use.

<details><summary>Papers (2)</summary>

- [Subset Sum in Time $`O(2^{0.49n})`$ ](https://github.com/openai/math/blob/main/preprints/Subset-Sum-in-Time-2-power-0-49n-October-4-2026/subset-sum.pdf)
- [A Low-Space Algorithm for Worst-Case Subset Sum](https://github.com/openai/math/blob/main/preprints/A-Low-Space-Algorithm-for-Worst-Case-Subset-Sum-September-26-2026/paper.pdf)

</details>

<a name="r139"></a>

### 139 · Subpolynomial query complexity for log-concave sampling

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/139.md) · 1 paper

Sampling from log-concave distributions (well-behaved bell-like shapes) using gradient queries: the number of queries can grow more slowly than any power of the dimension, so the optimal exponent is zero.

- **Quant trading:** ⚪ *No practical link:* It counts gradient queries only, allows unlimited computation between them, and needs a very well-conditioned target with a known minimizer. It does not make Langevin or HMC samplers faster in practice.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Subpolynomial query complexity for well-conditioned log-concave sampling](https://github.com/openai/math/blob/main/preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/article.pdf)

</details>

<a name="r140"></a>

### 140 · Memory–sample lower bounds for noiseless Gaussian regression

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/140.md) · 6 papers

A one-pass learner with limited memory (about d² bits) needs on the order of d·log(1/ε) exact Gaussian measurements to recover an unknown direction to accuracy ε.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (6)</summary>

- [Memory and precision in noiseless Gaussian regression](https://github.com/openai/math/blob/main/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/paper.pdf)
- [Posterior replicas and conditional information in Gaussian regression](https://github.com/openai/math/blob/main/preprints/Posterior-replicas-and-conditional-information-in-Gaussian-regression-September-27-2026/paper.pdf)
- [Localization costs and information growth for exact Gaussian observations](https://github.com/openai/math/blob/main/preprints/Localization-costs-and-information-growth-for-exact-Gaussian-observations-September-27-2026/paper.pdf)
- [Projection moments, positive cap domination, and Riesz estimates on the sphere](https://github.com/openai/math/blob/main/preprints/Projection-moments-positive-cap-domination-and-Riesz-estimates-on-the-sphere-September-27-2026/paper.pdf)
- [Replacing Gaussian observations in memory-constrained inference](https://github.com/openai/math/blob/main/preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/paper.pdf)
- [Subsphere methods for memory-sample lower bounds in noiseless Gaussian regression](https://github.com/openai/math/blob/main/preprints/Subsphere-methods-for-memory-sample-lower-bounds-in-noiseless-Gaussian-regression-September-27-2026/paper.pdf)

</details>

<a name="r141"></a>

### 141 · Existential–universal real sentences in the counting hierarchy

Not formally verified · 1 paper

Deciding the truth of sentences about real numbers with one ∃∀ quantifier alternation lies in the counting hierarchy, a strong new upper bound for the existential theory of the reals.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Existential–universal real sentences in the counting hierarchy](https://github.com/openai/math/blob/main/preprints/Existential-universal-real-sentences-in-the-counting-hierarchy-October-4-2026/etr-counting-hierarchy.pdf)

</details>

<a name="r142"></a>

### 142 · Deterministic polynomial factorization over prime fields

Not formally verified · 1 paper

This factors any polynomial over a prime field 𝔽_p deterministically in polynomial time, with no randomness and no Riemann-hypothesis assumption. It is a long-standing open problem; randomized algorithms have existed for decades.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Deterministic Polynomial Factorization over Prime Fields](https://github.com/openai/math/blob/main/preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/Deterministic-Polynomial-Factorization-over-Prime-Fields.pdf)

</details>

<a name="s-dynamical-systems-and-ergodic-theory"></a>

## Dynamical systems and ergodic theory

<a name="r143"></a>

### 143 · Hilbert's sixteenth problem: uniform bounds for limit cycles

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/143.md) · 2 papers

The second half of Hilbert's 16th problem (1900) asks how many isolated cycles ("limit cycles") a planar polynomial vector field of degree n can have. This proves there is a finite maximum that depends only on n, one of the most famous open questions in dynamics. It also shows classical quintic Liénard systems have at most two.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Uniform bounds for planar polynomial limit cycles](https://github.com/openai/math/blob/main/preprints/uniform-bounds-for-planar-polynomial-limit-cycles-September-24-2026/uniform-bounds-for-planar-polynomial-limit-cycles-September-24-2026.pdf)
- [Two limit cycles for quintic Liénard systems](https://github.com/openai/math/blob/main/preprints/two-limit-cycles-for-quintic-lienard-systems-September-24-2026/two-limit-cycles-for-quintic-lienard-systems-September-24-2026.pdf)

</details>

<a name="r144"></a>

### 144 · Banach’s simple Lebesgue-spectrum problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/144.md) · 1 paper

Banach's simple Lebesgue spectrum problem: this builds a smooth, volume-preserving map of the 3-torus in which the past and future iterates of a single observable form a perfect orthonormal basis, so the dynamics is completely "spread out" yet built from one signal.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A smooth three-torus diffeomorphism with simple Lebesgue spectrum](https://github.com/openai/math/blob/main/preprints/A-smooth-three-torus-diffeomorphism-with-simple-Lebesgue-spectrum-September-23-2026/paper.pdf)

</details>

<a name="r145"></a>

### 145 · Rokhlin’s multiple-mixing problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/145.md) · 1 paper

A system is "mixing" if any two events become independent as the time gap between them grows. Rokhlin asked in 1949 whether that automatically makes any finite number of events jointly independent when all their gaps grow ("mixing of all orders"). This proves yes, for a single transformation.

- **Quant trading:** ⚪ *No practical link:* The proof gives no rate, so it cannot set a bootstrap block length or an effective sample size, and the usual return models already had this property. Watching autocorrelations die out does not test its hypothesis anyway. For honest pass-rate error bars in prop-trio, see check 6 in the [NQ playbook](NQ-PROP-TRIO.md).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Rokhlin's multiple-mixing problem for one transformation](https://github.com/openai/math/blob/main/preprints/Rokhlins-multiple-mixing-problem-for-one-transformation-September-23-2026/paper.pdf)

</details>

<a name="r146"></a>

### 146 · Positive metric entropy for the standard map

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/146.md) · 1 paper

The standard (Chirikov) map is a textbook model of chaos. This proves it has genuine chaos on a set of positive area (positive metric entropy) for every large enough parameter, Sinai's conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Positive Metric Entropy for the Standard Map at Large Parameters](https://github.com/openai/math/blob/main/preprints/Positive-Metric-Entropy-for-the-Standard-Map-at-Large-Parameters-September-23-2026/paper.pdf)

</details>

<a name="r147"></a>

### 147 · The near-boundary Birkhoff conjecture

Not formally verified · 2 papers

The Birkhoff conjecture says the only convex billiard tables whose trajectories near the edge are organized into smooth invariant curves are ellipses. This proves the near-boundary version.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Continuous Phase Foliations Create Analytic Caustic Collars](https://github.com/openai/math/blob/main/preprints/Continuous-Phase-Foliations-Create-Analytic-Caustic-Collars-September-24-2026/paper.pdf)
- [Rigidity of Smooth Billiards with a Continuous Caustic Collar](https://github.com/openai/math/blob/main/preprints/Rigidity-of-Smooth-Billiards-with-a-Continuous-Caustic-Collar-September-24-2026/paper.pdf)

</details>

<a name="r148"></a>

### 148 · The entropy-rate dimension formula for self-similar measures

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/148.md) · 1 paper

Self-similar measures are fractals made by repeatedly shrinking copies of themselves. This proves their dimension equals min(1, entropy rate ÷ average contraction), even when the copies overlap.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The entropy-rate dimension formula for self-similar measures on the line](https://github.com/openai/math/blob/main/preprints/The-entropy-rate-dimension-formula-for-self-similar-measures-on-the-line-September-24-2026/main.pdf)

</details>

<a name="r149"></a>

### 149 · Classwise permanence for weakly reversible mass-action systems

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/149.md) · 2 papers

For chemical reaction networks with mass-action kinetics (weakly reversible ones), this proves "permanence": every species' concentration eventually stays between fixed positive lower and finite upper bounds, so nothing dies out or blows up.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Uniform Permanence in Weakly Reversible Mass-Action Systems](https://github.com/openai/math/blob/main/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/permanence.pdf)
- [Boundedness and persistence of weakly reversible mass-action systems](https://github.com/openai/math/blob/main/preprints/Boundedness-and-persistence-of-weakly-reversible-mass-action-systems-September-25-2026/paper.pdf)

</details>

<a name="r150"></a>

### 150 · Weak mixing of triangular billiards with an irrational angle

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/150.md) · 2 papers

For a billiard ball in any triangle with at least one angle that is an irrational multiple of π, this proves the motion is weakly mixing: the ball eventually "forgets" where it started, in a statistical sense.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Weak mixing of triangular billiards with an irrational angle](https://github.com/openai/math/blob/main/preprints/Weak-mixing-of-triangular-billiards-with-an-irrational-angle-October-5-2026/weak-mixing-triangular-billiards.pdf)
- [Ergodicity of triangular billiards with an irrational angle](https://github.com/openai/math/blob/main/preprints/Ergodicity-of-triangular-billiards-with-an-irrational-angle-September-25-2026/Ergodicity-of-triangular-billiards-with-an-irrational-angle-September-25-2026.pdf)

</details>

<a name="r151"></a>

### 151 · A <i>C</i><sup>1</sup> counterexample to the entropy conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/151.md) · 1 paper

Shub's entropy conjecture says that maps which stretch topology (homology) a lot must be chaotic (positive topological entropy). This disproves it for C¹ maps.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A C^1 Counterexample to the Entropy Conjecture](https://github.com/openai/math/blob/main/preprints/A-C1-Counterexample-to-the-Entropy-Conjecture-September-25-2026/article.pdf)

</details>

<a name="r152"></a>

### 152 · Zero entropy does not guarantee a smooth positive-volume model

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/152.md) · 1 paper

This builds a zero-entropy (non-chaotic) system that cannot be realized as any smooth volume-preserving system on any manifold.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A zero-entropy system without a smooth positive-volume model](https://github.com/openai/math/blob/main/preprints/A-finite-entropy-system-without-a-smooth-positive-volume-model-September-25-2026/paper.pdf)

</details>

<a name="r153"></a>

### 153 · Arithmetic classification and non-Pisot singularity for Bernoulli convolutions

Not formally verified · 1 paper

Bernoulli convolutions are the distributions of random series Σ ±λⁿ with fair coin-flip signs. This classifies exactly when the result is smooth and when it is singular, and finds new singular cases (reciprocals of quartic Salem numbers).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Arithmetic classification and non-Pisot singularity for Bernoulli convolutions](https://github.com/openai/math/blob/main/preprints/Arithmetic-classification-and-non-Pisot-singularity-for-Bernoulli-convolutions-October-3-2026/paper.pdf)

</details>

<a name="r154"></a>

### 154 · Pointwise multiple ergodic averages for mixing transformations

Not formally verified · 4 papers

This proves that multiple ergodic averages (time averages of products like f(Tⁿx)·g(T²ⁿx)·…) converge at almost every point for mixing transformations, with the expected limit.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Pointwise Multiple Ergodic Averages for Mixing Transformations](https://github.com/openai/math/blob/main/preprints/Pointwise-Multiple-Ergodic-Averages-for-Mixing-Transformations-October-4-2026/multiple-ergodic-averages.pdf)
- [Pointwise convergence of fourfold ergodic averages for mixing transformations](https://github.com/openai/math/blob/main/preprints/Pointwise-convergence-of-fourfold-ergodic-averages-for-mixing-transformations-October-4-2026/fourfold-ergodic-averages.pdf)
- [Triple ergodic averages with distinct integer slopes](https://github.com/openai/math/blob/main/preprints/Triple-ergodic-averages-with-distinct-integer-slopes-October-4-2026/triple-ergodic-distinct-slopes.pdf)
- [Pointwise convergence of triple ergodic averages for mixing transformations](https://github.com/openai/math/blob/main/preprints/Pointwise-convergence-of-triple-ergodic-averages-for-mixing-transformations-October-4-2026/pointwise-triple-ergodic-averages-mixing-transformations.pdf)

</details>

<a name="s-combinatorics"></a>

## Combinatorics

<a name="r155"></a>

### 155 · A counterexample to periodic tiling in dimension three

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/155.md) · 1 paper

Periodic tiling conjecture: if one shape tiles space by sliding copies around, can it also tile in a repeating (periodic) pattern? This gives a counterexample in 3D, the smallest dimension where one can exist.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A translational tile with no fully periodic tiling in dimension three](https://github.com/openai/math/blob/main/preprints/A-translational-tile-with-no-fully-periodic-tiling-in-dimension-three-September-23-2026/paper.pdf)

</details>

<a name="r156"></a>

### 156 · Borsuk's conjecture fails in dimension nine

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/156.md) · 1 paper

Borsuk's conjecture says every bounded set in ℝ^d can be split into d + 1 pieces of smaller diameter. It was known to fail in dimension 64 and up; this shows it already fails in dimension 9.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A nine-dimensional counterexample to Borsuk's covering assertion](https://github.com/openai/math/blob/main/preprints/A-nine-dimensional-counterexample-to-Borsuks-covering-assertion-September-23-2026/paper.pdf)

</details>

<a name="r157"></a>

### 157 · Graph coloring, clique minors, and Colin de Verdière invariants

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/157.md) · 3 papers

Hadwiger's conjecture (1943), one of the most famous in graph theory, says any graph that needs k colours contains the complete graph K_k as a "minor". This disproves it, even in a fractional form. On the positive side, the list-colouring number is at most a constant times the Hadwiger number.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [A counterexample to Hadwiger's conjecture](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-Hadwigers-conjecture-September-23-2026/paper.pdf)
- [A counterexample to the Colin de Verdière chromatic conjecture](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-the-Colin-de-Verdiere-chromatic-conjecture-September-23-2026/paper.pdf)
- [A linear list-coloring bound in terms of the Hadwiger number](https://github.com/openai/math/blob/main/preprints/A-linear-list-coloring-bound-in-terms-of-the-Hadwiger-number-September-23-2026/paper.pdf)

</details>

<a name="r158"></a>

### 158 · The Euclidean plane cannot be colored with five colors

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/158.md) · 1 paper

Hadwiger–Nelson problem: how many colours are needed to paint the plane so that no two points exactly 1 apart share a colour? Known: between 5 and 7. This proves 5 colours are not enough, leaving only 6 or 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Euclidean plane is not five-colorable](https://github.com/openai/math/blob/main/preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf)

</details>

<a name="r159"></a>

### 159 · Erdős’s reciprocal-sum conjecture and quasipolynomial Szemerédi bounds

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/159.md) · 1 paper · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/quasipolynomial-arithmetic-progressions.pdf)

Erdős's famous conjecture (a \$5,000 Erdős problem): if a set of positive integers has Σ 1/n = ∞, as the primes do, it contains arithmetic progressions of every length. This proves it, with much better (quasipolynomial) bounds in Szemerédi's theorem.

- **Quant trading:** ⚪ *No practical link:* These are worst-case existence statements and do not explain spurious backtest patterns: random data contain such runs far below the forcing sizes. Spurious edges come from chance plus the number of things tried, a classical multiple-testing problem. In prop-trio the biggest search is the 728-mix sizing optimizer; see check 2 in the [NQ playbook](NQ-PROP-TRIO.md).
- **Politeia:** 🟡 *Background.* The same caution applies to civic dashboards: "striking" patterns in large datasets can be inevitable. Add a "could this be chance?" check before highlighting one.

<details><summary>Papers (1)</summary>

- [Quasipolynomial Bounds for Arithmetic Progressions](https://github.com/openai/math/blob/main/preprints/Quasipolynomial-Bounds-for-Arithmetic-Progressions-September-23-2026/paper.pdf)

</details>

<a name="r160"></a>

### 160 · Superexponential van der Waerden numbers

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/160.md) · 1 paper

The van der Waerden number W_r(k) is the shortest run of integers that forces a single-coloured k-term arithmetic progression in any r-colouring. This proves it grows faster than exponentially, answering Erdős.

- **Quant trading:** ⚪ *No practical link:* See [159](#r159).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Quantitative Superexponential Bounds for van der Waerden Numbers](https://github.com/openai/math/blob/main/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/paper.pdf)

</details>

<a name="r161"></a>

### 161 · Counterexamples to Sidorenko’s conjecture and the forcing conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/161.md) · 1 paper

Sidorenko's conjecture says a random graph contains the fewest copies of any bipartite pattern for its edge density. This disproves it with a 35-vertex counterexample, and also disproves the related "forcing" conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A counterexample to Sidorenko's conjecture](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r162"></a>

### 162 · Counterexamples to Ryser’s covering conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/162.md) · 2 papers

Ryser's conjecture bounds how many vertices are needed to touch every edge of certain hypergraphs. This disproves it for infinitely many sizes, and also disproves Gyárfás's tree-cover conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Balanced counterexamples to Ryser's conjecture at prime orders](https://github.com/openai/math/blob/main/preprints/Balanced-Counterexamples-to-Rysers-Conjecture-at-Prime-Orders-September-27-2026/paper.pdf)
- [A counterexample to Ryser's covering conjecture](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-Rysers-Covering-Conjecture-September-23-2026/paper.pdf)

</details>

<a name="r164"></a>

### 164 · Hindman’s finite sums and products conjecture

Not formally verified · 1 paper

Hindman's conjecture: however you colour the positive integers with finitely many colours, there are arbitrarily large finite sets whose subset sums and subset products all have the same colour. This proves it.

- **Quant trading:** ⚪ *No practical link:* See [159](#r159).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Monochromatic finite sums and products in the positive integers](https://github.com/openai/math/blob/main/preprints/Monochromatic-finite-sums-and-products-in-the-positive-integers-September-23-2026/paper.pdf)

</details>

<a name="r165"></a>

### 165 · The Harary–Hill and Zarankiewicz crossing-number formulas

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/165.md) · 2 papers

What is the fewest number of crossings when you draw the complete graph K_n (every pair connected) in the plane? Harary and Hill gave a formula, and Zarankiewicz did the same for K_{m,n} (Turán's brickyard problem). This proves both formulas: the classical drawings are optimal.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* For network diagrams: a dense "everyone linked to everyone" view has unavoidable crossings, at a now-known minimum. For dense relationship data use matrix (heat-map) or edge-bundled layouts instead of node-link drawings.

<details><summary>Papers (2)</summary>

- [The crossing number of complete graphs](https://github.com/openai/math/blob/main/preprints/The-crossing-number-of-complete-graphs-September-23-2026/paper.pdf)
- [The crossing number of complete bipartite graphs](https://github.com/openai/math/blob/main/preprints/The-crossing-number-of-complete-bipartite-graphs-September-23-2026/paper.pdf)

</details>

<a name="r166"></a>

### 166 · The higher-dimensional Erdős distinct-distances conjecture

Not formally verified · 1 paper

Erdős's distinct-distances problem in higher dimensions: any n points in ℝ^d determine at least c·n^{2/d} different distances, which matches the grid. Proven for every fixed d ≥ 3.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The higher-dimensional Erdős distinct-distances conjecture](https://github.com/openai/math/blob/main/preprints/The-higher-dimensional-Erdos-distinct-distances-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r167"></a>

### 167 · Planar distinct distances and unit-distance bounds

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/167.md) · 2 papers

In the plane, this proves almost every point of an n-point set sees nearly n different distances (the weak pinned version), and improves the unit-distance bound to O(n^{4/3−δ}), the first progress since 1984.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The weak pinned planar distance theorem](https://github.com/openai/math/blob/main/preprints/The-weak-pinned-planar-distance-theorem-September-23-2026/paper.pdf)
- [A power saving for planar unit distances](https://github.com/openai/math/blob/main/preprints/A-power-saving-for-planar-unit-distances-September-23-2026/paper.pdf)

</details>

<a name="r168"></a>

### 168 · Combinatorial invariance of Kazhdan–Lusztig polynomials

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/168.md) · 1 paper

Kazhdan–Lusztig polynomials are central objects in representation theory. The combinatorial invariance conjecture (1980s) says they depend only on the shape of a certain ordered interval. This proves it in full generality.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Combinatorial invariance of Kazhdan–Lusztig polynomials](https://github.com/openai/math/blob/main/preprints/Combinatorial-Invariance-of-Kazhdan-Lusztig-Polynomials-September-24-2026/paper.pdf)

</details>

<a name="r169"></a>

### 169 · Shareshian–Wachs elementary positivity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/169.md) · 1 paper

This proves the Shareshian–Wachs refinement of the Stanley–Stembridge conjecture: chromatic quasisymmetric functions of unit interval graphs expand positively in the elementary basis, with an explicit counting rule.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Elementary positivity of chromatic quasisymmetric functions](https://github.com/openai/math/blob/main/preprints/Elementary-Positivity-of-Chromatic-Quasisymmetric-Functions-September-24-2026/paper.pdf)

</details>

<a name="r170"></a>

### 170 · Sharp logarithmic exponents for off-diagonal Ramsey numbers

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/170.md) · 2 papers

The off-diagonal Ramsey number r(s, t) is the smallest group size that forces s mutual friends or t mutual strangers. For each fixed s ≥ 5, this pins down its growth in t, including the logarithmic factor.

- **Quant trading:** ⚪ *No practical link:* See [159](#r159).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (2)</summary>

- [The sharp logarithmic exponent of r(5,t)](https://github.com/openai/math/blob/main/preprints/The-Sharp-Logarithmic-Exponent-of-r-5-t-September-24-2026/paper.pdf)
- [Sharp logarithmic exponents for fixed off-diagonal Ramsey numbers](https://github.com/openai/math/blob/main/preprints/Sharp-Logarithmic-Exponents-for-Fixed-Off-Diagonal-Ramsey-Numbers-September-24-2026/paper.pdf)

</details>

<a name="r171"></a>

### 171 · The hypercube Ramsey conjecture

Not formally verified · 1 paper

The Burr–Erdős hypercube conjecture: the Ramsey number of the n-dimensional cube graph is only a constant times its number of vertices (2ⁿ). Proven.

- **Quant trading:** ⚪ *No practical link:* See [159](#r159).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [The hypercube Ramsey number has linear order](https://github.com/openai/math/blob/main/preprints/The-hypercube-Ramsey-number-has-linear-order-September-23-2026/paper.pdf)

</details>

<a name="r172"></a>

### 172 · Classification of finite Euclidean Ramsey configurations

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/172.md) · 1 paper

This classifies exactly which finite point patterns are "Euclidean Ramsey", meaning they appear in a single colour in every finite colouring of high-dimensional space, and disproves the Leader–Russell–Walters conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A classification of finite Euclidean Ramsey configurations](https://github.com/openai/math/blob/main/preprints/A-classification-of-finite-Euclidean-Ramsey-configurations-September-23-2026/paper.pdf)

</details>

<a name="r173"></a>

### 173 · Seymour’s second-neighborhood conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/173.md) · 1 paper

Seymour's second-neighbourhood conjecture: in any directed network with no two-way links, some vertex reaches at least as many vertices in exactly two steps as in one step. This proves it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A proof of Seymour’s second-neighborhood conjecture](https://github.com/openai/math/blob/main/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r174"></a>

### 174 · Deterministic construction of strong thin spanning trees

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/174.md) · 2 papers

The strong thin-tree conjecture: every k-edge-connected graph has a spanning tree that uses only about a C/k fraction of the edges of every cut. This proves it, with a polynomial-time construction. Thin trees are a key tool for travelling-salesman approximation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The strong thin tree conjecture](https://github.com/openai/math/blob/main/preprints/The-strong-thin-tree-conjecture-September-23-2026/paper.pdf)
- [A polynomial-time construction of strong thin trees](https://github.com/openai/math/blob/main/preprints/A-polynomial-time-construction-of-strong-thin-trees-September-23-2026/paper.pdf)

</details>

<a name="r175"></a>

### 175 · Talagrand’s expectation thresholds, discrete convexity, and graph decompositions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/175.md) · 3 papers

For random structures, this proves the "integral" and "fractional" expectation thresholds agree up to a constant (a Talagrand conjecture), resolves Talagrand's discrete-convexity conjecture, and proves a graph-decomposition conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Graph Decompositions at the Integral Expectation Threshold](https://github.com/openai/math/blob/main/preprints/Graph-Decompositions-at-the-Integral-Expectation-Threshold-October-5-2026/graph-threshold-decompositions.pdf)
- [Integral and fractional expectation thresholds are equivalent](https://github.com/openai/math/blob/main/preprints/Integral-and-fractional-expectation-thresholds-are-equivalent-September-23-2026/paper.pdf)
- [Talagrand’s discrete-convexity conjecture](https://github.com/openai/math/blob/main/preprints/Talagrands-discrete-convexity-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r176"></a>

### 176 · The second Kahn–Kalai conjecture with an edge-count bound

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/176.md) · 1 paper

The second Kahn–Kalai conjecture: the edge density at which a random graph contains a copy of H is at most a log factor above an easy expectation bound. This proves it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The second Kahn–Kalai conjecture](https://github.com/openai/math/blob/main/preprints/The-second-Kahn-Kalai-conjecture-September-24-2026/paper.pdf)

</details>

<a name="r177"></a>

### 177 · Bounded-degree coboundary expanders

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/177.md) · 1 paper

This builds bounded-degree "coboundary expanders" (high-dimensional cousins of expander graphs) in every dimension. These matter for quantum error-correcting codes and property testing.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Bounded-degree coboundary expanders in every dimension](https://github.com/openai/math/blob/main/preprints/Bounded-degree-coboundary-expanders-in-every-dimension-September-24-2026/paper.pdf)

</details>

<a name="r178"></a>

### 178 · Deterministic nonbipartite Ramanujan graphs in every fixed degree

Not formally verified · 1 paper

Ramanujan graphs are the best possible expanders: sparse networks with the fastest possible mixing and no bottlenecks. This constructs them deterministically, for every degree d ≥ 3 and every large even size, in a non-bipartite form.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* If Politeia ever links local groups or delegates in a sparse network (who passes information to whom), Ramanujan graphs are the gold standard: few links, fast spread, no bottlenecks. A deterministic construction means the network design is reproducible and auditable.

<details><summary>Papers (1)</summary>

- [Deterministic nonbipartite Ramanujan graphs in every fixed degree](https://github.com/openai/math/blob/main/preprints/Deterministic-nonbipartite-Ramanujan-graphs-in-every-fixed-degree-September-23-2026/paper.pdf)

</details>

<a name="r179"></a>

### 179 · The circulant Hadamard and Barker-sequence conjectures

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/179.md) · 1 paper

Ryser's circulant Hadamard conjecture: a circulant ±1 matrix with orthogonal rows exists only in sizes 1 and 4. Proven. As a result, "Barker sequences" (binary codes with tiny autocorrelation, used in radar) exist only at the known lengths 2, 3, 4, 5, 7, 11, 13.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The circulant Hadamard conjecture](https://github.com/openai/math/blob/main/preprints/The-circulant-Hadamard-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r180"></a>

### 180 · Barnette’s Hamiltonian-cycle conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/180.md) · 1 paper

Barnette's conjecture: every cubic, bipartite, planar, 3-connected graph has a Hamiltonian cycle (a tour visiting every vertex exactly once). Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Paired states and Hamiltonian cycles in cubic bipartite planar graphs](https://github.com/openai/math/blob/main/preprints/Paired-states-and-Hamiltonian-cycles-in-cubic-bipartite-planar-graphs-September-24-2026/paper.pdf)

</details>

<a name="r181"></a>

### 181 · The Erdős–Gallai cycle-decomposition conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/181.md) · 1 paper

The Erdős–Gallai conjecture: the edges of any n-vertex graph can be split into at most C·n cycles and single edges. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A linear cycle-and-edge decomposition of every graph](https://github.com/openai/math/blob/main/preprints/A-linear-cycle-and-edge-decomposition-of-every-graph-September-24-2026/main.pdf)

</details>

<a name="r182"></a>

### 182 · Power savings for intersective polynomial differences and prime arguments

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/182.md) · 3 papers

Sets of integers that avoid having two members differ by a polynomial value (for example a perfect square) must be small. This proves power-saving bounds, including when the polynomial is evaluated at primes.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [A power saving for intersective polynomial differences with an exponent depending only on the degree](https://github.com/openai/math/blob/main/preprints/A-power-saving-for-intersective-polynomial-differences-with-an-exponent-depending-only-on-the-degree-October-5-2026/power-saving-intersective-polynomial-differences.pdf)
- [A Power Saving for Polynomial Differences at Prime Arguments](https://github.com/openai/math/blob/main/preprints/A-Power-Saving-for-Polynomial-Differences-at-Prime-Arguments-October-5-2026/prime-argument-polynomial-differences.pdf)
- [A power saving for square-difference-free sets](https://github.com/openai/math/blob/main/preprints/A-power-saving-for-square-difference-free-sets-September-24-2026/paper.pdf)

</details>

<a name="r183"></a>

### 183 · Power savings for planar halving lines and <i>k</i>-sets

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/183.md) · 1 paper

Halving lines split a planar point set into two equal halves. This proves there are at most O(n^{4/3−ε}) of them (for points with no three on a line), the first improvement in decades.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A power saving for planar halving lines](https://github.com/openai/math/blob/main/preprints/A-power-saving-for-planar-halving-lines-September-25-2026/main.pdf)

</details>

<a name="r184"></a>

### 184 · Correspondence coloring with a fixed forbidden subgraph

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/184.md) · 2 papers

Graphs that avoid any fixed subgraph can be coloured with about Δ/log Δ colours (Alon–Krivelevich–Sudakov), and K_r-free graphs have large independent sets (Ajtai–Erdős–Komlós–Szemerédi). Both are proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Correspondence coloring graphs with a forbidden clique](https://github.com/openai/math/blob/main/preprints/Correspondence-Coloring-Graphs-with-a-Forbidden-Clique-October-5-2026/correspondence-coloring-forbidden-clique.pdf)
- [A logarithmic independence bound for clique-free graphs](https://github.com/openai/math/blob/main/preprints/A-Logarithmic-Independence-Bound-for-Clique-Free-Graphs-September-25-2026/paper.pdf)

</details>

<a name="r185"></a>

### 185 · Counterexamples to infinite matroid intersection and packing/covering

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/185.md) · 1 paper

The infinite matroid intersection and packing/covering conjectures are disproved, using two self-dual matroids on a countable set.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Counterexample to the Infinite Matroid Packing/Covering Conjecture](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-the-Infinite-Matroid-Packing-Covering-Conjecture-September-24-2026/paper.pdf)

</details>

<a name="r186"></a>

### 186 · Uniform influence and sharp thresholds for graph and hypergraph properties

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/186.md) · 2 papers

Friedgut–Kalai: every symmetric property of random graphs that only gets more likely as edges are added switches from "unlikely" to "almost certain" within a window of width O(1/log² n) of the edge probability, a sharp threshold. Proven, with hypergraph versions.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* When a feature only works once enough participants connect (for example, a discussion network becoming fully connected), expect a tipping point: the switch from rare to near-certain happens over a narrow range. Plan rollouts and dashboards for thresholds, not steady linear growth.

<details><summary>Papers (2)</summary>

- [A uniform influence bound for hypergraph properties](https://github.com/openai/math/blob/main/preprints/A-uniform-influence-bound-for-hypergraph-properties-October-5-2026/hypergraph-influences.pdf)
- [A Sharp Threshold Bound for Monotone Graph Properties](https://github.com/openai/math/blob/main/preprints/A-Sharp-Threshold-Bound-for-Monotone-Graph-Properties-September-25-2026/paper.pdf)

</details>

<a name="r187"></a>

### 187 · Snaky in 21 Maker moves

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/187.md) · 1 paper

In a Maker–Breaker game on an infinite grid (a tic-tac-toe relative), Maker can force the 6-cell "Snaky" shape within 21 of their own moves. This settles the last open case of Harary's achievement games.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Snaky in 21 Maker moves](https://github.com/openai/math/blob/main/preprints/Snaky-in-21-Maker-moves-September-25-2026/article.pdf)

</details>

<a name="r188"></a>

### 188 · The sharp terminal leave in random triangle removal

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/188.md) · 1 paper

Start from a complete graph and repeatedly delete a random triangle until none is left. About n^{3/2}/(2√2) edges remain at the end, as conjectured.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The sharp terminal leave in random triangle removal](https://github.com/openai/math/blob/main/preprints/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026.pdf)

</details>

<a name="r189"></a>

### 189 · Cycle–clique Ramsey numbers

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/189.md) · 1 paper

This proves the exact Ramsey number for cycles versus cliques: R(C_m, K_n) = (m − 1)(n − 1) + 1 for all m ≥ n ≥ 3, except R(C_3, K_3) = 6.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Cycle--clique Ramsey numbers](https://github.com/openai/math/blob/main/preprints/Cycle-clique-Ramsey-numbers-September-25-2026/Cycle-clique-Ramsey-numbers-September-25-2026.pdf)

</details>

<a name="r190"></a>

### 190 · Polynomial removal fails for ordered binary matrices

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/190.md) · 1 paper

The "removal lemma" for ordered binary matrices cannot have polynomial bounds: this gives one fixed 66 × 66 pattern that defeats every proposed polynomial bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Polynomial removal fails for ordered binary matrices](https://github.com/openai/math/blob/main/preprints/Polynomial-removal-fails-for-ordered-binary-matrices-September-25-2026/paper.pdf)

</details>

<a name="r191"></a>

### 191 · A power improvement in the Heilbronn triangle lower bound

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/191.md) · 1 paper

Heilbronn's triangle problem: place n points in a square so the smallest triangle they form is as large as possible. This shows you can beat n^{−2} by a power, disproving the conjectured upper bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A power improvement in the Heilbronn triangle lower bound](https://github.com/openai/math/blob/main/preprints/A-power-improvement-in-the-Heilbronn-triangle-lower-bound-September-25-2026/main.pdf)

</details>

<a name="r192"></a>

### 192 · Boolean functions violate the square-root degree bound by arbitrary factors

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/192.md) · 1 paper

For Boolean functions, the total correlation with single input bits can exceed C·√(degree) for any constant C, disproving a proposed bound.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Unbounded Violations of the Square-Root Degree Bound](https://github.com/openai/math/blob/main/preprints/Unbounded-Violations-of-the-Square-Root-Degree-Bound-September-26-2026/Unbounded-Violations-of-the-Square-Root-Degree-Bound-September-26-2026.pdf)

</details>

<a name="s-algebra"></a>

## Algebra

<a name="r193"></a>

### 193 · Serre’s intersection-multiplicity conjecture

Not formally verified · 1 paper

Serre's intersection-multiplicity conjecture (positivity) is proven in the last open case, ramified mixed characteristic. Intersection multiplicities are how algebra counts how many times shapes meet.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Positivity of Serre's Intersection Multiplicity](https://github.com/openai/math/blob/main/preprints/Positivity-of-Serres-Intersection-Multiplicity-September-23-2026/paper.pdf)

</details>

<a name="r194"></a>

### 194 · Lech’s multiplicity conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/194.md) · 1 paper

Lech's conjecture (1960): multiplicity, a measure of how singular a point is, cannot go down along flat maps of local rings. Proven in every dimension and characteristic.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Lech's multiplicity conjecture](https://github.com/openai/math/blob/main/preprints/Lechs-multiplicity-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r195"></a>

### 195 · A counterexample to the small Cohen–Macaulay module conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/195.md) · 1 paper

The small Cohen–Macaulay module conjecture is disproved: this gives a three-dimensional complete local domain over ℂ with no nonzero finitely generated maximal Cohen–Macaulay module.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Complete Local Domain without a Small Cohen–Macaulay Module](https://github.com/openai/math/blob/main/preprints/A-Complete-Local-Domain-Without-a-Small-Cohen-Macaulay-Module-September-23-2026/paper.pdf)

</details>

<a name="r196"></a>

### 196 · A counterexample to Kaplansky’s zero-divisor conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/196.md) · 1 paper

Kaplansky's zero-divisor conjecture says that in the group algebra of a torsion-free group, two nonzero elements can never multiply to zero. This disproves it over the field with two elements.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Torsion-Free Group Algebra with Zero Divisors](https://github.com/openai/math/blob/main/preprints/A-Torsion-Free-Group-Algebra-with-Zero-Divisors-September-23-2026/paper.pdf)

</details>

<a name="r197"></a>

### 197 · A torsion-free group algebra that is not directly finite

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/197.md) · 4 papers · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/kaplansky-direct-finiteness-characteristic-two.pdf)

This disproves Kaplansky's direct-finiteness conjecture ("ab = 1 implies ba = 1" in group algebras) in characteristic 2 and in odd characteristic. The group used is non-sofic, which also settles the long-open question of whether non-sofic groups exist. Companion examples give an injective but non-surjective cellular automaton (disproving Gottschalk's surjunctivity conjecture) and disprove the group-ring determinant conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [A Torsion-Free Group Algebra That Is Not Directly Finite](https://github.com/openai/math/blob/main/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/direct-finiteness.pdf)
- [A Counterexample to Kaplansky's Direct-Finiteness Conjecture in Characteristic Two](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-Characteristic-Two-September-23-2026/paper.pdf)
- [A Counterexample to the Group-Ring Determinant Conjecture](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-the-Group-Ring-Determinant-Conjecture-September-23-2026/paper.pdf)
- [A Counterexample to Kaplansky's Direct-Finiteness Conjecture in Odd Characteristic](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-Odd-Characteristic-September-26-2026/paper.pdf)

</details>

<a name="r198"></a>

### 198 · A counterexample to finitistic-dimension finiteness

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/198.md) · 1 paper

The little finitistic dimension conjecture is disproved: this gives a finite-dimensional algebra whose modules have unboundedly large finite projective dimensions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An algebra of infinite little finitistic dimension](https://github.com/openai/math/blob/main/preprints/An-algebra-of-infinite-little-finitistic-dimension-September-23-2026/paper.pdf)

</details>

<a name="r199"></a>

### 199 · Counterexamples to Auslander–Reiten, Tachikawa and related homological conjectures

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/199.md) · 2 papers

This gives finite-dimensional algebras that disprove the Auslander–Reiten conjecture, Tachikawa's second conjecture and, via an associated algebra, the classical, generalized and strong Nakayama conjectures, plus related homological conjectures.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An explicit counterexample to the Auslander-Reiten conjecture](https://github.com/openai/math/blob/main/preprints/An-explicit-counterexample-to-the-Auslander-Reiten-conjecture-September-23-2026/paper.pdf)
- [A counterexample to Tachikawa's second conjecture](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-Tachikawas-second-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r200"></a>

### 200 · Eisenbud–Green–Harris and lex-plus-powers

Not formally verified · 2 papers

The Eisenbud–Green–Harris and lex-plus-powers conjectures (on the possible sizes and syzygies of polynomial ideals containing a regular sequence) are proven over every characteristic-zero field.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The Artinian Lex-Plus-Powers Betti Theorem](https://github.com/openai/math/blob/main/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/paper.pdf)
- [Commuting Division-Coefficient Forms and the Artinian Eisenbud--Green--Harris Conjecture](https://github.com/openai/math/blob/main/preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/paper.pdf)

</details>

<a name="r201"></a>

### 201 · A counterexample to Kurosh’s division-ring problem

Not formally verified · 1 paper

Kurosh's problem for division rings: this builds a division ring that is algebraic over its centre and generated by two elements, yet infinite-dimensional over its centre.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Counterexample to Kurosh’s Division-Ring Problem](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-Kuroshs-Division-Ring-Problem-September-23-2026/paper.pdf)

</details>

<a name="r202"></a>

### 202 · The blockwise Alperin weight conjecture

Not formally verified · 1 paper

Alperin's weight conjecture (blockwise numerical form) is proven for every finite group and prime. It counts the "modular" representations of a block by purely local data, and is a central conjecture in group representation theory.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Blockwise Alperin Weight Conjecture](https://github.com/openai/math/blob/main/preprints/The-Blockwise-Alperin-Weight-Conjecture-September-23-2026/paper.pdf)

</details>

<a name="r203"></a>

### 203 · Donovan's conjecture over fields and complete mixed-characteristic DVRs

Not formally verified · 2 papers

Donovan's conjecture: for blocks of finite groups with bounded defect group, there are only finitely many types up to Morita equivalence. Proven over algebraically closed fields and over Witt-vector rings.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Donovan's Conjecture over Algebraically Closed Fields](https://github.com/openai/math/blob/main/preprints/Donovans-Conjecture-over-Algebraic-Closures-of-Prime-Fields-September-24-2026/main.pdf)
- [Integral Donovan Finiteness over Witt Vectors](https://github.com/openai/math/blob/main/preprints/Integral-Donovan-Finiteness-over-Witt-Vectors-September-25-2026/main.pdf)

</details>

<a name="r204"></a>

### 204 · Tensor saturation for even spin groups

Not formally verified · 1 paper

This proves tensor-product "saturation" (factor one) for the even spin groups Spin(2n), the type-D case of the simply-laced saturation conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Tensor saturation for even spin groups](https://github.com/openai/math/blob/main/preprints/Tensor-Saturation-for-Even-Spin-Groups-September-24-2026/Tensor-Saturation-for-Even-Spin-Groups-September-24-2026.pdf)

</details>

<a name="r205"></a>

### 205 · Saxl’s conjecture and universal tensor squares

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/205.md) · 2 papers

Saxl's conjecture: the tensor square of the "staircase" representation of the symmetric group contains every irreducible representation. Proven; almost every S_n has such a universal representation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Universal Tensor Squares for Symmetric Groups](https://github.com/openai/math/blob/main/preprints/Universal-Tensor-Squares-for-Symmetric-Groups-September-24-2026/main.pdf)
- [A Cyclic Polytabloid Proof of Saxl's Conjecture](https://github.com/openai/math/blob/main/preprints/A-Cyclic-Polytabloid-Proof-of-Saxls-Conjecture-September-24-2026/paper.pdf)

</details>

<a name="r206"></a>

### 206 · Finite lattice representation and undecidability

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/206.md) · 2 papers

Some finite lattices are not the congruence lattice of any finite algebra, answering the Pálfy–Pudlák finite lattice representation problem negatively. Moreover, no algorithm can decide which ones are.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Finite congruence lattices: characterization and undecidability](https://github.com/openai/math/blob/main/preprints/Finite-Congruence-Lattices-Characterization-and-Undecidability-September-24-2026/paper.pdf)
- [A negative solution to the finite lattice representation problem](https://github.com/openai/math/blob/main/preprints/A-Negative-Solution-to-the-Finite-Lattice-Representation-Problem-September-24-2026/paper.pdf)

</details>

<a name="r207"></a>

### 207 · The ℓ¹-Bass conjecture for all discrete groups

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/207.md) · 2 papers

This proves the ℓ¹-Bass conjecture for every discrete group, and Kaplansky's idempotent conjecture over characteristic-zero domains for torsion-free groups.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The ℓ¹-Bass Conjecture for Discrete Groups](https://github.com/openai/math/blob/main/preprints/The-l1-Bass-Conjecture-for-Discrete-Groups-October-5-2026/l1-bass-conjecture.pdf)
- [The Bass trace conjecture and the characteristic-zero Kaplansky idempotent conjecture](https://github.com/openai/math/blob/main/preprints/The-Bass-trace-conjecture-for-complex-group-rings-September-24-2026/The-Bass-trace-conjecture-for-complex-group-rings-September-24-2026.pdf)

</details>

<a name="r208"></a>

### 208 · Finite symmetric tensor categories and the Verlinde tower

Not formally verified · 1 paper

Every finite symmetric tensor category in characteristic p maps faithfully to a higher Verlinde category, the finite case of the Benson–Etingof–Ostrik conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Fiber functors for finite symmetric tensor categories in positive characteristic](https://github.com/openai/math/blob/main/preprints/Fiber-functors-for-finite-symmetric-tensor-categories-in-positive-characteristic-September-24-2026/paper.pdf)

</details>

<a name="r209"></a>

### 209 · Integral counterexamples to Gersten’s conjecture

Not formally verified · 2 papers

Gersten's conjecture, an injectivity statement in algebraic K-theory, is disproved integrally by explicit two-dimensional ramified regular local rings.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An integral counterexample to Gersten's conjecture](https://github.com/openai/math/blob/main/preprints/An-Integral-Counterexample-to-Gerstens-Conjecture-September-25-2026/An-Integral-Counterexample-to-Gerstens-Conjecture-September-25-2026.pdf)
- [An integral degree-three Gersten counterexample](https://github.com/openai/math/blob/main/preprints/An-Integral-Degree-Three-Gersten-Counterexample-September-26-2026/paper.pdf)

</details>

<a name="r210"></a>

### 210 · Foulkes' conjecture for sixth powers and quadratic stabilization

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/210.md) · 2 papers

Foulkes' conjecture compares two ways of nesting symmetric powers. This proves the sixth case, and shows a canonical map becomes surjective once b ≥ a(a − 1).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Foulkes' conjecture for the sixth symmetric power](https://github.com/openai/math/blob/main/preprints/Foulkes-Conjecture-for-the-Sixth-Symmetric-Power-September-25-2026/main.pdf)
- [Quadratic stabilization of the canonical Foulkes--Howe map](https://github.com/openai/math/blob/main/preprints/Quadratic-Stabilization-of-the-Canonical-Foulkes-Howe-Map-September-25-2026/paper.pdf)

</details>

<a name="s-probability-and-statistical-mechanics"></a>

## Probability and statistical mechanics

<a name="r211"></a>

### 211 · The geometric phase diagram, diffusion, and spectra of random planar maps

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/211.md) · 7 papers

Random planar maps are random surfaces made by gluing polygons together. With Fortuin–Kasteleyn weights, this proves they converge to "Liouville quantum gravity" spheres when q ≤ 4 and collapse to a random tree when q > 4, and that random walks on them converge to Liouville Brownian motion.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (7)</summary>

- [Random Walks on Critical FK–Ising Maps and Liouville Brownian Motion](https://github.com/openai/math/blob/main/preprints/Random-Walks-on-Critical-FK-Ising-Maps-and-Liouville-Brownian-Motion-October-5-2026/fk-ising-walk-limit.pdf)
- [Spectral convergence for critical FK–Ising planar maps](https://github.com/openai/math/blob/main/preprints/Spectral-convergence-for-critical-FK-Ising-planar-maps-October-5-2026/spectral-convergence-critical-fk-ising-planar-maps.pdf)
- [A Linear Clock for Random Walk on Tree-Weighted Planar Maps](https://github.com/openai/math/blob/main/preprints/A-Linear-Clock-for-Random-Walk-on-Tree-Weighted-Planar-Maps-October-5-2026/linear-clock-random-walk-tree-weighted-planar-maps.pdf)
- [Canonical conformal limits of subcritical FK planar maps](https://github.com/openai/math/blob/main/preprints/Canonical-conformal-limits-of-subcritical-FK-planar-maps-September-24-2026/main.pdf)
- [The critical Liouville quantum sphere and geometric limits of FK maps at q=4](https://github.com/openai/math/blob/main/preprints/The-critical-Liouville-quantum-sphere-and-geometric-limits-of-FK-maps-at-q-equals-4-September-24-2026/main.pdf)
- [Metric-measure limits of subcritical FK and spanning-tree planar maps](https://github.com/openai/math/blob/main/preprints/Metric-measure-limits-of-subcritical-FK-and-spanning-tree-planar-maps-September-24-2026/main.pdf)
- [Brownian continuum random tree limits of finite Fortuin–Kasteleyn maps above four](https://github.com/openai/math/blob/main/preprints/Brownian-continuum-random-tree-limits-of-finite-Fortuin-Kasteleyn-maps-above-four-September-24-2026/main.pdf)

</details>

<a name="r212"></a>

### 212 · Planar first-passage geometry and the absence of bigeodesics

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/212.md) · 2 papers

First-passage percolation gives each edge of a grid a random travel time and studies the fastest routes. This proves no two-way infinite fastest route ("bigeodesic") exists in the plane, and that for exponential times the large-scale "ball" shape is strictly convex and smooth.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [No bigeodesics in planar first-passage percolation](https://github.com/openai/math/blob/main/preprints/No-bigeodesics-in-planar-first-passage-percolation-September-24-2026/main.pdf)
- [Strict convexity and differentiability of the planar exponential first-passage limit shape](https://github.com/openai/math/blob/main/preprints/Strict-convexity-and-differentiability-of-the-planar-exponential-first-passage-limit-shape-September-24-2026/main.pdf)

</details>

<a name="r213"></a>

### 213 · Critical percolation on every quasi-transitive graph

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/213.md) · 2 papers

Percolation: keep each edge of a lattice independently with probability p. Exactly at the critical p, is there an infinite connected cluster? This proves no, on the 3D cubic lattice (a famous open problem) and on every quasi-transitive graph.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Critical bond and site percolation on the cubic lattice](https://github.com/openai/math/blob/main/preprints/Critical-bond-and-site-percolation-on-the-cubic-lattice-September-24-2026/paper.pdf)
- [No percolation at criticality on quasi-transitive graphs](https://github.com/openai/math/blob/main/preprints/No-percolation-at-criticality-on-quasi-transitive-graphs-September-24-2026/paper.pdf)

</details>

<a name="r214"></a>

### 214 · The Benjamini–Schramm nonuniqueness conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/214.md) · 1 paper

On "tree-like" (non-amenable) graphs, there is a range of p where infinitely many infinite clusters coexist (p_c < p_u). This proves the Benjamini–Schramm conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Nonuniqueness of percolation on nonamenable quasi-transitive graphs](https://github.com/openai/math/blob/main/preprints/Nonuniqueness-of-percolation-on-nonamenable-quasi-transitive-graphs-September-24-2026/paper.pdf)

</details>

<a name="r215"></a>

### 215 · Canonical $`O(3)`$ continuum limit and exact $`O(4)`$ mass asymptotics

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/215.md) · 5 papers

This constructs the continuum limit of the 2D O(3) spin model, a quantum field theory with a mass gap, and finds the exact mass asymptotics for O(4). It is in the spirit of the Yang–Mills mass-gap problem, but in a simpler two-dimensional model.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5)</summary>

- [The canonical massive continuum limit of the two-dimensional O(3) model](https://github.com/openai/math/blob/main/preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/massive-continuum-o3.pdf)
- [An Isolated Particle Pole for the Two-Dimensional O(3) Spin Field](https://github.com/openai/math/blob/main/preprints/An-Isolated-Particle-Pole-for-the-Two-Dimensional-O3-Spin-Field-October-4-2026/o3-particle-pole.pdf)
- [Exact mass asymptotics for the two-dimensional O(4) lattice model](https://github.com/openai/math/blob/main/preprints/Exact-mass-asymptotics-for-the-two-dimensional-O4-lattice-model-October-5-2026/exact-mass-o4.pdf)
- [Sharp mass bounds for the two-dimensional O(4) model](https://github.com/openai/math/blob/main/preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/paper.pdf)
- [Exponential decay in two-dimensional classical O(n) models](https://github.com/openai/math/blob/main/preprints/Exponential-decay-in-two-dimensional-classical-On-models-September-23-2026/paper.pdf)

</details>

<a name="r216"></a>

### 216 · Critical and near-critical XY scaling and BKT universality

Not formally verified · 6 papers

For the XY model of planar spins and its Berezinskii–Kosterlitz–Thouless transition (Nobel Prize 2016), this proves the precise critical correlation decay r^(−1/4)(log r)^(1/8) and the predicted essential singularity of the correlation length.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (6)</summary>

- [The critical logarithmic correction for the planar XY model](https://github.com/openai/math/blob/main/preprints/The-critical-logarithmic-correction-for-the-planar-XY-model-October-5-2026/paper.pdf)
- [Critical Center Magnetization in the Planar XY Model](https://github.com/openai/math/blob/main/preprints/Critical-Center-Magnetization-in-the-Planar-XY-Model-October-5-2026/paper.pdf)
- [The Critical Spin Field of the Planar XY Model](https://github.com/openai/math/blob/main/preprints/The-Critical-Spin-Field-of-the-Planar-XY-Model-October-5-2026/paper.pdf)
- [Essential Singularity of the Correlation Length in the Planar XY Model](https://github.com/openai/math/blob/main/preprints/Essential-Singularity-of-the-Correlation-Length-in-the-Planar-XY-Model-October-5-2026/paper.pdf)
- [The critical correlation exponent of the planar XY model](https://github.com/openai/math/blob/main/preprints/The-critical-correlation-exponent-of-the-planar-XY-model-September-24-2026/paper.pdf)
- [BKT universality for height and planar spin fields](https://github.com/openai/math/blob/main/preprints/BKT-universality-for-height-and-planar-spin-fields-September-24-2026/paper.pdf)

</details>

<a name="r217"></a>

### 217 · The low-temperature Sherrington–Kirkpatrick fluctuation law

Not formally verified · 2 papers

For the Sherrington–Kirkpatrick spin glass at low temperature, this proves the free energy fluctuates on the predicted n^(1/6) scale, with a uniquely characterized limiting law.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The low-temperature Sherrington–Kirkpatrick free-energy limiting law](https://github.com/openai/math/blob/main/preprints/The-low-temperature-Sherrington-Kirkpatrick-free-energy-limiting-law-September-24-2026/The-low-temperature-Sherrington-Kirkpatrick-free-energy-limiting-law-September-24-2026.pdf)
- [The low-temperature Sherrington–Kirkpatrick fluctuation scale](https://github.com/openai/math/blob/main/preprints/The-low-temperature-Sherrington-Kirkpatrick-fluctuation-scale-September-24-2026/The-low-temperature-Sherrington-Kirkpatrick-fluctuation-scale-September-24-2026.pdf)

</details>

<a name="r218"></a>

### 218 · Conformal universality for weakly interacting and random-bond Ising models

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/218.md) · 6 papers

Universality for the Ising model: small changes to the interactions, or weak random disorder, do not change its critical large-scale picture (spin fields and SLE₃ interfaces).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (6)</summary>

- [Quenched SLE₃ limits for general weak random-bond Ising models](https://github.com/openai/math/blob/main/preprints/Quenched-SLE3-limits-for-general-weak-random-bond-Ising-models-October-5-2026/general-weak-random-bond-ising.pdf)
- [Quenched SLE₃ Universality for the Weak Random-Bond Ising Model](https://github.com/openai/math/blob/main/preprints/Quenched-SLE3-Universality-for-the-Weak-Random-Bond-Ising-Model-October-5-2026/quenched-sle3-weak-random-bond-ising.pdf)
- [Logarithmic Relative Fluctuations in the Weakly Disordered Planar Ising Model](https://github.com/openai/math/blob/main/preprints/Logarithmic-Relative-Fluctuations-in-the-Weakly-Disordered-Planar-Ising-Model-October-5-2026/critical-relative-second-moment-weak-random-bond-ising.pdf)
- [Conformal universality of bulk Ising correlations under weak interactions](https://github.com/openai/math/blob/main/preprints/Conformal-universality-of-bulk-Ising-correlations-under-weak-interactions-September-23-2026/paper.pdf)
- [SLE3 universality for weak finite-range Ising interactions](https://github.com/openai/math/blob/main/preprints/SLE3-universality-for-weak-finite-range-Ising-interactions-September-23-2026/paper.pdf)
- [Buffered comparison and stopping-band resolution in critical Ising](https://github.com/openai/math/blob/main/preprints/Buffered-comparison-and-stopping-band-resolution-in-critical-Ising-September-23-2026/paper.pdf)

</details>

<a name="r219"></a>

### 219 · GOE bulk universality for regular graphs with weak Anderson disorder

Not formally verified · 2 papers

The eigenvalues of a random d-regular graph (every vertex has d neighbours) follow the GOE random-matrix statistics at small scales, even for d = 3 and with weak random disorder added.

- **Quant trading:** ⚪ *No practical link:* Correlation-matrix cleaning rests on a different, older result (Marchenko–Pastur, for sample covariance matrices). This one is about the fine-scale spacing of eigenvalues of sparse random graphs and changes nothing there.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (2)</summary>

- [Fixed-energy universality for weak Anderson disorder on random regular graphs](https://github.com/openai/math/blob/main/preprints/Fixed-energy-universality-for-weak-Anderson-disorder-on-random-regular-graphs-October-5-2026/fixed-energy-universality-weak-anderson-disorder-random-regular-graphs.pdf)
- [GOE bulk universality for fixed-degree random regular graphs](https://github.com/openai/math/blob/main/preprints/GOE-bulk-universality-for-fixed-degree-random-regular-graphs-September-23-2026/paper.pdf)

</details>

<a name="r220"></a>

### 220 · Directional zero–one laws beyond iid environments and iid ballisticity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/220.md) · 3 papers

For a random walk in a random environment on ℤ^d, escaping in a given direction has probability 0 or 1, and escaping in a direction forces a positive limiting speed (the ballisticity conjecture).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [A directional zero–one law for finite-range-dependent random environments](https://github.com/openai/math/blob/main/preprints/A-directional-zero-one-law-for-finite-range-dependent-random-environments-October-5-2026/directional-zero-one-finite-range.pdf)
- [A directional zero–one law under strict ellipticity](https://github.com/openai/math/blob/main/preprints/A-directional-zero-one-law-under-strict-ellipticity-September-23-2026/paper.pdf)
- [Directional transience implies ballisticity](https://github.com/openai/math/blob/main/preprints/Directional-transience-implies-ballisticity-September-23-2026/paper.pdf)

</details>

<a name="r221"></a>

### 221 · The Mézard–Parisi formula for diluted spin glasses

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/221.md) · 1 paper · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/mezard-parisi-formula.pdf)

The Mézard–Parisi formula from physics gives the free energy of sparse ("diluted") spin glasses, a class that includes random-satisfiability-type models. This proves it under stated factorization and positivity assumptions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Mézard–Parisi formula for diluted spin glasses](https://github.com/openai/math/blob/main/preprints/The-Mezard-Parisi-formula-for-diluted-spin-glasses-September-23-2026/paper.pdf)

</details>

<a name="r222"></a>

### 222 · Perceptron free energies and microscopic jamming exponents

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/222.md) · 4 papers

A perceptron is the simplest neural network: a linear yes/no rule. "How many random patterns can it fit?" is a capacity question. This computes exact free energies for Ising and spherical perceptrons, and the "jamming" exponents at the critical density.

- **Quant trading:** 🟡 *Background.* The practical lesson is classical (Cover 1965: a linear rule with N weights can fit about 2N random labels), and these papers do not change it. The prop-trio version of "compare with shuffled labels" is a no-edge baseline: a zero-mean book still passes roughly 12–24% of Apex-style challenges, and S1's +40/−75 bracket alone gives about 65% winners with random entries. See check 1 in the [NQ playbook](NQ-PROP-TRIO.md).
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (4)</summary>

- [The free energy of the Ising random perceptron](https://github.com/openai/math/blob/main/preprints/The-free-energy-of-the-Ising-random-perceptron-September-24-2026/The-free-energy-of-the-Ising-random-perceptron-September-24-2026.pdf)
- [Microscopic jamming in the negative spherical perceptron](https://github.com/openai/math/blob/main/preprints/Microscopic-jamming-in-the-negative-spherical-perceptron-September-24-2026/Microscopic-jamming-in-the-negative-spherical-perceptron-September-24-2026.pdf)
- [The spherical perceptron with bi-orthogonally invariant disorder](https://github.com/openai/math/blob/main/preprints/The-spherical-perceptron-with-bi-orthogonally-invariant-disorder-September-24-2026/The-spherical-perceptron-with-bi-orthogonally-invariant-disorder-September-24-2026.pdf)
- [The free energy of the spherical random perceptron](https://github.com/openai/math/blob/main/preprints/The-free-energy-of-the-spherical-random-perceptron-September-24-2026/The-free-energy-of-the-spherical-random-perceptron-September-24-2026.pdf)

</details>

<a name="r223"></a>

### 223 · Random-cluster interfaces: critical, disordered, thermal, and natural-time scaling

Not formally verified · 6 papers

Interfaces in the critical random-cluster (FK) model converge to the random fractal curves SLE_κ, and nested loops converge to CLE_κ. This is conformal invariance of critical models for 0 < q ≤ 4.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (6)</summary>

- [Square-lattice FK interfaces and nested loops for 1 <= q < 4](https://github.com/openai/math/blob/main/preprints/Square-lattice-FK-interfaces-and-nested-loops-for-1-leq-q-lt-4-September-23-2026/paper.pdf)
- [Self-dual random-cluster interfaces below one](https://github.com/openai/math/blob/main/preprints/Self-dual-random-cluster-interfaces-below-one-September-23-2026/paper.pdf)
- [Quenched SLE Universality for Weakly Disordered FK–Ising Interfaces](https://github.com/openai/math/blob/main/preprints/Quenched-SLE-Universality-for-Weakly-Disordered-FK-Ising-Interfaces-October-5-2026/quenched-fk-ising.pdf)
- [Thermal FK–Ising interfaces and massive SLE](https://github.com/openai/math/blob/main/preprints/Thermal-FK-Ising-interfaces-and-massive-SLE-October-5-2026/paper.pdf)
- [Natural Occupation Measures for Critical Square-Lattice FK Interfaces](https://github.com/openai/math/blob/main/preprints/Natural-Occupation-Measures-for-Critical-Square-Lattice-FK-Interfaces-October-5-2026/natural-occupation-measures-critical-square-lattice-fk-interfaces.pdf)
- [Conformal Limits of Critical Square-Lattice Random-Cluster Interfaces](https://github.com/openai/math/blob/main/preprints/Conformal-Limits-of-Critical-Square-Lattice-Random-Cluster-Interfaces-October-5-2026/paper.pdf)

</details>

<a name="r224"></a>

### 224 · Critical and quenched near-critical universality for Poisson–Voronoi percolation

Not formally verified · 3 papers

For percolation on random Voronoi cells, this proves Cardy's formula for crossing probabilities and shows near-critical behaviour is universal.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [From critical crossings to quenched near-critical universality in Voronoi percolation](https://github.com/openai/math/blob/main/preprints/From-critical-crossings-to-quenched-near-critical-universality-in-Voronoi-percolation-October-5-2026/critical-crossings-quenched-near-critical-universality-voronoi-percolation.pdf)
- [A Pivotal Amplitude for Voronoi Percolation from Cardy's Formula](https://github.com/openai/math/blob/main/preprints/A-Pivotal-Amplitude-for-Voronoi-Percolation-from-Cardys-Formula-October-5-2026/voronoi-pivotal-amplitude.pdf)
- [Cardy’s formula for critical Poisson–Voronoi percolation](https://github.com/openai/math/blob/main/preprints/Cardys-formula-for-critical-Poisson-Voronoi-percolation-September-23-2026/paper.pdf)

</details>

<a name="r225"></a>

### 225 · Gaussian free field limits throughout the balanced six-vertex regime

Not formally verified · 1 paper

Height functions of the six-vertex model (a classic ice model) converge to the Gaussian free field throughout the balanced regime, with an exact variance constant 1/arcsin(c/2).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Gaussian free field limit of the balanced six-vertex model with variance multiplier 1/arcsin(c/2)](https://github.com/openai/math/blob/main/preprints/The-Gaussian-free-field-limit-of-the-balanced-six-vertex-model-with-variance-multiplier-1-over-arcsin-c-over-2-September-23-2026/The-Gaussian-free-field-limit-of-the-balanced-six-vertex-model-with-variance-multiplier-1-over-arcsin-c-over-2-September-23-2026.pdf)

</details>

<a name="r226"></a>

### 226 · The double-dimer loop ensemble converges to CLE<sub>4</sub>

Not formally verified · 1 paper

The loops formed by overlaying two random dimer tilings converge to the conformal loop ensemble CLE₄, the curves themselves and not just statistics about them.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The curve scaling limit of half-plane double dimers](https://github.com/openai/math/blob/main/preprints/The-curve-scaling-limit-of-half-plane-double-dimers-September-23-2026/paper.pdf)

</details>

<a name="r227"></a>

### 227 · Critical SK autocorrelation processes and dynamics across the temperature transition

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/227.md) · 8 papers

For the Sherrington–Kirkpatrick spin glass under heat-bath dynamics, this proves equilibrium is reached fast at high temperature (cutoff on the log n scale), in about n^(2/3) at the critical point, and only after stretched-exponential time at low temperature. "Critical slowing down" is made rigorous.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (8)</summary>

- [Universality of critical quench autocorrelations in the Sherrington–Kirkpatrick model](https://github.com/openai/math/blob/main/preprints/Universality-of-critical-quench-autocorrelations-in-the-Sherrington-Kirkpatrick-model-October-5-2026/main.pdf)
- [Functional universality of critical SK autocorrelations](https://github.com/openai/math/blob/main/preprints/Functional-universality-of-critical-SK-autocorrelations-October-5-2026/critical-sk-autocorrelations.pdf)
- [A spectral gap throughout the high-temperature Sherrington–Kirkpatrick phase](https://github.com/openai/math/blob/main/preprints/A-spectral-gap-throughout-the-high-temperature-Sherrington-Kirkpatrick-phase-September-24-2026/main.pdf)
- [Cutoff throughout the high-temperature Sherrington–Kirkpatrick phase](https://github.com/openai/math/blob/main/preprints/Cutoff-throughout-the-high-temperature-Sherrington-Kirkpatrick-phase-September-24-2026/paper.pdf)
- [Critical slowing down in the Sherrington–Kirkpatrick model](https://github.com/openai/math/blob/main/preprints/Critical-slowing-down-in-the-Sherrington-Kirkpatrick-model-September-24-2026/paper.pdf)
- [Stretched-exponential barriers for typical SK initial states](https://github.com/openai/math/blob/main/preprints/Stretched-exponential-barriers-for-typical-SK-initial-states-September-24-2026/paper.pdf)
- [A typical-start upper bound for low-temperature SK Glauber dynamics](https://github.com/openai/math/blob/main/preprints/A-typical-start-upper-bound-for-low-temperature-SK-Glauber-dynamics-September-24-2026/paper.pdf)
- [Critical mixing in the Sherrington–Kirkpatrick model](https://github.com/openai/math/blob/main/preprints/Critical-mixing-in-the-Sherrington-Kirkpatrick-model-September-25-2026/paper.pdf)

</details>

<a name="r228"></a>

### 228 · Continuum phase transitions for radial pair potentials

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/228.md) · 2 papers

This builds simple distance-based forces between particles in 3D that produce a genuine first-order phase transition (a jump, like boiling), answering Simon's question about continuum phase transitions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A continuum temperature singularity for a radial pair potential](https://github.com/openai/math/blob/main/preprints/A-continuum-temperature-singularity-for-a-radial-pair-potential-September-24-2026/paper.pdf)
- [A radial continuum phase transition with algebraic decay](https://github.com/openai/math/blob/main/preprints/A-radial-continuum-phase-transition-with-algebraic-decay-September-24-2026/paper.pdf)

</details>

<a name="r229"></a>

### 229 · Exact three- and four-state reconstruction thresholds and four-state tree capacity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/229.md) · 3 papers

Broadcasting on trees: a symbol is passed down a tree with noise at each step; can you guess the root from the leaves? This proves the exact threshold dλ² > 1 for 3- and 4-state models. Consequence: an exact threshold for detecting 3 communities in sparse networks (the stochastic block model).

- **Quant trading:** 🟡 *Background.* A reminder that community labels can be pure noise when the signal is weak. But the exact threshold is for an idealised sparse random network with three groups, so it is not a test you can run on a dense asset-correlation network.
- **Politeia:** 🟡 *Background.* Before showing "there are 3 camps in this discussion network", check the signal is above the detection threshold (a − b)² > 3(a + 2b), where a and b are the within-group and between-group link rates. Below it, any community map is noise.

<details><summary>Papers (3)</summary>

- [The Reconstruction Threshold for the Ferromagnetic Four-State Potts Model](https://github.com/openai/math/blob/main/preprints/The-Reconstruction-Threshold-for-the-Ferromagnetic-Four-State-Potts-Model-October-5-2026/four-state-potts.pdf)
- [A Capacity Criterion for Four-State Potts Reconstruction on Trees](https://github.com/openai/math/blob/main/preprints/A-Capacity-Criterion-for-Four-State-Potts-Reconstruction-on-Trees-October-5-2026/four-state-capacity.pdf)
- [The exact reconstruction threshold for the three-state symmetric channel](https://github.com/openai/math/blob/main/preprints/The-exact-reconstruction-threshold-for-the-three-state-symmetric-channel-September-25-2026/paper.pdf)

</details>

<a name="r230"></a>

### 230 · Exact Hausdorff gauges for SLE

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/230.md) · 2 papers

This finds the exact Hausdorff "gauge" for SLE curves, the precise way to measure the size of these random fractal curves, answering Schramm's question.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An exact Hausdorff gauge for SLE](https://github.com/openai/math/blob/main/preprints/An-exact-Hausdorff-gauge-for-SLE-September-25-2026/An-exact-Hausdorff-gauge-for-SLE-September-25-2026.pdf)
- [An explicit exact Hausdorff gauge for SLE](https://github.com/openai/math/blob/main/preprints/An-explicit-exact-Hausdorff-gauge-for-SLE-September-26-2026/An-explicit-exact-Hausdorff-gauge-for-SLE-September-26-2026.pdf)

</details>

<a name="r231"></a>

### 231 · The free uniform spanning forest is a factor of IID

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/231.md) · 1 paper

On every graph, the free uniform spanning forest can be produced by a local rule from independent random labels at the vertices (a "factor of IID"); the same holds for a broad class of determinantal processes.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The free uniform spanning forest is a factor of IID](https://github.com/openai/math/blob/main/preprints/The-free-uniform-spanning-forest-is-a-factor-of-IID-September-25-2026/The-free-uniform-spanning-forest-is-a-factor-of-IID-September-25-2026.pdf)

</details>

<a name="r232"></a>

### 232 · Gaussian fields and interfaces for triangular-lattice Lipschitz heights

Not formally verified · 3 papers · 🔧 proof repaired Oct 7

Random Lipschitz height functions on the triangular lattice converge to the Gaussian free field, and their interface converges to SLE₄ at a tuned boundary, confirming Schramm's predictions. Papers were revised on Oct 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Gaussian free-field limits of weighted integer Lipschitz heights](https://github.com/openai/math/blob/main/preprints/Gaussian-free-field-limits-of-weighted-integer-Lipschitz-heights-October-6-2026/paper.pdf)
- [The Gaussian free field limit of integer Lipschitz heights with two-arc boundary data](https://github.com/openai/math/blob/main/preprints/The-Gaussian-free-field-limit-of-integer-Lipschitz-heights-with-two-arc-boundary-data-October-6-2026/paper.pdf)
- [Uniform real Lipschitz surfaces on the triangular lattice](https://github.com/openai/math/blob/main/preprints/Uniform-real-Lipschitz-surfaces-on-the-triangular-lattice-October-6-2026/paper.pdf)

</details>

<a name="r233"></a>

### 233 · The joint critical Ashkin–Teller current limit

Not formally verified · 1 paper · 🔧 proof repaired Oct 7

This finds the joint scaling limit of heights and current clusters for the critical Ashkin–Teller model along its whole critical line. The paper was revised on Oct 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The joint scaling limit of critical Ashkin-Teller currents](https://github.com/openai/math/blob/main/preprints/The-joint-scaling-limit-of-critical-Ashkin-Teller-currents-October-6-2026/main.pdf)

</details>

<a name="r234"></a>

### 234 · All-temperature pressure of orthogonally invariant Ising spin glasses

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/234.md) · 1 paper

For spin glasses whose coupling matrix is a random rotation of a fixed spectrum, this gives an exact formula for the limiting free energy at every temperature.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [All-temperature pressure for orthogonally invariant Ising spin glasses](https://github.com/openai/math/blob/main/preprints/All-temperature-pressure-for-orthogonally-invariant-Ising-spin-glasses-September-25-2026/paper.pdf)

</details>

<a name="r235"></a>

### 235 · Limiting random SAT thresholds, sharp variance and computability

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/235.md) · 4 papers

Random k-SAT: a random logic formula with αn clauses switches sharply from satisfiable to unsatisfiable as α grows. This proves a limiting threshold exists for every k ≥ 3, that the hitting time has variance of order n, and that the 3-SAT threshold is computable. OpenAI credits Gaia Carenini, whose concurrent paper (public Oct 5, 2026) resolved threshold existence first.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [A Limiting Satisfiability Threshold for Every Fixed Clause Size](https://github.com/openai/math/blob/main/preprints/A-Limiting-Satisfiability-Threshold-for-Every-Fixed-Clause-Size-September-25-2026/article.pdf)
- [Linear Variance of the Random 3-SAT Hitting Time](https://github.com/openai/math/blob/main/preprints/Linear-Variance-of-the-Random-3-SAT-Hitting-Time-October-5-2026/linear-variance-of-the-random-3-sat-hitting-time.pdf)
- [Variance of the Random k-SAT Hitting Time](https://github.com/openai/math/blob/main/preprints/Variance-of-the-Random-k-SAT-Hitting-Time-September-27-2026/article.pdf)
- [Computing the Random 3-SAT Threshold](https://github.com/openai/math/blob/main/preprints/Computing-the-Random-3-SAT-Threshold-September-27-2026/article.pdf)

</details>

<a name="r236"></a>

### 236 · The exact factor-of-IID threshold for free Ising spins on trees

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/236.md) · 1 paper

For the Ising model on a regular tree, this finds exactly when the free state can be generated by a local rule from independent randomness: tanh β ≤ 1/√(d − 1).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The sharp factor-of-IID threshold for the free Ising model on regular trees](https://github.com/openai/math/blob/main/preprints/The-sharp-factor-of-IID-threshold-for-the-free-Ising-model-on-regular-trees-September-26-2026/article.pdf)

</details>

<a name="r237"></a>

### 237 · The three-quarter exponent for honeycomb self-avoiding walk

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/237.md) · 13 papers

A self-avoiding walk never revisits a point. This proves a random n-step self-avoiding walk on the honeycomb lattice spans a distance of about n^(3/4), Nienhuis's 1982 prediction (13 papers).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (13)</summary>

- [Radial transfer estimates and polygon length laws for honeycomb walks](https://github.com/openai/math/blob/main/preprints/Radial-transfer-estimates-and-polygon-length-laws-for-honeycomb-walks-September-26-2026/main.pdf)
- [Critical honeycomb chords with prescribed boundary endpoints](https://github.com/openai/math/blob/main/preprints/Critical-honeycomb-chords-with-prescribed-boundary-endpoints-September-26-2026/main.pdf)
- [Cylinder loop weights and planar nesting](https://github.com/openai/math/blob/main/preprints/Cylinder-loop-weights-and-planar-nesting-September-26-2026/main.pdf)
- [Mass and covering exponents for fixed-length honeycomb walks](https://github.com/openai/math/blob/main/preprints/Mass-and-covering-exponents-for-fixed-length-honeycomb-walks-September-26-2026/main.pdf)
- [Signed cylinder propagation and marked polygons on the honeycomb lattice](https://github.com/openai/math/blob/main/preprints/Signed-cylinder-propagation-and-marked-polygons-on-the-honeycomb-lattice-September-26-2026/main.pdf)
- [Cylinder amplitudes and logarithmic bridge-length windows on the honeycomb lattice](https://github.com/openai/math/blob/main/preprints/Cylinder-amplitudes-and-logarithmic-bridge-length-windows-on-the-honeycomb-lattice-September-26-2026/main.pdf)
- [Marked polygon correlations and one-arc bounds](https://github.com/openai/math/blob/main/preprints/Marked-polygon-correlations-and-one-arc-bounds-September-26-2026/main.pdf)
- [Disk transfer representations and confined bridge mass](https://github.com/openai/math/blob/main/preprints/Disk-transfer-representations-and-confined-bridge-mass-September-26-2026/main.pdf)
- [Polynomial vacuum representations and bridge mass for honeycomb walks](https://github.com/openai/math/blob/main/preprints/Polynomial-vacuum-representations-and-bridge-mass-for-honeycomb-walks-September-26-2026/main.pdf)
- [Renewal and changes of law for critical honeycomb walks](https://github.com/openai/math/blob/main/preprints/Renewal-and-changes-of-law-for-critical-honeycomb-walks-September-26-2026/main.pdf)
- [Critical strip-crossing mass on the honeycomb lattice](https://github.com/openai/math/blob/main/preprints/Critical-strip-crossing-mass-on-the-honeycomb-lattice-September-26-2026/main.pdf)
- [Uniform marked-polygon estimates and sharp finite bridge moments](https://github.com/openai/math/blob/main/preprints/Uniform-marked-polygon-estimates-and-sharp-finite-bridge-moments-September-26-2026/main.pdf)
- [Cap-selected amplitudes and triangle chords for honeycomb walks](https://github.com/openai/math/blob/main/preprints/Cap-selected-amplitudes-and-triangle-chords-for-honeycomb-walks-September-26-2026/main.pdf)

</details>

<a name="r238"></a>

### 238 · Optimal logarithmic mixing of the Thorp shuffle

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/238.md) · 12 papers

The Thorp shuffle cuts the deck in half and interleaves the halves, flipping a coin for each pair to decide which card goes first. This proves about log N shuffles randomize N = 2^d cards, the optimal order.

- **Quant trading:** ⚪ *No practical link.*
- **Politeia:** 🟡 *Background.* The Thorp shuffle is an engine behind "format-preserving encryption", which scrambles IDs while keeping their format (for example, pseudonymising record numbers). Faster provable mixing means security proofs need fewer rounds. Background only; use a vetted standard (such as NIST FF1) rather than rolling your own.

<details><summary>Papers (12)</summary>

- [Optimal-order mixing of the Thorp shuffle](https://github.com/openai/math/blob/main/preprints/Optimal-order-mixing-of-the-Thorp-shuffle-September-26-2026/paper.pdf)
- [Random coordinate frames and partial permutation laws](https://github.com/openai/math/blob/main/preprints/Random-coordinate-frames-and-partial-permutation-laws-September-26-2026/main.pdf)
- [From partial permutation information to Fourier bounds](https://github.com/openai/math/blob/main/preprints/From-partial-permutation-information-to-Fourier-bounds-September-26-2026/main.pdf)
- [Conditional information under deterministic coordinate sweeps](https://github.com/openai/math/blob/main/preprints/Conditional-information-under-deterministic-coordinate-sweeps-September-26-2026/main.pdf)
- [Conditional permutations in a revealed switching environment](https://github.com/openai/math/blob/main/preprints/Conditional-permutations-in-a-revealed-switching-environment-September-26-2026/paper.pdf)
- [Routing densities and representation contraction for Thorp sweeps](https://github.com/openai/math/blob/main/preprints/Routing-densities-and-representation-contraction-for-Thorp-sweeps-September-26-2026/paper.pdf)
- [Row&#8211;column symmetry and contraction of coordinate sweeps](https://github.com/openai/math/blob/main/preprints/Row-column-symmetry-and-contraction-of-coordinate-sweeps-September-26-2026/paper.pdf)
- [Random-subspace tests and trace smoothing for coordinate sweeps](https://github.com/openai/math/blob/main/preprints/Random-subspace-tests-and-trace-smoothing-for-coordinate-sweeps-September-26-2026/paper.pdf)
- [Compatibility entropy and the spectrum of a Thorp sweep](https://github.com/openai/math/blob/main/preprints/Compatibility-entropy-and-the-spectrum-of-a-Thorp-sweep-September-26-2026/paper.pdf)
- [Signed tensor densities and diagram budgets for the Thorp shuffle](https://github.com/openai/math/blob/main/preprints/Signed-tensor-densities-and-diagram-budgets-for-coordinate-sweeps-September-26-2026/paper.pdf)
- [Conditional coordinate sweeps and analytic transfer](https://github.com/openai/math/blob/main/preprints/Conditional-coordinate-sweeps-and-analytic-transfer-September-26-2026/main.pdf)
- [A strict four-row permanent inequality and permutation moments](https://github.com/openai/math/blob/main/preprints/A-strict-four-row-permanent-inequality-and-permutation-moments-September-26-2026/main.pdf)

</details>

<a name="r239"></a>

### 239 · Sharp singularity rates for symmetric random sign matrices

Not formally verified · 2 papers

A random symmetric matrix of ±1 entries is singular (determinant 0) with probability (1/2 + o(1))ⁿ, the sharp rate, with a matching formula for biased signs.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The sharp exponential rate of singularity for symmetric Bernoulli matrices](https://github.com/openai/math/blob/main/preprints/The-sharp-exponential-rate-of-singularity-for-symmetric-Bernoulli-matrices-October-3-2026/symmetric-bernoulli-singularity.pdf)
- [The sharp singularity rate for biased symmetric sign matrices](https://github.com/openai/math/blob/main/preprints/The-sharp-singularity-rate-for-biased-symmetric-sign-matrices-October-4-2026/biased-symmetric-sign-singularity.pdf)

</details>

<a name="s-mathematical-logic"></a>

## Mathematical logic

<a name="r240"></a>

### 240 · Shelah's eventual categoricity and the prescribed-threshold obstruction

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/240.md) · 2 papers

Shelah's eventual categoricity conjecture: if a class of mathematical structures has exactly one model (up to isomorphism) at one large size, it has exactly one at every larger size. Proven in ZFC.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A CH obstruction to a prescribed categoricity threshold](https://github.com/openai/math/blob/main/preprints/A-CH-Obstruction-to-a-Prescribed-Categoricity-Threshold-September-24-2026/paper.pdf)
- [Eventual categoricity for abstract elementary classes](https://github.com/openai/math/blob/main/preprints/Eventual-Categoricity-for-Abstract-Elementary-Classes-September-24-2026/paper.pdf)

</details>

<a name="r241"></a>

### 241 · Rigidity of the Turing degrees

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/241.md) · 1 paper

The Turing degrees rank problems by "what can compute what". This proves this ordering has no nontrivial symmetries (it is rigid), a long-open problem in computability theory.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Rigidity of the Turing degrees](https://github.com/openai/math/blob/main/preprints/Rigidity-of-the-Turing-degrees-September-24-2026/paper.pdf)

</details>

<a name="r242"></a>

### 242 · Single-fold Diophantine representations and undecidability under an at-most-one-solution promise

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/242.md) · 1 paper

Every computably enumerable set has a Diophantine representation with exactly one solution per member (single-fold). So Hilbert's 10th problem stays undecidable even under an "at most one solution" promise.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Single-fold Diophantine representations](https://github.com/openai/math/blob/main/preprints/Single-fold-Diophantine-representations-September-24-2026/paper.pdf)

</details>

<a name="r243"></a>

### 243 · Separating choiceless counting from polynomial time and witnessed choice

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/243.md) · 2 papers

Choiceless polynomial time with counting, a leading candidate logic for capturing polynomial time, cannot express whether a linear system over 𝔽₃ is solvable. This confirms the Blass–Gurevich–Shelah non-capture conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Choiceless polynomial time with counting does not capture polynomial time](https://github.com/openai/math/blob/main/preprints/Choiceless-polynomial-time-with-counting-does-not-capture-polynomial-time-September-23-2026/paper.pdf)
- [Witnessed symmetric choice is strictly stronger than choiceless polynomial time with counting](https://github.com/openai/math/blob/main/preprints/Witnessed-symmetric-choice-is-strictly-stronger-than-choiceless-polynomial-time-with-counting-September-24-2026/paper.pdf)

</details>

<a name="r244"></a>

### 244 · The Partition Principle does not imply Choice

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/244.md) · 1 paper

Without the axiom of choice, does the Partition Principle (if A maps onto B, then B fits inside A) imply full Choice? This is one of the oldest open problems in set theory. This shows it does not.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Partition Principle does not imply Choice](https://github.com/openai/math/blob/main/preprints/The-Partition-Principle-does-not-imply-Choice-September-24-2026/partition-principle-without-choice.pdf)

</details>

<a name="r245"></a>

### 245 · Weak normalization implies strong normalization in pure type systems

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/245.md) · 1 paper

In pure type systems (the logical foundation of proof assistants), if every term can be simplified to a normal form, then every simplification process terminates (weak implies strong normalization). The Barendregt–Geuvers–Klop conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Weak and strong normalization in pure type systems](https://github.com/openai/math/blob/main/preprints/Weak-and-strong-normalization-in-pure-type-systems-September-25-2026/paper.pdf)

</details>

<a name="s-group-theory"></a>

## Group theory

<a name="r246"></a>

### 246 · Cannon's conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/246.md) · 1 paper

Cannon's conjecture: any hyperbolic group whose boundary is a 2-sphere is essentially the fundamental group of a hyperbolic 3-manifold. One of the central problems of geometric group theory. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Modulus Proof of Cannon’s Conjecture](https://github.com/openai/math/blob/main/preprints/A-Modulus-Proof-of-Cannons-Conjecture-September-23-2026/paper.pdf)

</details>

<a name="r247"></a>

### 247 · An infinite finitely presented residually finite 2-group and a finitely presented nil algebra

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/247.md) · 2 papers

This builds an infinite, finitely presented group in which every element has finite order that is a power of 2, a negative answer to the finitely presented Burnside problem, plus a finitely presented nil algebra.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An infinite finitely presented residually finite 2-group](https://github.com/openai/math/blob/main/preprints/An-infinite-finitely-presented-residually-finite-2-group-October-5-2026/residually-finite-torsion.pdf)
- [An infinite finitely presented periodic group](https://github.com/openai/math/blob/main/preprints/An-infinite-finitely-presented-periodic-group-September-23-2026/paper.pdf)

</details>

<a name="r248"></a>

### 248 · Thompson's group <i>F</i> is nonamenable

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/248.md) · 1 paper

Thompson's group F (piecewise-linear maps of an interval with dyadic breakpoints) is proven non-amenable. This is a famous problem with a long history of claimed solutions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Thompson's group F is nonamenable](https://github.com/openai/math/blob/main/preprints/Thompsons-group-F-is-nonamenable-September-23-2026/paper.pdf)

</details>

<a name="r249"></a>

### 249 · A finitely generated Eilenberg–Ganea counterexample

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/249.md) · 1 paper

The Eilenberg–Ganea conjecture is disproved by a finitely generated group of cohomological dimension 2 but geometric dimension 3.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A finitely generated counterexample to the Eilenberg–Ganea conjecture](https://github.com/openai/math/blob/main/preprints/A-finitely-generated-counterexample-to-the-Eilenberg-Ganea-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r250"></a>

### 250 · Boone–Higman embeddings with higher finiteness

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/250.md) · 3 papers

Boone–Higman conjecture: a finitely generated group has a solvable word problem exactly when it sits inside a finitely presented simple group. Proven, with strong finiteness.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Finite algebraic envelopes and the Boone–Higman conjecture](https://github.com/openai/math/blob/main/preprints/Finite-algebraic-envelopes-and-the-Boone-Higman-conjecture-September-23-2026/paper.pdf)
- [Simple F∞ overgroups of groups with decidable word problem](https://github.com/openai/math/blob/main/preprints/Simple-F-infinity-overgroups-of-groups-with-decidable-word-problem-September-23-2026/paper.pdf)
- [A universal group of type F∞](https://github.com/openai/math/blob/main/preprints/A-universal-group-of-type-F-infinity-September-23-2026/paper.pdf)

</details>

<a name="r251"></a>

### 251 · Amenability, unitarizability, and strong Ulam stability

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/251.md) · 2 papers

Dixmier's problem: a group is amenable exactly when all its uniformly bounded representations can be made unitary. Proven for all discrete groups, along with a characterization by Ulam stability.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Unitarizability implies amenability for discrete groups](https://github.com/openai/math/blob/main/preprints/Unitarizability-Implies-Amenability-for-Countable-Groups-September-23-2026/paper.pdf)
- [Strong Ulam Stability Characterizes Amenability](https://github.com/openai/math/blob/main/preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/strong-ulam-stability.pdf)

</details>

<a name="r252"></a>

### 252 · A torsion-free hyperbolic group that is neither residually finite nor linear over any field

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/252.md) · 1 paper

This builds a torsion-free hyperbolic group that is not residually finite and not linear over any field, answering a famous question about hyperbolic groups negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A torsion-free hyperbolic group that is not residually finite](https://github.com/openai/math/blob/main/preprints/a-torsion-free-hyperbolic-group-that-is-not-residually-finite-September-23-2026/paper.pdf)

</details>

<a name="r253"></a>

### 253 · An infinite finitely presented simple amenable group

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/253.md) · 1 paper

This builds an infinite, finitely presented, simple, amenable group, showing these properties can all occur together.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An infinite finitely presented simple amenable group](https://github.com/openai/math/blob/main/preprints/An-Infinite-Finitely-Presented-Simple-Amenable-Group-September-23-2026/paper.pdf)

</details>

<a name="r254"></a>

### 254 · Classifying spaces and geometric obstructions for Artin groups

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/254.md) · 3 papers

The Artin K(π,1) conjecture is proven for all finite-rank Artin groups, along with the parabolic intersection conjecture, and an Artin group is found with no geometric CAT(0) action.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Harmonic heights and the Artin K(pi,1) conjecture](https://github.com/openai/math/blob/main/preprints/Harmonic-heights-and-the-Artin-K-pi-1-conjecture-September-23-2026/paper.pdf)
- [An Artin group with no geometric CAT(0) action](https://github.com/openai/math/blob/main/preprints/An-Artin-group-with-no-geometric-CAT-0-action-September-23-2026/paper.pdf)
- [Parabolic intersections in Artin groups](https://github.com/openai/math/blob/main/preprints/Parabolic-intersections-in-Artin-groups-September-23-2026/paper.pdf)

</details>

<a name="r255"></a>

### 255 · Quasi-isometric recognition of virtually polycyclic groups

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/255.md) · 1 paper

Any group that looks like a virtually polycyclic group from far away (quasi-isometric) is itself virtually polycyclic. The Eskin–Fisher–Whyte conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Quasi-isometric recognition of virtually polycyclic groups](https://github.com/openai/math/blob/main/preprints/quasi-isometric-recognition-of-virtually-polycyclic-groups-September-24-2026/paper.pdf)

</details>

<a name="r256"></a>

### 256 · Nonsingular systems of equations over arbitrary groups

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/256.md) · 2 papers

Kervaire's conjecture: adding one new generator and one new relation to a nontrivial group can never make it trivial. Proven, together with Howie's conjecture on solving equations over groups.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Nonsingular systems of equations over arbitrary groups](https://github.com/openai/math/blob/main/preprints/Nonsingular-systems-of-equations-over-arbitrary-groups-October-5-2026/nonsingular-systems-over-arbitrary-groups.pdf)
- [The Kervaire theorem for groups](https://github.com/openai/math/blob/main/preprints/The-Kervaire-Theorem-for-Groups-September-24-2026/The-Kervaire-Theorem-for-Groups-September-24-2026.pdf)

</details>

<a name="r257"></a>

### 257 · A hyperbolic group without a geometric CAT(0) action

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/257.md) · 1 paper

This gives a hyperbolic group with no proper cocompact action on any CAT(0) space, answering the "are all hyperbolic groups CAT(0)?" question negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A hyperbolic group with no geometric CAT(0) action](https://github.com/openai/math/blob/main/preprints/A-hyperbolic-group-with-no-geometric-CAT0-action-September-25-2026/paper.pdf)

</details>

<a name="r258"></a>

### 258 · Gersten’s conjecture and virtual compact specialness of one-relator groups

Not formally verified · 2 papers

Gersten's conjecture: one-relator groups with no Baumslag–Solitar subgroups are hyperbolic. Proven, along with "virtual compact specialness" for hyperbolic one-relator groups.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Baumslag-Solitar-free one-relator groups are hyperbolic](https://github.com/openai/math/blob/main/preprints/Baumslag-Solitar-free-one-relator-groups-are-hyperbolic-September-25-2026/paper.pdf)
- [Virtual compact specialness of hyperbolic one-relator groups](https://github.com/openai/math/blob/main/preprints/Virtual-compact-specialness-of-hyperbolic-one-relator-groups-September-25-2026/paper.pdf)

</details>

<a name="r259"></a>

### 259 · A group without fixed price

Not formally verified · 1 paper

Gaboriau's fixed-price problem: this builds a group with two free measure-preserving actions of different "cost", answering it negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A group without fixed price](https://github.com/openai/math/blob/main/preprints/A-group-without-fixed-price-October-5-2026/unequal-costs-rank-100-amalgam.pdf)

</details>

<a name="s-mathematical-physics"></a>

## Mathematical physics

<a name="r260"></a>

### 260 · Spacetime Penrose inequalities: enclosing area, charge, rotation, and anti-de Sitter extensions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/260.md) · 13 papers

The Penrose inequality from General Relativity says a spacetime's total mass is at least what the area of its black holes requires. This proves the full spacetime version (not only the time-symmetric case) in all dimensions, with charged, rotating (Kerr–Newman) and anti-de Sitter variants (13 papers).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (13)</summary>

- [The spacetime Penrose inequality with charge and original-data rigidity](https://github.com/openai/math/blob/main/preprints/The-spacetime-Penrose-inequality-with-charge-and-original-data-rigidity-October-5-2026/paper.pdf)
- [A Charged Reduction of the Spacetime Penrose Inequality in Spatial Dimensions at Least Four](https://github.com/openai/math/blob/main/preprints/A-Charged-Reduction-of-the-Spacetime-Penrose-Inequality-in-Spatial-Dimensions-at-Least-Four-October-5-2026/paper.pdf)
- [Spacetime Penrose inequalities: enclosing area, charge, and rigidity](https://github.com/openai/math/blob/main/preprints/Spacetime-Penrose-inequalities-enclosing-area-charge-and-rigidity-October-5-2026/paper.pdf)
- [The Kerr–Newman Penrose Inequality for Axisymmetric Electrovacuum Exteriors](https://github.com/openai/math/blob/main/preprints/The-Kerr-Newman-Penrose-Inequality-for-Axisymmetric-Electrovacuum-Exteriors-October-5-2026/paper.pdf)
- [Electromagnetic tails and the Kerr–Newman Penrose inequality](https://github.com/openai/math/blob/main/preprints/Electromagnetic-tails-and-the-Kerr-Newman-Penrose-inequality-October-5-2026/paper.pdf)
- [The nonmaximal anti-de Sitter Penrose Inequality and original-data rigidity](https://github.com/openai/math/blob/main/preprints/The-nonmaximal-anti-de-Sitter-Penrose-Inequality-and-original-data-rigidity-October-5-2026/paper.pdf)
- [The Penrose inequality for maximal asymptotically hyperbolic initial data](https://github.com/openai/math/blob/main/preprints/The-Penrose-inequality-for-maximal-asymptotically-hyperbolic-initial-data-October-5-2026/paper.pdf)
- [A local Penrose inequality for conformal perturbations of Schwarzschild–anti-de Sitter data](https://github.com/openai/math/blob/main/preprints/A-local-Penrose-inequality-for-conformal-perturbations-of-Schwarzschild-anti-de-Sitter-data-October-5-2026/paper.pdf)
- [The spacetime Penrose inequality and enclosing area](https://github.com/openai/math/blob/main/preprints/The-spacetime-Penrose-inequality-and-enclosing-area-September-27-2026/paper.pdf)
- [Conformal flow and the Riemannian Penrose inequality with minimizing frontiers](https://github.com/openai/math/blob/main/preprints/Conformal-flow-and-the-Riemannian-Penrose-inequality-with-minimizing-frontiers-September-27-2026/paper.pdf)
- [Equality and rigidity in the spacetime Penrose inequality](https://github.com/openai/math/blob/main/preprints/Equality-and-rigidity-in-the-spacetime-Penrose-inequality-September-27-2026/paper.pdf)
- [Boundary graph deformations for the spacetime Penrose inequality](https://github.com/openai/math/blob/main/preprints/Boundary-graph-deformations-for-the-spacetime-Penrose-inequality-September-27-2026/paper.pdf)
- [Area-controlled end replacement and the Bondi Penrose inequality in the CKS class](https://github.com/openai/math/blob/main/preprints/Area-controlled-end-replacement-and-the-Bondi-Penrose-inequality-in-the-CKS-class-September-27-2026/paper.pdf)

</details>

<a name="r261"></a>

### 261 · Localization and delocalization in the Anderson model

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/261.md) · 2 papers

Anderson localization concerns electrons in a disordered crystal. This proves that in 2D any amount of disorder traps them, while in 3D and above weak disorder still lets them travel (absolutely continuous spectrum), the long-sought "extended states" result.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Absolutely Continuous Spectrum for Weak-Disorder Anderson Models in Dimensions at Least Three](https://github.com/openai/math/blob/main/preprints/Absolutely-Continuous-Spectrum-for-Weak-Disorder-Anderson-Models-in-Dimensions-at-Least-Three-September-23-2026/paper.pdf)
- [Pure-Point Spectrum for the Two-Dimensional Anderson Model at Every Positive Disorder](https://github.com/openai/math/blob/main/preprints/Pure-Point-Spectrum-for-the-Two-Dimensional-Anderson-Model-at-Every-Positive-Disorder-September-23-2026/paper.pdf)

</details>

<a name="r262"></a>

### 262 · Sharp finite-matrix Lieb–Thirring inequalities and all equality cases

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/262.md) · 3 papers

This proves the sharp Lieb–Thirring inequality in one dimension for matrix-valued potentials, with all equality cases (sums of solitons).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Equality cases in the sharp one-dimensional matrix Lieb–Thirring inequality](https://github.com/openai/math/blob/main/preprints/Equality-cases-in-the-sharp-one-dimensional-matrix-Lieb-Thirring-inequality-October-5-2026/sharp-one-dimensional-lieb-thirring-inequalities-matrix-potentials.pdf)
- [Sharp one-dimensional Lieb–Thirring inequalities for matrix potentials](https://github.com/openai/math/blob/main/preprints/Sharp-one-dimensional-Lieb-Thirring-inequalities-for-matrix-potentials-October-5-2026/sharp-matrix-lieb-thirring.pdf)
- [Sharp one-dimensional Lieb–Thirring constants](https://github.com/openai/math/blob/main/preprints/Sharp-One-Dimensional-Lieb-Thirring-Constants-September-23-2026/paper.pdf)

</details>

<a name="r263"></a>

### 263 · The ionization and generalized ionization conjectures

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/263.md) · 3 papers

The ionization conjecture: a molecule with nuclear charge Z and M nuclei can bind at most Z + C·M electrons, and atomic ionization energies and radii have universal bounds. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Uniform excess charge for Coulomb molecules and the outer radius of neutral atoms](https://github.com/openai/math/blob/main/preprints/Uniform-excess-charge-for-Coulomb-molecules-and-the-outer-radius-of-neutral-atoms-September-24-2026/paper.pdf)
- [Generalized ionization energies for full Coulomb atoms](https://github.com/openai/math/blob/main/preprints/Generalized-ionization-energies-for-full-Coulomb-atoms-September-24-2026/paper.pdf)
- [Generalized outer-electron radii of neutral Coulomb atoms](https://github.com/openai/math/blob/main/preprints/Generalized-outer-electron-radii-of-neutral-Coulomb-atoms-September-24-2026/paper.pdf)

</details>

<a name="r264"></a>

### 264 · Strong cosmic censorship near two-ended Kerr data

Not formally verified · 3 papers

Strong cosmic censorship near rotating Kerr black holes: for generic perturbations, spacetime cannot be continued past the inner horizon in a reasonable sense, so General Relativity stays deterministic.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Generic Future Inextendibility with Square-Integrable Connection Near a Fixed Kerr Spacetime](https://github.com/openai/math/blob/main/preprints/Generic-Future-Inextendibility-with-Square-Integrable-Connection-Near-a-Fixed-Kerr-Spacetime-September-23-2026/paper.pdf)
- [Generic C1 Future Inextendibility Near Rotating Subextremal Kerr Spacetimes](https://github.com/openai/math/blob/main/preprints/Generic-C1-Future-Inextendibility-Near-Rotating-Subextremal-Kerr-Spacetimes-September-23-2026/paper.pdf)
- [Quantitative Near-Kerr Evolution and Generic C2 Future Inextendibility](https://github.com/openai/math/blob/main/preprints/Quantitative-Near-Kerr-Evolution-and-Generic-C2-Future-Inextendibility-September-23-2026/paper.pdf)

</details>

<a name="r265"></a>

### 265 · Area laws and tensor networks for two-dimensional gapped systems

Not formally verified · 2 papers

The area law: ground states of gapped 2D quantum systems have entanglement proportional to boundary length, and can be approximated by PEPS tensor networks of polynomial size.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A two-dimensional area law from a global spectral gap](https://github.com/openai/math/blob/main/preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/paper.pdf)
- [Polynomial PEPS approximation of gapped square-grid ground states](https://github.com/openai/math/blob/main/preprints/Polynomial-PEPS-approximation-of-gapped-square-grid-ground-states-September-24-2026/paper.pdf)

</details>

<a name="r266"></a>

### 266 · Exactly three mutually unbiased bases in dimension six

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/266.md) · 2 papers

In quantum information, mutually unbiased bases are measurement settings that are "maximally different". This proves dimension 6 has exactly 3 of them, not 4, using a certified computer computation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The maximum number of mutually unbiased bases in dimension six](https://github.com/openai/math/blob/main/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026.pdf)
- [Exact Fourier certificates for complex Hadamard matrices of order six](https://github.com/openai/math/blob/main/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026.pdf)

</details>

<a name="r267"></a>

### 267 · Positive-temperature Bose–Einstein condensation and exact quantum depletion

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/267.md) · 5 papers

This proves Bose–Einstein condensation for a gas of hard spheres at positive temperature, a central open problem in mathematical physics, plus Bogoliubov's quantum-depletion law at zero temperature.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5)</summary>

- [Bose–Einstein condensation at positive temperature in the dilute hard-sphere gas](https://github.com/openai/math/blob/main/preprints/Bose-Einstein-condensation-at-positive-temperature-in-the-dilute-hard-sphere-gas-October-5-2026/positive-temperature-hard-spheres.pdf)
- [Quantum Depletion and Momentum Distribution in the Dilute Hard-Sphere Bose Gas](https://github.com/openai/math/blob/main/preprints/Quantum-Depletion-and-Momentum-Distribution-in-the-Dilute-Hard-Sphere-Bose-Gas-October-5-2026/Quantum-Depletion-in-the-Dilute-Hard-Sphere-Bose-Gas.pdf)
- [Quantum Depletion for Fixed Bounded Repulsive Potentials](https://github.com/openai/math/blob/main/preprints/Quantum-Depletion-for-Fixed-Bounded-Repulsive-Potentials-October-5-2026/fixed-repulsion-quantum-depletion.pdf)
- [A density-uniform condensate bound for dilute Bose gases](https://github.com/openai/math/blob/main/preprints/A-density-uniform-condensate-bound-for-dilute-Bose-gases-September-27-2026/paper.pdf)
- [Ground-state condensation in the dilute hard-sphere gas](https://github.com/openai/math/blob/main/preprints/Ground-state-condensation-in-the-dilute-hard-sphere-gas-September-24-2026/paper.pdf)

</details>

<a name="r268"></a>

### 268 · The spin-one Haldane gap

Not formally verified · 2 papers

The Haldane gap: a chain of spin-1 particles with antiferromagnetic Heisenberg interactions has an energy gap, as Haldane predicted in 1983 (Nobel Prize 2016). Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The periodic spin-one Haldane gap](https://github.com/openai/math/blob/main/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/paper.pdf)
- [A boundary-field gap for the spin-one Heisenberg chain](https://github.com/openai/math/blob/main/preprints/A-boundary-field-gap-for-the-spin-one-Heisenberg-chain-September-24-2026/paper.pdf)

</details>

<a name="r269"></a>

### 269 · Uniform Laughlin gap and stability under bounded scalar disorder

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/269.md) · 2 papers

For the Laughlin state of the fractional quantum Hall effect (filling 1/3), this proves a uniform energy gap that survives weak disorder.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Uniform Stability of the Spherical Laughlin Gap](https://github.com/openai/math/blob/main/preprints/Uniform-Stability-of-the-Spherical-Laughlin-Gap-October-5-2026/uniform-stability-spherical-laughlin-gap.pdf)
- [A Fock-space inequality and the Laughlin spectral gap](https://github.com/openai/math/blob/main/preprints/A-Fock-space-inequality-and-the-Laughlin-spectral-gap-September-24-2026/A-Fock-space-inequality-and-the-Laughlin-spectral-gap-September-24-2026.pdf)

</details>

<a name="r270"></a>

### 270 · Threshold and positive-energy bound states of the BFSS matrix model

Not formally verified · 2 papers

The BFSS matrix model is a proposed definition of M-theory. This proves it has exactly one zero-energy bound state for every SU(N), while for SU(2) it has infinitely many positive-energy bound states, contradicting the original paper.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The unique threshold bound state of the SU(N) BFSS model](https://github.com/openai/math/blob/main/preprints/The-unique-threshold-bound-state-of-the-SU-N-BFSS-model-September-24-2026/paper.pdf)
- [Positive eigenvalues of the relative SU(2) BFSS Hamiltonian](https://github.com/openai/math/blob/main/preprints/Positive-eigenvalues-of-the-relative-SU-2-BFSS-Hamiltonian-October-5-2026/positive-eigenvalues-relative-su2-bfss.pdf)

</details>

<a name="r271"></a>

### 271 · Bloch's law, its lattice correction, and the spherical magnetization law

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/271.md) · 4 papers · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/spontaneous-magnetization-quantum-heisenberg-ferromagnet.pdf)

For the quantum Heisenberg ferromagnet, this proves Bloch's T^(3/2) law with its exact coefficient and lattice correction, and spontaneous magnetization in dimension 3 and above, a famous open problem.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Bloch's Law for Finite-Range Heisenberg Ferromagnets in Three Dimensions](https://github.com/openai/math/blob/main/preprints/Blochs-Law-for-Finite-Range-Heisenberg-Ferromagnets-in-Three-Dimensions-October-5-2026/bloch-law-heisenberg.pdf)
- [The first lattice correction to Bloch's law](https://github.com/openai/math/blob/main/preprints/The-first-lattice-correction-to-Blochs-law-October-5-2026/first-lattice-correction-bloch-law.pdf)
- [The spherical magnetization law for the three-dimensional quantum Heisenberg ferromagnet](https://github.com/openai/math/blob/main/preprints/The-spherical-magnetization-law-for-the-three-dimensional-quantum-Heisenberg-ferromagnet-October-5-2026/spherical-magnetization.pdf)
- [Spontaneous magnetization in the quantum Heisenberg ferromagnet](https://github.com/openai/math/blob/main/preprints/Spontaneous-magnetization-in-the-quantum-Heisenberg-ferromagnet-September-24-2026/paper.pdf)

</details>

<a name="r272"></a>

### 272 · Entanglement without distillable secret key

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/272.md) · 1 paper

This builds an entangled quantum state from which no secret key can be distilled (for the stated protocols), and disproves Christandl's PPT-square conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Entanglement with zero distillable secret key in local dimension ten](https://github.com/openai/math/blob/main/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/paper.pdf)

</details>

<a name="r273"></a>

### 273 · The entropy photon-number inequality

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/273.md) · 1 paper

The entropy photon-number inequality, the quantum-optics analogue of Shannon's entropy power inequality, is proven for beam-splitter mixing.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The entropy photon-number inequality](https://github.com/openai/math/blob/main/preprints/The-entropy-photon-number-inequality-September-24-2026/paper.pdf)

</details>

<a name="r274"></a>

### 274 · Parity is not in QAC<sup>0</sup>

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/274.md) · 2 papers

Moore's conjecture: constant-depth quantum circuits (QAC⁰) cannot compute parity, even with large Toffoli gates. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Product-projection localization and the QAC0 parity lower bound](https://github.com/openai/math/blob/main/preprints/Product-projection-localization-and-the-QAC0-parity-lower-bound-September-24-2026/paper.pdf)
- [Regular trajectories, pruning and quantum parity](https://github.com/openai/math/blob/main/preprints/Regular-trajectories-pruning-and-quantum-parity-September-24-2026/paper.pdf)

</details>

<a name="r275"></a>

### 275 · QMA-hardness of continuum Coulomb energy

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/275.md) · 2 papers

Computing the ground-state energy of electrons in a molecule (the full continuum Coulomb model) is QMA-hard: hard even for quantum computers in the worst case.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Continuum Coulomb hardness with binary nuclear charges](https://github.com/openai/math/blob/main/preprints/Continuum-Coulomb-hardness-with-binary-nuclear-charges-September-24-2026/Continuum-Coulomb-hardness-with-binary-nuclear-charges-September-24-2026.pdf)
- [QMA-hardness of continuum Coulomb energy with unit nuclear charges](https://github.com/openai/math/blob/main/preprints/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026.pdf)

</details>

<a name="r276"></a>

### 276 · Classical capacity of generalized amplitude damping

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/276.md) · 1 paper

This computes the exact classical capacity of the generalized amplitude-damping quantum channel (how many bits per use it can carry).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Classical capacity and entropy inequalities for generalized amplitude damping](https://github.com/openai/math/blob/main/preprints/Classical-capacity-and-entropy-inequalities-for-generalized-amplitude-damping-September-24-2026/paper.pdf)

</details>

<a name="r277"></a>

### 277 · Threshold repetition for entangled games

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/277.md) · 1 paper

For two-player games where players share entanglement, the chance of winning noticeably more than a v fraction of k repetitions decays exponentially in k (threshold parallel repetition).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Threshold parallel repetition for finite-dimensional entangled games](https://github.com/openai/math/blob/main/preprints/Threshold-parallel-repetition-for-finite-dimensional-entangled-games-September-25-2026/paper.pdf)

</details>

<a name="r278"></a>

### 278 · Failure of Kohn–Sham ensemble representation

Not formally verified · 1 paper

Kohn–Sham ensemble representability, a foundation of density functional theory in chemistry, fails: this gives a 3-electron molecule whose ground-state density has no non-interacting representation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Coulomb ground-state density without Kohn-Sham ensemble representation](https://github.com/openai/math/blob/main/preprints/A-Coulomb-Ground-State-Density-without-Kohn-Sham-Ensemble-Representation-September-25-2026/paper.pdf)

</details>

<a name="r279"></a>

### 279 · Exact quantum factoring over a fixed finite gate set

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/279.md) · 1 paper

This gives a polynomial-size quantum circuit family, using one fixed finite gate set, that outputs the complete prime factorization of any integer with probability exactly 1.

- **Quant trading:** 🟡 *Background.* For BTC holders: this is not a new threat. It is about factoring (RSA), not the elliptic-curve signatures Bitcoin uses, and Shor's algorithm already broke both in theory on a large enough quantum computer. The practical risk timeline still depends on quantum hardware.
- **Politeia:** 🟡 *Background.* The same holds for e-voting or identity cryptography: no new practical threat. Plan the move to post-quantum cryptography on the normal timeline.

<details><summary>Papers (1)</summary>

- [Exact quantum factoring over a fixed finite gate set](https://github.com/openai/math/blob/main/preprints/Exact-quantum-factoring-over-a-fixed-finite-gate-set-September-25-2026/main.pdf)

</details>

<a name="r280"></a>

### 280 · Unitary vertex operator algebras and conformal nets

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/280.md) · 1 paper

Two mathematical frameworks for 2D conformal field theory (vertex operator algebras and conformal nets) agree for strongly rational unitary theories.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Strongly rational unitary vertex operator algebras and conformal nets](https://github.com/openai/math/blob/main/preprints/Strongly-rational-unitary-vertex-operator-algebras-and-conformal-nets-September-25-2026/paper.pdf)

</details>

<a name="r281"></a>

### 281 · QAOA attains the SK optimum in the thermodynamic-first limit

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/281.md) · 2 papers

QAOA, a quantum optimization algorithm, reaches the optimal energy of the Sherrington–Kirkpatrick spin glass when system size grows before circuit depth, with consequences for MaxCut on random graphs.

- **Quant trading:** 🟡 *Background.* Quantum portfolio optimization is heavily marketed. This proves QAOA can match the optimum of a model spin-glass problem in one specific limit; it says nothing about beating classical solvers on real portfolio problems.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (2)</summary>

- [QAOA attains the SK ground-state energy in the thermodynamic-first limit](https://github.com/openai/math/blob/main/preprints/QAOA-attains-the-SK-ground-state-energy-in-the-thermodynamic-first-limit-September-25-2026/QAOA-attains-the-SK-ground-state-energy-in-the-thermodynamic-first-limit-September-25-2026.pdf)
- [Full support of the zero-temperature Sherrington-Kirkpatrick order parameter](https://github.com/openai/math/blob/main/preprints/Full-support-of-the-zero-temperature-Sherrington-Kirkpatrick-order-parameter-September-27-2026/main.pdf)

</details>

<a name="r282"></a>

### 282 · From scale symmetry to local conformal symmetry in four-dimensional QFT

Not formally verified · 1 paper

Under stated hypotheses, scale symmetry implies local conformal symmetry for 4D quantum field theories, a long-standing physics expectation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Scale and conformal symmetry in four-dimensional operational quantum field theory](https://github.com/openai/math/blob/main/preprints/Scale-and-conformal-symmetry-in-four-dimensional-operational-quantum-field-theory-September-26-2026/main.pdf)

</details>

<a name="r283"></a>

### 283 · Polynomial-time unitary synthesis from a Boolean oracle

Not formally verified · 1 paper

The Aaronson–Kuperberg unitary synthesis problem: any n-qubit unitary can be approximated by a polynomial-size quantum circuit that queries a suitably chosen Boolean oracle.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Polynomial-Time Unitary Synthesis from a Boolean Oracle](https://github.com/openai/math/blob/main/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/paper.pdf)

</details>

<a name="r284"></a>

### 284 · The optimal quartic separation between randomized and quantum queries

Not formally verified · 1 paper

The gap between randomized and quantum query complexity for total functions can be quartic: R(f) = O(Q(f)⁴) is tight in its exponent, disproving the conjectured cubic relation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Nearly Quartic Separation Between Randomized and Quantum Query Complexity](https://github.com/openai/math/blob/main/preprints/A-Nearly-Quartic-Separation-Between-Randomized-and-Quantum-Query-Complexity-October-5-2026/quartic-query-separation.pdf)

</details>

<a name="s-operator-algebras"></a>

## Operator algebras

<a name="r285"></a>

### 285 · Counterexamples to Baum–Connes and Kadison–Kaplansky

Not formally verified · 3 papers

The Baum–Connes conjecture links the topology of a group to its operator algebra. This disproves its coefficient-free reduced form (both injectivity and surjectivity fail), and disproves the Kadison–Kaplansky conjecture with a torsion-free group whose reduced C*-algebra has a nontrivial projection.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [A torsion-free counterexample to reduced Baum–Connes injectivity](https://github.com/openai/math/blob/main/preprints/A-Torsion-Free-Counterexample-to-Reduced-Baum-Connes-Injectivity-September-23-2026/paper.pdf)
- [A torsion-free counterexample to the Kadison–Kaplansky projection conjecture](https://github.com/openai/math/blob/main/preprints/A-Torsion-Free-Counterexample-to-the-Kadison-Kaplansky-Projection-Conjecture-September-23-2026/paper.pdf)
- [An irrational-trace counterexample to reduced Baum–Connes](https://github.com/openai/math/blob/main/preprints/An-Irrational-Trace-Counterexample-to-Reduced-Baum-Connes-September-23-2026/paper.pdf)

</details>

<a name="r286"></a>

### 286 · Rigidity and arithmetic of lattice von Neumann algebras

Not formally verified · 2 papers

For von Neumann algebras built from lattices in Lie groups over local fields, this classifies all finite-index "bridges" (bimodules) between them, and recovers the original group from the algebra (a strong rigidity theorem).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Arithmeticity of twisted finite correspondences for lattices over local fields](https://github.com/openai/math/blob/main/preprints/Arithmeticity-of-twisted-finite-correspondences-for-lattices-over-local-fields-September-23-2026/paper.pdf)
- [The arithmetic category and stable recovery of lattice factors](https://github.com/openai/math/blob/main/preprints/The-arithmetic-category-and-stable-recovery-of-lattice-factors-September-23-2026/paper.pdf)

</details>

<a name="r287"></a>

### 287 · Isomorphism of the free group factors

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/287.md) · 1 paper · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/free-group-factor-isomorphism.pdf)

The free group factor problem asks whether the von Neumann algebras of the free groups on 2 and on 3 generators are the same. It is one of the most famous open problems in operator algebras. This proves they are isomorphic, so all free group factors coincide.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An isomorphism of the free group factors](https://github.com/openai/math/blob/main/preprints/An-isomorphism-of-the-free-group-factors-September-23-2026/An-isomorphism-of-the-free-group-factors-September-23-2026.pdf)

</details>

<a name="r288"></a>

### 288 · Kadison's similarity conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/288.md) · 1 paper

Kadison's similarity problem (1955): every bounded representation of a C*-algebra on Hilbert space becomes a *-representation after a change of coordinates. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Kadison's similarity theorem through uniform derivation estimates](https://github.com/openai/math/blob/main/preprints/Kadisons-similarity-theorem-through-uniform-derivation-estimates-September-23-2026/paper.pdf)

</details>

<a name="r289"></a>

### 289 · Strong Kadison–Kastler stability and its spatial boundaries

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/289.md) · 3 papers

Two von Neumann algebras that are close enough are conjugate by a unitary close to the identity (strong Kadison–Kastler stability). Counterexamples show where this stops working.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Universal strong Kadison–Kastler stability](https://github.com/openai/math/blob/main/preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/paper.pdf)
- [Near Inclusions of von Neumann Algebras Without Small Spatial Embeddings](https://github.com/openai/math/blob/main/preprints/Near-Inclusions-of-von-Neumann-Algebras-Without-Small-Spatial-Embeddings-October-5-2026/near-inclusions.pdf)
- [Close Separable C*-Algebras Without Spatial Conjugacy](https://github.com/openai/math/blob/main/preprints/Close-Separable-Cstar-Algebras-Without-Spatial-Conjugacy-October-5-2026/paper.pdf)

</details>

<a name="r290"></a>

### 290 · Relative bicentralizers and modular spectral recovery

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/290.md) · 2 papers

This proves Connes' bicentralizer conjecture for every type III₁ factor, and a relative version for inclusions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Expected amenable subalgebras preserving core commutants](https://github.com/openai/math/blob/main/preprints/Expected-amenable-subalgebras-preserving-core-commutants-September-23-2026/Expected-amenable-subalgebras-preserving-core-commutants-September-23-2026.pdf)
- [Bounded recovery for modular spectral averages](https://github.com/openai/math/blob/main/preprints/Bounded-recovery-for-modular-spectral-averages-September-23-2026/Bounded-recovery-for-modular-spectral-averages-September-23-2026.pdf)

</details>

<a name="r291"></a>

### 291 · Cuntz comparison, nuclear dimension, and equivariant Jiang–Su stability

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/291.md) · 4 papers

This proves the unital Toms–Winter conjecture (three regularity properties of simple nuclear C*-algebras are equivalent) and equivariant Jiang–Su stability for amenable group actions (Szabó's conjecture, in this case).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (4)</summary>

- [Equivariant Jiang–Su Stability for Amenable Actions in the Unital Stably Finite Case](https://github.com/openai/math/blob/main/preprints/Equivariant-Jiang-Su-Stability-for-Amenable-Actions-in-the-Unital-Stably-Finite-Case-October-5-2026/paper.pdf)
- [Cuntz comparison and Jiang–Su absorption](https://github.com/openai/math/blob/main/preprints/Cuntz-comparison-and-Jiang-Su-absorption-September-23-2026/paper.pdf)
- [Nuclear dimension and Jiang–Su stability without elementary subquotients](https://github.com/openai/math/blob/main/preprints/Nuclear-dimension-and-Jiang-Su-stability-without-elementary-subquotients-September-23-2026/paper.pdf)
- [Tracial projection methods and uniform property Gamma](https://github.com/openai/math/blob/main/preprints/Tracial-projection-methods-and-uniform-property-Gamma-September-23-2026/paper.pdf)

</details>

<a name="r292"></a>

### 292 · Kirchberg's $`\mathcal O_2`$ norm-ultrapower embedding problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/292.md) · 1 paper

Kirchberg's question about embedding into ultrapowers of the Cuntz algebra O₂ is answered negatively with an explicit group C*-algebra.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [An explicit obstruction to nuclear norm-ultrapower embeddings](https://github.com/openai/math/blob/main/preprints/An-explicit-obstruction-to-nuclear-norm-ultrapower-embeddings-September-23-2026/paper.pdf)

</details>

<a name="r293"></a>

### 293 · Invariant projections, hyperinvariant subspaces, and transitive algebras

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/293.md) · 2 papers

This builds a quasinilpotent operator on Hilbert space with no nontrivial subspace left invariant by everything that commutes with it. That answers the hyperinvariant subspace question, a close relative of the famous invariant subspace problem.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Invariant-projection counterexamples for every irrational rotation](https://github.com/openai/math/blob/main/preprints/Invariant-projection-counterexamples-for-every-irrational-rotation-September-27-2026/paper.pdf)
- [Backward intertwiners and a transitive commutant](https://github.com/openai/math/blob/main/preprints/Backward-intertwiners-and-a-transitive-commutant-September-27-2026/paper.pdf)

</details>

<a name="r294"></a>

### 294 · Kaplansky's quasitrace conjecture and failure of tensor-product stable finiteness

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/294.md) · 1 paper

Kaplansky's quasitrace conjecture is disproved, and as a consequence the tensor product of two stably finite simple C*-algebras can be properly infinite.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A counterexample to Kaplansky's quasitrace conjecture and failure of tensor-product stable finiteness](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-Kaplanskys-quasitrace-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r295"></a>

### 295 · The Kadison–Ringrose cohomology conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/295.md) · 1 paper

The Kadison–Ringrose conjecture: all higher bounded Hochschild cohomology of a von Neumann algebra (with coefficients in itself) vanishes. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Vanishing of higher bounded Hochschild cohomology](https://github.com/openai/math/blob/main/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/paper.pdf)

</details>

<a name="r296"></a>

### 296 · The generator problem for finite factors

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/296.md) · 1 paper

The generator problem: every II₁ factor with separable predual is generated by a single operator. A famous open problem. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Relative generation and the generator problem for finite factors](https://github.com/openai/math/blob/main/preprints/Relative-generation-and-the-generator-problem-for-finite-factors-September-23-2026/paper.pdf)

</details>

<a name="r297"></a>

### 297 · A ZFC counterexample to Naimark's problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/297.md) · 1 paper

Naimark's problem: this gives an alternative ZFC construction (after Tanaka's earlier one) of an infinite-dimensional simple C*-algebra with only one irreducible representation.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A counterexample to Naimark's problem in ZFC](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-Naimarks-problem-in-ZFC-September-24-2026/naimark-counterexample-zfc.pdf)

</details>

<a name="r298"></a>

### 298 · Two notions of free entropy differ even when both are finite

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/298.md) · 1 paper

Voiculescu defined "free entropy" in two ways, via matrix approximations and via free Fisher information. This shows they can differ even when both are finite.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A finite-entropy separation of microstates and nonmicrostates free entropy](https://github.com/openai/math/blob/main/preprints/A-finite-entropy-separation-of-microstates-and-nonmicrostates-free-entropy-September-25-2026/paper.pdf)

</details>

<a name="r299"></a>

### 299 · The Kirchberg–Rørdam character criterion and infinite tensor-power Jiang–Su stability

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/299.md) · 1 paper

A C*-algebra is Jiang–Su stable exactly when its central-sequence algebra has no characters. This answers Kirchberg–Rørdam, and also the Dadarlat–Toms question about infinite tensor powers.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Kirchberg–Rørdam character criterion](https://github.com/openai/math/blob/main/preprints/The-Kirchberg-Rordam-character-criterion-September-25-2026/paper.pdf)

</details>

<a name="r300"></a>

### 300 · Approximation and quadratic strong-operator paving

Not formally verified · 2 papers

This proves the Popa–Vaes quadratic paving conjecture: self-adjoint operators can be "paved" into O(ε^−2) nearly diagonal blocks relative to any maximal abelian subalgebra.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Approximation Paving over Arbitrary Maximal Abelian Subalgebras](https://github.com/openai/math/blob/main/preprints/Approximation-Paving-over-Arbitrary-Maximal-Abelian-Subalgebras-September-25-2026/Approximation-Paving-over-Arbitrary-Maximal-Abelian-Subalgebras-September-25-2026.pdf)
- [Quadratic Strong-Operator Paving over Arbitrary Maximal Abelian Subalgebras](https://github.com/openai/math/blob/main/preprints/Quadratic-Strong-Operator-Paving-over-Arbitrary-Maximal-Abelian-Subalgebras-September-25-2026/Quadratic-Strong-Operator-Paving-over-Arbitrary-Maximal-Abelian-Subalgebras-September-25-2026.pdf)

</details>

<a name="r301"></a>

### 301 · Trace cones and Razak–Jacelon stabilization

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/301.md) · 1 paper

This classifies separable nuclear C*-algebras after stabilizing with the Razak–Jacelon algebra, using their cones of traces, which answers Robert's question.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The trace cone classifies Razak–Jacelon stabilizations](https://github.com/openai/math/blob/main/preprints/The-trace-cone-classifies-Razak-Jacelon-stabilizations-September-25-2026/The-trace-cone-classifies-Razak-Jacelon-stabilizations-September-25-2026.pdf)

</details>

<a name="r302"></a>

### 302 · Radius of comparison equals half the mean dimension

Not formally verified · 2 papers

For minimal dynamical systems, the radius of comparison of the crossed-product C*-algebra equals half the mean dimension of the system, a conjectured bridge between dynamics and operator algebras.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Filtered products and boundary-preserving compression in complex cobordism](https://github.com/openai/math/blob/main/preprints/Filtered-products-and-boundary-preserving-compression-in-complex-cobordism-September-25-2026/paper.pdf)
- [Radius of comparison equals half the mean dimension](https://github.com/openai/math/blob/main/preprints/Radius-of-comparison-equals-half-the-mean-dimension-September-25-2026/paper.pdf)

</details>

<a name="r303"></a>

### 303 · Weak pure infiniteness and Cuntz-algebra absorption

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/303.md) · 1 paper

Weak pure infiniteness implies absorption of the Cuntz algebra O∞ for separable nuclear algebras, resolving a Kirchberg–Rørdam question.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Weak pure infiniteness and O-infinity absorption](https://github.com/openai/math/blob/main/preprints/Weak-pure-infiniteness-and-O-infinity-absorption-September-25-2026/paper.pdf)

</details>

<a name="s-topology"></a>

## Topology

<a name="r304"></a>

### 304 · The Hilbert–Smith conjecture in every dimension

Not formally verified · 1 paper

The Hilbert–Smith conjecture: any locally compact group acting faithfully and continuously on a finite-dimensional manifold must be a Lie group. This is the last piece of Hilbert's 5th problem. Proven in every dimension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Hilbert–Smith conjecture in every finite dimension](https://github.com/openai/math/blob/main/preprints/The-Hilbert-Smith-conjecture-in-every-finite-dimension-September-23-2026/paper.pdf)

</details>

<a name="r305"></a>

### 305 · Four-dimensional disk embedding and Wall's conjecture

Not formally verified · 3 papers

In 4-dimensional topology, the unrestricted disk-embedding conjecture fails (the free group F₂ is not "good" in Freedman–Quinn's sense). Wall's conjecture is also disproved: some 4-dimensional Poincaré-duality group is not the fundamental group of any aspherical 4-manifold.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [A boundary-only obstruction to four-dimensional disk embedding](https://github.com/openai/math/blob/main/preprints/A-boundary-only-obstruction-to-four-dimensional-disk-embedding-September-24-2026/paper.pdf)
- [A marked tensor obstruction to four-dimensional disk embedding](https://github.com/openai/math/blob/main/preprints/A-marked-tensor-obstruction-to-four-dimensional-disk-embedding-September-24-2026/paper.pdf)
- [A PD4 group without an aspherical manifold model](https://github.com/openai/math/blob/main/preprints/A-PD4-group-without-an-aspherical-manifold-model-September-24-2026/paper.pdf)

</details>

<a name="r306"></a>

### 306 · The purely cosmetic surgery conjecture

Not formally verified · 1 paper

The purely cosmetic surgery conjecture: doing two different Dehn surgeries on a nontrivial knot never produces the same oriented 3-manifold. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Purely cosmetic surgery on knots in the three-sphere](https://github.com/openai/math/blob/main/preprints/Purely-Cosmetic-Surgery-on-Knots-in-the-Three-Sphere-September-23-2026/paper.pdf)

</details>

<a name="r307"></a>

### 307 · Failure of rational injectivity for maximal coarse assembly

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/307.md) · 2 papers

The rational coarse Novikov conjecture is disproved: this builds a bounded-geometry space whose coarse assembly map is not rationally injective.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Failure of rational injectivity for maximal coarse assembly](https://github.com/openai/math/blob/main/preprints/Failure-of-rational-injectivity-for-maximal-coarse-assembly-October-5-2026/paper.pdf)
- [A counterexample to the coarse Novikov conjecture](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-the-coarse-Novikov-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r308"></a>

### 308 · Finite Smith–Toda complexes at every height

Not formally verified · 2 papers

Smith–Toda complexes V(n), building blocks of chromatic homotopy theory, exist at every height if the prime is allowed to vary. For example, V(4) exists at p = 1009.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Finite Smith–Toda Complexes at Varying Primes](https://github.com/openai/math/blob/main/preprints/Finite-Smith-Toda-Complexes-at-Varying-Primes-September-23-2026/paper.pdf)
- [A finite Smith–Toda complex V(4) at the prime 1009](https://github.com/openai/math/blob/main/preprints/A-finite-Smith-Toda-complex-V4-at-the-prime-1009-September-23-2026/paper.pdf)

</details>

<a name="r309"></a>

### 309 · The Kervaire invariant problem at the prime three

Not formally verified · 1 paper

This resolves the Kervaire invariant problem at the prime 3: exactly the classes in stems 10, 106 and 322 survive.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Kervaire invariant problem at the prime three](https://github.com/openai/math/blob/main/preprints/The-Kervaire-Invariant-Problem-at-the-Prime-Three-September-24-2026/paper.pdf)

</details>

<a name="r310"></a>

### 310 · Quillen's conjecture in rational homology

Not formally verified · 1 paper

Quillen's conjecture (rational homology form): for a finite group with no nontrivial normal p-subgroup, the poset of elementary abelian p-subgroups is not contractible. Proven for every group and prime.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Rational homology and Quillen's conjecture](https://github.com/openai/math/blob/main/preprints/Rational-homology-and-Quillens-conjecture-September-24-2026/paper.pdf)

</details>

<a name="r311"></a>

### 311 · The Hovey–Strickland and Chai conjectures

Not formally verified · 1 paper

This proves Chai's conjecture and, through it, the Hovey–Strickland conjecture classifying the thick tensor ideals of dualizable K(n)-local spectra.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Stabilizer orbits and thick tensor ideals of dualizable K(n)-local spectra](https://github.com/openai/math/blob/main/preprints/Stabilizer-Orbits-and-Thick-Tensor-Ideals-of-Dualizable-Kn-Local-Spectra-September-24-2026/paper.pdf)

</details>

<a name="r312"></a>

### 312 · The Grothendieck homotopy hypothesis

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/312.md) · 1 paper

Grothendieck's homotopy hypothesis: his algebraic ∞-groupoids (with the Ara–Henry conventions) recover exactly the homotopy theory of spaces. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Grothendieck homotopy hypothesis via elementary expansions](https://github.com/openai/math/blob/main/preprints/The-Grothendieck-homotopy-hypothesis-via-elementary-expansions-September-24-2026/paper.pdf)

</details>

<a name="r313"></a>

### 313 · Finite generation for the $`K(n)`$-local sphere

Not formally verified · 1 paper

Every homotopy group of the K(n)-local sphere is finitely generated, answering Hovey and Strickland.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Finite generation for the K(n)-local sphere](https://github.com/openai/math/blob/main/preprints/Finite-generation-for-the-Kn-local-sphere-September-24-2026/Finite-generation-for-the-Kn-local-sphere-September-24-2026.pdf)

</details>

<a name="r314"></a>

### 314 · Cyclic length and chromatic fixed-point loss

Not formally verified · 1 paper

This determines exactly how much "chromatic height" is lost when passing between fixed points of a p-group and of a subgroup: it equals the length of the shortest cyclic subnormal chain.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Cyclic length and chromatic fixed-point loss](https://github.com/openai/math/blob/main/preprints/Cyclic-Length-and-Chromatic-Fixed-Point-Loss-September-24-2026/Cyclic-Length-and-Chromatic-Fixed-Point-Loss-September-24-2026.pdf)

</details>

<a name="r315"></a>

### 315 · The four-dimensional Singer conjecture

Not formally verified · 1 paper

The Singer conjecture in dimension 4: the L²-Betti numbers of aspherical 4-manifolds vanish outside the middle degree. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Singer conjecture in dimension four](https://github.com/openai/math/blob/main/preprints/The-Singer-conjecture-in-dimension-four-September-25-2026/paper.pdf)

</details>

<a name="r316"></a>

### 316 · Curtis’s conjecture

Not formally verified · 1 paper

Curtis's conjecture: at the prime 2, the only stable homotopy classes of spheres detected by homology are the Hopf-invariant-one and Kervaire-invariant-one classes. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Stable Hurewicz Image of the Sphere at Two](https://github.com/openai/math/blob/main/preprints/The-Stable-Hurewicz-Image-of-the-Sphere-at-Two-September-25-2026/paper.pdf)

</details>

<a name="r317"></a>

### 317 · Thomason model structures in all strict higher dimensions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/317.md) · 1 paper

The Ara–Maltsiniotis conjecture: strict n-categories (in every dimension, including ω) model the homotopy theory of spaces via Thomason model structures. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Thomason Model Structures in Every Strict Higher Dimension](https://github.com/openai/math/blob/main/preprints/Thomason-Model-Structures-in-Every-Strict-Higher-Dimension-September-25-2026/paper.pdf)

</details>

<a name="r318"></a>

### 318 · Chromatic splitting: filtrations and counterexamples

Not formally verified · 5 papers

The chromatic splitting conjecture is disproved at height 3 for primes p ≥ 5 (and weak splitting in other cases), while a corrected filtration by the predicted pieces is proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5)</summary>

- [Filtered chromatic splitting at generic primes](https://github.com/openai/math/blob/main/preprints/Filtered-chromatic-splitting-at-generic-primes-September-25-2026/paper.pdf)
- [The height-three chromatic overlap: an explicit filtration and its attachments](https://github.com/openai/math/blob/main/preprints/The-height-three-chromatic-overlap-an-explicit-filtration-and-its-attachments-September-27-2026/paper.pdf)
- [A rational obstruction to strong chromatic splitting at height three](https://github.com/openai/math/blob/main/preprints/A-rational-obstruction-to-strong-chromatic-splitting-at-height-three-September-25-2026/paper.pdf)
- [Failure of finite assembly for a chromatic overlap at the prime three](https://github.com/openai/math/blob/main/preprints/Failure-of-finite-assembly-for-a-chromatic-overlap-at-the-prime-three-September-25-2026/paper.pdf)
- [Counterexamples to weak chromatic splitting: sphere kernels and descent exponents](https://github.com/openai/math/blob/main/preprints/Counterexamples-to-weak-chromatic-splitting-sphere-kernels-and-descent-exponents-September-27-2026/paper.pdf)

</details>

<a name="r319"></a>

### 319 · Counterexamples to finite generation at chromatic height two

Not formally verified · 1 paper

The Hahn–Wilson conjecture is refuted at chromatic height 2 by spectra that cannot be built from BP⟨2⟩ in finitely many steps.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Counterexamples to the Hahn-Wilson conjecture at height two](https://github.com/openai/math/blob/main/preprints/Counterexamples-to-the-Hahn-Wilson-conjecture-at-height-two-September-26-2026/paper.pdf)

</details>

<a name="r320"></a>

### 320 · Nonhomeomorphic closed aspherical four-manifolds

Not formally verified · 1 paper

The Borel conjecture says aspherical manifolds with the same homotopy type are homeomorphic. This disproves it in dimension 4 with homotopy-equivalent but non-homeomorphic aspherical 4-manifolds.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Nonhomeomorphic closed aspherical four-manifolds with the same homotopy type](https://github.com/openai/math/blob/main/preprints/Nonhomeomorphic-closed-aspherical-four-manifolds-with-the-same-homotopy-type-October-4-2026/paper.pdf)

</details>

<a name="r321"></a>

### 321 · A counterexample to Wall's finite D(2) problem

Not formally verified · 1 paper

Wall's D(2) problem is answered with a counterexample: a 3-dimensional complex that looks 2-dimensional to every homological test but has no 2-dimensional model.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Counterexample to Wall's D(2) Problem](https://github.com/openai/math/blob/main/preprints/A-Counterexample-to-Walls-D2-Problem-October-6-2026/wall-d2-counterexample.pdf)

</details>

<a name="s-functional-analysis"></a>

## Functional analysis

<a name="r322"></a>

### 322 · Tingley’s sphere-isometry problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/322.md) · 1 paper

Tingley's problem: any distance-preserving map between the unit spheres of two Banach spaces extends to a linear isometry of the whole spaces. Proven in full generality.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A positive solution to Tingley’s problem](https://github.com/openai/math/blob/main/preprints/A-positive-solution-to-Tingleys-problem-September-23-2026/paper.pdf)

</details>

<a name="r323"></a>

### 323 · Independence of the separable quotient problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/323.md) · 1 paper

The separable quotient problem (does every infinite-dimensional Banach space have a separable infinite-dimensional quotient?) is independent of the usual axioms ZFC, relative to a measurable cardinal.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Relative independence of the separable quotient problem](https://github.com/openai/math/blob/main/preprints/Relative-independence-of-the-separable-quotient-problem-September-23-2026/paper.pdf)

</details>

<a name="r324"></a>

### 324 · Lipschitz equivalent Banach spaces need not be linearly isomorphic

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/324.md) · 2 papers

Two separable Banach spaces can be equivalent as metric spaces (bi-Lipschitz) without being linearly isomorphic, resolving a major open problem negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Lipschitz Equivalent Separable Banach Spaces Need Not Be Linearly Isomorphic](https://github.com/openai/math/blob/main/preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/paper.pdf)
- [Bi-Lipschitz Absorption of c0 Without a Linear Copy of c0](https://github.com/openai/math/blob/main/preprints/Bi-Lipschitz-Absorption-of-c0-Without-a-Linear-Copy-of-c0-September-26-2026/paper.pdf)

</details>

<a name="r325"></a>

### 325 · The complete Crouzeix conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/325.md) · 2 papers

The complete Crouzeix conjecture: for any matrix or operator A and any (matrix) polynomial p, ‖p(A)‖ is at most 2 × the largest value of |p| on the numerical range of A. The constant 2 is sharp. This also settles the famous scalar Crouzeix conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A direct proof of the complete Crouzeix inequality](https://github.com/openai/math/blob/main/preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/paper.pdf)
- [The complete Crouzeix theorem: optimal similarity and a common positive boundary representation](https://github.com/openai/math/blob/main/preprints/The-complete-Crouzeix-theorem-September-23-2026/paper.pdf)

</details>

<a name="r326"></a>

### 326 · The cotype–cotype conjecture under the approximation property

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/326.md) · 1 paper

The cotype–cotype conjecture (for spaces with the approximation property): a Banach space is K-convex exactly when it and its dual both have finite cotype. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The cotype–cotype conjecture under the approximation property](https://github.com/openai/math/blob/main/preprints/The-cotype-cotype-conjecture-under-the-approximation-property-September-23-2026/paper.pdf)

</details>

<a name="r327"></a>

### 327 · Markov type characterizes superreflexivity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/327.md) · 1 paper

Nontrivial Markov type characterizes superreflexive Banach spaces, answering Naor's renorming question.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Nontrivial Markov Type Forces Superreflexivity](https://github.com/openai/math/blob/main/preprints/Nontrivial-Markov-Type-Forces-Superreflexivity-September-23-2026/paper.pdf)

</details>

<a name="r328"></a>

### 328 · Nonexpansive fixed points in reflexive Banach spaces

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/328.md) · 1 paper

Kirk's fixed-point problem: every distance-non-increasing self-map of a closed, bounded, convex set in a reflexive Banach space has a fixed point. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Fixed Points of Nonexpansive Maps in Reflexive Banach Spaces](https://github.com/openai/math/blob/main/preprints/Fixed-Points-of-Nonexpansive-Maps-in-Reflexive-Banach-Spaces-September-24-2026/paper.pdf)

</details>

<a name="r329"></a>

### 329 · A counterexample to metric-entropy duality

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/329.md) · 1 paper

Pietsch's duality conjecture for metric entropy (covering numbers of a convex body versus those of its polar) is disproved.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Counterexamples to the duality conjecture for metric entropy](https://github.com/openai/math/blob/main/preprints/Counterexamples-to-the-duality-conjecture-for-metric-entropy-September-24-2026/main.pdf)

</details>

<a name="r330"></a>

### 330 · A uniformly discrete counterexample to bounded approximation in Lipschitz-free spaces

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/330.md) · 1 paper

This answers Kalton's question with a countable uniformly discrete metric space whose Lipschitz-free space has the approximation property but not the bounded approximation property.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A uniformly discrete counterexample to bounded approximation in Lipschitz-free spaces](https://github.com/openai/math/blob/main/preprints/Failure-of-Bounded-Approximation-in-a-Lipschitz-Free-Space-over-a-Uniformly-Discrete-Metric-Space-September-26-2026/main.pdf)

</details>

<a name="r331"></a>

### 331 · Reflexive midpoint convexity and diamond distortion

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/331.md) · 7 papers

This builds a reflexive Banach space with asymptotic midpoint uniform convexity but no asymptotically uniformly convex renorming, and with unbounded distortion for branching diamond graphs.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (7)</summary>

- [Asymptotic midpoint uniform convexity and unbounded diamond distortion in a reflexive tree space](https://github.com/openai/math/blob/main/preprints/Asymptotic-midpoint-uniform-convexity-and-unbounded-diamond-distortion-in-a-reflexive-tree-space-September-27-2026/manuscript.pdf)
- [Midpoint lenses in segment spaces](https://github.com/openai/math/blob/main/preprints/Midpoint-lenses-in-segment-spaces-September-27-2026/manuscript.pdf)
- [Distortion of countably branching diamonds from midpoint and tree energies](https://github.com/openai/math/blob/main/preprints/Diamond-distortion-from-midpoint-and-tree-energies-September-27-2026/manuscript.pdf)
- [Exact asymptotic moduli in a Daugavet subspace of L1](https://github.com/openai/math/blob/main/preprints/Exact-asymptotic-moduli-in-a-Daugavet-subspace-of-L1-September-27-2026/manuscript.pdf)
- [Midpoint convexity from bounded tree potentials and path costs](https://github.com/openai/math/blob/main/preprints/Midpoint-convexity-from-bounded-tree-potentials-and-path-costs-September-27-2026/manuscript.pdf)
- [Independent products in real L1: asymptotic midpoint convexity without AUC renormings](https://github.com/openai/math/blob/main/preprints/Independent-products-in-real-L1-asymptotic-midpoint-convexity-without-AUC-renormings-September-27-2026/manuscript.pdf)
- [Midpoint convexity from two recursive potentials](https://github.com/openai/math/blob/main/preprints/Midpoint-convexity-from-two-recursive-potentials-September-27-2026/manuscript.pdf)

</details>

<a name="r332"></a>

### 332 · Metric Markov cotype of <i>ℓ</i><sub>1</sub> and Hilbert-space Lipschitz extension

Not formally verified · 1 paper

The space ℓ₁ has metric Markov cotype 2, so Lipschitz maps from subsets of Hilbert space into ℓ₁ extend to the whole space with bounded loss (Ball's extension problem for this target).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Metric Markov Cotype Two of <i>ℓ</i><sub>1</sub> ](https://github.com/openai/math/blob/main/preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/l1-markov-cotype.pdf)

</details>

<a name="s-differential-geometry"></a>

## Differential geometry

<a name="r333"></a>

### 333 · Smooth isometric immersions of surfaces into ℝ<sup>4</sup>

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/333.md) · 1 paper

Every closed surface, with any way of measuring lengths on it, can be placed smoothly into 4-dimensional space without stretching (a smooth isometric immersion into ℝ⁴).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Smooth isometric immersions of closed surfaces into Euclidean four-space](https://github.com/openai/math/blob/main/preprints/Smooth-isometric-immersions-of-closed-surfaces-into-Euclidean-four-space-September-23-2026/paper.pdf)

</details>

<a name="r334"></a>

### 334 · A smooth surface metric with no local isometric immersion in ℝ<sup>3</sup>

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/334.md) · 1 paper

This builds a smooth way of measuring lengths on a small patch of surface that cannot be realized as an actual surface in 3D space, even after shrinking the patch. A classical question answered negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Smooth Metric with No Local Isometric Immersion into Three-Space](https://github.com/openai/math/blob/main/preprints/A-Smooth-Metric-with-No-Local-Isometric-Immersion-into-Three-Space-September-24-2026/paper.pdf)

</details>

<a name="r335"></a>

### 335 · Gromov’s integral scalar-curvature bound for simplicial volume

Not formally verified · 2 papers

This proves Gromov's integral bound linking negative scalar curvature to simplicial volume, and the Gromov–Lawson conjecture: closed aspherical manifolds cannot carry positive scalar curvature, and any nonnegative-scalar-curvature metric on one is flat.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [An integral scalar curvature bound for real simplicial volume](https://github.com/openai/math/blob/main/preprints/An-integral-scalar-curvature-bound-for-real-simplicial-volume-October-5-2026/v126-proof.pdf)
- [Positive scalar curvature forces rational inessentiality](https://github.com/openai/math/blob/main/preprints/Positive-scalar-curvature-forces-rational-inessentiality-September-23-2026/paper.pdf)

</details>

<a name="r336"></a>

### 336 · Spectral scalar curvature, Urysohn width, and macroscopic dimension

Not formally verified · 3 papers

Manifolds with positive "spectral" scalar curvature are thin in all but n − 2 directions (bounded Urysohn width), strengthening Gromov's width theorem.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Spectral scalar curvature and uniform Urysohn width](https://github.com/openai/math/blob/main/preprints/Spectral-scalar-curvature-and-uniform-Urysohn-width-October-5-2026/main.pdf)
- [Spectral scalar curvature and Urysohn width in dimension three](https://github.com/openai/math/blob/main/preprints/Spectral-scalar-curvature-and-Urysohn-width-in-dimension-three-October-5-2026/spectral-urysohn-three-manifolds.pdf)
- [Positive scalar curvature and uniform codimension-two width](https://github.com/openai/math/blob/main/preprints/Positive-scalar-curvature-and-uniform-codimension-two-width-September-23-2026/paper.pdf)

</details>

<a name="r337"></a>

### 337 · Sharp Cartan–Hadamard isoperimetry and rigidity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/337.md) · 2 papers

The Cartan–Hadamard conjecture: in nonpositively curved spaces, balls enclose at least as much volume for a given surface area as in flat space (the isoperimetric inequality). Proven in all dimensions, with sharp filling bounds in CAT(0) spaces.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Generalized Cartan–Hadamard isoperimetry and Euclidean equality rigidity](https://github.com/openai/math/blob/main/preprints/Generalized-Cartan-Hadamard-isoperimetry-and-Euclidean-equality-rigidity-September-23-2026/paper.pdf)
- [Sharp integral fillings in CAT(0) spaces](https://github.com/openai/math/blob/main/preprints/Sharp-integral-fillings-in-CAT%280%29-spaces-September-23-2026/paper.pdf)

</details>

<a name="r338"></a>

### 338 · Yau's uniformization conjecture

Not formally verified · 1 paper

Yau's uniformization conjecture: a complete non-compact Kähler manifold with positive bisectional curvature is biholomorphic to ℂⁿ. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Uniformization of complete Kähler manifolds with positive bisectional curvature](https://github.com/openai/math/blob/main/preprints/Uniformization-of-complete-Kahler-manifolds-with-positive-bisectional-curvature-September-23-2026/paper.pdf)

</details>

<a name="r339"></a>

### 339 · Katok's entropy rigidity conjecture

Not formally verified · 1 paper

Katok's entropy rigidity conjecture: on a negatively curved manifold, the natural (Liouville) measure has maximal entropy only when the metric is locally symmetric. Proven in dimension 3 and up.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Entropy equality and local symmetry in negative curvature](https://github.com/openai/math/blob/main/preprints/Entropy-equality-and-local-symmetry-in-negative-curvature-September-23-2026/paper.pdf)

</details>

<a name="r340"></a>

### 340 · A counterexample to the nearby Lagrangian conjecture

Not formally verified · 1 paper

The nearby Lagrangian conjecture is disproved: in a high-dimensional cotangent bundle there is a closed exact Lagrangian that is not Hamiltonian-isotopic to the zero section.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A counterexample to the nearby Lagrangian conjecture](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-the-nearby-Lagrangian-conjecture-September-23-2026/paper.pdf)

</details>

<a name="r341"></a>

### 341 · Donaldson's hypersymplectic deformation conjecture

Not formally verified · 1 paper · 🔧 proof repaired Oct 7

Donaldson's hypersymplectic deformation conjecture: positive triples of closed 2-forms on a 4-manifold deform to hyperkähler triples while keeping their cohomology. Proven. The paper was revised on Oct 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Deforming hypersymplectic four-manifolds to hyperkähler triples](https://github.com/openai/math/blob/main/preprints/Deforming-hypersymplectic-four-manifolds-to-hyperkahler-triples-October-7-2026/paper.pdf)

</details>

<a name="r342"></a>

### 342 · Donaldson's tamed-to-compatible conjecture

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/342.md) · 1 paper · 🔧 proof repaired Oct 7

Donaldson's tamed-to-compatible conjecture: on a closed 4-manifold, an almost complex structure tamed by some symplectic form is compatible with some (possibly different) symplectic form. Proven; revised on Oct 7 to correct a side claim.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Taming implies compatibility on four-manifolds](https://github.com/openai/math/blob/main/preprints/Taming-implies-compatibility-on-four-manifolds-October-6-2026/paper.pdf)

</details>

<a name="r343"></a>

### 343 · Symplectic ball packing in higher dimensions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/343.md) · 1 paper

Symplectic ball packing: this gives the exact rule for when several symplectic balls fit disjointly inside a bigger one in dimension 6 and higher (the Siegel–Yao conjecture).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Symplectic Ball Packings in Higher Dimensions](https://github.com/openai/math/blob/main/preprints/Symplectic-Ball-Packings-in-Higher-Dimensions-September-23-2026/paper.pdf)

</details>

<a name="r344"></a>

### 344 · The metric Blaschke conjecture

Not formally verified · 1 paper

The metric Blaschke conjecture: a manifold whose injectivity radius equals its diameter is, up to scaling, a round sphere or projective space. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The metric Blaschke theorem](https://github.com/openai/math/blob/main/preprints/The-metric-Blaschke-theorem-September-23-2026/paper.pdf)

</details>

<a name="r345"></a>

### 345 · Infinitely many closed geodesics on Riemannian spheres and closed three-manifolds

Not formally verified · 1 paper

Every way of measuring lengths on a sphere of any dimension has infinitely many different closed geodesics (closed "straightest" loops). The same holds on every closed 3-manifold.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Infinitely many closed geodesic images on every Riemannian sphere](https://github.com/openai/math/blob/main/preprints/Infinitely-many-closed-geodesic-images-on-every-Riemannian-sphere-September-24-2026/paper.pdf)

</details>

<a name="r346"></a>

### 346 · Sharp singular-set bounds for stationary integral varifolds

Not formally verified · 2 papers

Stationary integral varifolds are a very general notion of minimal surface, such as soap films. This proves their singular set has dimension at most m − 1, which is sharp, and almost-everywhere regularity on round spheres.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A Codimension-One Bound for the Singular Set of a Stationary Integral Varifold](https://github.com/openai/math/blob/main/preprints/A-Codimension-One-Bound-for-the-Singular-Set-of-a-Stationary-Integral-Varifold-October-5-2026/varifold-singular-dimension.pdf)
- [Almost-everywhere regularity of stationary integral varifolds](https://github.com/openai/math/blob/main/preprints/Almost-everywhere-regularity-of-stationary-integral-varifolds-September-23-2026/paper.pdf)

</details>

<a name="r347"></a>

### 347 · Counterexamples to stable-Morse and strong Arnold fixed-point bounds

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/347.md) · 5 papers

Lower bounds in the spirit of the Arnold conjecture fail: on certain 22-dimensional manifolds, Hamiltonian maps can have far fewer fixed points than the stable Morse number, and one map of the quadric threefold has only 3 fixed points.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (5)</summary>

- [Hamiltonian Fixed Points Below the Stable Morse Number in Dimension Twenty-Two](https://github.com/openai/math/blob/main/preprints/Hamiltonian-Fixed-Points-Below-the-Stable-Morse-Number-in-Dimension-Twenty-Two-October-5-2026/hamiltonian-fixed-points-below-stable-morse-number.pdf)
- [Sharpness of the Cyclic Integral Floer Bound Below the Stable Morse Number](https://github.com/openai/math/blob/main/preprints/Sharpness-of-the-Cyclic-Integral-Floer-Bound-Below-the-Stable-Morse-Number-October-5-2026/sharp-cyclic-integral-floer-bound-below-stable-morse-number.pdf)
- [Hamiltonian Fixed Points Below the Stable Morse Number](https://github.com/openai/math/blob/main/preprints/Hamiltonian-Fixed-Points-Below-the-Stable-Morse-Number-October-5-2026/paper.pdf)
- [A nondegenerate counterexample to the Morse-number Arnold bound](https://github.com/openai/math/blob/main/preprints/A-nondegenerate-counterexample-to-the-Morse-number-Arnold-bound-September-23-2026/paper.pdf)
- [Three fixed points on the symplectic quadric threefold](https://github.com/openai/math/blob/main/preprints/A-degenerate-counterexample-to-the-critical-number-Arnold-bound-September-23-2026/paper.pdf)

</details>

<a name="r348"></a>

### 348 · Nonnegative-curvature Einstein classification and an <i>L</i><sup>2</sup> topological gap

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/348.md) · 3 papers

This classifies Einstein 4-manifolds with positive Einstein constant and nonnegative curvature (only the round sphere, ℂP² and S² × S²), and proves an L² gap theorem.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Zero-Plane Rigidity for Einstein Four-Manifolds](https://github.com/openai/math/blob/main/preprints/Zero-Plane-Rigidity-for-Einstein-Four-Manifolds-October-4-2026/einstein-boundary.pdf)
- [An L² Einstein Gap for Nonnegatively Curved Four-Manifolds](https://github.com/openai/math/blob/main/preprints/An-L2-Einstein-Gap-for-Nonnegatively-Curved-Four-Manifolds-October-5-2026/einstein-gap.pdf)
- [Positively curved Einstein four-manifolds](https://github.com/openai/math/blob/main/preprints/Positively-curved-Einstein-four-manifolds-September-23-2026/paper.pdf)

</details>

<a name="r349"></a>

### 349 · The Solomon–Yau least-volume conjecture

Not formally verified · 1 paper

The Solomon–Yau conjecture: the least-volume non-trivial minimal hypersurface in a round sphere is the smallest Clifford product. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Solomon–Yau least-volume theorem](https://github.com/openai/math/blob/main/preprints/The-Solomon-Yau-least-volume-theorem-September-23-2026/paper.pdf)

</details>

<a name="r350"></a>

### 350 · Yau’s nodal bounds: surfaces and higher dimensions

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/350.md) · 3 papers

Yau's nodal conjecture asks how long the zero lines of vibration modes (eigenfunctions) can be. On surfaces, this proves the sharp bound C·√λ. It also shows the bound fails in dimensions 3, 4 and 5.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Sharp nodal length on smooth surfaces](https://github.com/openai/math/blob/main/preprints/Sharp-nodal-length-on-smooth-surfaces-September-23-2026/paper.pdf)
- [Smooth counterexamples to Yau's nodal upper bound in dimensions three and four](https://github.com/openai/math/blob/main/preprints/Smooth-counterexamples-to-Yaus-nodal-upper-bound-in-dimensions-three-and-four-September-23-2026/paper.pdf)
- [Power-law violations of Yau's nodal upper bound](https://github.com/openai/math/blob/main/preprints/Power-law-violations-of-Yaus-nodal-upper-bound-September-23-2026/paper.pdf)

</details>

<a name="r351"></a>

### 351 · Scalar curvature and finite-time Ricci-flow singularities

Not formally verified · 3 papers

In 4D, Ricci flow can be continued as long as scalar curvature stays bounded. In higher dimensions this fails, shown by a counterexample.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [A closed Ricci flow with bounded scalar curvature and finite-time curvature blowup](https://github.com/openai/math/blob/main/preprints/A-closed-Ricci-flow-with-bounded-scalar-curvature-and-finite-time-curvature-blowup-September-24-2026/paper.pdf)
- [Bounded scalar curvature and smooth extension of four-dimensional Ricci flow](https://github.com/openai/math/blob/main/preprints/Bounded-scalar-curvature-and-smooth-extension-of-four-dimensional-Ricci-flow-September-24-2026/paper.pdf)
- [Path selection and an elliptic inequality on degenerating Ricci-flat trees](https://github.com/openai/math/blob/main/preprints/Path-selection-and-an-elliptic-inequality-on-degenerating-Ricci-flat-trees-September-24-2026/paper.pdf)

</details>

<a name="r352"></a>

### 352 · A finite-time singularity of Calabi flow

Not formally verified · 1 paper

Calabi flow can form a singularity in finite time (shown on ℂP¹⁰), disproving Chen's long-time existence conjecture.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A finite-time singularity of Calabi flow on projective space](https://github.com/openai/math/blob/main/preprints/A-finite-time-singularity-of-Calabi-flow-on-projective-space-September-24-2026/paper.pdf)

</details>

<a name="r353"></a>

### 353 · Affine Bernstein rigidity through dimension nine and a smooth dimension-ten counterexample

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/353.md) · 2 papers

The affine Bernstein problem: complete affine-maximal graphs are paraboloids in dimensions 3 through 9, and a smooth counterexample exists in dimension 10, so the range is sharp.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A Smooth Nonquadratic Entire Affine Maximal Graph in Dimension Ten](https://github.com/openai/math/blob/main/preprints/Smooth-Nonquadratic-Affine-Maximal-Graph-in-Dimension-Ten-October-5-2026/affine-maximal-dimension-ten.pdf)
- [The affine Bernstein theorem in dimensions three through nine](https://github.com/openai/math/blob/main/preprints/The-affine-Bernstein-theorem-in-dimensions-three-through-nine-September-24-2026/main.pdf)

</details>

<a name="r354"></a>

### 354 · The isoperimetric profile of the cubic three-torus

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/354.md) · 1 paper

This finds the least-area way to enclose each volume inside a cubic 3-torus, and classifies all minimizers: balls, tubes, slabs, and their complements.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Isoperimetric Conjecture for the Cubic Flat Three-Torus](https://github.com/openai/math/blob/main/preprints/The-Isoperimetric-Conjecture-for-the-Cubic-Flat-Three-Torus-September-24-2026/article.pdf)

</details>

<a name="r355"></a>

### 355 · Unique tangent flows at the first surface singularity

Not formally verified · 1 paper

For mean curvature flow of surfaces in ℝ³, the zoomed-in picture ("tangent flow") at the first singularity is unique, with no extra assumptions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Uniqueness of tangent flows at the first singular time of embedded surface mean-curvature flow](https://github.com/openai/math/blob/main/preprints/Tangent-flow-uniqueness-2026-09-24/paper.pdf)

</details>

<a name="r356"></a>

### 356 · Gigli’s characterization of Alexandrov curvature

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/356.md) · 2 papers

Gigli's conjecture: Alexandrov curvature bounds are characterized by the RCD condition with distributional sectional curvature bounds, in every dimension. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Gigli’s distributional curvature characterization of Alexandrov spaces](https://github.com/openai/math/blob/main/preprints/Giglis-distributional-curvature-characterization-of-Alexandrov-spaces-September-24-2026/main.pdf)
- [Weak Hessian bounds along every geodesic in RCD spaces](https://github.com/openai/math/blob/main/preprints/Weak-Hessian-bounds-along-every-geodesic-in-RCD-spaces-September-24-2026/weak-hessian-geodesics.pdf)

</details>

<a name="r357"></a>

### 357 · Bi-Lipschitz coordinates at every regular RCD point

Not formally verified · 1 paper

At every regular point of a non-collapsed RCD space (a very general curved space), there are bi-Lipschitz coordinates to ordinary ℝⁿ.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Bi-Lipschitz Coordinates at Regular Points of Noncollapsed RCD Spaces](https://github.com/openai/math/blob/main/preprints/Bi-Lipschitz-Coordinates-at-Regular-Points-of-Noncollapsed-RCD-Spaces-September-25-2026/paper.pdf)

</details>

<a name="r358"></a>

### 358 · A three-manifold without conjugate points or nonpositive curvature

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/358.md) · 1 paper

This gives a closed 3-manifold that admits a metric without conjugate points but no metric of nonpositive curvature, answering an old question negatively.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A Three-Manifold Without Conjugate Points and Without a Nonpositively Curved Metric](https://github.com/openai/math/blob/main/preprints/A-Three-Manifold-Without-Conjugate-Points-and-Without-a-Nonpositively-Curved-Metric-September-24-2026/paper.pdf)

</details>

<a name="r359"></a>

### 359 · Negative Kähler curvature without bounded holomorphic coordinates

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/359.md) · 2 papers

This builds a domain in ℂ³ with a complete, negatively pinched Kähler metric but no bounded holomorphic coordinates, disproving bounded-domain uniformization in that setting.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A negatively pinched Kähler threefold without bounded holomorphic coordinates](https://github.com/openai/math/blob/main/preprints/A-negatively-pinched-Kahler-threefold-without-bounded-holomorphic-coordinates-September-25-2026/paper.pdf)
- [One-sided negative sectional curvature and the holomorphic Liouville property](https://github.com/openai/math/blob/main/preprints/One-sided-negative-sectional-curvature-and-the-holomorphic-Liouville-property-September-25-2026/paper.pdf)

</details>

<a name="r360"></a>

### 360 · Weak MTW curvature gives convexity and regular optimal transport

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/360.md) · 2 papers

For optimal transport on curved spaces satisfying the weak Ma–Trudinger–Wang condition, this proves Villani's convexity conjecture, and that optimal transport maps are Hölder continuous.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Global Support and Convex Injectivity Domains under Weak MTW](https://github.com/openai/math/blob/main/preprints/Global-Support-and-Convex-Injectivity-Domains-under-Weak-MTW-September-25-2026/paper.pdf)
- [Uniform Bi-Holder Transport from Weak MTW](https://github.com/openai/math/blob/main/preprints/Uniform-Bi-Holder-Transport-from-Weak-MTW-September-25-2026/paper.pdf)

</details>

<a name="r361"></a>

### 361 · Failure of integer-degree harmonic dimension comparison

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/361.md) · 2 papers

Yau proposed that harmonic functions of polynomial growth on spaces with nonnegative Ricci curvature are no more numerous than in flat space. This disproves the integer-degree version on ℝ³.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [A counterexample to integer-degree harmonic dimension comparison](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-integer-degree-harmonic-dimension-comparison-September-25-2026/paper.pdf)
- [A Three-Dimensional Counterexample to Integer-Degree Harmonic Dimension Comparison](https://github.com/openai/math/blob/main/preprints/A-Three-Dimensional-Counterexample-to-Integer-Degree-Harmonic-Dimension-Comparison-September-26-2026/paper.pdf)

</details>

<a name="s-partial-differential-equations"></a>

## Partial differential equations

<a name="r362"></a>

### 362 · Global smoothness for relativistic Vlasov–Maxwell

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/362.md) · 1 paper · 🧠 [reasoning summary](https://github.com/openai/math/blob/main/reasoning_traces/relativistic-vlasov-maxwell.pdf)

The relativistic Vlasov–Maxwell system describes a plasma: charged particles moving in their own electromagnetic field. This proves smooth solutions exist for all time in 3D for large data, a famous open problem (Glassey–Strauss).

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Global classical solutions of the three-dimensional relativistic Vlasov–Maxwell system](https://github.com/openai/math/blob/main/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/paper.pdf)

</details>

<a name="r363"></a>

### 363 · Nonuniqueness with local conservation for the hard-sphere Boltzmann equation

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/363.md) · 2 papers

For the hard-sphere Boltzmann equation (the basic model of a dilute gas), this builds two different global entropy solutions from the same initial state, so uniqueness fails in this class.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Nonuniqueness with local conservation for the hard-sphere Boltzmann equation](https://github.com/openai/math/blob/main/preprints/Nonuniqueness-with-local-conservation-for-the-hard-sphere-Boltzmann-equation-October-5-2026/paper.pdf)
- [Nonuniqueness for the periodic hard-sphere Boltzmann equation](https://github.com/openai/math/blob/main/preprints/Nonuniqueness-for-the-periodic-hard-sphere-Boltzmann-equation-September-23-2026/paper.pdf)

</details>

<a name="r364"></a>

### 364 · Kinetic limits and fluctuations over the Boltzmann lifespan

Not formally verified · 2 papers

This derives Boltzmann's gas equation from Newton's laws for many particles over the whole regular time interval (not just a short time), plus the Gaussian fluctuations around it.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [The Boltzmann–Grad limit for stable radial potentials on regular kinetic intervals](https://github.com/openai/math/blob/main/preprints/The-Boltzmann-Grad-limit-for-stable-radial-potentials-on-regular-kinetic-intervals-September-23-2026/paper.pdf)
- [Hard-sphere fluctuations on the regular Boltzmann lifespan](https://github.com/openai/math/blob/main/preprints/Hard-sphere-fluctuations-on-the-regular-Boltzmann-lifespan-September-23-2026/paper.pdf)

</details>

<a name="r365"></a>

### 365 · Joint metric and connection recovery from one boundary patch

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/365.md) · 3 papers

In Calderón's inverse problem (the maths of electrical impedance tomography: seeing inside a body from boundary measurements), measurements on one small patch determine a metric and connection in dimension 3 and up. But rough conductivities in 3D cannot always be recovered.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (3)</summary>

- [Determination of a metric and a unitary connection from one boundary patch](https://github.com/openai/math/blob/main/preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/paper.pdf)
- [Smooth anisotropic uniqueness in the Calderón problem from one boundary patch](https://github.com/openai/math/blob/main/preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/paper.pdf)
- [Nonuniqueness for bounded measurable scalar conductivities in three dimensions](https://github.com/openai/math/blob/main/preprints/Nonuniqueness-for-Bounded-Measurable-Scalar-Conductivities-in-Three-Dimensions-September-23-2026/paper.pdf)

</details>

<a name="r366"></a>

### 366 · The planar Mumford–Shah regularity conjecture and local weak-<i>L</i><sup>4</sup> gradient bounds

Not formally verified · 1 paper

The Mumford–Shah model segments an image into smooth regions separated by edges. This proves the planar regularity conjecture: the edge set of an optimal segmentation is locally a smooth curve, a crack tip, or three curves meeting at 120°.

- **Quant trading:** ⚪ *No practical link:* The one-dimensional version of this energy (a smooth fit with a penalty per jump) is a classical change-point method already solved exactly by dynamic programming (optimal partitioning, PELT). This 2D result adds nothing to it.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Interior regularity of planar Mumford–Shah minimizers](https://github.com/openai/math/blob/main/preprints/Interior-regularity-of-planar-Mumford-Shah-minimizers-September-24-2026/Interior-regularity-of-planar-Mumford-Shah-minimizers-September-24-2026.pdf)

</details>

<a name="r367"></a>

### 367 · The critical dimension for the one-phase Bernoulli problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/367.md) · 1 paper

For the one-phase Bernoulli free-boundary problem, minimizers are smooth up to dimension 6, and the first singular minimizer appears in dimension 7. This pins down the critical dimension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The critical dimension for one-phase Bernoulli minimizers](https://github.com/openai/math/blob/main/preprints/The-critical-dimension-for-one-phase-Bernoulli-minimizers-September-24-2026/The-critical-dimension-for-one-phase-Bernoulli-minimizers-September-24-2026.pdf)

</details>

<a name="r368"></a>

### 368 · The three-dimensional Ball–Evans approximation problem

Not formally verified · 2 papers

The Ball–Evans approximation problem from elasticity: in 3D, every Sobolev homeomorphism can be approximated by smooth diffeomorphisms. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (2)</summary>

- [Strong diffeomorphic approximation in three dimensions for 1≤p≤2](https://github.com/openai/math/blob/main/preprints/Strong-diffeomorphic-approximation-in-three-dimensions-for-1-le-p-le-2-September-24-2026/main.pdf)
- [Strong diffeomorphic approximation in three dimensions for p>2](https://github.com/openai/math/blob/main/preprints/Strong-diffeomorphic-approximation-in-three-dimensions-for-p-gt-2-September-24-2026/main.pdf)

</details>

<a name="r369"></a>

### 369 · The hot spots conjecture for simply connected planar domains

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/369.md) · 1 paper

The hot spots conjecture (Rauch, 1974): in an insulated, simply connected flat room, the hottest and coldest points of the slowest-decaying temperature pattern are on the walls. Proven in a strict form for smooth simply connected planar domains.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Strict hot spots and absence of interior critical points on smooth simply connected planar domains](https://github.com/openai/math/blob/main/preprints/Strict-hot-spots-and-absence-of-interior-critical-points-on-smooth-simply-connected-planar-domains-September-24-2026/main.pdf)

</details>

<a name="r370"></a>

### 370 · The Lane–Emden and Hénon–Lane–Emden conjectures

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/370.md) · 1 paper

The Lane–Emden conjecture: in the subcritical range, a classic system of nonlinear elliptic equations has no positive solution on all of space. Proven, with its weighted Hénon extension.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [The Subcritical Hénon–Lane–Emden Conjecture](https://github.com/openai/math/blob/main/preprints/The-Subcritical-Henon-Lane-Emden-Conjecture-September-24-2026/paper.pdf)

</details>

<a name="r371"></a>

### 371 · Stable blowup for the defocusing Schrödinger equation

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/371.md) · 1 paper

The defocusing nonlinear Schrödinger equation is usually expected to be well behaved. This shows that on a 12-dimensional torus, with a large enough power, finite-time blowup can happen and is stable under small perturbations.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Stable self-similar blowup for a supercritical defocusing Schrödinger equation on the torus](https://github.com/openai/math/blob/main/preprints/Stable-Self-Similar-Blowup-for-a-Supercritical-Defocusing-Schrodinger-Equation-on-the-Torus-September-24-2026/paper.pdf)

</details>

<a name="r372"></a>

### 372 · Global uniqueness in smooth isotropic elasticity

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/372.md) · 1 paper

In 3D elasticity, boundary measurements of displacement and force determine both elastic (Lamé) parameters everywhere inside, without extra assumptions.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Global Uniqueness for the Smooth Isotropic Elasticity Inverse Problem](https://github.com/openai/math/blob/main/preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/article.pdf)

</details>

<a name="r373"></a>

### 373 · Nonattainment of the three-marginal Coulomb Monge problem

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/373.md) · 1 paper

In multi-marginal Coulomb optimal transport (used in density functional theory), the optimal arrangement of 3 electrons need not be a deterministic function of the first one's position: the "Monge ansatz" fails.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A counterexample to the Monge ansatz for the three-marginal Coulomb cost](https://github.com/openai/math/blob/main/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/paper.pdf)

</details>

<a name="r374"></a>

### 374 · Sharp one-third stability of Brenier maps

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/374.md) · 1 paper

Optimal transport (Brenier) maps move one probability distribution onto another as cheaply as possible. This proves they are only cube-root stable: if the target moves by δ (in Wasserstein distance), the map can move by about δ^(1/3), and that is sharp. It disproves the conjectured square-root bound.

- **Quant trading:** 🟡 *Background.* Applies only in two or more dimensions: for 1D quantile mapping of one return series the map moves by exactly the distance, with no cube-root loss. If you ever build a multivariate OT scenario map (say, joint daily P&L of several strategies, or BTC/NQ return pairs), refit it on resampled data and measure how far the scenarios move; in the worst case it is far less stable than the data.
- **Politeia:** ⚪ *No practical link.*

<details><summary>Papers (1)</summary>

- [Sharp One-Third Stability of Brenier Maps](https://github.com/openai/math/blob/main/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/article.pdf)

</details>

<a name="r375"></a>

### 375 · De Giorgi's conjecture in dimension eight

Not formally verified · 1 paper

De Giorgi's conjecture (1978) at the sharp dimension 8: a solution of the Allen–Cahn phase-transition equation that increases in one direction is really one-dimensional, a flat transition. Proven.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [A positive resolution of De Giorgi's conjecture in dimension eight](https://github.com/openai/math/blob/main/preprints/De-Giorgis-conjecture-in-dimension-eight-September-26-2026/article.pdf)

</details>

<a name="r376"></a>

### 376 · Universal computation in forced Navier–Stokes flows

📐 [Lean-checked](https://github.com/openai/math/blob/main/lean/docs/376.md) · 9 papers · 🔧 proof repaired Oct 7

This designs external forces on a viscous 3D fluid so that it simulates any computer program: a marked particle reaches a target region exactly when the program halts. So predicting forced Navier–Stokes flows is undecidable in general. A paper was revised on Oct 7.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (9)</summary>

- [Finite Instructions and Solenoidal Shear Flows](https://github.com/openai/math/blob/main/preprints/Finite-Instructions-and-Solenoidal-Shear-Flows-September-27-2026/manuscript.pdf)
- [A Fixed Particle Test for Computation in a Forced Viscous Flow](https://github.com/openai/math/blob/main/preprints/A-Fixed-Particle-Test-for-Computation-in-a-Forced-Viscous-Flow-September-27-2026/manuscript.pdf)
- [Universal Computation with Eventually Stationary Navier–Stokes Forcing](https://github.com/openai/math/blob/main/preprints/Universal-Computation-with-Eventually-Stationary-Navier-Stokes-Forcing-September-27-2026/manuscript.pdf)
- [Geometric Programs for Solenoidal Forcing](https://github.com/openai/math/blob/main/preprints/Geometric-Programs-for-Solenoidal-Forcing-September-27-2026/manuscript.pdf)
- [Prefix Instructions and Incompressible Flows](https://github.com/openai/math/blob/main/preprints/Prefix-Instructions-and-Incompressible-Flows-September-27-2026/manuscript.pdf)
- [Computation under Rapidly Vanishing Navier–Stokes Forcing](https://github.com/openai/math/blob/main/preprints/Computation-under-Rapidly-Vanishing-Navier-Stokes-Forcing-September-27-2026/manuscript.pdf)
- [Velocity-Field Detection of Computation in Forced Navier–Stokes Flows](https://github.com/openai/math/blob/main/preprints/Velocity-Field-Detection-of-Computation-in-Forced-Navier-Stokes-Flows-September-27-2026/manuscript.pdf)
- [Scalar Potentials and Slow Clocks for Forced Fluid Computation](https://github.com/openai/math/blob/main/preprints/Scalar-Potentials-and-Slow-Clocks-for-Forced-Fluid-Computation-September-27-2026/manuscript.pdf)
- [Incompressible Box Transport and Finite Computation](https://github.com/openai/math/blob/main/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/manuscript.pdf)

</details>

<a name="r377"></a>

### 377 · Interior $`C^{1,\alpha}`$ regularity for infinity-harmonic functions

Not formally verified · 1 paper

Infinity-harmonic functions (the "tug-of-war game" equation, and best Lipschitz extensions) are proven to have Hölder-continuous gradients in every dimension. Before, this was known only in 2D.

- **Quant trading / Politeia:** ⚪ no practical link.

<details><summary>Papers (1)</summary>

- [Uniform Interior $`C^{1,\alpha}`$ Estimates for Infinity-Harmonic Functions](https://github.com/openai/math/blob/main/preprints/Uniform-Interior-C1alpha-Estimates-for-Infinity-Harmonic-Functions-October-4-2026/interior-c1-infinity-harmonic.pdf)

</details>
