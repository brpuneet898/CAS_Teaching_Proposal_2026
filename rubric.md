# ClimateTwin Assessment Rubric

Total: **100 marks**

This rubric is designed for the completed notebook plus final Climate Risk Committee recommendation. It expands the high-level proposal grading into performance-level criteria.

## 1. Coverage logic and case framing — 15 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 13–15 | Clearly distinguishes environmental stress, qualifying insured trigger, claim occurrence, covered loss, and paid loss. Correctly explains air, water, and compound coverage. Uses policy terms throughout. Does not treat poor environmental readings as automatic claims. |
| Good | 10–12 | Mostly correct coverage interpretation with minor imprecision. Recognizes that stress flags and triggers differ. Uses policy terms in most relevant places. |
| Satisfactory | 7–9 | Understands the broad idea but occasionally blurs hazard, trigger, and claim. Mentions policy terms but does not fully integrate them. |
| Weak | 4–6 | Treats several environmental indicators as claims or ignores key coverage requirements. Limited use of deductible, limit, or BI waiting-period concepts. |
| Poor | 0–3 | Fundamental misunderstanding of the insurance mechanism. Assumes pollution/contamination readings directly equal insured losses. |

## 2. Data understanding and exploratory analysis — 10 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 9–10 | Correctly validates 750 rows, 250 locations, three years, exposure, claims, and stress/trigger counts. Produces useful summaries by region and occupancy. Visualizations support the decision. |
| Good | 7–8 | Validates most core facts and provides relevant summaries. Visuals are understandable but may be limited. |
| Satisfactory | 5–6 | Basic summaries are present but incomplete. Some portfolio or exposure interpretation is missing. |
| Weak | 2–4 | Minimal EDA, few validations, or weak visual choices. |
| Poor | 0–1 | No meaningful data validation or EDA. |

## 3. Frequency modelling — 15 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 13–15 | Fits a defensible count model for `claim_count` with `log(exposure_years)` offset. Includes relevant occupancy, environmental, climate, mitigation, and compound-risk variables. Interprets rate ratios in actuarial terms. Notes model limitations. |
| Good | 10–12 | Uses a reasonable count model and exposure offset. Includes most important predictors. Interpretation is mostly correct. |
| Satisfactory | 7–9 | Fits a count model but misses some important predictors or provides limited interpretation. Exposure treatment may be shallow but not entirely absent. |
| Weak | 4–6 | Model is technically weak, omits exposure offset, or interprets coefficients poorly. |
| Poor | 0–3 | No valid frequency model or uses an inappropriate response/approach. |

## 4. Severity modelling — 15 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 13–15 | Correctly models conditional severity using claim-positive rows only. Uses Gamma-log or defensible Lognormal approach. Considers insured value, occupancy, environmental state, compound risk, and mitigation. Explains how severity drivers differ from frequency drivers. |
| Good | 10–12 | Severity model is appropriate and mostly well interpreted. Minor omissions in predictors or explanation. |
| Satisfactory | 7–9 | Basic severity model is present but limited. Some confusion about weighting or response construction. |
| Weak | 4–6 | Severity response is poorly defined or uses zero-claim rows incorrectly. Limited actuarial interpretation. |
| Poor | 0–3 | No valid conditional severity model. |

## 5. Pricing and premium adequacy — 12 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 11–12 | Correctly combines expected frequency and severity. Calculates expected loss, loss cost per exposure, indicated premium, current premium, and adequacy ratio. Uses the required expense/profit assumptions. Provides segment-level adequacy insight. |
| Good | 9–10 | Pricing calculations are mostly correct with minor errors or limited segmentation. |
| Satisfactory | 6–8 | Expected loss and adequacy are attempted but some formula or interpretation errors appear. |
| Weak | 3–5 | Pricing mechanics are incomplete or materially incorrect. |
| Poor | 0–2 | No coherent pricing or adequacy calculation. |

