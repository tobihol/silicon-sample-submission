# Pew Research Center American Trends Panel — Waves 42, 100, 114

## Version

Three ATP waves, downloaded 2026-08-15 from TheARDA's open OSF mirrors
(no login; direct links and pinned sha256 hashes are in `fetch.sh`):

- **Wave 42 — "Trust in Science"**, fielded Jan 7–21, 2019, n=4,464.
  DOI: https://doi.org/10.17605/OSF.IO/4Q2VH
- **Wave 100 — "Black and Hispanic Perspectives on Science and Society"**,
  fielded Nov 30–Dec 12, 2021, n=14,497 (9,964 ATP panelists plus a
  4,533-person Black/Hispanic oversample from Ipsos' KnowledgePanel).
  DOI: https://doi.org/10.17605/OSF.IO/QXNP4
- **Wave 114 — "COVID-19, Scientists and Religion"**, fielded
  Sept 13–18, 2022, n=10,588. DOI: https://doi.org/10.17605/OSF.IO/V8FX5

Data citation: Pew Research Center, American Trends Panel, Waves 42, 100,
and 114 [machine-readable data files]. Washington, D.C.: Pew Research
Center. Distributed by the Association of Religion Data Archives
(https://www.thearda.com/).

**License: Pew Research Center EULA (as distributed via ARDA) — research
use only, NO redistribution.** The raw data files must never be committed
to this repository or publicly deposited anywhere. They live in the
gitignored `downloads/` folder; anyone reproducing this repo runs
`sh fetch.sh` to re-download and hash-verify them from the pinned URLs.

## Contents

- `fetch.sh` — re-downloads all files below from the pinned OSF/ARDA URLs
  into `downloads/` and verifies their sha256 hashes
- `downloads/w42/ATP_W42.sav` — Wave 42 microdata (SPSS; read with
  `pyreadstat`/`haven`); `ATP_W42_codebook.txt` — full data codebook with
  frequencies
- `downloads/w100/ATP_W100.sav` — Wave 100 microdata;
  `ATP_W100_codebook.txt` — full data codebook with frequencies
- `downloads/w114/ATP_W114.sav` — Wave 114 microdata;
  `ATP_W114_codebook.txt` — full data codebook with frequencies;
  `ATP_W114_instrument.pdf` — the questionnaire instrument (ARDA's scan of
  the original Pew topline instrument)
- `downloads/toplines/` — **published topline aggregates, not microdata**
  (added 2026-08-15 by the operator, NOT fetched by `fetch.sh`; provenance
  narrative in `idea_01/run/OPEN.md` item 14a): `w149_topline.txt`
  (sha256 19205695d73c66fc…, Pew ATP W149 Jul 1–7 2024, N=9,424, agency
  favorability incl. its W123 Mar 2023 replicate), `w149_quest.txt`
  (8e8a1562b700ff77…), `w149_agency_favorability_topline.pdf`
  (d8c76c4b0d0feb96…, the Pew report PDF). Consumed by
  `idea_01/run/tools/measure_agency_anchor.py`. These are Pew's published
  percentages (excerpt-class material under the EULA), unlike the `.sav`
  microdata above.
  Added 2026-08-24 (same status: operator-downloaded aggregates, NOT
  fetched by `fetch.sh`; recipe in `docs/dataset-scouting-2026-08-24.md`
  §3 row `pew_w135_tables`): `w135_climate_harms_topline.pdf`
  (sha256 e8a7c03999dd7bab…, Pew ATP W135 Sep 25–Oct 1 2023, N=8,842,
  "How Americans View Future Harms From Climate Change…" science topline,
  printed pp. 42–50; ENV26a–d "how well do climate scientists
  understand…" 4-pt with 2016/2021/2023 trend and CCINFLU climate
  scientists' policy influence with 2021/2023 trend, both on printed
  p. 44) and `w135_climate_harms_report.pdf` (sha256 b889802c7619ac40…,
  the 50-page report PDF; its pp. 42–50 duplicate the topline; it carries
  no subgroup tables for ENV26/CCINFLU, only a pointer to the Oct 25 2023
  short read), with `pdftotext -layout` sidecars `w135_topline.txt` and
  `w135_report.txt`. `w135_climate_scientists.csv` is the hand-coded
  aggregate table (item, subitem, year, group, category, pct, n,
  source_url, page; 122 rows): the 58 all-adult topline cells, plus party,
  education, party×education and party×ideology splits transcribed from
  the four charts of Pew's short read "Americans continue to have doubts
  about climate scientists' understanding of climate change" (Oct 25 2023;
  text saved as `w135_short_read_2023-10-25.txt`, charts as
  `w135_short_read_chart_{1..4}.png`) — those rows cite the short-read URL
  and a `chartN` page tag because the values are NOT in either PDF. Subgroup
  rows have no n (Pew publishes none). Pew's terms allow reproducing and
  citing excerpts with attribution; the PDFs themselves are not to be
  mirrored publicly.

## Why it is here

These waves are the only openly downloadable U.S. source that carries a
trust-in-scientists measure AND party identification AND race/ethnicity in
one sample — they anchor the race×trust and party×trust control-condition
baselines the harness flagged as unanchored (its OPEN §2). All three waves
share Pew's standard 4-point confidence item ("How much confidence, if any,
do you have in ... to act in the best interests of the public? —
Scientists": a great deal / a fair amount / not too much / none at all),
plus `F_PARTY_FINAL` and a race/ethnicity classifier (`F_RACETHN` in W42;
`F_RACETHNMOD` in W114; `RACETHNMOD_W100` in W100).

Wave-specific value:

- **W42** adds a multi-item trust battery (the RQ series) for specific
  scientist groups, including environmental research scientists
  (`RQ1_F1B_W42`–`RQ7_F1B_W42`: overall view, perceived competence,
  fairness/accuracy, admitting mistakes, transparency, caring about the
  public's interests, views of research misconduct) alongside parallel
  batteries for medical research scientists and other groups.
- **W100** adds large Black and Hispanic oversamples, giving usable cell
  sizes for race×trust baselines that general-population waves cannot
  support.
- **W114** is the most recent measurement and carries both the scientists
  item (`CONF_G_W114`) and the medical-scientists item (`CONF_F_W114`),
  post-COVID.
