# ClimateTwin Instructor Guide

## Package position

This guide supports the ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management classroom case. It is designed to be used with:

- `dataset.csv`
- `data_dictionary.md`
- `case_study.md`
- `student_notebook.ipynb`
- `solution.ipynb`
- `expected_output.md`
- `rubric.md`
- `instructions.md`

The teaching goal is not to make students memorize a model. The goal is to make them reason like P&C actuaries facing emerging climate-linked risk: define coverage, translate environmental information into insured-loss variables, model frequency and severity separately, quantify pricing adequacy, stress the portfolio, and choose mitigation under a budget.

## Learning objectives

By the end of the case, students should be able to:

1. Distinguish environmental hazard indicators from qualifying insured triggers.
2. Explain how policy terms, exposure, deductibles, limits, and BI waiting periods affect paid loss.
3. Fit and interpret an exposure-adjusted claim-frequency model.
4. Fit and interpret a conditional severity model.
5. Combine frequency and severity into expected loss and indicated premium.
6. Compare current premium with indicated premium using a premium adequacy ratio.
7. Run baseline, air-stress, water-stress, and compound-stress scenarios.
8. Simulate aggregate annual loss and calculate VaR99 and TVaR99.
9. Choose a mitigation strategy under the 8,000,000 budget using TVaR as the primary criterion.
10. Communicate a practical pricing, underwriting, mitigation, and monitoring recommendation.

## Recommended teaching formats

### Full format: 4.5 to 6 hours

| Segment | Time | Activity |
|---|---:|---|
| Pre-class | 45–60 min | Students read `case_study.md`, `data_dictionary.md`, and inspect the CSV. |
| Launch | 20 min | Instructor introduces AquaAir, coverage logic, scenarios, and committee challenge. |
| Coverage and data walk-through | 40 min | Students verify grain, stress flags, triggers, claims, and policy terms. |
| Frequency model | 45–60 min | Students fit Poisson GLM with exposure offset and interpret rate ratios. |
| Severity model | 45–60 min | Students fit conditional severity model and compare frequency/severity drivers. |
| Pricing | 35–45 min | Students calculate expected loss, indicated premium, and adequacy. |
| Stress testing | 60–75 min | Students run four scenarios and compare expected loss, VaR, and TVaR. |
| Mitigation decision | 60 min | Teams choose a portfolio under budget and defend TVaR-focused choice. |
| Committee debrief | 30–45 min | Teams present recommendations; instructor compares with solution benchmark. |

### Short format: 90 to 120 minutes

Give students the fitted model specification or selected solution cells. Focus on:

1. Coverage interpretation.
2. Baseline premium adequacy.
3. Scenario comparison.
4. VaR/TVaR.
5. Mitigation choice.
6. Final committee recommendation.

### Exam or assignment format

Give `case_study.md`, `dataset.csv`, `data_dictionary.md`, and `student_notebook.ipynb`. Ask students to submit:

1. completed notebook;
2. short Climate Risk Committee memo; and
3. one-page limitation statement.

## Instructor preparation checklist

Before class:

1. Confirm all files are in one folder.
2. Run `data_script.py` once and verify it recreates `dataset.csv`.
3. Open and run `solution.ipynb` from start to finish.
4. Review `expected_output.md` so you know the approximate benchmark numbers.
5. Decide whether students will work individually or in teams.
6. Decide whether you will grade code correctness, actuarial interpretation, or both.
7. Decide whether to disclose that the dataset is synthetic before or after the first descriptive exercise. Recommended: disclose it immediately, but do not disclose the DGP coefficients.

## Suggested class launch script

AquaAir insures hospitals, manufacturing facilities, and food-processing facilities. Management is worried that deteriorating air and water quality may increase claims and create underpriced tail risk. However, the insurance contract does not pay simply because pollution readings are bad. There must be a qualifying insured event, and the amount paid depends on exposure, coverage terms, deductibles, limits, and mitigation.

Your job is to decide whether the current portfolio is adequately priced, how it behaves under air, water, and compound stress, and which mitigation actions should be funded under an 8,000,000 budget.

The committee does not want a perfect academic model. It wants a defensible actuarial decision.

