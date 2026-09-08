# ClimateTwin Student Case: Air–Water Climate Risk at AquaAir General Insurance

## 1. Your role

You are part of the Pricing and Climate Risk Team at AquaAir General Insurance, a fictional P&C insurer. AquaAir writes commercial property and business interruption coverage with a simplified Environmental Impairment Endorsement for:

- hospitals;
- manufacturing facilities; and
- food-processing facilities.

Management is concerned that deteriorating air and water conditions may be changing claim frequency, claim severity, premium adequacy, and portfolio tail risk.

Your task is to move through the ClimateTwin decision cycle:

Observe → Model → Price → Stress → Mitigate → Reprice

Your final deliverable is a short recommendation to the Climate Risk Committee supported by your notebook results.

## 2. The central insurance principle

A bad environmental reading is not automatically an insurance claim.

Use the following chain throughout the case:

Climate conditions → Environmental hazard → Exposure and vulnerability → Defined insured trigger → Claim frequency and severity → Policy terms → Insurer-paid loss → Pricing and risk decision

The case is designed to test whether you can translate environmental information into an actuarially meaningful insured-loss mechanism.

## 3. Portfolio and data

You are given `dataset.csv`, containing:

- 750 policy-location-year observations;
- 250 synthetic insured locations;
- policy years 2024–2026;
- five synthetic regions;
- three occupancy classes;
- policy financial terms;
- air- and water-quality indicators;
- selected climate variables;
- mitigation status;
- claim count; and
- aggregate ground-up, covered, and insurer-paid losses.

For model fitting, use all three years. For annual portfolio risk and scenario simulation, treat the 2026 records as the current portfolio snapshot so that the same insured location is not counted three times in one simulated year.

## 4. Simplified coverage architecture

### 4.1 Air-quality insured event

An air-related covered event requires:

1. adverse air-quality conditions under the case definition; and
2. a qualifying operational restriction, temporary closure, filtration/remediation response, or covered extra-expense/business-interruption consequence.

### 4.2 Water-quality insured event

A water-related covered event requires:

1. adverse water-quality conditions under the case definition; and
2. a qualifying cleanup, treatment, repair, extra-expense, or business-interruption consequence.

### 4.3 Compound insured event

A compound event occurs when qualifying air and water triggers affect the same insured location within the policy year.

The case does not assume that compound risk is simply the sum of standalone air and water risk.

### 4.4 Environmental screening thresholds

The dataset uses transparent teaching thresholds:

- Air stress: `pm25 >= 35` or `ozone >= 70`
- Water stress: `turbidity >= 5` or `water_quality_index <= 60`

The stress flags identify adverse environmental conditions only. They are not claims.

### 4.5 Policy terms

The dataset includes:

- insured value;
- per-claim policy limit;
- per-claim deductible;
- BI waiting period;
- exposure years;
- current premium; and
- mitigation status.

For a simulated covered claim:

`paid_loss = min(max(covered_loss - deductible, 0), policy_limit)`

The historical CSV already contains the resulting aggregate annual insurer-paid loss.

### 4.6 Core exclusions and simplifications

The core case excludes:

- workers compensation and employee health claims;
- third-party bodily injury and environmental liability;
- gradual pollution without a defined insured trigger;
- losses outside the endorsement event definition;
- intentional/known non-compliance;
- mold and other long-latency contamination;
- uninsured BI shutdowns below the waiting-period condition; and
- amounts above the policy limit.

Do not add advanced spatial dependence, copulas, credibility, reinsurance, or adaptive optimization to the required core solution.

## 5. Management assumptions for ratemaking

Use the following simplified pricing assumptions:

- Fixed expense: 750 currency units per exposure-year
- Variable expense ratio: 25%
- Profit / contingency provision: 5%

Calculate:

`Indicated Premium = (Expected Loss + 750 × Exposure) / (1 - 0.25 - 0.05)`

and:

`Premium Adequacy Ratio = Current Premium / Indicated Premium`

An adequacy ratio below 1.00 indicates that current premium is insufficient under the model/scenario assumptions.

## 6. Required four scenarios

Use exactly these four core scenarios.

| Scenario | Air transformation | Water transformation |
|---|---|---|
| Baseline | No change | No change |
| Air stress | PM2.5 + 15 µg/m³; ozone + 10 ppb | No change |
| Water stress | No change | Turbidity × 1.60; WQI − 15 |
| Compound stress | Apply air stress | Apply water stress |

After each transformation, recompute the environmental stress flags from the case thresholds.

Do not simply force every stressed location to become a claim.

## 7. Required actuarial analysis

### Stage 1 — Observe: coverage and portfolio understanding

1. Confirm the dataset grain, years, occupancies, regions, exposure, and claims.
2. Verify that adverse environmental readings and insured triggers are different concepts.
3. Summarize claim frequency and paid severity by region and occupancy.
4. Identify any obvious portfolio concentrations or unusual patterns.

Required output: a concise descriptive table and at least one useful visualization.

### Stage 2 — Model: exposure-adjusted frequency

Fit an actuarial count model for `claim_count`.

Minimum requirements:

