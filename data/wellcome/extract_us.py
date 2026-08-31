#!/usr/bin/env python
"""Extract the U.S. subsets of the Wellcome Global Monitor 2018 and 2020 waves.

Reads the raw files fetched by fetch.sh (data/wellcome/downloads/, gitignored)
and writes two small CSVs with the key trust-in-science items, demographics
and the national weight only:

    downloads/derived/wgm2018_us.csv   (2018 wave, WP5 == 1)
    downloads/derived/wgm2020_us.csv   (2020 wave, COUNTRYNEW == 'United States')

Codes are kept as in the source (1 = A lot ... 4 = Not at all for the trust
items) except that the DK/Refused codes 98/99 are set to NA. Age 100 (Refused,
2018) and Age 100 (DK/Refused, 2020; 99 = 99+) are set to NA as well.

Run:  uv run --with pandas --with openpyxl python data/wellcome/extract_us.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DL = HERE / "downloads"
OUT = DL / "derived"

XLSX_2018 = DL / "wgm2018-dataset-crosstabs-all-countries.xlsx"
ZIP_2020 = DL / "wgm_full_wave2_public_file.zip"
CSV_2020_MEMBER = "wgm_full_wave2_public_file_final (1)_csv.csv"

# 4-point trust items (1 = A lot, 2 = Some, 3 = Not much, 4 = Not at all)
ITEMS_2018 = ["Q11C", "Q12", "Q13", "Q14A", "Q14B", "Q15A", "Q15B", "WGM_Index"]
ITEMS_2020 = ["W5C", "W6", "W7A", "W7B", "W7C", "W15"]

DEMO_2018 = ["Age", "AgeCategories", "Gender", "Education", "Household_Income"]
DEMO_2020 = ["Age", "age_var1", "Gender", "Education", "Household_Income"]

MISSING = {98, 99}


def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip().replace({"": None}), errors="coerce")


def clean(df: pd.DataFrame, items: list[str], demo: list[str], weight: str) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for c in items + demo:
        v = to_num(df[c])
        out[c] = v.mask(v.isin(MISSING))  # WGM_Index is 1-4 only; masking is a no-op
    # Age: 2018 100 = Refused; 2020 100 = DK/Refused (99 = 99+ in both, keep)
    out["Age"] = out["Age"].mask(out["Age"] >= 100)
    out[weight] = to_num(df[weight])
    return out


def extract_2018() -> pd.DataFrame:
    df = pd.read_excel(XLSX_2018, sheet_name="Full dataset", dtype=str)
    us = df[to_num(df["WP5"]) == 1].copy()
    out = clean(us, ITEMS_2018, DEMO_2018, "wgt")
    out.insert(0, "FIELD_DATE", pd.to_datetime(us["FIELD_DATE"]).dt.date.astype(str))
    return out.reset_index(drop=True)


def extract_2020() -> pd.DataFrame:
    df = pd.read_csv(ZIP_2020, dtype=str, encoding="utf-8-sig")
    us = df[df["COUNTRYNEW"].str.strip() == "United States"].copy()
    out = clean(us, ITEMS_2020, DEMO_2020, "WGT")
    out.insert(0, "WPID_RANDOM", us["WPID_RANDOM"].str.strip())
    out.insert(1, "FIELD_DATE", us["FIELD_DATE"].str.strip())
    return out.reset_index(drop=True)


def wtab(df: pd.DataFrame, col: str, w: str) -> pd.DataFrame:
    d = df[[col, w]].dropna()
    t = pd.DataFrame(
        {
            "n": d.groupby(col)[w].size(),
            "unweighted_%": (d.groupby(col)[w].size() / len(d) * 100).round(1),
            "weighted_%": (d.groupby(col)[w].sum() / d[w].sum() * 100).round(1),
        }
    )
    return t


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    d18 = extract_2018()
    d20 = extract_2020()
    d18.to_csv(OUT / "wgm2018_us.csv", index=False)
    d20.to_csv(OUT / "wgm2020_us.csv", index=False)
    print(f"2018 US n = {len(d18)}  (weight sum {d18['wgt'].sum():.1f}, mean {d18['wgt'].mean():.3f})")
    print(f"2020 US n = {len(d20)}  (weight sum {d20['WGT'].sum():.1f}, mean {d20['WGT'].mean():.3f})")
    for c in ["Q11C", "Q14B", "Q13", "Q14A"]:
        print(f"\n2018 {c}\n{wtab(d18, c, 'wgt')}")
    for c in ["W5C", "W7B"]:
        print(f"\n2020 {c}\n{wtab(d20, c, 'WGT')}")
    print("\n2018 missing per column:\n", d18.isna().sum().to_dict())
    print("2020 missing per column:\n", d20.isna().sum().to_dict())