## Core case narrative

The case follows this chain:

Environmental condition → stress flag → qualifying insured trigger → claim count → covered loss → paid loss → premium adequacy → risk decision

The most important student misconception is to jump directly from environmental stress to claims. The dataset deliberately separates:

- `air_stress_flag` from `air_trigger_flag`
- `water_stress_flag` from `water_trigger_flag`
- `compound_trigger_flag` from merely having bad air and bad water readings

Students should learn that exposure and coverage definitions are part of the actuarial model, not administrative details.

## Data-generating process overview

The dataset contains 750 policy-location-year rows: 250 synthetic commercial locations across policy years 2024, 2025, and 2026. The data are deterministic synthetic data generated from `data_script.py` using a fixed seed and SHA-256-derived pseudo-random streams.

The DGP intentionally embeds:

1. location-level region and occupancy structure;
2. policy terms including insured value, deductible, limit, BI waiting period, current premium, and exposure;
3. air and water environmental indicators;
4. climate variables: temperature, rainfall, and drought;
5. environmental stress thresholds;
6. separate probabilistic qualifying insured triggers;
7. exposure-adjusted Poisson claim frequency;
8. Lognormal claim-level severity before financial terms;
9. per-claim deductible and limit application;
10. mitigation effects on frequency and severity;
11. a positive hidden compound-risk mechanism; and
12. a current-premium structure that does not fully price emerging compound environmental risk.

Do not disclose the detailed DGP coefficients to students before they complete the analysis. You may disclose the high-level design after the debrief.

## Hidden DGP teaching explanation

### Frequency mechanism

Claim counts are generated using an exposure-adjusted Poisson structure. The claim rate increases when qualifying air or water triggers occur and increases further under a compound trigger. Occupancy, temperature, drought, rainfall, and mitigation also affect the expected rate. Mitigation reduces frequency, especially when it directly addresses the relevant hazard.

### Severity mechanism

Claim-level ground-up losses are generated using a Lognormal severity structure. Severity depends on occupancy, insured value, trigger type, climate pressure, mitigation, and whether the BI waiting period is met. The deductible and per-claim limit are then applied to produce insurer-paid loss.

### Premium mechanism

Current premium is based on more conventional portfolio rating variables and partial mitigation credits. It does not fully price the hidden compound climate interaction. This creates a realistic teaching tension: some segments may look acceptable historically but inadequate under forward-looking stress.

### Scenario mechanism

The required scenarios transform environmental variables and then recompute stress flags. They do not force every location into claim. This is important: a scenario changes risk conditions, but insurance loss still passes through coverage, exposure, frequency, severity, and financial terms.

## Instructor answer key — conceptual checkpoints

### Checkpoint 1: Data grain

Expected answer: one row is one policy-location-year. There are 750 rows, 250 unique locations, and three years. For annual portfolio simulation, use only 2026 records so the same location is not counted three times.

### Checkpoint 2: Hazard versus claim

Expected answer: environmental stress flags identify adverse conditions. Insured trigger flags represent qualifying covered events. Claims occur only when a qualifying insured trigger exists.

### Checkpoint 3: Frequency model

Expected answer: the model should use `claim_count` as the response and include `log(exposure_years)` as an offset. Students should interpret coefficients as rate ratios. They should include at least one compound-risk term.

### Checkpoint 4: Severity model

Expected answer: severity should be conditional on claims. A reasonable response is `aggregate_paid_loss / claim_count` for rows with claims. A Gamma GLM with log link or Lognormal model is acceptable.

### Checkpoint 5: Pricing

Expected answer: expected loss equals expected frequency multiplied by expected severity. Indicated premium uses fixed expense, variable expense ratio, and profit/contingency. Premium adequacy below 1 indicates underpricing.

### Checkpoint 6: Stress testing

Expected answer: run baseline, air stress, water stress, and compound stress. Recompute stress flags after scenario transformations. Compare expected loss, indicated premium, VaR99, and TVaR99.

### Checkpoint 7: Mitigation

Expected answer: choose a feasible portfolio under 8,000,000. The primary selection criterion is lowest TVaR99, not highest benefit-cost ratio. Students should also report expected-loss reduction and premium adequacy after mitigation.

