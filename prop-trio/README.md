# Prop Trio: Matteo's three NQ prop-firm strategies, tested properly

Three strategies from the interview, built to pass a prop-firm challenge: hit the profit target
before the drawdown.

| | Strategy | Chart logic | Side |
|---|---|---|---|
| S1 | **Vault Break**: breakout above the midnight "noise" barrier, above VWAP | 30-min signals | long |
| S2 | **VWAP pullback + ADX gate**: arm above the 08:30–09:00 range, buy the VWAP reclaim | 1-min | long |
| S3 | **Overnight bias ORB**: overnight-range third sets the side, 08:30–08:45 range breakout | 15-min signals | long + short |

* **[SPEC.md](SPEC.md)**: every rule with its transcript timestamp, what DeepSeek's summary gets
  wrong, each ambiguity with the default and the variant tested, and the pre-registered
  in-sample/out-of-sample plan.
* **[multicharts/](multicharts/)**: PowerLanguage signals for all three, faithful by default, each
  improvement an input switch. Setup: [multicharts/SETUP.md](multicharts/SETUP.md).
* **[bench/](bench/)**: Python test bench (numpy + pandas only). It reads your NQ 1-minute export
  and runs the full protocol: faithful versions, variants, in-sample selection, sizing,
  out-of-sample check, Apex / LucidPro / 21-day challenge simulations, correlation, the bench
  rule, and fill/cost sensitivity. It writes one HTML report.

## Run it on your data (laptop, Desktop\NQ Section)

```bat
cd %USERPROFILE%\Desktop
git clone -b claude/affectionate-planck-8z8kpp https://github.com/Aeov/Vvseav.git prop-trio-repo
cd prop-trio-repo\prop-trio
pip install numpy pandas
python -m bench.run --data "%USERPROFILE%\Desktop\NQ Section"
```

Open `results\NQ_Section\report.html`. A 10-year run takes a few minutes.

**The data it needs:** NQ continuous, **1-minute** bars, 24-hour session, with volume. It searches
the folder (including subfolders) for `.txt` / `.csv` files with "NQ" in the name. If several are
found (other timeframes, trade lists), point `--data` at the 1-minute file itself. It detects on its
own:

* the date format, including DD/MM/YYYY (Greek locale)
* the clock the file was written in (Central, Eastern, Athens, London, UTC)
* whether bars are stamped at their open or close

It prints what it found. If the detection is wrong, override it with
`--tz America/New_York --stamp close`.

**No 1-minute export yet?** In MultiCharts: QuoteManager → NQ (continuous) → right-click → **Export
Data** → 1 minute, all dates, ASCII → save as `NQ_1min.txt` in the NQ Section folder.

### Or let a Claude session on the laptop do it

Paste this into the Claude session that can see `Desktop\NQ Section`:

> Clone branch `claude/affectionate-planck-8z8kpp` of github.com/Aeov/Vvseav. In `prop-trio/`, run
> `python -m unittest discover -s tests`, then
> `python -m bench.run --data "<full path to Desktop\NQ Section or the NQ 1-minute file>"`.
> Commit `prop-trio/results/<name>/summary.json` and `report.html` to the same branch and push.

The cloud session can then read the results and continue from there.

### Or push the bars here instead

Split the 1-minute file by year, gzip each (`NQ_1min_2016.txt.gz` …, well under GitHub's 100 MB
limit), copy them into `prop-trio/data/`, then
`git add -f prop-trio/data/*.gz && git commit -m "NQ 1-min bars" && git push`.

## Check the plumbing first

```bash
python -m unittest discover -s tests        # 25 tests, about a minute
python -m bench.run --synthetic --quick     # the whole pipeline on FAKE data, ~20 s
```

The tests cover these, on hand-built bars:

* every rule: re-entries and the 3-trade cap, the arm/touch/ADX wait, the bias thirds, the
  30-minute opening range, stop/target distances
* the indicators against hand calculations
* the challenge rules: end-of-day trailing drawdown, consistency, expiry
* the loader on Eastern, Central and Athens exports

They also check that **the MultiCharts code (ported line by line) and the bench produce identical
trades**.

## Honest limits

* **No result in this folder comes from real market data yet.** The synthetic run only proves the
  pipeline works.
* Pass rates from rolling starts overlap and aren't independent. The bootstrap and back-to-back
  numbers in the report are the fairer read.
* Firm rules come from your 13 Aug 2026 sheet. Check them against your own account.
