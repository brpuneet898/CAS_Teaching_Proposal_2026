# ClimateTwin: An Actuarial Digital Twin for Air–Water Climate Risk Management

Teaching-material repository for the **CAS Global Teaching Materials Innovation Challenge 2026**.

ClimateTwin is a scenario-based P&C actuarial case in which students act as the Pricing and Climate Risk Team for **AquaAir General Insurance**, a fictional insurer covering hospitals, manufacturing facilities, and food-processing facilities under a simplified commercial property, business-interruption, and environmental-impairment framework.

The case asks students to translate changing air- and water-quality conditions into defensible actuarial decisions through the cycle:

**Observe → Model → Price → Stress → Mitigate → Reprice**

> **Core insurance principle:** environmental deterioration is a hazard signal, not automatically an insurance claim.  
> A covered loss must pass through the chain  
> **environmental condition → insured trigger → claim → coverage mechanics → insurer-paid loss**.

---

## What students learn

By completing the full case, students should be able to:

- distinguish environmental hazards from qualifying insured events;
- explain the effects of exposure, deductibles, limits, and BI waiting periods;
- fit and interpret an exposure-adjusted frequency model;
- fit and interpret a conditional severity model;
- combine frequency and severity into expected loss and indicated premium;
- assess premium adequacy;
- stress-test the portfolio under baseline, air, water, and compound scenarios;
- simulate aggregate annual loss and calculate **VaR99** and **TVaR99**;
- compare feasible mitigation strategies under a resilience budget; and
- communicate an actuarial recommendation to a simulated Climate Risk Committee.

---

## Repository contents

| File | Audience | Purpose |
|---|---|---|
| `proposal.md` | Reviewers / instructors | Full V2 teaching proposal and pedagogical design. |
| `case_study.md` | Students | Student-facing insurance case, tasks, scenarios, worked coverage examples, and required deliverables. |
| `student_notebook.ipynb` | Students | Guided full-case notebook with helper functions for routine simulation and portfolio evaluation. |
| `dataset.csv` | Students | Synthetic policy-location-year portfolio used for modelling and analysis. |
| `data_dictionary.md` | Students / instructors | Variable definitions, insurance mechanics, scenario definitions, and modelling guidance. |
| `case_study.pptx` | Instructors / students | Classroom launch deck introducing AquaAir, coverage logic, scenarios, and committee challenge. |
| `rubric.md` | Students / instructors | 100-point assessment rubric aligned to observable learning evidence. |
| `setup_instructions.md` | Students / instructors | Environment, package, folder, execution, and troubleshooting instructions. |
| `solution.ipynb` | Instructor only | Executed reference implementation for the complete V2 workflow. |
| `expected_output.md` | Instructor only / post-class | Regenerated V2 benchmark outputs, ranges, diagnostics, and validation notes. |
| `instructor_guide.md` | Instructor only | Teaching plan, DGP explanation, diagnostics, warnings, misconceptions, timing, and debrief guidance. |
| `data_script.py` | Instructor only | Reproducible synthetic-data generator and validation logic; single source of truth for the V2 DGP. |

The generator also produces an instructor-side **claim-level table** used to reconcile claim-level loss mechanics with the annual policy-location-year dataset.

---

## V2 data architecture

The V2 implementation treats the generator, claim-level records, and annual portfolio table as one consistent system.

### Student-facing portfolio

`dataset.csv` contains:

- **750 policy-location-year rows**;
- **250 synthetic insured locations**;
- policy years **2024–2026**;
- three commercial occupancy classes;
- policy financial terms;
- air, water, and climate indicators;
- mitigation status;
- claim counts; and
- annual aggregate loss fields.

All three years are used for model fitting. The **2026 records** are treated as the current portfolio snapshot for annual portfolio simulation so that the same location is not counted three times in one simulated year.

### Claim-level mechanics

Claims are generated at claim level and then aggregated to the annual dataset. This keeps frequency, severity, and policy financial terms internally consistent.

For each claim, the V2 contract distinguishes:

1. **ground-up loss**;
2. **covered loss**;
3. **business-interruption eligibility under the waiting-period rule**;
4. **loss after deductible**; and
5. **insurer-paid loss after the per-claim policy limit**.

Legitimate **zero-paid claims are allowed**. For example, a covered loss may fall below the deductible even though a valid insured event occurred.

The generator validates that:

- claim counts are valid non-negative integers;
- severity responses used by positive-severity models are valid;
- deductibles are applied exactly once;
- BI waiting-period rules are applied consistently;
- insurer payment never exceeds the applicable policy limit;
- claim-level and annual aggregates reconcile;
- generated values are finite where required; and
- the fixed seed reproduces the same dataset.

---

## Four core scenarios

The required classroom scenarios are:

