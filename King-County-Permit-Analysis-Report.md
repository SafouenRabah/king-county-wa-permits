# King County Permit Duration Analysis

**Processing times, milestone breakdowns, and year-over-year trends**

Data: January 2023 – January 2026 | Report generated February 2026

---

| Metric | Value |
|--------|-------|
| Total Permits Analyzed | 12,148 |
| Permit Type Groups | 28 |
| Median IC → Issued* | 41 days |
| Average IC → Issued* | 87 days |

*\* Excluding same-day (zero-day) Mechanical permits, which account for 65.9% of all permits*

---

## 1. Data Sources & Pipeline

This analysis draws on **monthly permit reports** downloaded from the King County permitting portal. Two report types were combined:

- **Issued Permits** — 34 monthly Excel files (Jan 2023 – Jan 2026) containing milestone dates: Application Date, Open Date, Intake Complete Date, Ready to Issue Date, and Issued Date.
- **New Applications** — 38 monthly Excel files with application metadata: permit type, project description, job value, parcel data, and applicant information.

The two datasets were joined on Permit Number, producing **12,148 matched permits** (75.4% match rate). Match rates are strongest for recent months (92–98%) and weaker for early 2023 (~63%). All five duration columns were independently verified against the raw dates with **zero calculation errors**.

### Data Completeness

| Date Field | Records Available | Coverage | Notes |
|------------|------------------:|----------|-------|
| Application Date | 12,148 | 100.0% | |
| Open Date | 5,985 | 49.3% | Discontinued after June 2024 |
| Intake Complete Date | 12,137 | 99.9% | |
| Ready to Issue Date | 12,138 | 99.9% | |
| Issued Date | 12,148 | 100.0% | |

> **⚠️ Open Date limitation.** The Open Date field was discontinued after June 2024 and is only available for 49.3% of permits. Any analysis of the Open → Intake Complete stage covers pre-July 2024 permits only. After June 2024, the only available processing milestones are Intake Complete, Ready to Issue, and Issued.

---

## 2. Key Findings

### 2.1 Residential Permits: Year-over-Year Trends

Residential permits are the highest-profile and most closely watched category. The three main residential types — Dwelling-Single, Addition-Improvement, and Basic — tell very different stories.

| Permit Type | Year | Permits | Median IC→RTI | Median RTI→Iss | Median Total | Avg Total | P90 |
|-------------|------|--------:|--------------:|---------------:|-------------:|----------:|----:|
| Residential Dwelling-Single | 2023 | 73 | 150 | 12 | 176 | 181 | 252 |
| Residential Dwelling-Single | 2024 | 146 | 184 | 8 | 202 | 225 | 362 |
| Residential Dwelling-Single | 2025 | 172 | 172 | 12 | 184 | 245 | 551 |
| Residential Addition-Improvement | 2023 | 383 | 40 | 5 | 50 | 69 | 144 |
| Residential Addition-Improvement | 2024 | 500 | 39 | 5 | 61 | 86 | 204 |
| Residential Addition-Improvement | 2025 | 515 | 29 | 6 | 39 | 73 | 194 |
| Residential Basic | 2023 | 110 | 19 | 11 | 32 | 51 | 143 |
| Residential Basic | 2024 | 98 | 31 | 7 | 43 | 46 | 81 |
| Residential Basic | 2025 | 19 | 210 | 55 | 222 | 282 | 557 |

> **✅ Residential Addition-Improvement is improving.** Median processing time dropped from 61 days (2024) to 39 days (2025) — a 36% reduction. The plan review stage (IC→RTI) tightened from 39 to 29 median days. With 515 permits in 2025, this is a statistically robust improvement at scale.

> **⚠️ Residential Dwelling-Single has a growing tail problem.** While the median improved slightly (202 → 184 days), the P90 surged from 362 to 551 days — meaning 1 in 10 permits now takes over 18 months. The mean rose from 225 to 245 days. The typical permit is getting a bit faster, but the worst cases are getting much worse.

> **⚠️ Residential Basic: small 2025 sample is alarming.** Only 19 Residential Basic permits were issued in 2025 (vs. 98 in 2024 and 110 in 2023). The median spiked from 43 to 222 days. Whether this reflects a genuine slowdown or a data timing artifact (many 2025 permits still in the pipeline) requires further investigation.

### 2.2 Intake Friction: Open → Intake Complete

Before a permit enters plan review, it must clear the **intake stage** — the period from when a permit is opened to when it's formally accepted as complete for review. This stage was measurable for pre-June 2024 permits only.

| Permit Type | Median (days) | Average (days) | P90 (days) |
|-------------|-------------:|---------------:|-----------:|
| Residential Dwelling-Single | 26 | 53 | 118 |
| Residential Addition-Improvement | 20 | 38 | 90 |
| Residential Basic | 18 | 25 | 53 |
| Grade/Clearing | 6 | 25 | 54 |
| Addition-Improvement/Tenant | 5 | 9 | 14 |
| Electrical Comm Device/Antenna | 4 | 7 | 12 |

For Residential Dwelling-Single, the average intake time was **53 days** (median 26), meaning applicants wait nearly two months before their permit even enters the review queue. Residential Addition-Improvement averaged 38 days and Residential Basic averaged 25 days. These delays compound: time spent in intake is time not yet counted toward plan review.

