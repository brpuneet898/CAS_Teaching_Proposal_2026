# ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management

### Proposed Teaching Material for the CAS Global Teaching Materials Innovation Challenge 2026

## 1. Project Title and Summary

ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management

ClimateTwin is a compact, scenario-based actuarial case in which students act as the pricing and risk team for AquaAir General Insurance, a fictional insurer writing commercial property and business interruption coverage with a defined environmental impairment endorsement for hospitals, manufacturing facilities, and food-processing facilities.

The case focuses on one practical question: How should an insurer translate deteriorating air and water conditions into defensible frequency, severity, pricing, tail-risk, and mitigation decisions for a commercial portfolio?

Students work with a synthetic policy-location-year dataset and a ready-to-run notebook. They estimate exposure-adjusted claim frequency and conditional claim severity, calculate expected loss cost and indicated premium, simulate aggregate annual portfolio loss, measure VaR and TVaR, test premium adequacy under climate stress, and evaluate the financial value of mitigation.

The core case is deliberately limited to four scenarios:

1. Baseline conditions
2. Air-quality stress
3. Water-quality stress
4. Compound air–water stress

The teaching cycle is:

Observe → Model → Price → Stress → Mitigate → Reprice

Advanced topics such as spatial models, copulas, alternative dependence structures, and adaptive optimization are retained only as optional extensions. The first release is therefore designed as a minimum viable classroom package that can be executed, taught, assessed, and piloted, rather than as a broad conceptual climate-risk framework.

## 2. Insurance Setting and Coverage Architecture

### 2.1 Portfolio

Students receive a synthetic portfolio of approximately 750 policy-location-year records covering three commercial occupancies:

- hospitals;
- manufacturing facilities; and
- food-processing facilities.

Policies are distributed across several synthetic regions with different environmental conditions, insured values, policy structures, and mitigation characteristics. Each record represents one insured location for one policy year.

The instructional portfolio is not intended to reproduce any specific insurer's policy wording. It is a simplified, internally consistent P&C teaching contract created so that the path from environmental hazard to covered insurance loss is explicit.

### 2.2 Covered losses

The fictional policy combines commercial property/business interruption coverage with an Environmental Impairment Endorsement. For the case, a claim can arise only when a defined insured trigger occurs.

Air-quality insured event

A covered air event occurs when:

- the location's air-quality indicator exceeds the case threshold for the required duration; and
- the facility experiences a documented operational restriction, temporary closure, or insured filtration/remediation response under the policy conditions.

Covered amounts may include qualifying extra expense and business-interruption loss after the applicable waiting period and deductible.

Water-quality insured event

A covered water event occurs when:

- a defined water-quality indicator exceeds the case contamination threshold or an official no-use/boil-water condition is triggered; and
- the event causes covered cleanup, treatment, repair, extra expense, or business interruption at the insured location.

Compound insured event

A compound event occurs when both air and water triggers affect the same insured location within the defined event window or policy year. Compound risk is not assumed to equal the simple sum of the two standalone risks because the conditions may jointly affect claim frequency, severity, and portfolio accumulation.

### 2.3 What is not a claim

Environmental deterioration by itself is not an insurance claim. A high PM2.5 value, poor water reading, or adverse climate indicator only becomes actuarially relevant when it changes the probability or size of a covered insured event.

The case therefore uses the following chain:

Climate conditions → Environmental hazard → Exposure and vulnerability → Defined coverage trigger → Claim frequency and severity → Policy terms → Portfolio loss → Premium and risk decision

### 2.4 Policy terms

Each record contains:

- insured value;
- policy limit;
- deductible;
- business-interruption waiting-period indicator;
- exposure measure;
- current premium; and
- mitigation status.

Claim payments are calculated after applying the deductible and policy limit. The student notebook clearly distinguishes ground-up loss, covered loss, and insurer-paid loss.

### 2.5 Exclusions and simplifications

To keep the exercise focused, the core case excludes:

