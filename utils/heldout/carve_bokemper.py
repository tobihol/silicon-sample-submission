#!/usr/bin/env python3
"""Carve bokemper2022 (PLOS One, doi:10.1371/journal.pone.0264782, data CC0 doi:10.7910/DVN/VUKNOQ)
as a jointly-held-out head-to-head task for idea_01 vs idea_02.

Outputs (disk-only; data/*/carved/ is gitignored):
  data/bokemper2022/carved/truth.csv                condition,outcome,ate,se,n_treat,n_control (pp)
  data/bokemper2022/carved/truth_mod_<m>.csv        party/gender/age_band moderator ATEs (E2 only)
  data/bokemper2022/carved/manifest.json            shas + provenance
  data/bokemper2022/carved/brief/task.json          design-only brief (verbatim stimuli, outcomes)
  data/bokemper2022/carved/brief/template.csv       55 cells
Leak checks: brief must not contain any truth value (2-decimal word-boundary probe) nor the
strings 'ate','truth' as data keys beyond the template header.

Scales follow ReplicationCode.do exactly (mean imputation + missingness caps for E2).
ATEs are unadjusted difference-in-means vs the experiment's own control, in pp of scale range.
Verified against the paper's covariate-adjusted Table/Fig coefficients (within 0.6 pp).
"""
import hashlib, json, re, sys
from pathlib import Path
import numpy as np
import pandas as pd
import pyreadstat

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/bokemper2022/downloads"
OUT = ROOT / "data/bokemper2022/carved"
BRIEF = OUT / "brief"

TREAT1 = {"treat_sVo_Is_As": "Protect Yourself - Individual Action",
          "treat_sVo_Is_Atc": "Protect Yourself - Threshold Cooperation",
          "treat_sVo_Is_Alc": "Protect Yourself - Linear Cooperation",
          "treat_sVo_Io_As": "Protect Others - Individual Action",
          "treat_sVo_Io_Atc": "Protect Others - Threshold Cooperation",
          "treat_sVo_Io_Alc": "Protect Others - Linear Cooperation",
          "treat_notbrave": "Reframing Bravery",
          "treat_notbravewpollution": "Reframing Bravery + Pollution",
          "treat_returnnormal": "Return to Normal",
          "treat_newnormal": "Adapt to New Normal"}
TREAT2 = {"treatment_baseline": "Baseline Information",
          "treatment_linear": "Protect Others - Linear Cooperation",
          "treatment_notbravery": "Reframing Bravery"}


def build_e1():
    d, _ = pyreadstat.read_dta(str(RAW / "Experiment1.dta"))
    d["e1_normsbeliefs"] = d[["agree_socdiststopmesick", "agree_socdiststopotherssick",
                              "agree_guiltyifnotsocdist"]].mean(axis=1, skipna=False)
    d["e1_distancing"] = d[["maskwearing_likely", "agree_liketosocdist", "rc_likely_electivemed",
                            "rc_likely_friendshouse", "rc_likely_familyhouse",
                            "rc_likely_smallparty"]].mean(axis=1, skipna=False)
    d["e1_food"] = d[["rc_likely_outtoeat", "rc_likely_coffeeshop",
                      "restaurant_binary_in_vs_all"]].mean(axis=1, skipna=False)
    d["e1_others"] = d[["persuade_likely", "report_likely", "noncompliers_selfish",
                        "rc_noncompliers_trustworthy", "rc_noncompliers_likeable",
                        "rc_noncompliers_competent"]].mean(axis=1, skipna=False)
    d["ctrl"] = (d[list(TREAT1)].sum(axis=1) == 0).astype(int)
    # moderators (Lucid profile)
    d["gender"] = np.where(d.lucid_female == 1, "Female", "Male")
    d["age_band"] = pd.cut(d.lucid_age, [17, 34, 54, 200], labels=["18-34", "35-54", "55+"]).astype(str)
    d["party"] = np.select([d.lucid_party7 <= 3, d.lucid_party7 == 4, d.lucid_party7 >= 5],
                           ["Democrat", "Independent", "Republican"], default="Independent")
    return d, ["e1_normsbeliefs", "e1_distancing", "e1_food", "e1_others"], TREAT1, "E1"


