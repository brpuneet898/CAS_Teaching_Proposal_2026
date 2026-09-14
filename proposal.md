# ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management

### Proposed Teaching Material for the CAS Global Teaching Materials Innovation Challenge 2026

## 1. Project Title and Summary

ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management

ClimateTwin is a compact, scenario-based actuarial case in which students act as the pricing and risk team for AquaAir General Insurance, a fictional insurer writing commercial property and business interruption coverage with a defined environmental impairment endorsement for hospitals, manufacturing facilities, and food-processing facilities.

In this teaching material, **"digital twin" is used in a deliberately limited pedagogical sense**: ClimateTwin is a reproducible synthetic portfolio and scenario simulator that represents how a defined insurer's loss distribution changes when environmental conditions, policy terms, and mitigation assumptions change. It is not a real-time physical twin, does not ingest live sensor feeds, and is not intended to reproduce all operational features of an insurer or city.

The case focuses on one practical question: How should an insurer translate deteriorating air and water conditions into defensible frequency, severity, pricing, tail-risk, and mitigation decisions for a commercial portfolio?

Students work with a synthetic policy-location-year dataset and a ready-to-run notebook. They estimate exposure-adjusted claim frequency and conditional claim severity, calculate expected loss cost and indicated premium, simulate aggregate annual portfolio loss, measure VaR and TVaR, test premium adequacy under climate stress, and evaluate the financial value of a defined set of mitigation strategies.

The core case is deliberately limited to four scenarios:

1. Baseline conditions
2. Air-quality stress
3. Water-quality stress
4. Compound air–water stress

The teaching cycle is:

Observe → Model → Price → Stress → Mitigate → Reprice

The core classroom materials, student workflow, solution workflow, assessment structure, and reproducible simulation framework have been implemented in the first package and are being synchronized in V2 to the corrected data-generating process and review requirements. Advanced topics such as spatial models, copulas, alternative dependence structures, and adaptive optimization remain optional extensions rather than claims of the core simulator.

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
   Estimate claim frequency using an actuarial count model with an exposure offset and interpret the fitted effects of relevant portfolio and environmental variables.

3. Model conditional claim severity.  
   Estimate **claim-level severity conditional on a claim occurring**, distinguish claim-level severity from policy-year aggregate loss, and explain the influence of insured value, occupancy, trigger type, policy terms, and mitigation.

4. Calculate loss cost and indicated premium.  
   Combine frequency and severity into expected loss cost and apply a transparent expense/profit structure to produce an indicated premium.

5. Measure aggregate and tail risk.  
   Simulate annual portfolio losses and calculate VaR and TVaR under baseline and stress conditions.

6. Evaluate premium adequacy under stress.  
   Compare current premium with stressed expected loss and indicated premium and identify where the portfolio becomes underpriced under the stated assumptions.

7. Evaluate mitigation financially.  
   Quantify expected-loss reduction, benefit-cost ratio, and tail-risk reduction for the **candidate mitigation portfolios evaluated**.

8. Make and communicate an actuarial recommendation.  
   Select and defend a feasible candidate strategy using the model outputs, while clearly stating assumptions, simulation uncertainty, and limitations to the scope of the decision.

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

The synthetic data are generated by a documented instructor-only process with a fixed random seed and explicit parameter settings. The V2 proposal intentionally describes that process at the level required for teaching design; the generator, data dictionary, student notebook, and solution notebook will contain the exact implemented equations and parameter values so that the proposal does not state relationships that differ from the released simulation.

The generator separates three concepts that students must not conflate:

1. **policy-location-year exposure and environmental state**;
2. **claim occurrence/frequency during that exposure period**; and
3. **individual claim severity**, generated only when a claim occurs.

Claim frequency is therefore generated at the policy-location-year level using an exposure-aware count mechanism. Environmental and portfolio variables affect frequency through the implemented trigger/risk structure rather than through an illustrative equation that is not identical to the released code.

For each simulated claim, a positive ground-up severity is generated at the **claim level**. Claim-level losses are then processed through the applicable deductible and policy limit and aggregated back to the policy-location-year and portfolio levels. This preserves the distinction between conditional claim severity, aggregate ground-up loss, and aggregate insurer-paid loss.

