"""Load NQ 1-minute bars exported from MultiCharts (or any similar CSV/TXT).

Handles, without being told:
  * delimiter , ; or tab, with or without a header row
  * MultiCharts QuoteManager / chart exports (Date,Time,Open,High,Low,Close,Volume
    or ...,Up,Down), NinjaTrader 8 exports (yyyyMMdd HHmmss;O;H;L;C;V), generic
    datetime,open,high,low,close,volume files
  * date written MM/DD/YYYY, DD/MM/YYYY (Greek locale), YYYY-MM-DD, YYYYMMDD, DD.MM.YYYY
  * bars stamped at their close (MultiCharts convention) or at their open
  * the clock the file was written in (Central, Eastern, Athens, London, UTC ...)

The last two are detected from the regular-session open: NQ's busiest-jump minute
is the 08:30 Central bar. Override with tz= / stamp= when the detector is unsure.
"""
from __future__ import annotations

import glob
import gzip
import io
import os
import re
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

CT = "America/Chicago"
RTH_OPEN_MIN = 8 * 60 + 30  # 08:30 CT

# (January offset, July offset) of a clock relative to US Central -> zone name.
_OFFSET_TO_TZ = {
    (0, 0): "America/Chicago",
    (1, 1): "America/New_York",
    (-1, -1): "America/Denver",
    (-2, -2): "America/Los_Angeles",
    (6, 5): "UTC",
    (6, 6): "Europe/London",
    (7, 7): "Europe/Berlin",
    (8, 8): "Europe/Athens",
}

_DATE_FORMATS = ["%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y%m%d", "%d.%m.%Y",
                 "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y", "%m/%d/%y", "%d/%m/%y"]