- employee health and workers compensation claims;
- third-party bodily injury and environmental liability;
- gradual pollution with no defined insured trigger;
- losses outside the endorsement's event definition;
- intentional or known non-compliance;
- mold and other long-latency contamination;
- uninsured shutdowns below the stated waiting period; and
- amounts above the policy limit.

These exclusions prevent students from incorrectly interpreting general environmental harm as automatically covered P&C loss.

## 3. Core Teaching Innovation

ClimateTwin is designed as an actuarial decision laboratory, not simply a predictive-modelling exercise.

Each team receives the same AquaAir portfolio and is asked to answer a sequence of increasingly difficult insurance questions:

1. What is the portfolio's baseline frequency and severity?
2. Which environmental variables materially change expected insured loss?
3. Is the current premium adequate?
4. What happens to aggregate loss and tail risk when air quality worsens?
5. What happens when water quality worsens?
6. What happens when both stresses occur together?
7. Which mitigation actions should the insurer fund under a limited resilience budget?
8. After mitigation, how should the insurer reprice or manage the portfolio?

The intended "aha" moment is that the region with the worst environmental measurement is not necessarily the region that contributes most to insured loss or tail risk. Insurance risk depends on the interaction of hazard, exposure, vulnerability, policy terms, and dependence.

## 4. Learning Objectives

By the end of the case, students should be able to:

1. Translate climate information into insured-loss mechanisms.  
   Distinguish environmental hazard from exposure, vulnerability, trigger, covered claim, and insurer-paid loss.

2. Model exposure-adjusted claim frequency.  
   Estimate claim frequency using an actuarial count model with an exposure offset and interpret the effect of occupancy, climate, environmental, and mitigation variables.

3. Model conditional claim severity.  
   Estimate claim severity conditional on a claim occurring and explain the influence of insured value, occupancy, trigger type, and mitigation.

4. Calculate loss cost and indicated premium.  
   Combine frequency and severity into expected loss cost and apply a transparent expense/profit structure to produce an indicated premium.

5. Measure aggregate and tail risk.  
   Simulate annual portfolio losses and calculate VaR and TVaR under baseline and stress conditions.

6. Evaluate premium adequacy under stress.  
   Compare current premium with stressed expected loss and indicated premium and identify where the portfolio becomes underpriced.

7. Evaluate mitigation financially.  
   Quantify expected-loss reduction, benefit-cost ratio, and tail-risk reduction from mitigation.

8. Make and communicate an actuarial recommendation.  
   Defend pricing, underwriting, mitigation, or portfolio actions to a simulated Climate Risk Committee.

## 5. Dataset and Known Data-Generating Process

### 5.1 Student dataset

The core dataset will contain approximately 750 policy-location-year observations in CSV format. A parallel Excel version may also be provided for accessibility.

The student-facing data will include the following variable groups.

| Group | Example variables |
|---|---|
| Policy | `policy_id`, `year`, `region`, `occupancy`, `exposure_years` |
| Financial exposure | `insured_value`, `policy_limit`, `deductible`, `current_premium` |
| Air | `pm25`, `ozone`, `air_stress_flag` |
| Water | `turbidity`, `water_quality_index`, `water_stress_flag` |
| Climate | `temperature`, `rainfall`, `drought_indicator` |
| Mitigation | `air_filtration`, `water_treatment`, `business_continuity_plan` |
| Claims | `claim_count`, `aggregate_ground_up_loss`, `aggregate_paid_loss` |

Only variables required for the core learning objectives are included. Additional spatial or high-dimensional predictors are reserved for optional extensions.

### 5.2 Instructor-only data-generating process

The synthetic data will be generated from a documented process stored in the instructor materials. The exact coefficients are hidden from students but known to the instructor so that expected actuarial relationships are intentional and reproducible.

The frequency component will follow a structure such as:

$$
N_i \sim \text{Poisson or Negative Binomial}(\lambda_i)
$$

with

