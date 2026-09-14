# ClimateTwin V2 Expected Output Sheet

This instructor sheet gives regenerated V2 benchmark outputs for `dataset.csv`, `claim_level_data.csv`, `data_script.py`, `student_notebook.ipynb`, and `solution.ipynb`. The values below are based on the corrected V2 data-generating process and the executed V2 solution notebook. Do not reuse V1 numerical targets.

Exact model outputs can vary if students use a different defensible model specification, severity family, simulation count, or random seed. The basic data-validation and contract-mechanics checks should match exactly.

## 1. Dataset validation outputs

| Item | Expected value |
|---|---:|
| Policy-year rows | 750 |
| Policy-year columns | 35 |
| Unique policy IDs | 750 |
| Unique locations | 250 |
| Years | 2024, 2025, 2026 |
| Total exposure | 642.068 |
| Total claims | 95 |
| Policy-years with at least one claim | 71 |
| Claim-level rows | 95 |
| Legitimate zero-paid claim rows | 33 |
| Total ground-up loss | 12,287,359.07 |
| Total covered loss | 7,747,945.08 |
| Total paid loss | 3,480,012.62 |
| Total current premium | 40,978,000 |

## 2. Contract-mechanics validation

The solution notebook should audit the V2 claim-level table before modelling.

| Check | Expected result |
|---|---:|
| Every claim-level `covered_loss` is positive | True |
| Legitimate zero-paid claims are present | 33 |
| BI covered days equal `max(interruption_days - waiting_period, 0)` | True |
| `covered_loss = remediation_loss + covered_bi_loss` | True |
| Deductible is applied exactly once per claim | True |
| Paid loss respects the per-claim policy limit | True |
| Paid loss never exceeds policy limit | True |
| Claim-level paid loss reconciles to annual aggregate paid loss | True |

Teaching point: zero-paid claims are valid insurance outcomes after deductible/limit/waiting-period mechanics. They should not be forced into a positive paid-severity response.

## 3. Worked insurance examples

These values should match the case document, generator logic, and solution notebook.

| Example | Remediation loss | Daily BI loss | Interruption days | Waiting period | Deductible | Policy limit | Ground-up loss | Covered BI loss | Covered loss | After deductible | Paid loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Below deductible | 20,000 | 0 | 0 | 2 | 50,000 | 500,000 | 20,000 | 0 | 20,000 | 0 | 0 |
| Limited payment | 900,000 | 0 | 0 | 2 | 50,000 | 400,000 | 900,000 | 0 | 900,000 | 850,000 | 400,000 |
| BI waiting not met, other cost payable | 100,000 | 30,000 | 2 | 3 | 50,000 | 500,000 | 160,000 | 0 | 100,000 | 50,000 | 50,000 |

## 4. Stress and trigger validation

| Measure | Expected count |
|---|---:|
| Air stress rows | 381 |
| Air trigger rows | 94 |
| Water stress rows | 338 |
| Water trigger rows | 73 |
| Compound trigger rows | 9 |
| Claims without insured trigger | 0 |

Expected interpretation: environmental stress is more common than qualifying insured triggers. A stress flag is not a claim.

## 5. Experience by occupancy

| Occupancy | Exposure | Claims | Paid loss | Claim frequency per exposure | Paid severity per claim |
|---|---:|---:|---:|---:|---:|
| Food Processing | 193.994 | 25 | 458,918.82 | 0.129 | 18,356.75 |
| Hospital | 158.574 | 28 | 1,463,565.79 | 0.177 | 52,270.21 |
| Manufacturing | 289.500 | 42 | 1,557,528.01 | 0.145 | 37,084.00 |

Teaching point: claim count, severity, and contribution to paid loss tell different stories. Hospitals have the highest average paid severity, while manufacturing contributes the most claims and paid loss in the full historical table.

## 6. Experience by region

| Region | Exposure | Claims | Paid loss | Claim frequency per exposure | Paid severity per claim |
|---|---:|---:|---:|---:|---:|
| Central Metro | 159.014 | 27 | 825,556.66 | 0.170 | 30,576.17 |
| Coastview | 152.159 | 8 | 138,538.77 | 0.053 | 17,317.35 |
| Drylands | 141.552 | 43 | 2,266,065.17 | 0.304 | 52,699.19 |
| Northgate | 105.829 | 8 | 112,482.06 | 0.076 | 14,060.26 |
| Riverbend | 83.514 | 9 | 137,369.96 | 0.108 | 15,263.33 |

Teaching point: Drylands should emerge as the most important descriptive risk concentration in the V2 dataset.

## 7. Expected visual outputs

Students should produce visuals that support the actuarial decision. Acceptable examples include:

1. Bar chart comparing stress rows with trigger rows.
2. Claim count, frequency, or paid loss by occupancy or region.
3. Scenario aggregate-loss distribution or VaR/TVaR comparison.
4. Mitigation strategy comparison table or chart.

