# ClimateTwin: An Actuarial Digital Twin for Air--Water Climate Risk Management

### (Proposed Teaching Material for the CAS Global Teaching Materials Innovation Challenge 2026)

## 1. Project Title and Summary

ClimateTwin: An Actuarial Digital Twin for Air--Water Climate Risk Management

ClimateTwin is a scenario-based actuarial teaching laboratory in which students manage a simulated commercial insurance portfolio exposed to two increasingly interconnected climate risks: deteriorating air quality and deteriorating water quality.

Rather than treating climate risk as a single catastrophe event, ClimateTwin teaches students to quantify a form of risk that develops through repeated environmental stress, threshold exceedances, spatial dependence, accumulation, and compound events. Students combine environmental measurements, exposure information, insurance losses, climate scenarios, and statistical models to estimate expected loss, tail risk, premiums, capital requirements, and intervention value.

The innovation is that students do not stop after building a predictive model. They operate an Actuarial Climate Risk Digital Twin.

They repeatedly move through the cycle:

Observe → Model → Price → Stress → Intervene → Reprice

Students therefore experience actuarial science as a real risk-management decision process rather than as a collection of isolated statistical techniques.

The final question of the case is: **Can an actuary convert environmental signals into financially meaningful risk signals early enough to change underwriting, pricing, capital allocation, and risk-mitigation decisions before losses materialize?**

# 2. Why This Problem Matters

Climate risk is often taught through hurricanes, floods, wildfires, or other clearly identifiable catastrophe events. These are important, but they represent only one form of climate-related risk.

A second class of risk is more gradual and much harder to price.

Consider a commercial insurer covering hospitals, manufacturing facilities, schools, warehouses, food-processing companies, hospitality businesses, and municipal infrastructure.

During an extreme climate period:

-   high temperatures and stagnant atmospheric conditions increase concentrations of PM2.5, ozone, and other pollutants;

-   drought reduces river flow and pollutant dilution;

-   flooding can introduce sewage, industrial contaminants, and agricultural runoff into water systems;

-   water treatment costs increase;

-   outdoor or industrial activity may be restricted;

-   businesses experience interruptions or remediation costs;

-   environmental liability claims can emerge;

-   worker and public exposure can increase;

-   multiple insured locations may experience losses simultaneously.

These risks are neither purely environmental nor purely financial.

They create an actuarial question: **How does a changing environmental state alter the probability, severity, dependence, and accumulation of insured losses?**

ClimateTwin makes this question measurable.

Students learn that a pollutant reading is not itself an insurance loss. The actuarial task is to construct the chain:

Climate Conditions can include - Environmental Hazard, Exposure, Vulnerability, Insurance Event, Claim Frequency and Severity, Portfolio Loss, and Premium and Capital Decision

This becomes the central intellectual framework of the exercise.

# 3. The Core Teaching Innovation: The Actuarial Climate Risk Digital Twin

Each student team receives a fictional insurer called AquaAir General Insurance with a portfolio of commercial properties distributed across several geographic zones.

Every zone contains a different combination of:

-   air-quality measurements;

-   water-quality measurements;

-   weather and climate variables;

-   population and industrial density;

-   insured property values;

-   business types;

-   historical claim frequency;

-   historical claim severity;

-   mitigation infrastructure.

The teaching environment represents the portfolio as a simplified digital twin.

Students initially see the insurer under Current Conditions.

They then progressively activate future or adverse scenarios such as:

### Scenario A: Heat and Air Stagnation

Extreme heat and low wind increase PM2.5 and ozone concentrations.

Students investigate whether claim frequency rises non-linearly after environmental thresholds are crossed.

### Scenario B: Drought and Water Stress

Reduced water availability increases contaminant concentration and pressure on industrial and municipal water systems.

### Scenario C: Extreme Rainfall and Contamination

Heavy rainfall creates runoff and contamination events, producing possible property, business-interruption, cleanup, and liability losses.

### Scenario D: Compound Air--Water Stress

A prolonged climate episode produces poor air quality and deteriorating water quality simultaneously.

This is the most important scenario.

Students discover that:

$$ Risk(Air + Water) \neq Risk(Air) + Risk(Water) $$

because exposures can be correlated and losses may accumulate geographically and temporally.

The digital twin allows students to change assumptions and immediately observe how the insurer\'s expected loss, premium adequacy and tail-risk position change.