$$
\log(\lambda_i) =
\log(\text{Exposure}_i)
+ \beta_0
+ \beta_{\text{occupancy}}
+ \beta_{\text{air}}
+ \beta_{\text{water}}
+ \beta_{\text{compound}}
+ \beta_{\text{climate}}
+ \beta_{\text{mitigation}}.
$$

The severity component, conditional on a claim, will use a positive continuous distribution such as Gamma or Lognormal:

$$
X_i \mid N_i>0 \sim \text{Gamma or Lognormal}
$$

with expected severity driven by insured value, occupancy, event type, and mitigation status.

Policy deductibles and limits are then applied to simulated ground-up losses to generate insurer-paid losses.

The data-generating process will intentionally include:

- higher claim frequency under air stress;
- higher claim frequency and/or severity under water stress;
- a non-zero compound air–water interaction;
- occupancy differences;
- mitigation effects that reduce expected and/or tail loss; and
- enough random variation that the correct conclusions are not visually obvious from raw data.

A fixed random seed and full generation script will be supplied in the instructor package so that the dataset is completely reproducible.

## 6. Four Core Scenarios

### Scenario 1 — Baseline

Students estimate the portfolio under current environmental conditions.

They calculate:

- exposure-adjusted frequency;
- conditional severity;
- expected loss cost;
- indicated premium;
- aggregate annual loss distribution;
- VaR and TVaR; and
- baseline premium adequacy.

### Scenario 2 — Air-Quality Stress

Air-quality variables are stressed while the water environment remains at baseline.

The scenario represents a persistent heat/stagnation episode that raises air-quality indicators and therefore the probability of qualifying operational restrictions and covered extra-expense/business-interruption claims.

### Scenario 3 — Water-Quality Stress

Water-quality variables are stressed while air conditions remain at baseline.

The scenario represents drought or contamination pressure sufficient to increase the probability of defined water-related insured events and associated cleanup, treatment, extra-expense, and business-interruption losses.

### Scenario 4 — Compound Air–Water Stress

Both stresses occur together.

Students compare the compound portfolio result with the standalone scenarios and examine whether the combination materially changes expected loss, premium adequacy, and tail risk.

The core case does not require copula modelling or advanced spatial dependence. The dependence embedded in the synthetic scenario is handled through the instructor-defined data-generating process and scenario simulation. Copulas, spatial modelling, and alternative dependence structures are optional advanced modules.

## 7. Actuarial Mechanics Required in the Core Case

### 7.1 Exposure-adjusted frequency

Students estimate claim frequency using an appropriate count model with exposure as an offset or denominator.

A simplified conceptual form is:

$$
\text{Claim Frequency} = \frac{\text{Claim Count}}{\text{Exposure}}
$$

with regression used to estimate systematic effects.

### 7.2 Conditional severity

Severity is measured conditional on a claim occurring:

$$ \text{Conditional Severity} = E(\text{Paid Loss}\mid N>0).$$

Students compare at least one defensible severity distribution/model and interpret the fitted effects.

### 7.3 Expected loss cost

Expected loss cost is obtained from the frequency-severity framework:

$$
E(L) = E(N)\times E(X).
$$

Where relevant, the notebook distinguishes loss cost per exposure from total portfolio expected loss.

### 7.4 Indicated premium

The case supplies an expense ratio and target underwriting/profit provision. Students calculate an indicated premium using a transparent simplified indication:

$$
\text{Indicated Premium}
=
\frac{\text{Expected Loss + Fixed Expense per Exposure}}
{1-\text{Variable Expense Ratio}-\text{Profit/Contingency Provision}}.
$$

Students then compare the indicated premium with the current premium.

### 7.5 Premium adequacy

Premium adequacy is evaluated using both:

$$
\text{Adequacy Ratio}
=
\frac{\text{Current Premium}}{\text{Indicated Premium}}
$$

and an expected loss-ratio view.

Values below the required adequacy threshold indicate that the current premium is insufficient under the scenario assumptions.

### 7.6 Aggregate annual loss and tail risk

