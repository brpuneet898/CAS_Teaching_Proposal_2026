# ClimateTwin V2 Student Case: Air–Water Climate Risk at AquaAir General Insurance

## 1. Your role

You are part of the Pricing and Climate Risk Team at AquaAir General Insurance, a fictional P&C insurer. AquaAir writes commercial property and business interruption (BI) coverage with a simplified Environmental Impairment Endorsement for hospitals, manufacturing facilities, and food-processing facilities.

Management is concerned that deteriorating air and water conditions may change claim frequency, claim severity, premium adequacy, and portfolio tail risk. Your task is to move through the ClimateTwin decision cycle:

**Observe → Model → Price → Stress → Mitigate → Reprice**

Your final deliverable is a short recommendation to the Climate Risk Committee supported by your notebook results.

---

## 2. The central insurance principle

A bad environmental reading is **not automatically an insurance claim**.

Use this chain throughout the case:

**Climate conditions → environmental hazard → exposure/vulnerability → insured trigger → claim frequency and severity → coverage and policy terms → insurer-paid loss → pricing/risk decision**

The case is designed to test whether you can translate environmental information into an actuarially meaningful insured-loss mechanism.

---

## 3. Portfolio and data

The student-facing `dataset.csv` contains:

- exactly 750 policy-location-year observations;
- 250 synthetic insured locations;
- policy years 2024–2026;
- five synthetic regions;
- three occupancy classes;
- exposure, insured value, deductible, per-claim policy limit, and BI waiting period;
- air, water, and climate variables;
- mitigation status and prospective upgrade costs;
- claim counts; and
- annual ground-up, covered, and insurer-paid losses.

For model fitting, use all three years. For annual portfolio risk and scenario simulation, use the **2026** rows as the current portfolio snapshot so the same location is not counted three times in one simulated year.

The instructor package also contains `claim_level_data.csv`, generated from the same V2 data-generating process. The reference solution uses that table to audit claim-level contract mechanics and to model strictly positive covered severity. The student notebook uses the annual table for a classroom-friendly severity approximation unless your instructor supplies the claim-level table.

---

## 4. Simplified coverage architecture

### 4.1 Environmental screening thresholds

The case uses transparent screening rules:

- **Air stress:** `pm25 >= 35` **or** `ozone >= 70`
- **Water stress:** `turbidity >= 5` **or** `water_quality_index <= 60`

These flags identify adverse environmental states only. They are **not** claim indicators.

### 4.2 Insured triggers

An air or water claim can arise only if the adverse environmental state also produces a qualifying insured operational/remediation trigger under the teaching contract. A location-year with no insured trigger has zero claim frequency in the V2 DGP.

A compound state occurs when qualifying air and water triggers are both active for the same policy-location-year. Compound risk is not assumed to equal the simple sum of standalone air and water risk.

### 4.3 Exact claim payment order

For every claim, the contract calculations occur in this order:

1. Generate **ground-up remediation / extra-expense loss**.
2. Generate **ground-up BI loss** from interruption duration and daily BI loss.
3. Apply the BI waiting period **only to the BI component**.
4. Form **covered loss** as remediation/extra expense plus BI remaining after the waiting period.
5. Apply the **deductible exactly once to total covered loss**.
6. Apply the **per-claim policy limit**.

The formulas are:

```text
ground_up_bi_loss = daily_bi_loss × interruption_days

covered_bi_days = max(interruption_days - bi_waiting_period_days, 0)
covered_bi_loss = daily_bi_loss × covered_bi_days

ground_up_loss = remediation_loss + ground_up_bi_loss
covered_loss   = remediation_loss + covered_bi_loss

loss_after_deductible = max(covered_loss - deductible, 0)
paid_loss = min(loss_after_deductible, policy_limit)
```

Therefore a valid claim can have **positive covered loss but zero insurer payment** when the covered amount is at or below the deductible.

### 4.4 Three worked insurance examples

These examples use exactly the same calculation order implemented in the V2 generator and the solution notebook.

| Example | Inputs | Result |
|---|---|---|
| **A. Loss below deductible** | Remediation = 20,000; BI = 0; deductible = 50,000; limit = 500,000 | Covered loss = 20,000; after deductible = 0; **paid loss = 0** |
| **B. Payment constrained by policy limit** | Remediation = 900,000; BI = 0; deductible = 50,000; limit = 400,000 | After deductible = 850,000; **paid loss = 400,000** |
| **C. BI waiting period not met, but another covered cost remains payable** | Remediation = 100,000; daily BI = 30,000; interruption = 2 days; waiting period = 3 days; deductible = 50,000; limit = 500,000 | Ground-up BI = 60,000; covered BI = 0; covered loss = 100,000; **paid loss = 50,000** |