## Common misconceptions and corrections

| Misconception | Correction |
|---|---|
| Bad environmental readings are claims. | They are hazard indicators. Claims require qualifying insured triggers. |
| Use all 750 rows for one annual portfolio simulation. | Fit models on all rows, but use 2026 as the current annual portfolio snapshot. |
| Ignore exposure because all policies are roughly annual. | Exposure varies and should be included as an offset in frequency modelling. |
| Model aggregate loss directly and skip frequency/severity. | The case objective is to teach frequency-severity decomposition. |
| Use paid loss for rows with zero claims in severity model. | Conditional severity should use claim-positive rows only. |
| The highest BCR mitigation is automatically best. | The decision criterion is lowest TVaR99 under budget. BCR is supporting evidence. |
| Compound stress equals air stress plus water stress. | Compound risk can interact nonlinearly. |
| Current premium is the right answer because it is in the data. | It is a baseline market/current rating value; the task is to test adequacy. |
| A statistically insignificant coefficient is irrelevant. | With synthetic classroom data, focus on actuarial direction, materiality, and model purpose. |
| One model output is enough for management. | Management needs expected loss, tail risk, adequacy, mitigation impact, and limitations. |

## Discussion prompts

Use these during the debrief:

1. What exactly converts an environmental hazard into an insured loss?
2. Which variable did your model treat as most important for frequency?
3. Which variable did your model treat as most important for severity?
4. Did frequency and severity have the same drivers?
5. Which scenario produced the largest expected loss?
6. Which scenario produced the largest TVaR?
7. Why might a strategy with high expected-loss reduction fail to reduce TVaR enough?
8. Would you recommend repricing, mandatory mitigation, coverage sublimits, monitoring, or risk selection?
9. What would you tell a regulator or board member about limitations?
10. What real-world data would AquaAir need before deploying this framework?

## Expected modelling choices

Acceptable baseline choices:

- Poisson GLM for frequency with log exposure offset.
- Gamma GLM with log link for average paid severity.
- Claim-count weights for severity rows.
- Frequency-severity expected loss calculation.
- Monte Carlo simulation for aggregate annual paid loss.
- VaR99 and TVaR99 from the simulated aggregate distribution.
- Scenario transformations exactly as stated in the case document.
- Greedy or manageable candidate-portfolio mitigation search, provided it is documented and budget-constrained.

Do not penalize students for not matching every numerical result exactly if their approach is defensible, reproducible, and aligned with the case logic. Use `expected_output.md` as a benchmark range rather than a rigid answer key, except for basic data validation numbers.

## Recommended debrief sequence

1. Ask teams to explain the coverage chain before showing numerical results.
2. Show the stress-versus-trigger counts to reinforce the central misconception.
3. Compare frequency model choices.
4. Compare severity model choices.
5. Put scenario expected loss and TVaR side by side.
6. Ask whether compound stress is merely additive.
7. Compare mitigation portfolios and highlight difference between BCR and TVaR optimization.
8. End with committee recommendations and limitations.

## Instructor grading emphasis

Strong submissions will:

- preserve the coverage distinction throughout;
- use exposure correctly;
- fit separate frequency and severity models;
- calculate pricing metrics correctly;
- compare all four scenarios;
- simulate aggregate loss with a fixed seed;
- choose mitigation under budget based on TVaR99;
- communicate results in actuarial language; and
- state limitations clearly.

Weak submissions usually fail because they treat environmental stress as claims, ignore exposure, use all three years as a single portfolio, skip severity modelling, select mitigation only by BCR, or present code without a business recommendation.

## Optional extensions

If time permits, advanced students may explore:

1. Negative Binomial frequency model.
2. Alternative severity distribution.
3. Model validation and train/test split.
4. Segment-level underwriting actions.
5. Alternative budgets.
6. Alternative VaR/TVaR confidence levels.
7. Sensitivity to Monte Carlo simulation count.
8. Parameter uncertainty.
9. Simple reinsurance layer.
10. Credibility or Bayesian updating.

These are extensions only. They should not replace the core case.