Monte Carlo simulation generates the annual portfolio loss distribution under each scenario.

Students calculate:

$$
VaR_{99}
$$

and

$$
TVaR_{99}
=
E[L \mid L > VaR_{99}].
$$

The comparison focuses on how stress affects both the center and the tail of the distribution.

### 7.7 Financial value of mitigation

Each mitigation option has a fixed implementation cost and an instructor-defined effect on frequency and/or severity.

Students report:

- expected-loss reduction;
- mitigation cost;
- benefit-cost ratio;
- reduction in VaR;
- reduction in TVaR; and
- post-mitigation premium adequacy.

The primary decision is not based only on the expected-loss-reduction-to-cost ratio.

Instead, teams solve a constrained portfolio decision:

$$
\min TVaR_{99}
$$

subject to

$$
\sum_i \text{Mitigation Cost}_i \leq \text{Climate Resilience Budget}.
$$

Expected-loss reduction and benefit-cost ratios are reported as supporting measures. This prevents the exercise from rewarding a mitigation choice that looks efficient on average while leaving severe tail exposure largely unchanged.

## 8. Teaching Structure and Duration

The full version separates in-class and independent work.

### Full version: approximately 6–7 hours

| Component | Mode | Time | Main output |
|---|---|---:|---|
| Pre-class preparation | Independent | 45–60 min | Read case, inspect data dictionary, answer hazard-to-claim questions |
| Session 1: Insurance setting and baseline | In class | 60 min | Coverage map, descriptive analysis, baseline expectations |
| Session 2: Frequency, severity and pricing | In class | 75 min | Frequency model, severity model, loss cost, indicated premium |
| Session 3: Stress testing and tail risk | In class | 75 min | Scenario loss distributions, VaR, TVaR, adequacy comparison |
| Session 4: Mitigation and committee decision | In class | 60 min | Budget-constrained mitigation decision and recommendation |
| Final committee memo | Independent | 60–90 min | Short actuarial recommendation with quantitative support |

In-class time: approximately 4.5 hours  
Independent work: approximately 2–2.5 hours

### One-session version: approximately 2 hours

A shorter version will provide pre-fitted frequency and severity models. Students will:

1. review the coverage mechanism;
2. calculate baseline loss cost and indicated premium;
3. run the four provided scenarios;
4. compare VaR/TVaR and premium adequacy;
5. choose mitigation under a fixed budget; and
6. deliver a short committee recommendation.

This version preserves the main actuarial decision insight without requiring full model fitting.

## 9. Mapping to CAS Education and General-Insurance Competencies

The case is intentionally aligned with current CAS general-insurance education rather than using climate risk as a stand-alone environmental topic.

| Learning objective | General-insurance competency | CAS education connection |
|---|---|---|
| Translate hazard into covered loss | Coverage interpretation, exposure definition, actuarial judgment | Supports the practical insurance context required across P&C work and ratemaking exercises |
| Model exposure-adjusted frequency | Frequency modelling, GLMs, predictive analytics | MAS-II: statistical learning concepts; Exam 8: interpretation/evaluation of classification ratemaking models and GLM-based approaches |
| Model conditional severity | Severity modelling and loss-cost estimation | Exam 5: loss experience and ratemaking foundations; Exam 8: component models and individual/classification risk pricing |
| Calculate expected loss cost | Frequency-severity framework, pure premium | Exam 5: basic ratemaking and rate-level indication concepts |
| Calculate indicated premium | Expense/profit loads, pricing indication | Exam 5: ratemaking, underwriting provisions, and indications |
| Evaluate premium adequacy | Pricing sufficiency and scenario sensitivity | Exam 5 / Exam 8: pricing and classification/rate adequacy applications |
| Simulate aggregate loss and calculate VaR/TVaR | Portfolio risk and tail-risk measurement | Exam 9: risk management, risk-adjusted decision-making, and financial risk management |
| Evaluate mitigation under a budget | Risk reduction, capital-aware decision-making | Exam 9: risk management, cost of risk, risk-adjusted pricing/performance concepts |
| Present committee recommendation | Professional judgment and communication | Reinforces communication of actuarial results, assumptions, limitations, and business recommendations |