Example C is important: failing the BI waiting-period condition removes the BI portion, but it does **not** automatically eliminate otherwise eligible remediation or extra-expense loss.

### 4.5 Core exclusions and simplifications

The core case excludes workers compensation and employee health claims; third-party bodily injury/environmental liability; gradual pollution without a defined trigger; mold and other long-latency contamination; intentional/known non-compliance; losses outside the endorsement definition; BI days within the waiting period; and amounts above the per-claim policy limit.

---

## 5. Severity modelling rule

Do **not** fit a Gamma model to insurer-paid severity if zero-paid claims are present.

For the student-facing annual table, define a strictly positive response only for policy-years with claims:

```text
average_covered_severity = aggregate_covered_loss / claim_count
```

For the instructor/reference implementation, the preferred claim-level response is:

```text
claim_level_data.csv -> covered_loss
```

`covered_loss` is strictly positive by construction. Payment is handled separately through the deductible and limit. If paid severity itself were modelled directly, a two-part/hurdle model or conditioning on positive payment would be required.

---

## 6. Management assumptions for ratemaking

Use:

- fixed expense = **750 currency units per exposure-year**;
- variable expense ratio = **25%**;
- profit/contingency provision = **5%**.

```text
Indicated Premium =
(Expected Paid Loss + 750 × Exposure)
/
(1 - 0.25 - 0.05)
```

```text
Premium Adequacy Ratio = Current Premium / Indicated Premium
```

A ratio below 1.00 indicates underpricing under the stated model/scenario assumptions.

---

## 7. Four required scenarios

Use exactly these four scenarios on the same 2026 portfolio.

| Scenario | Air transformation | Water transformation |
|---|---|---|
| **Baseline** | Observed PM2.5 and ozone | Observed turbidity and WQI |
| **Air stress** | `PM2.5 + 15`; `ozone + 10` | Unchanged |
| **Water stress** | Unchanged | `turbidity × 1.60`; `WQI - 15` |
| **Compound stress** | Apply air stress | Apply water stress |

After transformation, recompute the environmental stress flags. Do **not** simply force every stressed location to become a claim.

The V2 generator uses common random numbers for scenario comparisons and adds non-additivity under compound stress when both insured triggers are active.

### Compound-scenario limitation

In the V2 DGP, air-trigger and water-trigger draws are **conditionally independent given the simulated covariates**. Non-additivity is introduced through an explicit compound frequency interaction and compound severity multiplier once both triggers are active. The core simulator does **not** contain a copula, latent common shock, or spatial dependence process. State this limitation when interpreting compound-tail results.

---

## 8. Required actuarial analysis

### Stage 1 — Observe

Confirm the dataset grain and exposure; compare hazard flags with insured triggers; summarize claims/losses by region and occupancy; and identify meaningful concentrations.

**Required output:** concise table + at least one useful visualization + interpretation.

### Stage 2 — Exposure-adjusted frequency

Fit a Poisson GLM (or justify an alternative) for `claim_count` with `log(exposure_years)` as an offset. Use environmental, occupancy, region, climate, and mitigation variables. Include an explicit air–water stress interaction or equivalent compound-risk feature.

Report a dispersion diagnostic and interpret selected rate ratios.

**Do not use the insured-trigger flags as the only frequency predictors.** They are primarily coverage-audit variables and are too close to the DGP claim gate.

### Stage 3 — Conditional covered severity

Using claim-positive policy-years, model:

```text
average_covered_severity = aggregate_covered_loss / claim_count
```

with a positive model such as Gamma-log or a defensible Lognormal model. Include insured value, occupancy, environmental/climate state, mitigation, and BI waiting-period information as appropriate.

Explain why covered severity—not zero-including paid severity—is being used for the positive model.

### Stage 4 — Price

For the 2026 portfolio, combine expected claim count with expected covered severity. Convert simulated covered claim losses to insurer-paid losses by applying the deductible once and then the per-claim policy limit.

Report expected paid loss, loss cost per exposure, indicated premium, current premium, and premium adequacy.

