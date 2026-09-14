# ClimateTwin V2 Assessment Rubric

Total: **100 points**

This rubric is for the completed notebook plus the final Climate Risk Committee recommendation. It avoids double-penalizing the same mistake: apply the most relevant criterion first, then use the penalty guidance only when a separate deliverable is affected.

## 1. Competency and evidence map

| Learning objective | Student activity | Actuarial technique | Relevant CAS competency or syllabus area | Evidence of achievement |
|---|---|---|---|---|
| Distinguish hazard from insured loss | Trace environmental stress, trigger, claim, covered loss, and paid loss | Coverage interpretation and exposure definition | P&C coverage context; ratemaking problem definition; actuarial judgment | Correct coverage-chain explanation and no treatment of stress flags as claims |
| Explain policy-term effects | Work through deductible, limit, and BI waiting-period examples | Policy financial-term application | Ratemaking data preparation; contract mechanics; claim-cost measurement | Correct calculations for below-deductible, limited-payment, and BI waiting-period examples |
| Model exposure-adjusted frequency | Fit count model for `claim_count` | Poisson/GLM frequency modelling with exposure offset | Predictive analytics; frequency modelling; classification ratemaking | Valid model with `log(exposure_years)` offset and rate-ratio interpretation |
| Model conditional severity | Fit severity model using claim-level positive severity | Gamma/lognormal severity modelling | Severity modelling; loss-cost estimation; predictive analytics | Positive severity response, valid diagnostics, and explanation of severity drivers |
| Calculate loss cost and premium adequacy | Combine frequency and severity predictions | Frequency-severity expected loss and indicated premium | Basic ratemaking; rate indication; expense/profit loading | Expected loss, indicated premium, current premium, and adequacy ratio calculated correctly |
| Evaluate climate stress | Run baseline, air, water, and compound scenarios | Scenario testing and model-based projection | Risk management; climate/emerging-risk applications; stress testing | Scenario table with expected loss, premium adequacy, VaR99, and TVaR99 |
| Measure aggregate tail risk | Simulate annual portfolio loss | Aggregate-loss simulation, VaR, TVaR | Enterprise/risk management; risk-adjusted decision-making | Reproducible simulation using 2026 portfolio only and correct tail metrics |
| Choose mitigation under budget | Compare feasible candidate portfolios | Budget-constrained candidate evaluation and tail-risk ranking | Risk management; cost of risk; mitigation economics | Feasible strategy, cost, BCR, TVaR reduction, and no global-optimum claim |
| Communicate actuarial recommendation | Prepare Climate Risk Committee memo | Professional actuarial communication | Communication of assumptions, uncertainty, limitations, and business action | Concise recommendation with quantitative support and limitations |

## 2. Graded criteria

### A. Coverage logic and insurance examples — 14 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 13–14 | Clearly distinguishes environmental stress, insured trigger, claim, covered loss, and paid loss. Correctly explains air, water, compound coverage, deductible, limit, and BI waiting period. All three worked examples are correct. |
| Good | 10–12 | Coverage interpretation is mostly correct. Minor wording issues, but examples and policy-term logic are substantially correct. |
| Satisfactory | 7–9 | Understands the broad idea but occasionally blurs hazard, trigger, and claim or misses one example detail. |
| Weak | 4–6 | Several coverage errors or weak use of policy terms. |
| Poor | 0–3 | Fundamental misunderstanding; treats environmental readings as direct insured losses. |

### B. Data validation and exploratory analysis — 10 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 9–10 | Validates rows, locations, years, exposure, claims, claim-level reconciliation, zero-paid claims, stress/trigger counts, and useful region/occupancy summaries. Visuals support decisions. |
| Good | 7–8 | Most core validations and useful summaries are present. Visuals are relevant but limited. |
| Satisfactory | 5–6 | Basic summaries are present, but claim-level or trigger validation is incomplete. |
| Weak | 2–4 | Minimal EDA or weak validation. |
| Poor | 0–1 | No meaningful data validation. |

### C. Frequency modelling — 14 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 13–14 | Fits a defensible count model for `claim_count` with `log(exposure_years)` offset; includes relevant occupancy, environmental, climate, mitigation, and compound-risk predictors; reports diagnostics and rate-ratio interpretation. |
| Good | 10–12 | Reasonable count model with exposure offset and most key predictors. Interpretation is mostly correct. |
| Satisfactory | 7–9 | Count model is present but predictor set, diagnostics, or interpretation is limited. |
| Weak | 4–6 | Omits exposure offset or uses weak coefficient interpretation. |
| Poor | 0–3 | No valid frequency model. |