The implemented DGP is designed so that the synthetic portfolio exhibits intentional actuarial relationships, including occupancy differences, environmental stress effects, mitigation effects, and sufficient random variation that the intended conclusions are not visually predetermined from the raw data. Exact coefficients and distributional choices are documented in the instructor materials rather than inferred by students from this proposal.

The compound scenario is also described conservatively. Air and water pathways are stressed together, but the core simulator does **not** claim to reproduce all physical or statistical dependence between the hazards. Unless an explicit dependence term is included in the released V2 generator, the air- and water-related stochastic components are treated as **conditionally independent given the modelled portfolio, environmental, and scenario inputs**. Shared inputs can therefore move both pathways at the same time, but unmodelled residual dependence is outside the core case.

A fixed seed, reproducible generation script, data dictionary, and instructor documentation are included in the classroom package so that the released dataset can be recreated and the assumptions can be inspected.

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

The core case does not require copula modelling or advanced spatial dependence. In V2, the compound scenario is interpreted as a **joint stress test of both modelled pathways**, not as evidence that the simulator captures every form of air–water dependence. Unless dependence is explicitly parameterized in the released generator, residual air- and water-related stochastic components are conditionally independent given the modelled inputs. Copulas, spatial dependence, and alternative dependence structures are therefore optional advanced extensions and useful sensitivity analyses.

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

$$ \text{Indicated Premium} = \frac{\text{Expected Loss + Fixed Expense per Exposure}} {1-\text{Variable Expense Ratio}-\text{Profit/Contingency Provision}}.$$

Students then compare the indicated premium with the current premium.

### 7.5 Premium adequacy

Premium adequacy is evaluated using both:

$$ \text{Adequacy Ratio} = \frac{\text{Current Premium}}{\text{Indicated Premium}}$$

and an expected loss-ratio view.

Values below the required adequacy threshold indicate that the current premium is insufficient under the scenario assumptions.

### 7.6 Aggregate annual loss and tail risk

Monte Carlo simulation generates the annual portfolio loss distribution under each scenario.

Students calculate:

$$
VaR_{99}
$$

and

$$ TVaR_{99} = E[L \mid L > VaR_{99}].$$

The comparison focuses on how stress affects both the center and the tail of the distribution.

### 7.7 Financial value of mitigation

Each mitigation option has a defined implementation cost and an instructor-defined effect on frequency and/or severity.

Students report:

- expected-loss reduction;
- mitigation cost;
- benefit-cost ratio;
- reduction in VaR;
- reduction in TVaR; and
- post-mitigation premium adequacy.

The primary decision is not based only on the expected-loss-reduction-to-cost ratio. Students evaluate a **finite set of candidate mitigation portfolios** under the Climate Resilience Budget and identify the feasible candidate with the lowest estimated TVaR at the chosen confidence level.

For candidate portfolio $ \(j\) $,

$$
j^* = \arg\min_{j \in \mathcal{F}} \widehat{TVaR}_{99,j},
$$

where

$$
\mathcal{F} = \left\{j : \text{Mitigation Cost}_j \leq \text{Climate Resilience Budget}\right\}.
$$

The conclusion is therefore stated as:

> **Select the strategy with the lowest estimated TVaR99 among the feasible candidate portfolios evaluated under the stated budget.**

This is a comparison over the candidate set supplied in the case; it is **not a claim of a globally optimal mitigation portfolio**. Expected-loss reduction and benefit-cost ratios are reported as supporting measures, and Monte Carlo estimates are interpreted with appropriate simulation uncertainty.

## 8. Teaching Structure, Prerequisites, and Duration

### 8.1 Prerequisites

The full case is intended for actuarial students or early-career learners who have:

- introductory probability and statistics;
- familiarity with insurance loss concepts and basic P&C terminology;
- basic frequency/severity concepts;
- introductory regression or GLM exposure;
- basic Python/Jupyter competence; and
- a conceptual understanding of simulation and quantiles.

Students do **not** need prior climate-science, environmental-engineering, copula, spatial-statistics, or optimization coursework. Brief definitions and the insurance coverage mechanism are provided inside the case.

For cohorts with weaker coding or modelling prerequisites, the short version uses prepared/prefitted model outputs so that the learning focus remains on actuarial interpretation and decision-making.

### 8.2 Full version: approximately 6–7 hours