@dataclass
class Bars:
    """1-minute bars in Central time, keyed by bar open time."""
    t: np.ndarray        # datetime64[m], bar open time, Central, naive
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    v: np.ndarray
    info: dict = field(default_factory=dict)

    def __post_init__(self):
        mins = self.t.astype("int64")
        self.day = (mins // 1440).astype("int64")          # calendar day number (CT)
        self.mod = (mins % 1440).astype("int64")           # minute of day of bar open
        # Globex session date: the 17:00 open belongs to the next calendar day.
        self.sess = ((mins + 7 * 60) // 1440).astype("int64")
        self.n = len(self.t)

    def slice_dates(self, start=None, end=None) -> "Bars":
        m = np.ones(self.n, bool)
        if start is not None:
            m &= self.t >= np.datetime64(pd.Timestamp(start), "m")
        if end is not None:
            m &= self.t < np.datetime64(pd.Timestamp(end), "m")
        return Bars(self.t[m], self.o[m], self.h[m], self.l[m], self.c[m], self.v[m], dict(self.info))

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame({"t": self.t, "o": self.o, "h": self.h, "l": self.l,
                             "c": self.c, "v": self.v})


# ----------------------------------------------------------------------------- reading
def _open_text(path: str) -> io.TextIOBase:
    if path.endswith(".gz"):
        return io.TextIOWrapper(gzip.open(path, "rb"), encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")


def _sniff(path: str):
    with _open_text(path) as fh:
        head = [fh.readline() for _ in range(5)]
    head = [h for h in head if h.strip()]
    if not head:
        raise ValueError(f"{path}: empty file")
    first = head[0]
    delim = max([",", ";", "\t"], key=lambda d: first.count(d))
    has_header = bool(re.search(r"[A-Za-z]{3,}", first.replace("AM", "").replace("PM", "")))
    return delim, has_header


def _norm(name: str) -> str:
    return re.sub(r"[^a-z]", "", name.lower())


def _read_one(path: str) -> pd.DataFrame:
    delim, has_header = _sniff(path)
    df = pd.read_csv(path, sep=delim, header=0 if has_header else None, dtype=str,
                     compression="infer", skipinitialspace=True)
    df = df.dropna(how="all")
    if has_header:
        cols = {_norm(c): c for c in df.columns}
    else:
        n = df.shape[1]
        if n >= 7:
            names = ["date", "time", "open", "high", "low", "close", "volume"] + [f"x{i}" for i in range(n - 7)]
        elif n == 6:
            names = ["datetime", "open", "high", "low", "close", "volume"]
        else:
            raise ValueError(f"{path}: cannot interpret {n} unnamed columns")
        df.columns = names
        cols = {c: c for c in names}

    def pick(*keys):
        for k in keys:
            if k in cols:
                return cols[k]
        return None

    c_date = pick("date", "day")
    c_time = pick("time")
    c_dt = pick("datetime", "timestamp", "dateandtime", "localtime", "gmttime", "ts")
    c_o, c_h, c_l, c_c = pick("open", "o"), pick("high", "h"), pick("low", "l"), pick("close", "last", "c")
    c_v = pick("volume", "vol", "totalvolume", "v", "ticks")
    c_up, c_dn = pick("up", "upvol", "upticks", "upvolume"), pick("down", "downvol", "downticks", "downvolume")
    if None in (c_o, c_h, c_l, c_c):
        raise ValueError(f"{path}: need open/high/low/close columns, found {list(df.columns)}")

    out = pd.DataFrame({"o": pd.to_numeric(df[c_o], errors="coerce"),
                        "h": pd.to_numeric(df[c_h], errors="coerce"),
                        "l": pd.to_numeric(df[c_l], errors="coerce"),
                        "c": pd.to_numeric(df[c_c], errors="coerce")})
    if c_v is not None:
        out["v"] = pd.to_numeric(df[c_v], errors="coerce")
    elif c_up is not None and c_dn is not None:
        out["v"] = pd.to_numeric(df[c_up], errors="coerce") + pd.to_numeric(df[c_dn], errors="coerce")
    else:
        out["v"] = np.nan

    if c_date is not None and c_time is not None:
        out["date_s"] = df[c_date].str.strip().str.strip('"')
        out["time_s"] = df[c_time].str.strip().str.strip('"')
    elif c_dt is not None or (c_date is not None and c_time is None):
        s = df[c_dt if c_dt is not None else c_date].str.strip().str.strip('"')
        parts = s.str.split(r"[ T]", n=1, regex=True, expand=True)
        out["date_s"] = parts[0]
        out["time_s"] = parts[1] if parts.shape[1] > 1 else "00:00"
    else:
        raise ValueError(f"{path}: no date/time columns found")
    return out


def _parse_dates(date_s: pd.Series) -> pd.Series:
    uniq = pd.Series(date_s.unique())
    best = None
    for fmt in _DATE_FORMATS:
        parsed = pd.to_datetime(uniq, format=fmt, errors="coerce")
        ok = parsed.notna().mean()
        if ok < 0.999:
            continue
        # Prefer the reading that keeps the file in chronological order.
        order = (parsed.diff().dt.days.fillna(0) >= 0).mean()
        score = (ok, order)
        if best is None or score > best[0]:
            best = (score, fmt, parsed)
    if best is None:
        raise ValueError(f"unrecognised date format, e.g. {uniq.iloc[0]!r}")
    mapping = dict(zip(uniq, best[2]))
    return date_s.map(mapping), best[1]


def _parse_times(time_s: pd.Series) -> pd.Series:
    """Return minutes since midnight."""
    s = time_s.astype(str).str.strip()
    ampm = s.str.contains(r"[AaPp][Mm]$", regex=True)
    digits = s.str.replace(r"[^0-9:]", "", regex=True)
    has_colon = digits.str.contains(":")
    hh = pd.Series(0, index=s.index, dtype="int64")
    mm = pd.Series(0, index=s.index, dtype="int64")
    if has_colon.any():
        p = digits[has_colon].str.split(":", expand=True)
        hh[has_colon] = p[0].astype(int)
        mm[has_colon] = p[1].astype(int)
    nc = ~has_colon
    if nc.any():
        d = digits[nc].str.zfill(4)
        long = d.str.len() >= 6          # HHMMSS
        hh[nc] = np.where(long, d.str[:-4], d.str[:-2]).astype(int)
        mm[nc] = np.where(long, d.str[-4:-2], d.str[-2:]).astype(int)
    if ampm.any():
        pm = s.str.upper().str.endswith("PM")
        hh = np.where(ampm & pm & (hh < 12), hh + 12, np.where(ampm & ~pm & (hh == 12), 0, hh))
        hh = pd.Series(hh, index=s.index)
    return hh * 60 + mm


def read_files(paths) -> tuple[pd.DataFrame, dict]:
    frames = [_read_one(p) for p in paths]
    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["o", "h", "l", "c"])
    day, fmt = _parse_dates(df["date_s"])
    minutes = _parse_times(df["time_s"])
    ts = day + pd.to_timedelta(minutes, unit="m")
    raw = pd.DataFrame({"ts": ts.values, "o": df["o"].values, "h": df["h"].values,
                        "l": df["l"].values, "c": df["c"].values, "v": df["v"].values})
    raw = raw.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last")
    return raw.reset_index(drop=True), {"date_format": fmt, "files": [os.path.basename(p) for p in paths]}


# ----------------------------------------------------------------------------- detection
def _spike_minute(ts: pd.Series, v: pd.Series, months) -> int | None:
    m = ts.dt.month.isin(months) & ts.dt.dayofweek.lt(5)
    if m.sum() < 2000 or v[m].isna().all():
        return None
    mod = ts[m].dt.hour * 60 + ts[m].dt.minute
    med = v[m].groupby(mod.values).median().reindex(range(1440))
    prev = med.shift(1)
    ratio = (med / prev.replace(0, np.nan)).fillna(0)
    ratio[med < med.median()] = 0      # ignore jumps between near-empty minutes
    return int(ratio.idxmax())


def detect_clock(raw: pd.DataFrame) -> dict:
    """Infer timestamp convention and source time zone from the 08:30 CT volume jump."""
    ts, v = raw["ts"], raw["v"]
    out = {"tz": None, "stamp": None, "jan_spike": None, "jul_spike": None, "confident": False}
    jan = _spike_minute(ts, v, [1, 2, 12])
    jul = _spike_minute(ts, v, [6, 7, 8])
    out["jan_spike"], out["jul_spike"] = jan, jul
    spikes = [s for s in (jan, jul) if s is not None]
    if not spikes:
        return out
    # Bar stamped at close => spike lands on hh:31, at open => hh:30 (for an hh:30 open).
    sub = [s % 60 for s in spikes]
    if all(x == 31 for x in sub):
        out["stamp"] = "close"
    elif all(x == 30 for x in sub):
        out["stamp"] = "open"
    shift = 1 if out["stamp"] == "close" else 0
    offs = [round((s - shift - RTH_OPEN_MIN) / 60) for s in (jan if jan is not None else jul,
                                                               jul if jul is not None else jan)]
    out["offsets"] = tuple(offs)
    tz = _OFFSET_TO_TZ.get(tuple(offs))
    out["tz"] = tz
    out["confident"] = tz is not None and out["stamp"] is not None and None not in (jan, jul)
    return out


# ----------------------------------------------------------------------------- main entry
def find_data_files(path: str) -> list[str]:
    if os.path.isfile(path):
        return [path]
    pats = ["*.csv", "*.txt", "*.csv.gz", "*.txt.gz"]
    files = []
    for p in pats:
        files += glob.glob(os.path.join(path, "**", p), recursive=True)
    # keep files that look like NQ price data, not trade lists or notes
    keep = [f for f in sorted(set(files)) if re.search(r"nq", os.path.basename(f), re.I)]
    return keep or sorted(set(files))


def load_bars(path, tz: str | None = None, stamp: str | None = None,
              interval_min: int = 1, verbose: bool = True) -> Bars:
    """Load 1-minute NQ bars and return them in Central time keyed by bar open."""
    paths = find_data_files(path) if isinstance(path, str) else list(path)
    if not paths:
        raise FileNotFoundError(f"no data files under {path}")
    raw, info = read_files(paths)
    det = detect_clock(raw)
    info["detected"] = det
    tz = tz or det["tz"]
    stamp = stamp or det["stamp"] or "close"
    if tz is None:
        raise ValueError("could not detect the file's time zone; pass tz='America/New_York' (etc.). "
                         f"Detection: {det}")
    ts = raw["ts"]
    if stamp == "close":
        ts = ts - pd.Timedelta(minutes=interval_min)
    if tz != CT:
        ts = (ts.dt.tz_localize(tz, ambiguous="NaT", nonexistent="NaT")
                .dt.tz_convert(CT).dt.tz_localize(None))
    keep = ts.notna().values
    raw = raw[keep]
    ts = ts[keep]
    t = ts.values.astype("datetime64[m]")
    order = np.argsort(t, kind="stable")
    t = t[order]
    vals = {k: raw[k].values[order].astype("float64") for k in "ohlcv"}
    vals["v"] = np.nan_to_num(vals["v"], nan=0.0)
    uniq = np.concatenate([[True], t[1:] != t[:-1]])
    bars = Bars(t[uniq], *(vals[k][uniq] for k in "ohlcv"))
    gaps = np.diff(bars.t.astype("int64"))
    info.update({"tz_source": tz, "stamp": stamp, "bars": bars.n,
                 "first": str(bars.t[0]), "last": str(bars.t[-1]),
                 "median_step_min": float(np.median(gaps)) if len(gaps) else None,
                 "zero_volume_share": float((bars.v == 0).mean())})
    bars.info = info
    if verbose:
        print(f"[data] {len(paths)} file(s), {bars.n:,} bars {info['first']} -> {info['last']} CT")
        print(f"[data] date format {info['date_format']}, source clock {tz} "
              f"({'detected' if det['tz'] == tz else 'given'}), stamped at bar {stamp}")
        if not det["confident"]:
            print(f"[data] WARNING clock detection not certain: {det}. Pass --tz/--stamp if wrong.")
        if info["median_step_min"] and info["median_step_min"] > interval_min:
            print(f"[data] WARNING median bar spacing {info['median_step_min']} min; strategy 2 needs 1-minute bars.")
    return bars
