# ClimateTwin V2 Instructor Guide

## Package position

This guide supports **ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management**. The V2 package is built around the corrected `data_script.py`, which is the single source of truth for the synthetic portfolio, claim-level losses, annual aggregates, scenario rules, and insurance-payment mechanics.

Use this guide with:

- `dataset.csv`
- `claim_level_data.csv` — instructor-side claim-level table
- `data_dictionary.md`
- `case_study.md`
- `student_notebook.ipynb`
- `solution.ipynb`
- `expected_output.md`
- `rubric.md`
- `setup_instructions.md`
- `case_study.pptx`

The teaching goal is not to make students memorize a model. The goal is to make them reason like P&C actuaries facing emerging climate-linked risk: define coverage, translate environmental information into insured-loss variables, model frequency and severity separately, quantify pricing adequacy, stress the portfolio, and choose a feasible mitigation candidate under a budget.

## Prerequisites

Students should have basic familiarity with:

- commercial P&C insurance terms such as premium, deductible, policy limit, claim count, and paid loss;
- introductory ratemaking concepts, including frequency, severity, pure premium/loss cost, expense provisions, and indicated premium;
- introductory statistics or predictive modelling, especially GLM interpretation;
- basic Python/Jupyter use, including reading CSV files and running notebook cells.

The short version can be used with weaker coding groups because routine simulation helpers are supplied.

## Learning objectives

By the end of the case, students should be able to:

1. Distinguish environmental hazard indicators from qualifying insured triggers.
2. Explain how policy terms, exposure, deductibles, limits, and BI waiting periods affect paid loss.
3. Fit and interpret an exposure-adjusted claim-frequency model.
4. Fit and interpret a positive conditional severity model.
5. Combine frequency and severity into expected loss and indicated premium.
6. Compare current premium with indicated premium using a premium adequacy ratio.
7. Run baseline, air-stress, water-stress, and compound-stress scenarios.
8. Simulate aggregate annual loss and calculate VaR99 and TVaR99.
9. Compare feasible mitigation candidates under the 8,000,000 budget using TVaR as the primary criterion.
10. Communicate a practical pricing, underwriting, mitigation, and monitoring recommendation.

## Exact teaching timetable

The proposal separates preparation and independent final submission from the **4.5 classroom hours**. Use the table below for the main full version.

| Segment | Mode | Time | Instructor focus | Student output |
|---|---|---:|---|---|
| Pre-class preparation | Independent | 45–60 min | Students read the case and data dictionary before class. | Initial notes on coverage chain and variables. |
| 1. Launch and coverage framing | In class | 30 min | AquaAir narrative, policy terms, environmental-stress versus insured-trigger distinction. | Coverage-chain explanation. |
| 2. Data validation and EDA | In class | 30 min | Dataset grain, 2026 portfolio snapshot, trigger/stress counts, zero-paid claims. | Validation table and one descriptive visual. |
| 3. Frequency and severity modelling | In class | 75 min | Exposure offset, claim-level positive severity, diagnostics, warning interpretation. | Frequency and severity model outputs with interpretation. |
| 4. Pricing and scenario stress testing | In class | 75 min | Expected loss, indicated premium, adequacy, four scenarios, VaR99, TVaR99. | Scenario comparison table and tail-risk visual. |
| 5. Mitigation and committee decision | In class | 60 min | Candidate feasible strategies, budget, TVaR ranking, uncertainty, decision trade-offs. | Selected candidate strategy and committee recommendation outline. |
| Final committee memo | Independent | 60–90 min | Instructor grades using rubric. | Completed notebook and final memo. |

Total in-class time: **270 minutes = 4.5 hours**.

## Short teaching version

For a 90–120 minute version, give students fitted model cells or pre-run outputs. The short version should focus on:

1. coverage interpretation;
2. baseline adequacy;
3. scenario comparison;
4. VaR/TVaR interpretation;
5. candidate mitigation choice; and
6. committee recommendation.

Students should not spend the short session writing routine simulation machinery.

## Class launch script

AquaAir insures hospitals, manufacturing facilities, and food-processing facilities. Management is worried that deteriorating air and water quality may increase claims and create underpriced tail risk. However, the contract does not pay simply because pollution or contamination readings are bad. There must be a qualifying insured trigger, and the payment depends on exposure, coverage terms, deductibles, limits, BI waiting periods, and mitigation.