The full version is the primary teaching pathway and separates in-class modelling from independent preparation and communication.

| Component | Mode | Time | Main output |
|---|---|---:|---|
| Pre-class preparation | Independent | 45–60 min | Read case, inspect data dictionary, answer hazard-to-claim questions |
| Session 1: Insurance setting and baseline | In class | 60 min | Coverage map, descriptive analysis, baseline expectations |
| Session 2: Frequency, severity and pricing | In class | 75 min | Frequency model, severity model, loss cost, indicated premium |
| Session 3: Stress testing and tail risk | In class | 75 min | Scenario loss distributions, VaR, TVaR, adequacy comparison |
| Session 4: Mitigation and committee decision | In class | 60 min | Candidate-strategy comparison under the budget and recommendation |
| Final committee memo | Independent | 60–90 min | Short actuarial recommendation with quantitative support |

In-class time: approximately 4.5 hours  
Independent work: approximately 2–2.5 hours

### 8.3 Short version: approximately 2 hours

The short version is a **separate facilitated pathway**, not the full exercise compressed without modification. It uses prepared or pre-fitted frequency and severity results so that students can complete the decision cycle within one session.

Students:

1. review the coverage mechanism and key assumptions;
2. interpret baseline loss cost and indicated premium;
3. run or inspect the four provided scenarios;
4. compare expected loss, VaR/TVaR, and premium adequacy;
5. compare the supplied feasible mitigation candidates under the fixed budget; and
6. deliver a short Climate Risk Committee recommendation.

The short version preserves the hazard-to-covered-loss, stress-testing, tail-risk, and mitigation-decision insights, but it does not assess full model fitting to the same depth as the full version.

## 9. Mapping to CAS Education and General-Insurance Competencies

ClimateTwin is designed around general-insurance competencies that are central to actuarial practice: coverage interpretation, exposure definition, frequency-severity modelling, ratemaking, portfolio risk, risk management, and communication. The mapping below is intended as an **educational alignment**, not a claim that completion of the case substitutes for any particular CAS examination objective.

| Learning objective | General-insurance competency | CAS-relevant connection |
|---|---|---|
| Translate hazard into covered loss | Coverage interpretation, exposure definition, actuarial judgment | Connects environmental information to insurance contract triggers, exposure, and covered loss |
| Model exposure-adjusted frequency | Frequency modelling, GLMs, predictive analytics | Reinforces count modelling, exposure treatment, variable interpretation, and model judgment used in P&C analytics |
| Model conditional claim severity | Severity modelling and loss-cost estimation | Reinforces claim-level severity, conditional modelling, policy terms, and component-model thinking |
| Calculate expected loss cost | Frequency-severity framework, pure premium | Applies standard ratemaking logic by combining expected frequency and severity |
| Calculate indicated premium | Expense/profit loads, pricing indication | Applies transparent premium-indication mechanics and separates expected loss from pricing provisions |
| Evaluate premium adequacy | Pricing sufficiency and scenario sensitivity | Requires comparison of current and indicated premium under changing assumptions |
| Simulate aggregate loss and calculate VaR/TVaR | Portfolio risk and tail-risk measurement | Introduces simulation-based risk measurement and the distinction between central and tail outcomes |
| Evaluate candidate mitigation strategies under a budget | Risk reduction and risk-adjusted decision-making | Compares expected-loss efficiency with tail-risk reduction while respecting a business constraint |
| Present committee recommendation | Professional judgment and communication | Requires concise communication of results, assumptions, uncertainty, limitations, and recommended action |

The case therefore integrates technical analysis with actuarial judgment. Students are assessed not only on whether they obtain numerical outputs, but also on whether they understand what those outputs mean for an insurance contract and whether they communicate the limits of the model appropriately.

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
11. Among the feasible candidate mitigation portfolios evaluated, which has the lowest estimated TVaR while remaining within the resilience budget?
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

ClimateTwin is organized as a ready-to-use classroom package rather than a proposal-only concept. The first package has established the end-to-end teaching workflow; V2 synchronizes each deliverable to the corrected generator, terminology, assumptions, and review requirements.

The package consists of:

1. Instructor Guide  
   Teaching objectives, prerequisite knowledge, schedule, classroom flow, model assumptions, data-generating process, common misconceptions, expected results, discussion prompts, and limitations.