### Stage 5 — Stress and tail risk

For each scenario, estimate the annual paid-loss distribution and report:

- expected annual paid loss;
- indicated premium;
- premium adequacy ratio;
- `VaR_99`; and
- `TVaR_99`.

Use reproducible Monte Carlo simulation. The helper functions in the notebook handle routine simulation mechanics so your work should focus on assumptions, interpretation, comparison, diagnostics, and decision-making.

Because TVaR is simulation-sensitive, assess Monte Carlo uncertainty with multiple seeds or repeated runs. Do not over-interpret tiny TVaR differences whose uncertainty intervals overlap materially.

### Stage 6 — Candidate mitigation decision

AquaAir has a **Climate Resilience Budget of 8,000,000** currency units.

Candidate actions are:

- install enhanced air filtration where absent;
- install enhanced water treatment where absent;
- implement a business continuity plan where absent.

Evaluate a **finite, defensible set of feasible candidate portfolios**. Report:

- total cost;
- expected-loss reduction;
- benefit-cost ratio;
- VaR reduction;
- TVaR reduction;
- post-mitigation premium adequacy; and
- Monte Carlo uncertainty around TVaR.

Your conclusion must use language such as:

> “Among the feasible candidate portfolios evaluated under the stated budget, Strategy X had the lowest estimated TVaR99.”

Do **not** state that this proves a global optimum over every possible mitigation allocation.

---

## 9. Guiding questions

1. What must happen for an adverse environmental reading to become a covered claim?
2. Why can a valid covered claim have zero insurer payment?
3. Which variables most strongly affect exposure-adjusted frequency?
4. Which variables most strongly affect covered severity?
5. Do frequency and severity respond to the same factors?
6. Is the current 2026 portfolio adequately priced at baseline?
7. Which standalone stress changes expected paid loss most?
8. Which scenario changes TVaR most?
9. Is the compound scenario materially different from considering the standalone stresses separately?
10. Which segments contribute most to expected loss and tail risk?
11. Which evaluated feasible mitigation candidate has the lowest estimated TVaR within budget?
12. Is that ranking stable across simulation seeds?
13. Would your recommendation change if you looked only at expected-loss benefit-cost ratio?
14. After mitigation, should AquaAir maintain, reprice, mitigate, restrict, or monitor?
15. What assumptions and limitations should management understand?

---

## 10. Final Climate Risk Committee deliverable

Prepare a concise committee recommendation containing:

1. **Baseline position:** expected paid loss, indicated premium, adequacy, VaR, and TVaR.
2. **Most material stress:** identify the scenario and quantify the change.
3. **Mitigation decision:** identify the best-performing candidate among those evaluated, its cost, expected-loss effect, tail-risk effect, and ranking uncertainty.
4. **Pricing/underwriting action:** recommend Maintain / Reprice / Mitigate / Restrict / Monitor, with rationale.
5. **Limitations:** state at least three, including the conditional-independence limitation of the compound DGP.

---

## 11. Suggested time and prerequisites

### Prerequisites

Students should be comfortable with:

- basic P&C frequency/severity concepts;
- GLM interpretation at an introductory level;
- expected loss and premium indication;
- basic Python/pandas notebook use; and
- VaR/TVaR definitions.

No prior climate modelling, copula modelling, or optimization coursework is required.

### Full case

- Pre-class reading/data review: 45–60 minutes
- Coverage and baseline: 60 minutes
- Frequency/severity/pricing: 75 minutes
- Stress testing/tail risk: 75 minutes
- Mitigation/committee decision: 60 minutes
- Independent memo: 60–90 minutes

### Two-hour version

A separate short-version notebook should supply fitted models or selected completed cells. The two-hour class should focus on coverage interpretation, baseline pricing, four-scenario comparison, VaR/TVaR, mitigation choice among supplied candidate portfolios, and committee communication—not routine simulation coding.

---

## 12. Reproducibility and submission

- Keep `dataset.csv` in the same folder as the student notebook.
- Do not modify the original CSV.
- Use the supplied helper functions rather than rebuilding routine Monte Carlo machinery.
- Use reproducible seeds and report the simulation count.
- Clearly label assumptions and scenario transformations.
- Submit the completed notebook and Climate Risk Committee recommendation.

All data, regions, policies, environmental measurements, premiums, claims, and losses are synthetic and for teaching purposes only.