| Scenario | Air transformation | Water transformation |
|---|---|---|
| **Baseline** | Observed values | Observed values |
| **Air stress** | PM2.5 + 15; ozone + 10 | No change |
| **Water stress** | No change | Turbidity × 1.60; WQI − 15 |
| **Compound stress** | Apply air stress | Apply water stress |

Environmental stress flags are recomputed after each transformation.

A stressed environmental state does **not** automatically produce a claim. The scenario changes the risk conditions; insured loss still passes through trigger, frequency, severity, policy-term, and payment mechanics.

### Compound-risk limitation

The V2 generator includes an explicit compound-risk effect, but the air and water trigger draws are conditionally independent given the model covariates. This is a deliberate classroom simplification rather than a claim that real air–water hazards are independent.

---

## Modelling workflow

The reference implementation follows six stages.

### 1. Observe

Students inspect:

- portfolio composition;
- environmental stress;
- qualifying insured triggers;
- exposure;
- claim counts;
- paid losses; and
- concentrations by region and occupancy.

### 2. Model frequency

The case uses an exposure-adjusted count model with:

```text
response = claim_count
offset   = log(exposure_years)
```

Students interpret rate effects rather than reporting coefficients without actuarial context.

### 3. Model conditional severity

The V2 solution models a **strictly positive claim-level severity response before policy financial terms**. This avoids incorrectly forcing legitimate zero-paid claims into a Gamma response.

The simulator then applies the contract mechanics to obtain insurer-paid loss.

### 4. Price

Students combine frequency and severity to estimate expected loss and calculate indicated premium using the case expense and profit assumptions.

```text
Indicated Premium =
(Expected Loss + Fixed Expense × Exposure)
/
(1 - Variable Expense Ratio - Profit / Contingency Provision)
```

Premium adequacy is summarized as:

```text
Current Premium / Indicated Premium
```

### 5. Stress

For each scenario, students compare:

- expected annual loss;
- indicated premium;
- premium adequacy;
- VaR99; and
- TVaR99.

The reference solution uses reproducible Monte Carlo simulation and repeated-seed checks to assess the stability of tail-risk rankings.

### 6. Mitigate

AquaAir has a fixed **Climate Resilience Budget**.

Students evaluate a manageable set of **candidate feasible mitigation strategies** and select the strategy with the **lowest estimated TVaR99 among the candidate portfolios evaluated under the stated budget**.

The exercise does **not** claim to establish a global optimum.

Expected-loss reduction, benefit-cost ratio, VaR reduction, TVaR reduction, and post-mitigation premium adequacy are supporting decision measures.

---

## Worked insurance mechanics

The student case includes three explicit examples that must reconcile with the generator and solution:

1. **Covered loss below the deductible**  
   A valid insured event can produce a zero insurer payment.

2. **Payment constrained by the policy limit**  
   After applying the deductible once, payment is capped by the applicable per-claim limit.

3. **BI waiting period not met**  
   The BI component can be ineligible while another qualifying covered cost remains payable.

These examples are included to ensure that students treat coverage mechanics as part of actuarial modelling rather than as an afterthought.

---

## Teaching formats

### Full version

The full version contains **4.5 classroom hours**, with preparation and final submission separated from classroom time.

| Component | Mode | Approximate time |
|---|---|---:|
| Preparation | Independent | 45–60 min |
| Insurance setting and baseline | In class | 60 min |
| Frequency, severity, and pricing | In class | 75 min |
| Stress testing and tail risk | In class | 75 min |
| Mitigation and committee decision | In class | 60 min |
| Final committee memo | Independent | 60–90 min |

### Short version

A two-hour adaptation can be run by supplying fitted models or selected completed notebook cells and focusing student time on:

- coverage interpretation;
- baseline pricing;
- scenario comparison;
- VaR/TVaR;
- mitigation choice; and
- committee recommendation.

The short format is intended to preserve the actuarial decision-making insight without requiring students to spend most of class writing routine simulation machinery.