2. Student Case Document  
   Insurance background, policy structure, scenario definitions, tasks, guiding questions, and required deliverables.

3. Synthetic Dataset and Data Dictionary  
   A compact policy-location-year dataset with documented variable definitions and the fields required for the core exercise.

4. Data-Generation Script  
   A reproducible instructor-only script with a fixed seed and documented implemented relationships.

5. Student Notebook  
   Ready-to-run scaffolding for data checks, frequency, severity, loss cost, pricing, simulation, VaR/TVaR, scenario comparison, and candidate mitigation analysis.

6. Solution Notebook  
   Completed calculations, expected outputs, interpretation notes, and instructor checkpoints.

7. Presentation Slides  
   A classroom launch deck introducing AquaAir, the coverage mechanism, four scenarios, and the committee challenge.

8. Assessment Rubric  
   Performance-level criteria for technical work, actuarial interpretation, decision quality, and professional communication.

9. Software and Setup Instructions  
   Python/package requirements, Jupyter/Colab instructions, file structure, and troubleshooting guidance.

10. Expected-Output Sheet  
    Instructor reference containing expected ranges, tables, figures, and checkpoints for each stage.

The interactive dashboard is **not part of the required core package** and no real-time monitoring capability is implied by the use of the term digital twin. A dashboard may be developed later as an optional interface to the same synthetic scenario engine.

## 14. Pedagogical Effectiveness and Pilot Validation

Pilot validation is treated as an empirical check on the teaching material, not as a result to be assumed in advance.

The V2 pilot protocol uses a small group of approximately 4–8 students or recent actuarial learners with the stated prerequisites who have not seen the instructor solution. The pilot records:

- actual total completion time;
- completion rate by stage;
- questions or instructions that cause confusion;
- coding/setup difficulties;
- whether the dataset and data dictionary are sufficient without unplanned instructor intervention;
- errors in distinguishing environmental indicators from insurance triggers;
- difficulty with frequency-severity modelling;
- difficulty interpreting VaR/TVaR and premium adequacy;
- whether learners distinguish the best evaluated candidate from a claimed global optimum;
- whether learners recognize the compound-scenario dependence limitation;
- quality of final insurance recommendations; and
- specific revisions made after the pilot.

A short pre/post prompt is used:

Before the case: "Which region do you believe is the insurer's greatest climate risk, and why?"

After the case: "Which part of the portfolio creates the greatest financial/tail risk, and what action should the insurer take?"

This provides a simple way to assess whether learners move from environmental-risk intuition toward actuarial-risk reasoning.

**Pilot-status rule for the final submission:** this proposal does not present planned outcomes as completed evidence. After the actual pilot is conducted, this section and the Instructor Guide's Pilot and Revision Note will be updated with the observed participant count, completion time, difficulties, learning evidence, and changes made. Until those observations exist, no pilot result is reported or invented.

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

Its innovation is the integration of:

- a clearly defined commercial insurance contract;
- air and water quality as climate-linked risk signals;
- exposure-aware frequency modelling;
- claim-level conditional severity modelling;
- ratemaking;
- aggregate simulation;
- tail-risk measurement;
- transparent stress testing;
- mitigation economics; and
- professional insurance decision-making.

The term **ClimateTwin** describes the pedagogical scenario simulator: a reproducible synthetic representation of one insurer portfolio under alternative environmental and mitigation states. The core tool does not claim live-data ingestion, continuous calibration, physical-system replication, or exhaustive hazard dependence.

The scope is intentionally controlled. Students work with one portfolio, one coverage architecture, one compact synthetic dataset, four scenarios, and a finite set of candidate mitigation strategies. Their mitigation conclusion is correspondingly bounded: they identify the feasible **evaluated candidate** with the lowest estimated TVaR, rather than claiming to solve an unrestricted global optimization problem.

The central learning message is: Environmental severity is not the same as insurance severity. Actuarial climate-risk management requires translating hazard into covered loss, quantifying the loss distribution, testing premium adequacy, comparing feasible interventions, and communicating what the model does and does not establish.

ClimateTwin is therefore designed to be innovative enough to expose students to an emerging area of actuarial work, while remaining concrete enough to run, assess, reproduce, critique, and improve in an ordinary actuarial classroom.