# 4. Learning Objectives

At the end of the exercise, students should be able to:

### 1. Translate climate information into actuarial variables

Students distinguish between:

-   hazard,

-   exposure,

-   vulnerability,

-   event,

-   claim,

-   and financial loss.

This prevents the common mistake of treating an environmental indicator directly as an insurance outcome.

### 2. Model insurance frequency and severity

Students model claim frequency using approaches such as:

-   Poisson regression,

-   Negative Binomial regression,

-   Generalized Linear Models,

-   nonlinear environmental-response functions.

Claim severity can be modelled using Gamma, Lognormal, Pareto, or related loss distributions.

### 3. Identify environmental thresholds

Students investigate whether loss behaviour changes when measures such as PM2.5 or water contamination cross critical levels.

This introduces nonlinear risk relationships rather than assuming that climate risk increases uniformly.

### 4. Measure compound and dependent risk

Students examine whether adverse air- and water-quality conditions occur together and how dependence alters aggregate portfolio losses.

More advanced students may use:

-   correlation structures,

-   copulas,

-   spatial dependence models,

-   or multivariate simulation.

### 5. Quantify tail risk

Students estimate:

-   expected annual loss,

-   loss exceedance probabilities,

-   Value-at-Risk,

-   Tail Value-at-Risk,

-   probable maximum or stress losses.

### 6. Translate modelling results into insurance decisions

Students use results to recommend changes to:

-   underwriting,

-   premiums,

-   deductibles,

-   limits,

-   geographic concentration,

-   risk engineering,

-   mitigation incentives,

-   and capital allocation.

### 7. Evaluate mitigation economically

Students compare the cost of interventions against expected avoided losses.

They therefore move beyond: "Which region is risky?"

toward the actuarial question: "Where does one dollar of risk mitigation generate the greatest reduction in expected and tail loss?"

# 5. Suggested Curriculum Structure

The teaching material is designed as four classroom sessions plus one Climate Risk Lab.

Approximate total teaching time: 6--8 hours, adaptable for undergraduate, graduate, or professional actuarial courses.

## Session 1 --- From Environmental Data to Insurable Risk

Students are introduced to the AquaAir insurance portfolio.

They learn the distinction between climate hazard, environmental condition, exposure, vulnerability, and insured loss.

Teams examine maps and summary statistics showing regional air and water conditions.

The session concludes with a challenge: Which locations would you expect to generate the largest insurance loss, and why?

Students make an initial judgement before modelling.

Their answers are saved for comparison with later results.

## Session 2 --- Building the Environmental Loss Function

Students merge environmental and insurance data.

They investigate relationships such as:

$$ ClaimFrequency = f(PM_{2.5}, Ozone, Temperature, WaterQuality, Exposure) $$

and

$$ ClaimSeverity = g(Hazard, Industry, PropertyValue, Vulnerability) $$

Students estimate frequency and severity separately and then combine them:

$$ E(Loss)=E(N)\times E(X) $$

The emphasis is not simply on finding the best statistical fit.

Students must explain: What does the model imply about how climate conditions become insurance losses?

## Session 3 --- Compound Risk, Dependence and Tail Loss

Students now discover a limitation in their initial model.

Air and water risks cannot always be modelled independently.

They simulate correlated environmental conditions and generate a portfolio loss distribution using Monte Carlo simulation.

Students calculate:

$$ VaR_{99} $$

and

$$ TVaR_{99} $$

and compare them across scenarios.

This introduces a powerful actuarial lesson: An insurer can appear adequately priced under average conditions while remaining dangerously exposed to correlated climate stress.

## Session 4 --- Underwriting and Climate Risk Intervention

Students become the insurer\'s Climate Risk Committee.

They receive a limited Climate Resilience Budget.

Possible interventions might include:

-   improved water filtration,

-   backup water systems,

-   pollution-control technology,

-   air-filtration upgrades,

-   operational shutdown protocols,

-   environmental monitoring,

-   reduced geographic concentration,

-   policy deductible changes,

-   premium adjustments,

-   risk-engineering inspections.

Every intervention has a cost and an assumed effect on risk.

Students cannot select everything.

They must determine the portfolio of interventions producing the greatest risk reduction subject to a budget constraint.

A simplified optimisation can be expressed as:

$$ \max \frac{\text{Expected Loss Reduction}}{\text{Mitigation Cost}} $$