---

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/brpuneet898/CAS_Teaching_Proposal_2026.git
cd CAS_Teaching_Proposal_2026
```

### 2. Create a Python environment

See [`setup_instructions.md`](setup_instructions.md) for the validated environment and complete platform-specific instructions.

Typical setup:

```bash
python -m venv .venv
```

Activate the environment, then install the packages listed in the setup instructions.

### 3. Student workflow

Students should begin with:

1. [`case_study.md`](case_study.md)
2. [`data_dictionary.md`](data_dictionary.md)
3. [`student_notebook.ipynb`](student_notebook.ipynb)

Keep `dataset.csv` in the same working directory as the notebook.

### 4. Instructor validation

Before class, instructors should:

1. run `data_script.py`;
2. confirm the generated data pass the built-in checks;
3. run `solution.ipynb` top to bottom;
4. compare outputs with `expected_output.md`; and
5. review `instructor_guide.md`.

---

## Assessment

The case is assessed using [`rubric.md`](rubric.md), which totals **exactly 100 points**.

The rubric evaluates:

- insurance coverage logic;
- data understanding;
- frequency modelling;
- severity modelling;
- pricing and premium adequacy;
- scenario and tail-risk analysis;
- mitigation decision-making;
- professional communication; and
- reproducibility/professional practice.

The design avoids applying a separate blanket penalty for an error that has already been scored within the relevant criterion unless it creates a genuinely distinct failure.

---

## Learning-objective and CAS competency alignment

The instructor materials use the following required structure:

| Learning objective | Student activity | Actuarial technique | Relevant CAS competency or syllabus area | Evidence of achievement |
|---|---|---|---|---|
| Translate environmental conditions into insured-loss mechanisms | Trace hazard-to-payment examples | Coverage and exposure definition | P&C insurance context / actuarial judgment | Correctly distinguishes stress, trigger, claim, covered loss, and payment |
| Model claim frequency | Fit and interpret an exposure-adjusted count model | Poisson/GLM frequency modelling | Predictive modelling / ratemaking | Valid model with exposure offset and actuarial interpretation |
| Model claim severity | Fit and interpret conditional severity | Gamma/lognormal severity modelling | Loss modelling / ratemaking | Positive conditional-severity model with meaningful interpretation |
| Price the portfolio | Combine frequency and severity | Expected loss and indicated premium | Ratemaking | Correct indicated premium and adequacy assessment |
| Measure tail risk | Simulate annual aggregate loss | Monte Carlo, VaR, TVaR | Risk management | Scenario-specific VaR/TVaR with uncertainty discussion |
| Evaluate mitigation | Compare feasible candidate portfolios | Budget-constrained risk comparison | Risk management / decision analysis | Defensible strategy choice based primarily on TVaR |
| Communicate recommendation | Prepare committee recommendation | Actuarial communication and judgment | Professional practice | Quantified recommendation with assumptions and limitations |

See `proposal.md` and `instructor_guide.md` for the complete mapping and teaching rationale.

---

## Reproducibility

The project is designed so instructors can regenerate the synthetic data from the documented V2 generator.

```bash
python data_script.py
```

The generator uses a fixed seed and built-in validation checks.

The reference notebook should be run from top to bottom without blanket warning suppression. Model warnings, where they occur, should be interpreted rather than hidden. Tail-risk conclusions should also be checked for Monte Carlo stability rather than treated as exact from one seed.

---

## Important limitations

ClimateTwin is a **teaching digital twin**, not an operational insurer digital twin or deployed catastrophe model.

It is deliberately simplified:

- all data are synthetic;
- environmental thresholds are instructional;
- coverage is a simplified teaching contract;
- the DGP is known to instructors;
- spatial dependence is not part of the required core case;
- compound trigger dependence is simplified;
- parameter/model uncertainty is only partially explored; and
- mitigation is evaluated over specified candidate strategies rather than through exhaustive global optimization.

Real-world implementation would require insurer data, legal/coverage review, external validation, governance, model-risk controls, and materially richer hazard and dependency modelling.

---

## Intended audience and prerequisites

The material is suitable for upper-level actuarial students, graduate students, or early-career actuarial learners.

Recommended prerequisites:

- basic probability and statistics;
- introductory general-insurance concepts;
- familiarity with frequency and severity;
- basic regression/GLM concepts; and
- introductory Python/Jupyter skills.

Students do not need prior climate-science expertise.

---

## Synthetic-data notice

All insurers, policies, locations, environmental measurements, claims, premiums, mitigation costs, and loss amounts in this repository are **synthetic and created for teaching purposes**.

They should not be interpreted as observations about any real insurer, insured, city, environmental event, or portfolio.

---

## Project status

This repository contains the **V2 classroom package** developed after faculty review. The V2 revision focuses on:

- internally consistent claim-level and annual loss mechanics;
- legitimate zero-paid claims;
- explicit deductible, policy-limit, and BI waiting-period treatment;
- a more stable frequency DGP;
- formal scenario definitions;
- model diagnostics and warning interpretation;
- Monte Carlo uncertainty around TVaR rankings;
- candidate-strategy language rather than unsupported global-optimum claims;
- a 100-point assessment rubric;
- reconciled full/short teaching formats; and
- regenerated benchmark outputs based on the corrected implementation.

Pilot results should only be added after an actual classroom or learner pilot has been completed; no pilot outcomes are assumed in this repository.

---

## License and reuse

This repository is currently presented as a teaching-material project. Users should check the repository's stated license, if/when one is added, before redistribution or adaptation.

---

## Repository

**GitHub:** https://github.com/brpuneet898/CAS_Teaching_Proposal_2026