Your job is to decide whether the current portfolio is adequate, how it behaves under air, water, and compound stress, and which candidate mitigation strategy should be funded under an 8,000,000 budget.

The committee does not want a perfect academic model. It wants a defensible actuarial decision.

## V2 data-generating process overview

The dataset contains 750 policy-location-year rows: 250 synthetic commercial locations across 2024–2026. `claim_level_data.csv` contains the 95 generated claim-level records used to create the annual aggregates in `dataset.csv`.

The V2 generator embeds:

1. location-level region and occupancy structure;
2. policy terms including insured value, deductible, per-claim limit, BI waiting period, current premium, and exposure;
3. air and water indicators plus climate variables;
4. transparent stress thresholds;
5. separate probabilistic qualifying insured triggers;
6. exposure-adjusted Poisson claim frequency;
7. positive claim-level covered severity;
8. per-claim policy mechanics from ground-up loss to covered loss to paid loss;
9. legitimate zero-paid claims when deductible/waiting-period mechanics eliminate payment;
10. mitigation effects on frequency and severity;
11. a positive compound-risk mechanism; and
12. current premium that does not fully price stressed water/compound risk.

Do not disclose detailed DGP coefficients before students complete the analysis. Disclose the high-level design during debrief.

## Correct V2 insurance mechanics

For every simulated claim:

1. **Ground-up loss** equals remediation loss plus total BI loss before waiting-period treatment.
2. **Covered BI loss** equals daily BI loss multiplied by days above the waiting period.
3. **Covered loss** equals remediation loss plus covered BI loss.
4. **Loss after deductible** equals `max(covered_loss - deductible, 0)`.
5. **Paid loss** equals `min(loss_after_deductible, policy_limit)`.

The deductible is applied once per claim. The policy limit is applied after the deductible. A claim may have positive covered loss but zero paid loss.

## Required worked insurance examples

Use these during class before modelling.

| Example | Explanation | Paid-loss result |
|---|---|---:|
| Loss below deductible | A 20,000 covered remediation loss with a 50,000 deductible produces no insurer payment. | 0 |
| Payment constrained by policy limit | A 900,000 covered loss less a 50,000 deductible gives 850,000 after deductible, but a 400,000 limit caps payment. | 400,000 |
| BI waiting period not met, other cost payable | A two-day BI interruption with a three-day waiting period has no covered BI, but a 100,000 remediation cost is still eligible; after a 50,000 deductible, paid loss is 50,000. | 50,000 |

These examples must match `case_study.md`, `solution.ipynb`, and `data_script.py`.

## Model diagnostics and warnings

The V2 solution intentionally avoids blanket warning suppression. In the reference run:

- the Poisson frequency GLM converges;
- Pearson dispersion is about 1.329;
- deviance/df is about 0.510;
- the Gamma covered-severity GLM converges;
- Gamma scale is about 0.4688;
- no model-fitting warnings are captured.

If students see warnings, ask them to identify the source rather than hiding the warnings. Common causes include unstable interaction terms, collinearity among environmental indicators, sparse trigger categories, invalid severity responses, or using all 750 rows as one portfolio-year.

## Instructor answer checkpoints

### Checkpoint 1: Data grain

Expected answer: one row is one policy-location-year. There are 750 rows, 250 unique locations, and three years. Model fitting can use all years, but annual portfolio simulation should use the 2026 snapshot only.

### Checkpoint 2: Hazard versus claim

Expected answer: stress flags identify adverse environmental conditions. Trigger flags represent qualifying insured events. Claims occur only when an insured trigger exists.

### Checkpoint 3: Zero-paid claims

Expected answer: 33 claim-level records have zero paid loss. These are valid payment outcomes after contract mechanics, not bad data.

### Checkpoint 4: Frequency model

Expected answer: use `claim_count` with `log(exposure_years)` as an offset. Interpret coefficients as rate ratios and include a compound-risk term.

### Checkpoint 5: Severity model

Expected answer: model positive claim-level `covered_loss` or another defensible positive conditional severity response. Do not fit a Gamma model to zero paid losses.

### Checkpoint 6: Pricing

Expected answer: expected paid loss is combined with fixed expense, variable expense, and profit/contingency to calculate indicated premium. Adequacy below 1.00 indicates underpricing.

### Checkpoint 7: Stress testing

Expected answer: run baseline, air stress, water stress, and compound stress. Recompute stress flags after transformations. Compare expected loss, indicated premium, VaR99, and TVaR99.