### D. Severity modelling — 14 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 13–14 | Models positive claim-level covered severity, or another defensible positive conditional severity response; preserves zero-paid claims as payment outcomes; includes insured value, occupancy, environmental/compound terms, mitigation, diagnostics, and interpretation. |
| Good | 10–12 | Appropriate severity model with minor omissions in predictors, diagnostics, or interpretation. |
| Satisfactory | 7–9 | Basic severity model is present but response construction or weighting is only partly explained. |
| Weak | 4–6 | Severity response is poorly defined or invalid zero-paid values are mishandled. |
| Poor | 0–3 | No valid conditional severity model. |

### E. Pricing and premium adequacy — 12 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 11–12 | Correctly combines expected frequency and severity; calculates expected loss, loss cost per exposure, indicated premium, current premium, adequacy ratio, and at least one segment-level adequacy insight. |
| Good | 9–10 | Pricing calculations are mostly correct with minor errors or limited segmentation. |
| Satisfactory | 6–8 | Expected loss and adequacy are attempted, but one formula or interpretation error appears. |
| Weak | 3–5 | Pricing mechanics are incomplete or materially incorrect. |
| Poor | 0–2 | No coherent pricing or adequacy calculation. |

### F. Scenario stress testing and tail risk — 15 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 13–15 | Applies all four scenarios correctly; recomputes stress flags; uses fitted models for scenario risk; simulates 2026 aggregate annual paid loss reproducibly; reports expected loss, indicated premium, adequacy, VaR99, and TVaR99; interprets compound risk. |
| Good | 10–12 | All scenarios are run with mostly correct mechanics and sound interpretation. |
| Satisfactory | 7–9 | Scenarios are attempted, but one or two mechanics are incomplete. |
| Weak | 4–6 | Major implementation or interpretation errors in scenario analysis. |
| Poor | 0–3 | No meaningful scenario/tail-risk analysis. |

### G. Mitigation candidate evaluation — 10 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 9–10 | Constructs feasible candidate portfolios under the 8,000,000 budget; reports cost, expected-loss reduction, BCR, VaR reduction, TVaR reduction, adequacy, and simulation uncertainty; selects based on TVaR among evaluated candidates without claiming global optimality. |
| Good | 7–8 | Feasible candidate analysis with most required metrics and TVaR-based reasoning. |
| Satisfactory | 5–6 | Mitigation is attempted, but candidate construction or metrics are incomplete. |
| Weak | 2–4 | Chooses mainly by intuition or BCR only; budget or TVaR is weak. |
| Poor | 0–1 | No credible mitigation decision. |

### H. Communication, recommendation, and limitations — 11 points

| Level | Points | Observable evidence |
|---|---:|---|
| Excellent | 10–11 | Committee recommendation is concise, quantitative, and business-ready. It states baseline position, material stress, selected mitigation, pricing/underwriting action, uncertainty, and limitations. |
| Good | 8–9 | Clear recommendation with most decision metrics and limitations. |
| Satisfactory | 5–7 | Recommendation exists but is generic or missing important evidence. |
| Weak | 2–4 | Mostly code outputs with limited business interpretation. |
| Poor | 0–1 | No usable final recommendation. |

## 3. Point-total check

| Criterion | Points |
|---|---:|
| A. Coverage logic and insurance examples | 14 |
| B. Data validation and exploratory analysis | 10 |
| C. Frequency modelling | 14 |
| D. Severity modelling | 14 |
| E. Pricing and premium adequacy | 12 |
| F. Scenario stress testing and tail risk | 15 |
| G. Mitigation candidate evaluation | 10 |
| H. Communication, recommendation, and limitations | 11 |
| **Total** | **100** |

## 4. Common penalty guidance

Apply these only where the error is not already fully captured in the criterion score.

| Issue | Suggested penalty |
|---|---:|
| Treats stress flags as claims | -8 to -14 |
| Uses all 750 rows as one simulated annual portfolio | -5 to -10 |
| Omits exposure offset in frequency model | -5 to -8 |
| Fits Gamma severity directly to zero paid losses | -5 to -8 |
| Skips VaR or TVaR | -5 to -10 |
| Exceeds the 8,000,000 mitigation budget | -5 to -10 |
| Claims global optimum from finite candidate comparison | -4 to -8 |
| Selects mitigation solely by BCR | -4 to -8 |
| Does not state limitations | -3 to -6 |
| Notebook does not run | -8 to -20 depending on severity |

## 5. Suggested grade interpretation

| Score | Interpretation |
|---:|---|
| 85–100 | Strong actuarial case solution; ready for committee presentation. |
| 70–84 | Good solution with minor technical or communication gaps. |
| 55–69 | Acceptable but incomplete; key mechanics need strengthening. |
| 40–54 | Weak solution with major coverage, modelling, or decision errors. |
| Below 40 | Does not demonstrate the required case competencies. |

## 6. Optional bonus credit

Award up to **5 bonus points** for high-quality extensions that do not replace the core case, such as Negative Binomial sensitivity, alternative severity models, train/test validation, sensitivity to simulation count or random seed, alternative budgets, segment-level underwriting recommendations, parameter uncertainty, or a polished committee slide/memo.