## 6. Scenario stress testing and tail risk — 15 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 13–15 | Applies all four required scenarios correctly. Recomputes stress flags after transformations. Uses fitted models to estimate scenario risk. Simulates aggregate annual loss reproducibly. Reports expected loss, indicated premium, adequacy, VaR99, and TVaR99. Correctly interprets compound risk. |
| Good | 10–12 | Runs all scenarios with mostly correct mechanics. Reports key risk metrics. Interpretation is sound but not deeply developed. |
| Satisfactory | 7–9 | Scenarios are attempted but one or two mechanics are incomplete, such as weak flag recomputation or limited tail-risk discussion. |
| Weak | 4–6 | Scenario analysis has major implementation or interpretation errors. |
| Poor | 0–3 | No meaningful scenario/tail-risk analysis. |

## 7. Mitigation decision under budget — 10 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 9–10 | Constructs feasible mitigation portfolios under the 8,000,000 budget. Evaluates expected-loss reduction, BCR, VaR reduction, TVaR reduction, and adequacy. Selects strategy primarily by lowest TVaR99 and explains trade-offs. |
| Good | 7–8 | Feasible mitigation analysis with most required metrics. Uses TVaR or tail-risk reasoning, though trade-off discussion may be brief. |
| Satisfactory | 5–6 | Mitigation is attempted and budget is considered, but metrics or selection logic are incomplete. |
| Weak | 2–4 | Chooses mitigation mainly by intuition or BCR only; budget or tail risk not handled correctly. |
| Poor | 0–1 | No credible mitigation decision. |

## 8. Communication, recommendation, and limitations — 8 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 8 | Final recommendation is concise, executive-ready, and actuarially grounded. Clearly states baseline position, material stress, selected mitigation, pricing/underwriting action, and limitations. |
| Good | 6–7 | Recommendation is clear and mostly complete but less polished or less quantitative. |
| Satisfactory | 4–5 | Recommendation exists but is generic or missing important decision metrics. |
| Weak | 2–3 | Limited communication; mostly code outputs with little business interpretation. |
| Poor | 0–1 | No usable final recommendation. |

## 9. Reproducibility, code quality, and professional practice — 10 marks

| Performance level | Marks | Criteria |
|---|---:|---|
| Excellent | 9–10 | Notebook runs top-to-bottom. Uses fixed random seed. Code is organized and readable. Outputs are labelled. Assumptions are stated. No hard-coded unexplained results. |
| Good | 7–8 | Notebook mostly runs and is understandable. Minor organization or reproducibility issues. |
| Satisfactory | 5–6 | Notebook partially runs or requires small fixes. Some unclear code or assumptions. |
| Weak | 2–4 | Significant execution, organization, or reproducibility issues. |
| Poor | 0–1 | Notebook does not run or is not submitted in usable form. |

## Suggested grade interpretation

| Score | Interpretation |
|---:|---|
| 85–100 | Excellent actuarial case solution; ready for strong committee presentation. |
| 70–84 | Good solution with minor technical or communication gaps. |
| 55–69 | Acceptable but incomplete; key actuarial mechanics need strengthening. |
| 40–54 | Weak solution; major coverage, modelling, or decision errors. |
| Below 40 | Does not demonstrate the required case competencies. |

## Common penalty guidance

Apply these penalties where relevant, even if code executes:

| Issue | Suggested penalty |
|---|---:|
| Treats stress flags as claims | -8 to -15 |
| Uses all 750 rows as one simulated annual portfolio | -5 to -10 |
| Omits exposure offset in frequency model | -5 to -8 |
| Uses zero-claim rows in severity model | -5 to -8 |
| Skips VaR or TVaR | -5 to -10 |
| Exceeds 8,000,000 mitigation budget | -5 to -10 |
| Selects mitigation solely by BCR | -4 to -8 |
| Does not state limitations | -3 to -6 |
| Notebook does not run | -8 to -20 depending on severity |

## Optional bonus credit: up to 5 marks

Award bonus credit for high-quality extensions that do not replace the core case:

- Negative Binomial frequency sensitivity.
- Alternative severity model comparison.
- Train/test validation.
- Sensitivity to simulation count or random seed.
- Alternative budget levels.
- Segment-level underwriting recommendations.
- Parameter uncertainty discussion.
- Clear, polished committee slide or memo.
