# ClimateTwin Synthetic Dataset — Data Dictionary

## Purpose

`dataset.csv` is the student-facing synthetic portfolio for **ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management**. It contains **750 policy-location-year observations**: 250 synthetic commercial locations observed for policy years 2024–2026.

Each record represents one insured location for one policy year for AquaAir General Insurance. The data are entirely synthetic and are designed for teaching frequency-severity modelling, ratemaking, stress testing, aggregate-loss simulation, VaR/TVaR, premium adequacy, and mitigation decisions.

A crucial coverage principle is embedded in the data:

> **Environmental deterioration alone is not an insurance claim.**

`air_stress_flag` and `water_stress_flag` indicate adverse environmental conditions. A covered claim can arise only when a qualifying insured trigger is also present (`air_trigger_flag` and/or `water_trigger_flag`). This lets students distinguish **hazard → insured trigger → claim → policy payment**.

## Dataset grain and keys

- **Rows:** 750
- **Unique locations:** 250
- **Policy years:** 2024, 2025, 2026
- **Grain:** one insured location × one policy year
- **Unique row key:** `policy_id`
- **Repeated-location key:** `location_id`

## Variables

| Variable | Type | Unit / Allowed values | Student-facing meaning |
|---|---|---|---|
| `policy_id` | string | `POL###-YYYY` | Unique policy-location-year identifier. |
| `location_id` | string | `LOC001`–`LOC250` | Synthetic insured location identifier. Repeats across years. |
| `year` | integer | 2024, 2025, 2026 | Policy year. |
| `region` | category | Northgate; Riverbend; Central Metro; Coastview; Drylands | Synthetic geographic region used to create different environmental and portfolio conditions. |
| `occupancy` | category | Hospital; Manufacturing; Food Processing | Commercial occupancy class. |
| `exposure_years` | float | 0.680–1.000 | Earned exposure in policy-years. Use as the exposure denominator or count-model offset. |
| `insured_value` | integer | currency units | Total insured value for the location. Synthetic monetary values use a generic currency unit. |
| `policy_limit` | integer | currency units | Maximum insurer payment **per claim** after the deductible is applied. |
| `deductible` | integer | currency units | Amount retained by the insured **per claim** before insurer payment. |
| `bi_waiting_period_days` | integer | 1, 2, 3 | Business-interruption waiting period in days. |
| `current_premium` | integer | currency units | Current annual premium charged for the observed exposure. It intentionally does not fully price all emerging climate interactions. |
| `pm25` | float | µg/m³ | Annual/representative PM2.5 air-quality indicator used in the case. |
| `ozone` | float | ppb | Representative ozone indicator. |
| `turbidity` | float | NTU | Water turbidity indicator. |
| `water_quality_index` | float | 0–100 style index; higher is better | Synthetic water-quality index. Lower values indicate worse water quality. |
| `temperature_c` | float | °C | Representative annual temperature condition. |
| `annual_rainfall_mm` | float | mm/year | Synthetic annual rainfall. |
| `drought_indicator` | float | 0–1 | Synthetic drought-pressure index. Higher values indicate greater drought pressure. |
| `air_stress_flag` | binary | 0, 1 | 1 when PM2.5 ≥ 35 µg/m³ **or** ozone ≥ 70 ppb. This indicates adverse air conditions, not automatically a claim. |
| `water_stress_flag` | binary | 0, 1 | 1 when turbidity ≥ 5 NTU **or** water-quality index ≤ 60. This indicates adverse water conditions, not automatically a claim. |
| `air_trigger_flag` | binary | 0, 1 | 1 when adverse air conditions also produce a qualifying insured operational/remediation trigger under the simplified teaching contract. |
| `water_trigger_flag` | binary | 0, 1 | 1 when adverse water conditions also produce a qualifying insured operational/remediation trigger. |
| `compound_trigger_flag` | binary | 0, 1 | 1 when both air and water insured triggers occur for the same location-year. |
| `insured_trigger_type` | category | None; Air; Water; Compound | Convenient classification of the qualifying insured trigger(s). |
| `bi_waiting_period_met_flag` | binary | 0, 1 | Whether the qualifying event duration meets the BI waiting-period condition. A trigger can still generate covered remediation/extra-expense loss even if the BI waiting period is not met. |
| `air_filtration` | binary | 0, 1 | 1 if enhanced air-filtration mitigation is already installed. |
| `water_treatment` | binary | 0, 1 | 1 if enhanced water-treatment mitigation is already installed. |
| `business_continuity_plan` | binary | 0, 1 | 1 if a formal business-continuity plan is in place. |
| `air_filtration_upgrade_cost` | integer | currency units; 0 if already installed | Prospective implementation cost used for the mitigation decision exercise. |
| `water_treatment_upgrade_cost` | integer | currency units; 0 if already installed | Prospective water-treatment upgrade cost. |
| `bcp_upgrade_cost` | integer | currency units; 0 if already in place | Prospective business-continuity-plan implementation cost. |
| `claim_count` | integer | 0, 1, 2, ... | Number of covered claims during the location-year. Claims can occur only when at least one insured trigger is present. |
| `aggregate_ground_up_loss` | float | currency units | Sum of claim-level losses before deductible and policy-limit application. |
| `aggregate_covered_loss` | float | currency units | Sum of covered claim amounts before deductible and policy-limit application. In this first-release teaching contract it equals ground-up covered event loss; the separate field is retained to teach the distinction and support later extensions. |
| `aggregate_paid_loss` | float | currency units | Sum of insurer-paid claim amounts after applying the deductible and per-claim policy limit. |