The case therefore connects predictive modelling, frequency-severity analysis, ratemaking, portfolio risk, risk management, and professional communication in one classroom exercise.

## 10. Student Workflow and Expected Outputs

Students complete the case in five stages.

### Stage 1 — Coverage and data interpretation

Expected output

- one hazard-to-claim diagram;
- identification of insured triggers and exclusions;
- descriptive summary of the portfolio.

### Stage 2 — Baseline actuarial model

Expected output

- exposure-adjusted frequency estimate/model;
- conditional severity estimate/model;
- expected loss cost by selected segment;
- baseline aggregate expected loss.

### Stage 3 — Pricing

Expected output

- indicated premium;
- adequacy ratio;
- identification of underpriced or adequately priced segments.

### Stage 4 — Climate stress test

Expected output

A comparison table containing, at minimum:

- expected annual loss;
- indicated premium;
- adequacy ratio;
- VaR at 99%;
- TVaR at 99%;

for baseline, air stress, water stress, and compound stress.

### Stage 5 — Mitigation decision

Expected output

- selected mitigation portfolio within budget;
- expected-loss reduction;
- benefit-cost ratio;
- TVaR reduction;
- post-mitigation premium adequacy; and
- a short recommendation to the Climate Risk Committee.

## 11. Guiding Questions

1. What must happen for an adverse air- or water-quality observation to become a covered claim?
2. Which variables most strongly affect exposure-adjusted claim frequency?
3. Which variables most strongly affect conditional severity?
4. Do the same variables affect frequency and severity in the same direction?
5. Which occupancy has the highest expected loss cost after controlling for exposure?
6. Is the current portfolio premium adequate under baseline conditions?
7. Which standalone stress produces the largest change in expected loss?
8. Which scenario produces the largest change in TVaR?
9. Does the compound scenario create a materially different portfolio result from considering air and water stresses separately?
10. Which locations or occupancy groups contribute most to expected loss and which contribute most to tail risk?
11. Which mitigation set minimizes TVaR while remaining within the resilience budget?
12. Would the mitigation decision change if the insurer focused only on expected-loss benefit-cost ratio?
13. After mitigation, should the insurer reprice, change deductibles/limits, restrict capacity, require mitigation, or maintain current terms?
14. What assumptions or model limitations should be communicated to management?

## 12. Assessment Strategy

The final student deliverable is a short Climate Risk Committee Memo supported by notebook outputs.

| Criterion | Weight | Evidence of strong performance |
|---|---:|---|
| Coverage and loss-mechanism understanding | 15% | Correctly distinguishes environmental deterioration from covered insured events |
| Frequency-severity modelling | 25% | Uses exposure appropriately, fits/interprets models correctly, and separates frequency from conditional severity |
| Ratemaking and premium adequacy | 20% | Calculates loss cost and indicated premium correctly and interprets adequacy under stress |
| Portfolio and tail-risk analysis | 20% | Correctly calculates/interprets aggregate loss, VaR, TVaR, and scenario differences |
| Mitigation decision | 10% | Uses the budget constraint and reports both tail-risk and expected-loss effects |
| Professional communication | 10% | Gives a concise, defensible recommendation with assumptions and limitations |

A scoring rubric with performance levels will be supplied to instructors.

## 13. Complete Classroom Package

The submission will be organized as a ready-to-use instructor package rather than a proposal alone.

The minimum package will include:

1. Instructor Guide  
   Teaching objectives, prerequisite knowledge, schedule, classroom flow, model assumptions, data-generating process, common misconceptions, expected results, and discussion notes.

2. Student Case Document  
   Insurance background, policy structure, scenario definitions, tasks, guiding questions, and required deliverables.

3. Synthetic Dataset  
   Approximately 750 policy-location-year records in CSV, plus a data dictionary.

