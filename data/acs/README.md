# American Community Survey 2018 1-Year PUMS (person + housing files)

## Version

U.S. Census Bureau, ACS Public Use Microdata Sample, 2018 1-Year, person and housing records — the survey
behind [folktexts](https://github.com/socialfoundations/folktexts) / folktables.

Data citation: U.S. Census Bureau (2019). American Community Survey 2018 1-Year Public Use
Microdata Sample [Data set]. [https://www2.census.gov/programs-surveys/acs/data/pums/2018/1-Year/](https://www2.census.gov/programs-surveys/acs/data/pums/2018/1-Year/)

## Dataset download

Public, no account needed. From the Census PUMS pages, into `downloads/`:

- [x] `unix_pus.zip` — the US person file 
    - [x] `unix_pus/psam_pusa.sas7bdat` and `unix_pus/psam_pusb.sas7bdat` (SAS data files; carries all variable labels — Value labels come from the data dictionary.)
    - [x] `ACS2018_PUMS_README.pdf`
- [x] `unix_hus.zip` — the US housing file
    - [x] `unix_hus/psam_husa.sas7bdat` and `unix_hus/psam_husb.sas7bdat` (SAS data files; needed for household income `HINCP` as a moderator in idea_01 — household-level variables live here, joinable to person records via `SERIALNO`.)
- [x] `PUMS_Data_Dictionary_2018.pdf` — the codebook
- [x] `2018AccuracyPUMS.pdf` — design/accuracy documentation (weights, replicate weights)
- [x] `quest18.pdf` — the 2018 questionnaire

## Publications download

The U.S. Census Bureau's publications on the 2018 1-Year PUMS person records, into `publications/`:

- [x] U.S. Census Bureau (2021). Understanding and Using the American Community Survey Public Use Microdata Sample Files: What Data Users Need to Know. [https://www.census.gov/programs-surveys/acs/library/handbooks/pums.html](https://www.census.gov/programs-surveys/acs/library/handbooks/pums.html)
- [x] U.S. Census Bureau (2019). 2018 ACS 1-Year PUMS README. [https://www2.census.gov/programs-surveys/acs/tech_docs/pums/ACS2018_PUMS_README.pdf](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/ACS2018_PUMS_README.pdf)
- [x] U.S. Census Bureau (2019). PUMS Estimates for User Verification, 2018 1-Year (`pums_estimates_18.csv`) — the published per-state estimates, SEs, and MOEs to reproduce. [https://www2.census.gov/programs-surveys/acs/tech_docs/pums/estimates/](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/estimates/)

Publications with estimates computed from the 2018 1-Year PUMS, into `publications/`:

- [x] Erickson, Lee & von Schrader (2020). 2018 Disability Status Report: United States. Cornell University Yang-Tan Institute. [https://www.disabilitystatistics.org/](https://www.disabilitystatistics.org/)
- [x] Paul, Rafal & Houtenville (2020). 2019 Annual Report on People with Disabilities in America. UNH Institute on Disability. [https://eric.ed.gov/?id=ED605685](https://eric.ed.gov/?id=ED605685)
- [x] Sansone & Carpenter (2020). Turing's children: Representation of sexual minorities in STEM. *PLOS ONE*, 15(11), e0241596. [https://doi.org/10.1371/journal.pone.0241596](https://doi.org/10.1371/journal.pone.0241596)
- [x] Oreffice & Sansone (2022). Transportation to work by sexual orientation. *PLOS ONE*, 17(2), e0263687. [https://doi.org/10.1371/journal.pone.0263687](https://doi.org/10.1371/journal.pone.0263687)
- [x] Sassler & Meyerhofer (2023). Factors shaping the gender wage gap among college-educated computer science workers. *PLOS ONE*, 18(10), e0293300. [https://doi.org/10.1371/journal.pone.0293300](https://doi.org/10.1371/journal.pone.0293300)
- [x] Wongkamthong & Akande. A Comparative Study of Imputation Methods for Multivariate Ordinal Data. [arXiv:2010.10471](https://arxiv.org/abs/2010.10471)
- [x] Kelly, Deichert & Holley (2020). Direct Care Workforce: Where the Boys Really Are. *Innovation in Aging*, 4(S1), 180–181 (conference abstract). [https://doi.org/10.1093/geroni/igaa057.584](https://doi.org/10.1093/geroni/igaa057.584)