def build_e2():
    d, _ = pyreadstat.read_dta(str(RAW / "Experiment2.dta"))
    rc = lambda s: (1 - s).abs()

    def scale(items, denom, min_ct):
        M = pd.concat(items, axis=1)
        ct = M.notna().sum(axis=1)
        v = M.apply(lambda c: c.fillna(c.mean())).sum(axis=1) / denom
        v[ct < min_ct] = np.nan
        return v

    d["e2_distancing"] = scale([d["agree_liketosocdist"], d["ly_selfisolate"],
                                d["authorities_alertifpositive"]] +
                               [rc(d[v]) for v in ["ly_church", "ly_library", "ly_electivemed",
                                                   "ly_familyhouse_inside", "ly_friendshouse_inside",
                                                   "ly_protest", "ly_publictransport", "ly_airplane",
                                                   "ly_workoutsidehome", "meetings_smalloutside",
                                                   "meetings_smallinside", "meetings_bigoutside",
                                                   "meetings_biginside"]], 16, 12)
    d["e2_food"] = scale([rc(d[v]) for v in ["ly_coffeeshop", "ly_outtoeat_inside",
                                             "ly_outtoeat_outside", "ly_bar"]], 4, 3)
    d["e2_others"] = scale([d["persuade_likely"], d["report_likely"], d["noncompliers_selfish"],
                            d["auth_contacttrace"]] +
                           [rc(d[v]) for v in ["noncompliers_trustworthy", "noncompliers_likeable",
                                               "noncompliers_competent", "noncompliers_intelligent"]], 8, 6)
    d["e2_normsbeliefs"] = d[["agree_socdiststopmesick", "agree_socdiststopotherssick",
                              "agree_guiltyifnotsocdist"]].sum(axis=1, min_count=3) / 3
    d["maskdiff"] = ((d.ly_store_reqmasks - d.ly_store_banmasks) + 1) / 2
    d["e2_masks"] = scale([d[v] for v in ["mask_work", "mask_pubtransport", "mask_walk",
                                          "mask_shopinside", "mask_visitfriend", "mask_park",
                                          "maskdiff"]], 7, 7)
    d["ctrl"] = (d[list(TREAT2)].sum(axis=1) == 0).astype(int)
    d["gender"] = d.D_gender.map({1.0: "Male", 2.0: "Female"}).fillna(
        d.D_gender if d.D_gender.dtype == object else d.D_gender.astype(str))
    d["age_band"] = d.D_age.astype(str)
    d["party"] = d.D_newpid7.map(lambda x: "Democrat" if x <= 3 else ("Independent" if x == 4 else "Republican")
                                 if pd.notna(x) else np.nan) if np.issubdtype(d.D_newpid7.dtype, np.number) \
        else d.D_newpid7.astype(str)
    return d, ["e2_normsbeliefs", "e2_distancing", "e2_food", "e2_others", "e2_masks"], TREAT2, "E2"


