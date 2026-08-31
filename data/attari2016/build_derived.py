#!/usr/bin/env python
"""Build PII-free, recoded respondent-level CSVs from the Attari, Krantz & Weber
2016/2019 workbooks in downloads/ (fetched by fetch.sh).

Run:  uv run --with pandas --with openpyxl --with xlrd python data/attari2016/build_derived.py

Outputs (all under downloads/derived/, gitignored like the raw workbooks):

  attari2016_adhom.csv               Ad_Hom_Final.xls  (2016 paper; Survey 1 + 2, 18 arms)
  attari2019_study1_policy.csv       Study1_Policy.xlsx (2019 paper Study 1, 12 arms)
  attari2019_study2_reformation.csv  Study2_Reformation.xls (2019 paper Study 2, 6 arms)
  arm_summary.csv                    per-arm n, credibility means/SDs, intention rates
                                     (the only table intended for any deposit)

What the builder does, per study:
  * drops `Zip` (Study 1 only; 5-digit ZIP + age/gender/income is re-identifying)
  * keeps every other raw column under its codebook name (sheet `Codes`), except
    the check-all-that-apply column `None`, renamed `No_Action`
  * reconstructs the arm from `Study`/`Condition` into `arm` (unique label) plus
    factor columns (`domain`, `footprint`, `frame`, `researcher_gender`, `policy`,
    `reform`, ...) per the codebook
  * builds the six credibility items in the credibility direction: the four
    positively worded items (Consistent, Sincere, Good_Reason, Advice) are
    reversed 1..5 -> 5..1; the two negatively worded items (No_Authority,
    No_Cred) are kept (strongly agree = 1 = low credibility). Result columns
    `cred_consistent` ... `cred_advice` (1..5, 5 = most credible).
  * `cred_sum` (6..30), `cred_mean` (1..5), and the papers' `cred_score`
    = (cred_sum - 18) / 12 in [-1, +1]
  * recodes the Qualtrics income quirk (code 8 -> 7 = "> $200,000") wherever a
    workbook has code 8 and no code 7 (in practice: Ad_Hom_Final.xls)
  * gender: `gender` in {male, female, other, NA}; `male` 1/0 with other -> NA
    (Ad_Hom's `MaleC` uses 3 for "other")
  * coerces blank-string cells in Study 2 (`MPG`, `Flights`, `Meat`) to NA
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DL = HERE / "downloads"
OUT = DL / "derived"

CRED_POS = ["Consistent", "Sincere", "Good_Reason", "Advice"]  # reverse these
CRED_NEG = ["No_Authority", "No_Cred"]  # keep as coded
CRED_ORDER = ["Consistent", "Sincere", "No_Authority", "Good_Reason", "No_Cred", "Advice"]
INTENTIONS = ["Fly", "Home", "Transport", "Some", "No_Action", "Other", "Conserve"]

# ---- arm definitions (from sheet `Codes` of each workbook) -------------------

# Ad_Hom_Final.xls: Study x Condition -> label, domain, footprint, frame, researcher gender
ADHOM_ARMS: dict[tuple[int, int], tuple[str, str, str, str, str]] = {
    # (study, cond): (label, domain, footprint, frame, researcher_gender)
    (1, 1): ("S1 High Fly", "fly", "high", "later_learn", "male"),
    (1, 2): ("S1 Low Fly", "fly", "low", "later_learn", "male"),
    (1, 3): ("S1 Offset", "fly", "offset", "later_learn", "male"),
    (1, 4): ("S1 High Home", "home", "high", "later_learn", "male"),
    (1, 5): ("S1 Low Home", "home", "low", "later_learn", "male"),
    (1, 6): ("S1 High Fly Female", "fly", "high", "later_learn", "female"),
    (1, 7): ("S1 Low Fly Female", "fly", "low", "later_learn", "female"),
    (2, 1): ("S2 High Fly", "fly", "high", "later_learn", "male"),
    (2, 2): ("S2 Low Fly", "fly", "low", "later_learn", "male"),
    (2, 3): ("S2 Offset", "fly", "offset", "later_learn", "male"),
    (2, 4): ("S2 High Home", "home", "high", "later_learn", "male"),
    (2, 5): ("S2 Low Home", "home", "low", "later_learn", "male"),
    (2, 6): ("S2 Audience High Fly", "fly", "high", "audience_question", "male"),
    (2, 7): ("S2 Audience Low Fly", "fly", "low", "audience_question", "male"),
    (2, 8): ("S2 Offset Supercharged", "fly", "offset_supercharged", "later_learn", "male"),
    (2, 9): ("S2 Audience Offset Supercharged", "fly", "offset_supercharged", "audience_question", "male"),
    (2, 10): ("S2 Audience High Home", "home", "high", "audience_question", "male"),
    (2, 11): ("S2 Audience Low Home", "home", "low", "audience_question", "male"),
}

# Study1_Policy.xlsx: Condition 1..12 = policy x {odd = low CF, even = high CF}
STUDY1_POLICIES = ["CCS", "Carbon tax", "Nuclear", "Population", "Renewables", "Transit"]

# Study2_Reformation.xls: Condition 1..6 = {Travel, Home} x {No, Some, Absolute}
STUDY2_ARMS: dict[int, tuple[str, str, str]] = {
    1: ("Travel No Reform", "fly", "none"),
    2: ("Travel Some Reform", "fly", "some"),
    3: ("Travel Complete Reform", "fly", "complete"),
    4: ("Home No Reform", "home", "none"),
    5: ("Home Some Reform", "home", "some"),
    6: ("Home Complete Reform", "home", "complete"),
}


# ---- helpers ---------------------------------------------------------------

def read_data(name: str) -> pd.DataFrame:
    path = DL / name
    if not path.exists():
        sys.exit(f"missing {path}; run data/attari2016/fetch.sh first")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # openpyxl "Unknown extension" noise
        df = pd.read_excel(path, sheet_name="Data")
    df.columns = [str(c).strip() for c in df.columns]
    if "None" in df.columns:
        df = df.rename(columns={"None": "No_Action"})
    # Study 2 stores a few open-ended numeric answers (MPG, Flights, Meat) with
    # blank or "-" cells; every non-numeric token becomes NA (no free text kept).
    for c in df.columns:
        if df[c].dtype == object:
            num = pd.to_numeric(df[c], errors="coerce")
            bad = df[c][num.isna() & df[c].notna()]
            if len(bad):
                print(f"  {name}: {c}: {len(bad)} non-numeric cell(s) -> NA "
                      f"{sorted(set(map(repr, bad.astype(str).str.strip())))}")
            df[c] = num
    return df


def add_credibility(df: pd.DataFrame) -> pd.DataFrame:
    for item in CRED_ORDER:
        vals = df[item].astype("float")
        assert vals.dropna().between(1, 5).all(), f"{item} out of 1..5"
        df[f"cred_{item.lower()}"] = (6 - vals) if item in CRED_POS else vals
    cred_cols = [f"cred_{i.lower()}" for i in CRED_ORDER]
    df["cred_sum"] = df[cred_cols].sum(axis=1, min_count=6)
    df["cred_mean"] = df[cred_cols].mean(axis=1)
    df["cred_score"] = (df["cred_sum"] - 18) / 12  # papers' -1..+1 rescaling
    return df


def fix_income(df: pd.DataFrame, label: str) -> pd.DataFrame:
    codes = set(df["Income"].dropna().astype(int))
    if 8 in codes and 7 not in codes:
        n = int((df["Income"] == 8).sum())
        print(f"  {label}: Income code 8 -> 7 (> $200,000) for {n} rows (Qualtrics quirk)")
        df["Income"] = df["Income"].replace({8: 7})
    assert df["Income"].dropna().between(1, 7).all(), "Income outside 1..7"
    return df


def add_gender(df: pd.DataFrame) -> pd.DataFrame:
    if "Gender" in df.columns:  # 1 male, 2 female, 3 other
        df["gender"] = df["Gender"].map({1: "male", 2: "female", 3: "other"})
    else:  # Ad_Hom: MaleC 1 male, 0 female, 3 other
        df["gender"] = df["MaleC"].map({1: "male", 0: "female", 3: "other"})
    df["male"] = df["gender"].map({"male": 1, "female": 0}).astype("Int64")
    return df


def finish(df: pd.DataFrame, study_id: str, front: list[str]) -> pd.DataFrame:
    df.insert(0, "dataset", study_id)
    df = add_credibility(df)
    df = add_gender(df)
    rest = [c for c in df.columns if c not in front]
    return df[front + rest]


# ---- per-study builders -----------------------------------------------------

def build_adhom() -> pd.DataFrame:
    df = read_data("Ad_Hom_Final.xls")
    assert "Zip" not in df.columns
    keys = list(zip(df["Study"].astype(int), df["Condition"].astype(int)))
    assert set(keys) <= set(ADHOM_ARMS), sorted(set(keys) - set(ADHOM_ARMS))
    meta = pd.DataFrame([ADHOM_ARMS[k] for k in keys],
                        columns=["arm", "domain", "footprint", "frame", "researcher_gender"],
                        index=df.index)
    df["arm_id"] = [f"S{s}_C{c}" for s, c in keys]
    df = pd.concat([df, meta], axis=1)
    df = df.rename(columns={"Study": "survey"})
    df = fix_income(df, "Ad_Hom")
    front = ["dataset", "ID", "survey", "Condition", "arm_id", "arm", "domain", "footprint",
             "frame", "researcher_gender"]
    return finish(df, "attari2016_adhom", front)


def build_study1() -> pd.DataFrame:
    df = read_data("Study1_Policy.xlsx")
    assert "Zip" in df.columns, "expected Zip in Study1 raw"
    df = df.drop(columns=["Zip"])  # PII: 5-digit ZIP with age/gender/income
    cond = df["Condition"].astype(int)
    assert cond.between(1, 12).all()
    df["policy"] = [STUDY1_POLICIES[(c - 1) // 2] for c in cond]
    df["footprint"] = ["low" if c % 2 == 1 else "high" for c in cond]
    df["arm_id"] = [f"C{c}" for c in cond]
    df["arm"] = df["policy"] + " x " + df["footprint"].str.capitalize() + " CF"
    df["domain"] = "home"  # all 2019 Study 1 vignettes manipulate home energy use
    df = fix_income(df, "Study1")
    front = ["dataset", "ID", "Condition", "arm_id", "arm", "policy", "footprint", "domain"]
    return finish(df, "attari2019_study1_policy", front)


def build_study2() -> pd.DataFrame:
    df = read_data("Study2_Reformation.xls")
    assert "Zip" not in df.columns  # codebook: "Removed from data sheet"
    cond = df["Condition"].astype(int)
    assert set(cond) <= set(STUDY2_ARMS)
    meta = pd.DataFrame([STUDY2_ARMS[c] for c in cond], columns=["arm", "domain", "reform"],
                        index=df.index)
    df["arm_id"] = [f"C{c}" for c in cond]
    df = pd.concat([df, meta], axis=1)
    df = fix_income(df, "Study2")
    front = ["dataset", "ID", "Condition", "arm_id", "arm", "domain", "reform"]
    return finish(df, "attari2019_study2_reformation", front)


def arm_summary(frames: list[pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for df in frames:
        df = df.sort_values([c for c in ("survey", "Condition") if c in df.columns])
        g = df.groupby(["dataset", "arm_id", "arm"], sort=False)
        s = g.agg(n=("ID", "size"),
                  cred_score_mean=("cred_score", "mean"),
                  cred_score_sd=("cred_score", "std"),
                  cred_mean_mean=("cred_mean", "mean"))
        for col in INTENTIONS:
            if col in df.columns:
                s[f"share_{col.lower()}"] = g[col].mean()
        if "Policy_Support" in df.columns:  # 1 strongly support .. 5 strongly oppose
            s["policy_support_mean_1to5"] = g["Policy_Support"].mean()
            s["policy_trust_mean_1to5"] = g["Trust"].mean()
        rows.append(s.reset_index())
    out = pd.concat(rows, ignore_index=True)
    return out.round(4)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("building derived CSVs")
    frames = {
        "attari2016_adhom.csv": build_adhom(),
        "attari2019_study1_policy.csv": build_study1(),
        "attari2019_study2_reformation.csv": build_study2(),
    }
    for name, df in frames.items():
        assert "Zip" not in df.columns
        text_cols = {c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])}
        allowed = {"dataset", "arm_id", "arm", "domain", "footprint", "frame",
                   "researcher_gender", "policy", "reform", "gender"}
        assert text_cols <= allowed, f"unexpected free-text column(s): {text_cols - allowed}"
        df.to_csv(OUT / name, index=False)
        print(f"  wrote {name}: {df.shape[0]} rows x {df.shape[1]} cols, "
              f"{df['arm_id'].nunique()} arms, mean cred_score {df['cred_score'].mean():+.3f}")
    summ = arm_summary(list(frames.values()))
    summ.to_csv(OUT / "arm_summary.csv", index=False)
    print(f"  wrote arm_summary.csv: {len(summ)} arms")


if __name__ == "__main__":
    main()