> **Intake friction is significant for residential permits.** Pre-June 2024, the Open → Intake Complete stage accounted for 21% of total processing time for Dwelling-Single, 34% for Addition-Improvement, and 36% for Basic permits. Reducing intake turnaround by even a week would meaningfully shorten the end-to-end experience for applicants.

### 2.3 Plan Review: Where Permits Stall

The **Intake Complete → Ready to Issue (IC→RTI)** stage is the plan review and approval phase. This is the single stage with the most variation across permit types and the largest absolute durations.

| Permit Type | Count | Median (days) | Average (days) | P90 (days) |
|-------------|------:|--------------:|---------------:|-----------:|
| Residential Dwelling-Single | 400 | 170 | 199 | 379 |
| Grade/Clearing | 90 | 112 | 221 | 583 |
| Addition-Improvement/Tenant | 172 | 44 | 84 | 187 |
| Residential Addition-Improvement | 1,427 | 35 | 59 | 141 |
| Mechanical/Commercial | 120 | 28 | 58 | 131 |
| Residential Basic | 230 | 24 | 49 | 90 |
| Electrical Comm Device/Antenna | 169 | 22 | 34 | 66 |
| Fire Permit Systems/Sprinkler/Commercial | 93 | 20 | 42 | 81 |
| Special Events/Specific | 155 | 19 | 24 | 55 |
| Fire Permit Systems/Sprinkler/Residential | 531 | 14 | 23 | 36 |
| Fire Permit Systems/Alarm | 221 | 7 | 22 | 41 |

Residential Dwelling-Single permits spend a median of **170 days in plan review** — nearly 6 months. Grade/Clearing permits are even more variable, with a median of 112 days but a P90 of 583 days. By contrast, the Ready to Issue → Issued stage (final clearance and inspections) is typically short: median 10 days for Dwelling-Single and 5 days for Addition-Improvement.

### 2.4 What's Improving and What's Not (2024 → 2025)

Comparing median processing times across all high-volume permit types reveals which categories are getting faster and which are falling behind.

| Permit Type | n (2024) | Median 2024 | n (2025) | Median 2025 | Change |
|-------------|--------:|------------:|--------:|------------:|-------:|
| Addition-Improvement/Tenant | 67 | 97 | 105 | 22 | **-74** |
| Grade/Clearing | 37 | 230 | 50 | 173 | **-57** |
| Electrical Comm Device/Antenna | 70 | 47 | 93 | 20 | **-28** |
| Mechanical/Commercial | 35 | 44 | 82 | 18 | **-26** |
| Residential Addition-Improvement | 500 | 61 | 515 | 39 | **-22** |
| Residential Dwelling-Single | 146 | 202 | 172 | 184 | **-18** |
| Fire Permit Systems/Alarm | 79 | 5 | 100 | 6 | +1 |
| Fire Permit Systems/Sprinkler/Residential | 192 | 9 | 257 | 14 | +5 |
| Special Events/Specific | 51 | 14 | 73 | 27 | +13 |
| Fire Permit Systems/Sprinkler/Commercial | 31 | 3 | 56 | 25 | +22 |
| Residential Basic | 98 | 43 | 19 | 222 | +179 |

> **✅ Several categories improved meaningfully in 2025:**
> - **Addition-Improvement/Tenant:** median dropped from 97 to 22 days (–74 days)
> - **Grade/Clearing:** 230 → 173 days (–57 days)
> - **Electrical Comm Device/Antenna:** 47 → 20 days (–28 days)
> - **Mechanical/Commercial:** 44 → 18 days (–26 days)
> - **Residential Addition-Improvement:** 61 → 39 days (–22 days)
> - **Residential Dwelling-Single:** 202 → 184 days (–18 days median, though P90 worsened)

> **⚠️ Residential Basic stands out as a concern:** median jumped from 43 to 222 days (+179), though the small 2025 sample (n=19) warrants caution before drawing conclusions. Fire Permit Systems/Sprinkler/Commercial also increased (+22 days).

---

## 3. Methodology & Assumptions

**Permit lifecycle.** King County permits follow a four-stage pipeline: Open → Intake Complete → Ready to Issue → Issued. After June 2024, the Open Date field was discontinued, leaving three measurable milestones: Intake Complete, Ready to Issue, and Issued. The Ready to Issue → Issued stage depends on completing inspections and final clearance.

**Type grouping.** Raw permit types (39 unique labels) were simplified by stripping common prefixes. Twelve niche types with ≤10 records were collapsed into "Other", leaving 28 categories. Most analyses in this report focus on **high-volume types (≥90 total permits)** to ensure statistical reliability.

**Same-day permits.** 8,000 permits (65.9%) were issued on the same day as Intake Complete — nearly all Mechanical/Residential permits approved over the counter. These are included in counts but excluded from headline duration metrics.

**Averages vs. medians.** This report uses medians for single-metric comparisons (less sensitive to outliers) and means for stage breakdowns (means are additive; medians are not). Both are shown where relevant.

**Data quality.** Eight records (0.07%) have negative durations — source data anomalies too few to affect aggregates. 1,702 records have Open Date before Application Date, likely reflecting legacy system definitions. Zero duplicate permit numbers were found.

---

*King County Permit Duration Analysis | Data: Jan 2023 – Jan 2026 | Generated Feb 2026*