def ates(d, outcomes, treat, tag, by=None):
    rows = []
    groups = [(None, d)] if by is None else [(lv, d[d[by] == lv]) for lv in sorted(d[by].dropna().unique())]
    for lv, g in groups:
        for tv, name in treat.items():
            for o in outcomes:
                t = g.loc[g[tv] == 1, o].dropna() * 100
                c = g.loc[g.ctrl == 1, o].dropna() * 100
                if len(t) < 20 or len(c) < 20:
                    continue
                row = {"condition": f"{tag}: {name}", "outcome": o,
                       "ate": t.mean() - c.mean(),
                       "se": float(np.sqrt(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c))),
                       "n_treat": len(t), "n_control": len(c)}
                if by is not None:
                    row["moderator_level"] = str(lv)
                rows.append(row)
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    BRIEF.mkdir(parents=True, exist_ok=True)
    e1, out1, t1, _ = build_e1()
    e2, out2, t2, _ = build_e2()
    truth = pd.concat([ates(e1, out1, t1, "E1"), ates(e2, out2, t2, "E2")], ignore_index=True)
    assert len(truth) == 55, len(truth)
    truth.to_csv(OUT / "truth.csv", index=False)
    for m in ("party", "gender", "age_band"):
        pd.concat([ates(e1, out1, t1, "E1", by=m), ates(e2, out2, t2, "E2", by=m)],
                  ignore_index=True).to_csv(OUT / f"truth_mod_{m}.csv", index=False)

    stim = json.loads((RAW / "stimuli.json").read_text())
    brief = {
        "task_id": "bokemper2022",
        "study": "bokemper2022 (two survey experiments on persuasive messaging for COVID-19 risk "
                 "reduction, fielded May 2020 and mid-July-early-August 2020 in the United States)",
        "design_note": "Experiment 1: 10 message conditions plus a baseline-informational reference "
                       "group (between subjects), convenience sample from Lucid, fielded May 2020. "
                       "Effects are vs the baseline-informational group. Experiment 2: 3 message "
                       "conditions plus a pure placebo control (unrelated bird-feeding text), "
                       "nationally representative YouGov sample, fielded mid-July to early August "
                       "2020. Effects are vs the placebo control. Respondents read the assigned "
                       "message once, then answered the outcome battery immediately.",
        "sample": {"E1": "n=3,184 U.S. adults, Lucid convenience sample (May 2020); analysis n per "
                         "cell ~185-210 treated vs ~550-575 reference",
                   "E2": "n=6,079 U.S. adults, YouGov nationally representative (July-August 2020); "
                         "~1,300-1,550 per condition"},
        "arms": stim,
        "outcomes": {
            "e1_normsbeliefs": "BELIEFS scale: mean of 3 items (social distancing stops me getting sick / stops others getting sick / I'd feel guilty if I did not distance), each 0-1 agreement slider. Units below: pp of scale range (0-100).",
            "e1_distancing": "DISTANCING scale: mean of 6 items (likelihood of mask wearing, practicing distancing; reverse-coded willingness to get elective medical care, visit friend's house, family's house, attend small party), 0-1. Units: pp of range.",
            "e1_food": "FOOD scale: mean of 3 items (reverse-coded willingness to eat out, go to coffee shop; preference for indoor dining), 0-1. Units: pp of range.",
            "e1_others": "OTHERS scale: mean of 6 items (persuade others to distance, report violating business, non-compliers are selfish, reverse-coded non-compliers trustworthy/likeable/competent), 0-1. Units: pp of range.",
            "e2_normsbeliefs": "BELIEFS scale, same 3 items as E1. Units: pp of range.",
            "e2_distancing": "DISTANCING scale: 16 items (like to distance, self-isolate if exposed, alert authorities if positive, and 13 reverse-coded willingness-to-do-activities items: church, library, elective med, family/friends house inside, protest, public transport, airplane, work outside home, small/big meetings inside/outside), 0-1. Units: pp of range.",
            "e2_food": "FOOD scale: 4 reverse-coded items (coffee shop, eat inside, eat outside, bar), 0-1. Units: pp of range.",
            "e2_others": "OTHERS/peers scale: 8 items (persuade, report, non-compliers selfish, cooperate with contact tracing, reverse-coded trustworthy/likeable/competent/intelligent), 0-1. Units: pp of range.",
            "e2_masks": "MASKS scale: 7 items (mask at work, public transport, walking, shopping, visiting friend, park, and preference for mask-requiring over mask-banning store), 0-1. Units: pp of range."},
        "instruction": "Predict the average treatment effect (ATE) of each condition vs its "
                       "experiment's reference group for every cell in template.csv, in percentage "
                       "points of scale range. E1 cells are vs the baseline-informational message; "
                       "E2 cells are vs a no-information placebo. Optional moderator files use the "
                       "same format with a moderator_level column.",
        "moderators": {"party": ["Democrat", "Independent", "Republican"],
                       "gender": ["Male", "Female"],
                       "age_band_E1": ["18-34", "35-54", "55+"],
                       "age_band_E2": "YouGov 5-category age bands as in template_mod_age_band.csv"},
    }
    (BRIEF / "task.json").write_text(json.dumps(brief, indent=1))
    truth[["condition", "outcome"]].to_csv(BRIEF / "template.csv", index=False)
    for m in ("party", "gender", "age_band"):
        pd.read_csv(OUT / f"truth_mod_{m}.csv")[["condition", "outcome", "moderator_level"]] \
            .to_csv(BRIEF / f"template_mod_{m}.csv", index=False)

    # leak checks: no truth value (2dp) appears in the brief
    blob = (BRIEF / "task.json").read_text()
    bad = []
    for v in truth.ate.tolist() + truth.se.tolist():
        for pat in (f"{v:.2f}", f"{v:.3f}"):
            if re.search(rf"(?<![\d.]){re.escape(pat)}(?![\d])", blob):
                bad.append(pat)
    assert not bad, f"value echo in brief: {bad[:5]}"
    for kw in ("ate", "truth", "effect size"):
        assert f'"{kw}"' not in blob.lower().replace('"instruction"', "").replace(
            '"design_note"', ""), kw
    man = {"source_doi": "10.7910/DVN/VUKNOQ (CC0)", "paper_doi": "10.1371/journal.pone.0264782",
           "carved": "2026-08-26", "cells": len(truth),
           "sealed_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(OUT.glob("truth*.csv"))}}
    (OUT / "manifest.json").write_text(json.dumps(man, indent=1))
    print(f"carved {len(truth)} cells; mods: " +
          ", ".join(f"{m}={len(pd.read_csv(OUT / f'truth_mod_{m}.csv'))}" for m in ("party", "gender", "age_band")))
    print("brief leak checks passed; manifest written")


if __name__ == "__main__":
    main()