or, for advanced classes:

$$ \min TVaR_{99} $$

subject to:

$$ \sum InterventionCost_i \leq Budget $$

This transforms the exercise from climate-risk measurement into actuarial climate-risk management.

# 6. Climate Risk Lab --- The "Aha!" Moment

The final laboratory is designed to produce the key teaching experience.

Teams press Run Climate Stress Test.

The portfolio is simulated thousands of times under:

1.  Baseline environmental conditions

2.  Severe air-quality stress

3.  Severe water-quality stress

4.  Compound air--water stress

5.  Compound stress after mitigation

Students compare distributions rather than single-point estimates.

They may discover, for example, that the region generating the highest average loss is not necessarily the region generating the greatest contribution to portfolio tail risk.

They may also discover that the intervention producing the greatest reduction in average loss does not necessarily produce the greatest reduction in TVaR.

This creates the central actuarial insight: Managing climate risk is not simply predicting where environmental conditions will worsen. It is deciding which environmental changes matter financially, where losses accumulate, how extreme outcomes behave, and which interventions change that distribution most efficiently.

# 7. Datasets and Teaching Tools

The case can be distributed using compact CSV datasets and a ready-to-run Python or R notebook.

Potential variables include:

### Environmental Data

-   PM2.5

-   PM10

-   ozone

-   temperature

-   humidity

-   rainfall

-   drought indicator

-   water pH

-   dissolved oxygen

-   turbidity

-   conductivity

-   selected contamination indicators

### Insurance Portfolio Data

-   location

-   occupancy or industry

-   insured value

-   policy limit

-   deductible

-   historical claims

-   claim type

-   claim amount

### Geographic and Exposure Data

-   industrial density

-   proximity to water

-   climate zone

-   population density

-   vulnerability score

Public environmental data can be used where appropriate, while an instructional synthetic insurance portfolio avoids privacy and commercial-data restrictions.

A simplified version could operate entirely in Excel.

The full version can use Python/Jupyter or R.

# 8. Guiding Questions for Students

Students progress through questions such as:

1.  Which environmental variables demonstrate the strongest relationship with claim frequency?

2.  Does deterioration in environmental quality create a linear increase in risk, or are there identifiable thresholds?

3.  Are claim frequency and claim severity affected in the same manner?

4.  What happens if air and water risks are assumed to be independent?

5.  How does the result change when dependence is introduced?

6.  Which geographic areas contribute most to expected loss?

7.  Which contribute most to TVaR?

8.  Should the insurer increase premiums, reduce limits, introduce deductibles, require mitigation, or withdraw capacity?

9.  Which mitigation strategy creates the greatest expected loss reduction per unit of expenditure?

10. After intervention, is the portfolio merely safer on average, or is its tail also safer?

The final question asks each team to defend a recommendation to the insurer\'s hypothetical board.

# 9. Assessment Strategy

Student performance can be evaluated across five dimensions.

### Actuarial Modelling

Correct selection and application of frequency, severity, aggregate-loss, and tail-risk techniques.

### Statistical Reasoning

Ability to recognize nonlinearity, uncertainty, dependence, model limitations, and potential confounding.

### Climate-Risk Interpretation

Ability to convert environmental indicators into meaningful actuarial risk mechanisms.

### Insurance Decision-Making

Quality of pricing, underwriting, capital, and mitigation recommendations.

### Communication

Ability to explain a technically sophisticated climate-risk problem to a non-technical insurance executive.

The final deliverable can be a short Climate Risk Committee Report rather than a traditional examination.

Teams must recommend: Insure / Reprice / Mitigate / Restrict / Monitor

for selected parts of the portfolio and defend each decision quantitatively.

# 10. Suggested Presentation Materials and Instructor Package

The complete classroom package would include:

-   instructor slide deck;

-   student case document;

-   environmental dataset;

-   synthetic insurance portfolio dataset;

-   Jupyter/R analytical notebook;

-   ClimateTwin scenario simulator;

-   student worksheet;

-   Climate Risk Committee decision sheet;

-   solution notebook;

-   assessment rubric;

-   teaching notes.

A lightweight interactive dashboard could visually display:

Environmental State → Exposure → Expected Loss → VaR/TVaR → Premium → Capital → Mitigation

allowing students to alter assumptions and immediately observe their consequences.
