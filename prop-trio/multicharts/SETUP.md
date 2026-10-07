# MultiCharts setup for the three signals

The `.txt` files are PowerLanguage source. In the PowerLanguage Editor: File → New → Signal,
name it as the file (e.g. `PT_S1_VaultBreak`), paste, compile (F3).

## One chart per strategy

MultiCharts holds one net position per chart. S1 and S2 are both long NQ, so on one chart they would
net into a single position. Use **three charts**, the way Matteo runs them [01:17:23], or Portfolio Trader.

| Setting | Value |
|---|---|
| Symbol | **NQ** to compare with Matteo's per-contract numbers; **MNQ** to trade the challenge |
| Resolution | **1 minute**, all three signals (each refuses to run on anything else) |
| Session | CME Globex 24-hour (17:00–16:00 CT) |
| Format Instrument → Settings → Time Zone | **Exchange** |
| Data range | as much as you have; out-of-sample starts **2023-01-01** |
| Max bars back | 50 |

## Strategy Properties

| Setting | Value |
|---|---|
| Commission | $2.09 per contract per side (NQ) / $0.62 (MNQ) |
| Slippage | 1 tick per contract per side ($5 NQ / $0.50 MNQ) |
| Backtesting → fill limit orders | **only when price trades through** the limit |
| Contracts | 1 NQ to compare; **5 MNQ** per strategy is Matteo's challenge size |
| Bar Magnifier | not needed on a 1-minute chart; tick magnifier if you have ticks (more exact) |

Stops and targets are written in **points × BigPointValue**, so the same code is correct on NQ and
MNQ. They call `SetStopContract`, so they don't change size when you trade 5 micros. (This was the
stop bug in Kun.)

## Inputs: faithful versus variants

Each file's header lists them. The defaults are the interview's rules.

| Signal | Input | Faithful | Variant |
|---|---|---|---|
| S1 | `UseATRExits`, `TargetATR`, `StopATR` | false | S1-v1: true, with the two multiples printed in the Python report (40 ÷ and 75 ÷ in-sample median ATR) |
| S1 | `UseTODBand` | false | S1-v2: true |
| S2 | `VWAPAnchor` | 0 (midnight) | S2-v1: 830 |
| S2 | `DynamicExits` | false | S2-v2: true |
| S2 | `MaxTrades` | 1 | S2-v3: 3 |
| S3 | `ONStart` | 0 (midnight) | S3-v1: 1700; sensitivity 2300 |
| S3 | `TargetR` | 3.0 | S3-v2: 1.5 |
| S3 | `FirstSignal` | 900 | sensitivity 915, 930 |

## Matching the Python bench

`tests/pl_port.py` is a line-by-line Python port of these three files, run with MultiCharts' order
semantics. `tests/test_pl_parity.py` checks that it produces **the same trades** as the bench for the
faithful version and every variant. So the MultiCharts List of Trades should match the bench's
`trades_all.csv.gz`, apart from three known differences:

* **Early-close days** (12:15 CT halt, about 3 a year): the bench exits at the last bar before the
  halt; MultiCharts holds to the next 17:00 bar.
* **Volume**: the code uses `MaxList(Volume, Ticks)`, which is total volume under either "Build volume
  on" setting. If your exported file holds something else, VWAP differs slightly.
* **Missing 1-minute bars** at a :00/:15/:30 boundary: MultiCharts skips that signal check, and the
  bench does too. Only the first-bar MaxBarsBack warm-up differs.