- use a Poisson GLM or another justified count model;
- incorporate `log(exposure_years)` as an offset;
- include occupancy and selected environmental/climate/mitigation variables;
- include an air–water interaction or other explicit way to test compound risk;
- interpret the important effects rather than reporting coefficients only.

Required output: fitted frequency model, selected coefficient/rate-ratio interpretation, and expected claim count.

### Stage 3 — Model: conditional severity

For observations with claims, model insurer-paid severity conditional on claim occurrence.

A practical response is:

`average_paid_severity = aggregate_paid_loss / claim_count`

Minimum requirements:

- use a positive severity model such as Gamma GLM with log link or a defensible Lognormal model;
- include insured value, occupancy, environmental state/compound effect, and mitigation variables;
- explain which factors affect severity and whether those factors are the same as frequency drivers.

Required output: fitted conditional severity model and interpretation.

### Stage 4 — Price: expected loss cost and indicated premium

Combine frequency and severity predictions:

`Expected Loss = Expected Claim Count × Expected Conditional Severity`

Calculate for the 2026 current portfolio:

- expected annual loss;
- expected loss cost per exposure-year;
- indicated premium;
- current premium;
- premium adequacy ratio.

Also summarize premium adequacy by at least one meaningful segment such as region or occupancy.

### Stage 5 — Stress: aggregate annual loss, VaR and TVaR

For each of the four scenarios:

1. transform the environmental variables;
2. recompute stress flags;
3. use the fitted models to estimate scenario frequency and severity;
4. simulate annual aggregate portfolio loss;
5. calculate:
   - expected annual loss;
   - indicated premium;
   - premium adequacy ratio;
   - VaR at 99%; and
   - TVaR at 99%.

Use a reproducible random seed and enough Monte Carlo simulations for stable classroom results.

`TVaR_99 = mean(loss | loss >= VaR_99)`

Required output: one scenario comparison table and one loss-distribution/tail-risk visualization.

### Stage 6 — Mitigate: constrained resilience decision

AquaAir has a Climate Resilience Budget of 8,000,000 currency units.

Candidate actions are:

- install enhanced air filtration where absent;
- install enhanced water treatment where absent;
- implement a business continuity plan where absent.

Upgrade costs are provided in the dataset.

Your primary decision criterion is:

Choose a feasible mitigation portfolio within the budget that produces the lowest simulated TVaR at 99%.

You must also report:

- total mitigation cost;
- expected-loss reduction;
- benefit-cost ratio;
- VaR reduction;
- TVaR reduction; and
- post-mitigation premium adequacy.

Do not choose the mitigation portfolio solely from expected-loss reduction divided by cost. A strategy can look efficient on average while leaving the severe tail largely unchanged.

You may compare a manageable set of defensible candidate portfolios/strategies rather than solve a large-scale exact optimization problem.

## 8. Guiding questions

1. What must happen for an adverse environmental observation to become a covered claim?
2. Which variables most strongly affect exposure-adjusted claim frequency?
3. Which variables most strongly affect conditional severity?
4. Do frequency and severity respond to the same variables?
5. Which occupancy has the highest expected loss cost after allowing for exposure?
6. Is the current 2026 portfolio adequately priced under baseline conditions?
7. Which standalone stress creates the largest increase in expected loss?
8. Which scenario creates the largest increase in TVaR?
9. Is compound stress materially different from looking at air and water stress separately?
10. Which regions or occupancies contribute most to expected loss?
11. Which mitigation portfolio gives the best tail-risk outcome within the 8,000,000 budget?
12. Would your decision change if you looked only at benefit-cost ratio?
13. After mitigation, should AquaAir reprice, alter terms, restrict capacity, require mitigation, or monitor?
14. What model assumptions and limitations should management understand?

## 9. Final Climate Risk Committee deliverable

At the end of the notebook, prepare a concise committee recommendation containing:

1. Baseline position — expected loss, indicated premium, adequacy, VaR and TVaR.
2. Most material climate stress — identify the scenario and quantify the change.
3. Mitigation decision — selected actions/portfolio, cost, and financial/tail-risk effect.
4. Pricing/underwriting action — recommend one or more of: Maintain / Reprice / Mitigate / Restrict / Monitor.
5. Limitations — state at least three assumptions or limitations.

The goal is not to find a single “magic model.” The goal is to make a defensible P&C actuarial decision from an evolving environmental state.

---

## 10. Suggested time

### Full case

- Pre-class reading/data review: 45–60 minutes
- In-class coverage and baseline: 60 minutes
- In-class frequency/severity/pricing: 75 minutes
- In-class stress testing/tail risk: 75 minutes
- In-class mitigation/committee decision: 60 minutes
- Independent final memo: 60–90 minutes

### Short one-session version

If fitted frequency and severity models are supplied by the instructor, focus on:

1. coverage interpretation;
2. baseline pricing;
3. four scenarios;
4. VaR/TVaR;
5. mitigation under budget; and
6. committee recommendation.

## 11. Reproducibility and submission

- Keep `dataset.csv` in the same folder as the notebook.
- Use a fixed random seed for simulation.
- Do not modify the original CSV.
- Clearly label assumptions and transformations.
- Submit the completed notebook and the requested committee recommendation.

All data, regions, policies, environmental measurements, premiums, claims, and losses in this case are synthetic and for teaching purposes only.