### Checkpoint 8: Mitigation

Expected answer: compare a manageable set of candidate feasible strategies under the 8,000,000 budget. Select the candidate with the lowest simulated TVaR99 among those evaluated. Do not claim a global mathematical optimum.

## Expected benchmark interpretation

The V2 reference solution produces the following high-level story:

- Baseline 2026 premium is adequate under the fitted reference model.
- Air stress increases expected loss and TVaR but remains adequate in the reference benchmark.
- Water stress materially reduces adequacy below 1.00.
- Compound stress is the dominant risk state by expected loss, VaR, and TVaR.
- The best evaluated mitigation candidate materially reduces TVaR but does not fully restore compound-stress adequacy.
- AquaAir should combine targeted mitigation funding with repricing, monitoring, and selective underwriting controls.

## Candidate mitigation strategy construction

The solution constructs action-level candidates where mitigation is absent and upgrade cost is positive. It compares finite feasible strategies such as:

- no new mitigation;
- air priority;
- water priority;
- BCP priority;
- balanced benefit-cost ranking; and
- largest expected reduction first.

This construction is intentionally manageable for teaching. It demonstrates budgeted actuarial decision-making without turning the case into a large integer-programming exercise.

## Simulation uncertainty

Use repeated seeds to show whether tail-risk rankings are stable. In the V2 solution, compound stress is clearly the highest-risk scenario, and the Balanced BCR candidate has the lowest mean TVaR among the candidate strategies evaluated. The repeated-seed check supports this ranking, but it still does not prove global optimality over every possible mitigation combination.

## Common misconceptions and corrections

| Misconception | Correction |
|---|---|
| Bad environmental readings are claims. | They are hazard indicators. Claims require qualifying insured triggers. |
| Stress flags and triggers are the same. | Stress flags are environmental screens; triggers are insured-event indicators. |
| Zero-paid claims are data errors. | They are valid outcomes after deductible and waiting-period mechanics. |
| Use all 750 rows for one annual simulation. | Fit on all rows; simulate the 2026 current portfolio snapshot. |
| Exposure can be ignored. | Frequency modelling should use an exposure offset. |
| Aggregate loss modelling alone is enough. | The teaching objective is frequency-severity decomposition. |
| Gamma paid severity can include zero paid losses. | Gamma response must be positive; use covered severity or another valid approach. |
| Compound stress equals air plus water. | Compound stress includes interaction and changes the portfolio risk state. |
| Highest BCR is automatically best. | TVaR99 is the primary candidate-selection criterion. |
| Candidate comparison proves a global optimum. | It identifies the best among evaluated feasible candidates only. |
| One simulation seed is definitive. | Tail-risk rankings should be checked for Monte Carlo stability. |

## Discussion prompts

1. What exactly converts an environmental hazard into an insured claim?
2. Why can a claim have positive covered loss but zero paid loss?
3. Which variable most changed frequency in your model?
4. Which variable most changed severity in your model?
5. Why are frequency and severity not interchangeable?
6. Which scenario most changed expected loss?
7. Which scenario most changed TVaR?
8. Why does water stress matter more than air stress in this V2 benchmark?
9. Does mitigation solve pricing adequacy by itself?
10. What real-world validation would AquaAir need before deployment?

## Grading emphasis

Strong submissions will:

- preserve the coverage distinction throughout;
- calculate the three insurance examples correctly;
- use exposure correctly;
- fit separate frequency and severity models;
- use positive severity responses;
- calculate pricing metrics correctly;
- compare all four scenarios;
- simulate aggregate annual loss reproducibly;
- choose mitigation under budget based on TVaR99 among evaluated candidates;
- discuss simulation uncertainty; and
- communicate limitations clearly.

Weak submissions usually fail because they treat environmental stress as claims, ignore exposure, use all three years as a single annual portfolio, fit Gamma severity to zero paid losses, select mitigation only by BCR, claim a global optimum, or present code without a business recommendation.

## Optional extensions

Use only after the core case is completed:

1. Negative Binomial frequency sensitivity.
2. Alternative severity distributions.
3. Train/test or cross-validation exercise.
4. Segment-level underwriting actions.
5. Alternative budgets.
6. Alternative VaR/TVaR confidence levels.
7. Sensitivity to Monte Carlo simulation count.
8. Parameter uncertainty.
9. Simple reinsurance layer.
10. Credibility or Bayesian updating.