4. Data-Generation Script  
   Reproducible instructor-only script with fixed seed and documented hidden relationships.

5. Ready-to-Run Python Notebook  
   Data checks, frequency, severity, loss cost, pricing, simulation, VaR/TVaR, scenario comparison, and mitigation analysis.

6. Solution Notebook  
   Completed calculations, expected outputs, interpretation notes, and instructor checkpoints.

7. Presentation Slides  
   Short slide deck introducing the insurer, coverage mechanism, four scenarios, and committee challenge.

8. Assessment Rubric  
   Scoring criteria for technical work and professional communication.

9. Software and Setup Instructions  
   Python version, package requirements, Jupyter/Colab instructions, file structure, and a no-install cloud option where feasible.

10. Expected-Output Sheet  
    Instructor reference containing expected ranges/tables/figures for each stage.

The interactive dashboard is not required for the minimum viable submission. It will be described only as a future extension unless a stable, tested version is completed before submission.

## 14. Pedagogical Effectiveness and Pilot Validation

The case will be pilot-tested before the final CAS submission with a small group of approximately 4–8 students or recent actuarial learners who have basic statistics and insurance knowledge but have not seen the instructor solution.

The pilot will record:

- total completion time;
- completion rate by stage;
- questions or instructions that caused confusion;
- coding/setup difficulties;
- whether the dataset was sufficient without instructor intervention;
- errors in distinguishing environmental indicators from insurance triggers;
- difficulty with frequency-severity modelling;
- difficulty interpreting VaR/TVaR and premium adequacy;
- whether students reached the intended insight about expected loss versus tail risk;
- quality of final insurance recommendations; and
- specific revisions made after the pilot.

A short pre/post prompt will also be used:

Before the case: "Which region do you believe is the insurer's greatest climate risk, and why?"

After the case: "Which part of the portfolio creates the greatest financial/tail risk, and what action should the insurer take?"

The comparison provides simple evidence that students moved from environmental-risk intuition to actuarial-risk reasoning.

The final submission's instructor guide will contain a brief Pilot and Revision Note reporting actual participants, completion time, observed difficulties, intended learning outcome achievement, and changes made after testing. No pilot results will be invented; this section will be completed from the actual classroom trial before submission.

## 15. Optional Advanced Extensions

The following topics are deliberately excluded from the required core case and may be offered as optional graduate/professional extensions:

- spatial dependence and geographic accumulation;
- copula-based air–water dependence;
- alternative severity distributions;
- zero-inflated count models;
- credibility;
- model validation and out-of-sample testing;
- uncertainty intervals around indicated premium;
- reinsurance or aggregate stop-loss structures;
- alternative capital/risk-load approaches;
- adaptive mitigation optimization; and
- an interactive ClimateTwin dashboard.

This separation keeps the first release teachable while preserving a pathway for more advanced actuarial courses.

## 16. Why ClimateTwin Is Innovative and Doable

ClimateTwin does not ask students merely to forecast pollution or discuss climate change qualitatively. It asks them to make a P&C actuarial decision from a changing environmental state.

The exercise is innovative because it brings together:

- a clearly defined commercial insurance contract;
- air and water quality as emerging climate-linked risk signals;
- frequency-severity modelling;
- ratemaking;
- aggregate simulation;
- tail-risk measurement;
- stress testing;
- mitigation economics; and
- professional insurance decision-making.

At the same time, the scope is intentionally controlled. Students work with one portfolio, one coverage architecture, one compact synthetic dataset, four scenarios, and one decision framework.

The central learning message is: Environmental severity is not the same as insurance severity. Actuarial climate-risk management requires translating hazard into covered loss, quantifying the full loss distribution, testing premium adequacy, and deciding how pricing and mitigation should change before losses materialize.

ClimateTwin is therefore designed to be innovative enough to expose students to an emerging area of actuarial work, but concrete enough to be run, assessed, reproduced, and improved in an ordinary actuarial classroom.