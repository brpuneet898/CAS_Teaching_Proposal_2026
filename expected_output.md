# ClimateTwin Expected Output Sheet

This sheet gives instructor benchmark outputs for the supplied `dataset.csv`, `student_notebook.ipynb`, and `solution.ipynb`. Exact numbers can vary slightly if students use a different defensible model specification, severity family, simulation count, or random seed. Basic data validation numbers should match exactly.

## 1. Dataset validation outputs

| Item | Expected value |
|---|---:|
| Rows | 750 |
| Columns | 35 |
| Unique policy IDs | 750 |
| Unique locations | 250 |
| Years | 2024, 2025, 2026 |
| Total claims | 138 |
| Rows with at least one claim | 100 |
| Total paid loss | 22,583,153.26 |
| Total current premium | 40,132,000 |

## 2. Stress and trigger validation

| Measure | Expected count |
|---|---:|
| Air stress rows | 405 |
| Air trigger rows | 150 |
| Water stress rows | 327 |
| Water trigger rows | 107 |
| Compound trigger rows | 17 |
| Claims without insured trigger | 0 |

Expected interpretation: environmental stress is more common than qualifying insured triggers. A stress flag is not a claim.

## 3. Experience by occupancy

| Occupancy | Exposure | Claims | Paid loss | Claim frequency | Paid severity |
|---|---:|---:|---:|---:|---:|
| Food Processing | 193.47 | 45 | 5,635,443.67 | 0.23 | 125,232.08 |
| Hospital | 156.78 | 35 | 8,530,565.74 | 0.22 | 243,730.45 |
| Manufacturing | 296.42 | 58 | 8,417,143.85 | 0.20 | 145,123.17 |

Teaching point: the highest total claim count is not necessarily the highest severity or highest risk concentration. Exposure, occupancy, and insured value matter.

## 4. Experience by region

| Region | Exposure | Claims | Paid loss | Claim frequency | Paid severity |
|---|---:|---:|---:|---:|---:|
| Central Metro | 153.87 | 40 | 4,343,974.92 | 0.26 | 108,599.37 |
| Coastview | 147.64 | 20 | 4,091,448.86 | 0.14 | 204,572.44 |
| Drylands | 138.99 | 47 | 9,102,158.03 | 0.34 | 193,662.94 |
| Northgate | 121.06 | 10 | 1,348,643.16 | 0.08 | 134,864.32 |
| Riverbend | 85.11 | 21 | 3,696,928.29 | 0.25 | 176,044.20 |

Teaching point: Drylands should appear as an important risk concentration in descriptive analysis.

## 5. Expected visual outputs

Students should produce at least the following kinds of figures:

1. Bar chart comparing environmental stress rows with insured trigger rows.
2. Claim frequency or paid loss by occupancy or region.
3. Scenario aggregate-loss distribution or VaR/TVaR comparison.
4. Mitigation strategy comparison table or bar chart.

Visuals do not need to match the solution exactly, but they must support the actuarial decision rather than merely decorate the notebook.

## 6. Frequency model benchmark

The solution notebook uses an exposure-adjusted Poisson GLM with:

- response: `claim_count`
- offset: `log(exposure_years)`
- occupancy and region factors
- scaled environmental/climate variables
- stress flags
- air-water interaction
- mitigation indicators

Selected solution rate-ratio outputs:

| Variable | Coefficient | Rate ratio | Comment |
|---|---:|---:|---|
| `air_filtration` | -0.228 | 0.796 | Lower fitted frequency. |
| `water_treatment` | -0.387 | 0.679 | Lower fitted frequency. |
| `business_continuity_plan` | -0.282 | 0.754 | Lower fitted frequency. |

Some stress-flag and interaction coefficients can be unstable because trigger logic and stress flags are highly related in this synthetic case. Students should not over-interpret extreme coefficients mechanically. They should explain the actuarial reason for including a compound-risk term.

Acceptable student range: model should produce baseline 2026 expected claim count roughly **45 to 70** if using a comparable exposure-adjusted GLM.

## 7. Severity model benchmark

The solution notebook uses a Gamma GLM with log link for:

`average_paid_severity = aggregate_paid_loss / claim_count`

for claim-positive rows only, weighted by `claim_count`.

Selected solution multiplicative effects:

| Variable | Coefficient | Multiplicative effect | Comment |
|---|---:|---:|---|
| `log_iv` | 0.475 | 1.608 | Higher insured value increases severity. |
| `air_filtration` | -0.588 | 0.555 | Lower fitted paid severity. |
| `water_treatment` | -0.263 | 0.768 | Lower fitted paid severity. |
| `business_continuity_plan` | -0.379 | 0.685 | Lower fitted paid severity. |
| `water_stress_flag` | 1.010 | 2.745 | Higher fitted severity under water stress. |