Do not reward visuals that are decorative only and do not help explain coverage, pricing, stress, mitigation, or tail risk.

## 8. Frequency model benchmark

The V2 solution notebook uses an exposure-adjusted Poisson GLM with:

- response: `claim_count`;
- offset: `log(exposure_years)`;
- occupancy and region factors;
- scaled environmental/climate variables;
- an air-water stress interaction; and
- mitigation indicators.

Diagnostics:

| Diagnostic | Solution value |
|---|---:|
| GLM converged | True |
| Pearson dispersion | 1.329 |
| Deviance / df | 0.510 |
| Captured warnings | 0 |

Selected fitted rate-ratio outputs:

| Variable | Coefficient | Rate ratio | Comment |
|---|---:|---:|---|
| `turbidity_2` | 0.574 | 1.776 | Higher turbidity is associated with higher fitted claim frequency. |
| `water_treatment` | -0.525 | 0.592 | Water treatment lowers fitted frequency. |
| `air_filtration` | -0.427 | 0.652 | Air filtration lowers fitted frequency. |
| `business_continuity_plan` | -0.431 | 0.650 | BCP lowers fitted frequency. |
| `air_water_stress_interaction` | 0.512 | 1.669 | Compound stress raises fitted frequency. |

Acceptable student range: a comparable GLM should produce a 2026 baseline expected claim count roughly **15 to 30**. A materially different value needs explanation through model choice.

## 9. Severity model benchmark

The V2 reference model uses claim-level positive `covered_loss`, not annual paid severity, as the Gamma response. Paid loss is generated in simulation by applying the deductible and per-claim limit. This avoids invalid Gamma responses while preserving legitimate zero-paid claims.

Diagnostics:

| Diagnostic | Solution value |
|---|---:|
| Claim-level observations | 95 |
| Minimum covered loss | 12,878.08 |
| Zero-paid claims retained | 33 |
| Gamma GLM converged | True |
| Gamma dispersion/scale | 0.4688 |
| Captured warnings | 0 |

Selected fitted multiplicative effects:

| Variable | Coefficient | Multiplicative effect | Comment |
|---|---:|---:|---|
| `bi_waiting_period_days` | -0.332 | 0.717 | Longer waiting period lowers covered severity in this simplified contract. |
| `log_insured_value` | 0.465 | 1.593 | Higher insured value increases fitted covered severity. |
| `pm25_10` | 0.176 | 1.192 | Higher PM2.5 increases fitted covered severity directionally. |
| `turbidity_2` | 0.092 | 1.097 | Higher turbidity increases fitted covered severity directionally. |
| `air_water_stress_interaction` | 0.149 | 1.160 | Compound stress raises covered severity directionally. |

Acceptable student range: fitted covered severities should be strictly positive and policy terms should be applied after severity simulation.

## 10. Baseline 2026 pricing benchmark

The solution treats 2026 as the current annual portfolio snapshot.

| Metric | Solution value |
|---|---:|
| 2026 policy rows | 250 |
| 2026 exposure | 214.199 |
| Expected annual paid loss | 1,579,995.52 |
| Current premium | 14,130,800 |
| Indicated premium | 2,486,667.53 |
| Premium adequacy ratio | 5.681 |
| VaR99 | 2,886,835.57 |
| TVaR99 | 3,133,296.59 |

Teaching point: baseline premium is adequate in the V2 benchmark. The committee issue is not current-year baseline inadequacy; it is deterioration under water and compound stress.

## 11. Scenario comparison benchmark

| Scenario | Expected annual paid loss | Current premium | Indicated premium | Adequacy ratio | VaR99 | TVaR99 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 1,579,995.52 | 14,130,800 | 2,486,667.53 | 5.68 | 2,886,835.57 | 3,133,296.59 |
| Air stress | 2,795,165.95 | 14,130,800 | 4,222,625.29 | 3.35 | 4,662,297.31 | 5,019,203.97 |
| Water stress | 11,233,830.43 | 14,130,800 | 16,277,860.25 | 0.87 | 14,999,369.84 | 15,675,254.10 |
| Compound stress | 19,741,145.53 | 14,130,800 | 28,431,167.55 | 0.50 | 25,196,709.35 | 25,988,897.73 |

Expected interpretation: compound stress is the most material scenario by both expected loss and tail risk. Water stress alone is more material than air stress in the V2 benchmark.

Acceptable student ranges with similar modelling:

| Scenario | Expected loss range | TVaR99 range |
|---|---:|---:|
| Baseline | 1.2M–2.2M | 2.6M–3.7M |
| Air stress | 2.1M–3.6M | 4.2M–6.0M |
| Water stress | 9M–14M | 13M–18M |
| Compound stress | 16M–24M | 22M–30M |

## 12. Scenario TVaR simulation uncertainty

Repeated-seed check using six seeds and 8,000 simulations per seed:

| Scenario | Mean TVaR99 | Monte Carlo SE | Approx. 95% low | Approx. 95% high | Mean VaR99 |
|---|---:|---:|---:|---:|---:|
| Baseline | 3,107,996.48 | 24,275.00 | 3,060,417.48 | 3,155,575.47 | 2,880,558.58 |
| Air stress | 5,015,744.47 | 14,328.42 | 4,987,660.76 | 5,043,828.17 | 4,664,828.70 |
| Water stress | 15,593,569.43 | 43,212.70 | 15,508,872.54 | 15,678,266.31 | 14,971,284.23 |
| Compound stress | 25,919,949.35 | 47,417.81 | 25,827,010.44 | 26,012,888.26 | 25,059,444.50 |

Teaching point: the scenario ranking is not a Monte Carlo artifact; the confidence bands are well separated.

## 13. Mitigation benchmark under compound stress

Budget: **8,000,000** currency units.

The solution compares a finite set of feasible candidate strategies. This is not a proof of global optimality.

| Strategy | Actions selected | Cost | Expected annual loss | Expected-loss reduction | BCR | VaR99 | TVaR99 | TVaR reduction | Post-mitigation adequacy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No new mitigation | 0 | 0 | 19,741,145.53 | 0.00 | n/a | 25,196,709.35 | 25,988,897.73 | 0.00 | 0.50 |
| Air priority | 85 | 7,988,000 | 15,697,630.89 | 4,043,514.64 | 0.51 | 20,657,145.39 | 21,509,315.45 | 4,479,582.28 | 0.62 |
| Water priority | 65 | 7,983,000 | 15,065,957.84 | 4,675,187.69 | 0.59 | 19,742,247.01 | 20,559,437.33 | 5,429,460.40 | 0.65 |
| BCP priority | 146 | 7,625,000 | 16,350,870.38 | 3,390,275.16 | 0.44 | 21,519,148.61 | 22,306,714.00 | 3,682,183.73 | 0.60 |
| Balanced BCR | 91 | 7,975,000 | 13,002,128.31 | 6,739,017.22 | 0.85 | 17,383,675.71 | 18,165,898.50 | 7,822,999.23 | 0.75 |
| Largest reduction first | 78 | 7,972,000 | 13,165,552.95 | 6,575,592.58 | 0.82 | 17,537,823.78 | 18,320,881.18 | 7,668,016.55 | 0.74 |

Solution-selected strategy: **Balanced BCR**, because it has the lowest simulated TVaR99 among the candidate strategies evaluated.

## 14. Mitigation ranking stability

Repeated-seed check using six seeds and 8,000 simulations per strategy:

| Strategy | Mean TVaR99 | TVaR SD | Best-rank count | Monte Carlo SE | Approx. 95% low | Approx. 95% high |
|---|---:|---:|---:|---:|---:|---:|
| Balanced BCR | 18,063,370.05 | 94,866.01 | 6 | 38,728.89 | 17,987,461.44 | 18,139,278.67 |
| Largest reduction first | 18,312,340.29 | 127,015.20 | 0 | 51,853.74 | 18,210,706.96 | 18,413,973.62 |
| Water priority | 20,495,213.80 | 146,908.25 | 0 | 59,975.04 | 20,377,662.72 | 20,612,764.88 |
| Air priority | 21,382,487.57 | 161,424.41 | 0 | 65,901.24 | 21,253,321.14 | 21,511,654.00 |
| BCP priority | 22,119,023.64 | 169,136.65 | 0 | 69,049.75 | 21,983,686.13 | 22,254,361.15 |
| No new mitigation | 25,895,391.89 | 114,259.34 | 0 | 46,646.18 | 25,803,965.38 | 25,986,818.40 |

Teaching point: Balanced BCR has a clear candidate-set advantage in this implementation, but the instructor should still describe this as the best among evaluated candidates, not as the mathematical global optimum.

## 15. Strong final recommendation should say

A high-quality committee recommendation should include:

1. Baseline premium is adequate under the fitted V2 reference model.
2. Air stress increases loss but does not threaten adequacy in the benchmark.
3. Water stress materially reduces adequacy below 1.00.
4. Compound stress is the dominant risk state by expected loss, VaR, and TVaR.
5. The best evaluated mitigation candidate materially reduces compound-stress TVaR but does not fully restore adequacy.
6. AquaAir should combine targeted mitigation funding, repricing for stressed water/compound risk, monitoring, and selective underwriting action.
7. The data are synthetic, the models are simplified, and real deployment would require validation, governance, external data, and dependence modelling.

## 16. Red flags in student outputs

Flag submissions that:

- treat stress flags as claims;
- ignore the exposure offset;
- simulate all 750 rows as one current annual portfolio;
- fit Gamma severity to zero paid losses;
- skip policy-term mechanics;
- report VaR but not TVaR;
- select mitigation solely by BCR;
- claim the mitigation result is a global optimum;
- exceed the 8,000,000 budget;
- fail to recompute stress flags after scenario transformations;
- provide code without actuarial interpretation; or
- make external real-world claims from the synthetic data.