## Core coverage thresholds

The student case uses the following transparent environmental screening thresholds:

- **Air stress:** `pm25 >= 35` **or** `ozone >= 70`
- **Water stress:** `turbidity >= 5` **or** `water_quality_index <= 60`

These thresholds identify adverse environmental conditions only. They are intentionally separated from the insured trigger fields so that a high pollution/contamination reading does not automatically become an insurance loss.

## Loss definitions

For each simulated covered claim:

1. **Ground-up loss** is the loss before policy financial terms.
2. **Covered loss** is the amount within the simplified defined insured event. In version 1, the full simulated event loss is treated as covered before financial terms.
3. **Paid loss** is calculated per claim as:

```text
paid_loss = min(max(covered_loss - deductible, 0), policy_limit)
```

The CSV stores annual aggregates of these claim-level amounts.

## Recommended actuarial use

### Frequency

Use `claim_count` as the response and `exposure_years` as the exposure measure. A Poisson or Negative Binomial GLM can use `log(exposure_years)` as an offset.

Potential explanatory variables include occupancy, region, air/water indicators, climate variables, trigger type, and mitigation indicators.

### Conditional severity

For observations with `claim_count > 0`, model a severity response such as:

```text
aggregate_paid_loss / claim_count
```

or use the supplied solution notebook's claim-level approximation. Appropriate positive severity families include Gamma or Lognormal models.

### Expected loss cost

A standard frequency-severity construction is:

```text
Expected Loss = Expected Claim Count × Expected Severity
Loss Cost per Exposure = Expected Loss / Exposure
```

### Indicated premium

The classroom package should use the following simplified assumptions unless the instructor changes them:

- **Fixed expense per exposure-year:** 750
- **Variable expense ratio:** 25%
- **Profit / contingency provision:** 5%

Thus:

```text
Indicated Premium =
(Expected Loss + 750 × Exposure)
/
(1 - 0.25 - 0.05)
```

### Premium adequacy

```text
Adequacy Ratio = Current Premium / Indicated Premium
```

An adequacy ratio below 1.00 indicates underpricing under the scenario assumptions.

## Core stress-scenario rules

These transformations are intended for the baseline notebook and are applied to the environmental state before re-estimating/simulating risk.

| Scenario | Air transformation | Water transformation | Additional teaching assumption |
|---|---|---|---|
| Baseline | observed values | observed values | No change |
| Air stress | PM2.5 + 15 µg/m³; ozone + 10 ppb | unchanged | Higher chance of qualifying air triggers |
| Water stress | unchanged | turbidity × 1.60; WQI − 15 points | Higher chance of qualifying water triggers |
| Compound stress | apply both air and water transformations | apply both | Include a non-zero compound interaction in frequency/severity |

The scenario notebook should recompute stress and trigger probabilities from the stressed environmental variables rather than simply switching every location to a claim state.

## Mitigation exercise

The three status variables show mitigation already present. The three upgrade-cost fields represent the cost of adding missing mitigation.

For the core decision exercise, teams should compare candidate mitigation sets under a fixed **Climate Resilience Budget** and select a portfolio that minimizes simulated `TVaR_99`, while also reporting:

- expected-loss reduction;
- benefit-cost ratio;
- VaR reduction;
- TVaR reduction; and
- post-mitigation premium adequacy.

A recommended initial classroom budget is **8,000,000 currency units**, but the instructor may change it.

## Instructor-only data-generating process

The public/student dataset does **not** reveal the exact hidden relationships. The accompanying `data_script.py` is instructor-only and documents them explicitly.

The generator intentionally embeds:

- an exposure-adjusted Poisson claim-frequency mechanism;
- higher frequency for qualifying air and water triggers;
- an additional positive compound air–water interaction;
- occupancy effects;
- climate contributions from temperature, drought, and rainfall;
- lower frequency when relevant mitigation is present;
- claim-level Lognormal severity;
- severity effects from insured value, occupancy, trigger type, compound risk, climate, and mitigation;
- per-claim deductible and limit application;
- conventional current-premium rating that does not fully reflect the hidden compound environmental interaction; and
- random variation sufficient to prevent the intended conclusions from being visually obvious.

The exact coefficients are contained in `data_script.py` so instructors can know the expected direction of effects while students still have to discover them empirically.