Acceptable student range: conditional paid severity predictions should be positive and generally in a plausible range for this dataset; no zero-claim rows should be used as severity observations.

## 8. Baseline 2026 pricing benchmark

The solution notebook treats the 2026 records as the current annual portfolio snapshot.

| Metric | Solution value |
|---|---:|
| 2026 exposure | 215.174 |
| Expected claim count | 55.936 |
| Expected annual paid loss | 10,180,997.71 |
| Loss cost per exposure | 47,315.19 |
| Current premium | 13,748,900 |
| Indicated premium | 14,774,826.01 |
| Premium adequacy ratio | 0.931 |

Teaching point: baseline appears underpriced but not catastrophically so. Stress scenarios reveal the larger concern.

## 9. Scenario comparison benchmark

| Scenario | Expected annual loss | Current premium | Indicated premium | Adequacy ratio | VaR99 | TVaR99 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 10,180,997.71 | 13,748,900 | 14,774,826.01 | 0.93 | 15,538,062.83 | 16,587,144.51 |
| Air stress | 23,103,033.84 | 13,748,900 | 33,234,877.63 | 0.41 | 30,780,087.38 | 32,095,252.87 |
| Water stress | 19,458,641.57 | 13,748,900 | 28,028,602.96 | 0.49 | 26,596,913.03 | 28,018,265.43 |
| Compound stress | 41,237,611.54 | 13,748,900 | 59,141,417.20 | 0.23 | 51,728,461.85 | 53,504,276.49 |

Expected interpretation: compound stress is the most material scenario by both expected loss and tail risk. Air stress is more severe than water stress in the solution benchmark, but both standalone stresses materially reduce premium adequacy.

Acceptable student ranges with similar modelling:

| Scenario | Expected loss range | TVaR99 range |
|---|---:|---:|
| Baseline | 8M–13M | 14M–20M |
| Air stress | 18M–29M | 27M–38M |
| Water stress | 15M–25M | 23M–34M |
| Compound stress | 32M–50M | 45M–65M |

## 10. Mitigation benchmark under compound stress

Budget: **8,000,000**.

The solution compares five manageable candidate strategies. Exact strategy composition may differ if students choose different heuristics. They should still remain within budget and use TVaR99 as the primary decision criterion.

| Strategy | Actions selected | Cost | Expected annual loss | Expected-loss reduction | BCR | VaR99 | TVaR99 | TVaR reduction | Post-mitigation adequacy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Air-focused | 82 | 7,976,000 | 26,914,790.97 | 14,322,820.57 | 1.80 | 33,659,454.93 | 34,605,891.33 | 18,898,385.16 | 0.36 |
| Water-focused | 63 | 7,989,000 | 30,877,230.96 | 10,360,380.57 | 1.30 | 38,842,397.59 | 40,029,715.05 | 13,474,561.44 | 0.31 |
| BCP-focused | 137 | 7,078,000 | 28,280,888.37 | 12,956,723.17 | 1.83 | 35,939,728.24 | 37,079,930.31 | 16,424,346.18 | 0.34 |
| Balanced BCR-ranked | 100 | 7,995,000 | 25,876,548.65 | 15,361,062.89 | 1.92 | 32,345,579.49 | 33,384,167.21 | 20,120,109.28 | 0.37 |
| Tail-focused | 95 | 7,982,000 | 26,311,525.22 | 14,926,086.32 | 1.87 | 32,815,192.86 | 33,889,146.65 | 19,615,129.85 | 0.36 |

Solution-selected strategy: **Balanced BCR-ranked**, because it has the lowest simulated TVaR99 among the candidate strategies tested.

Teaching point: students may obtain a different feasible selected strategy if they define candidate portfolios differently. That is acceptable if the strategy is budget-feasible, evaluated through compound stress, and selected primarily on TVaR99.

## 11. Strong final recommendation should say

A high-quality final committee recommendation should include:

1. Baseline premium is slightly inadequate under the fitted model.
2. Compound stress is the most material risk state.
3. Current premium is deeply inadequate under compound stress.
4. Mitigation materially reduces expected loss and TVaR but does not fully restore premium adequacy.
5. AquaAir should combine mitigation requirements, repricing, and monitoring.
6. Underwriting restrictions or sublimits may be needed for persistently inadequate high-risk segments.
7. The data are synthetic, the models are simplified, and real deployment would require validation, governance, and external data.

## 12. Red flags in student outputs

Flag submissions that:

- treat stress flags as claims;
- ignore the exposure offset;
- simulate all 750 rows as one current annual portfolio;
- fit severity using zero-claim rows;
- skip policy terms;
- report VaR but not TVaR;
- select mitigation solely by BCR;
- exceed the 8,000,000 budget;
- fail to recompute stress flags after scenario transformations;
- provide code without actuarial interpretation; or
- make external real-world claims from the synthetic data.
