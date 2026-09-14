"""
ClimateTwin V2 synthetic data generator
=======================================

Single source of truth for the ClimateTwin teaching dataset.

Running
-------
    python data_script.py

Outputs
-------
    dataset.csv              Student-facing 750-row policy-location-year table.
    claim_level_data.csv     Instructor-side supplementary claim-level table.

Design principles
-----------------
1. Environmental deterioration is not itself a claim.
2. A qualifying insured trigger must exist before a claim can occur.
3. Claim severity is generated at CLAIM level, not policy-year level.
4. Ground-up, covered, and paid loss are separate quantities.
5. BI waiting period is applied only to the BI component.
6. The deductible is applied exactly once per claim, after coverage adjustment.
7. The per-claim policy limit is applied after the deductible.
8. Legitimate zero-paid claims are retained (e.g. covered loss <= deductible).
9. Scenario transformations are explicit and use common random numbers.
10. Air and water trigger draws are conditionally independent given covariates;
    the compound scenario therefore does NOT model residual/copula dependence.

The generator deliberately uses only the Python standard library. Random values
come from SHA-256 keyed streams, making the output deterministic for a fixed
SEED and stable regardless of row-generation order.
"""

from __future__ import annotations

import csv
import hashlib
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SEED = "ClimateTwin-CAS-2026-v2"
N_LOCATIONS = 250
YEARS = (2024, 2025, 2026)
BASE_DIR = Path(__file__).resolve().parent
DATASET_FILE = BASE_DIR / "dataset.csv"
CLAIM_FILE = BASE_DIR / "claim_level_data.csv"

SCENARIOS = ("Baseline", "Air stress", "Water stress", "Compound stress")

# Transparent scenario rules used throughout the package.
SCENARIO_RULES = {
    "Baseline": {
        "pm25_add": 0.0,
        "ozone_add": 0.0,
        "turbidity_mult": 1.0,
        "wqi_add": 0.0,
        "compound_freq_log_effect": 0.0,
        "compound_severity_mult": 1.0,
    },
    "Air stress": {
        "pm25_add": 15.0,
        "ozone_add": 10.0,
        "turbidity_mult": 1.0,
        "wqi_add": 0.0,
        "compound_freq_log_effect": 0.0,
        "compound_severity_mult": 1.0,
    },
    "Water stress": {
        "pm25_add": 0.0,
        "ozone_add": 0.0,
        "turbidity_mult": 1.60,
        "wqi_add": -15.0,
        "compound_freq_log_effect": 0.0,
        "compound_severity_mult": 1.0,
    },
    "Compound stress": {
        "pm25_add": 15.0,
        "ozone_add": 10.0,
        "turbidity_mult": 1.60,
        "wqi_add": -15.0,
        # Non-additive effect activated only when both insured triggers are active.
        "compound_freq_log_effect": 0.28,
        "compound_severity_mult": 1.18,
    },
}

REGIONS = ("Northgate", "Riverbend", "Central Metro", "Coastview", "Drylands")
OCCUPANCIES = ("Hospital", "Manufacturing", "Food Processing")

REGION_PROFILE = {
    "Northgate": {
        "pm25": 31.0, "ozone": 60.0, "turbidity": 2.4, "wqi": 74.0,
        "temperature": 23.0, "rainfall": 920.0, "drought": 0.24,
        "premium_factor": 1.00,
    },
    "Riverbend": {
        "pm25": 27.0, "ozone": 56.0, "turbidity": 5.4, "wqi": 61.0,
        "temperature": 25.0, "rainfall": 1280.0, "drought": 0.18,
        "premium_factor": 1.04,
    },
    "Central Metro": {
        "pm25": 44.0, "ozone": 74.0, "turbidity": 3.1, "wqi": 69.0,
        "temperature": 27.0, "rainfall": 780.0, "drought": 0.31,
        "premium_factor": 1.08,
    },
    "Coastview": {
        "pm25": 24.0, "ozone": 52.0, "turbidity": 4.7, "wqi": 66.0,
        "temperature": 28.0, "rainfall": 1520.0, "drought": 0.12,
        "premium_factor": 1.02,
    },
    "Drylands": {
        "pm25": 38.0, "ozone": 68.0, "turbidity": 4.2, "wqi": 63.0,
        "temperature": 31.0, "rainfall": 510.0, "drought": 0.67,
        "premium_factor": 1.10,
    },
}

# Frequency uses bounded continuous hazard scores rather than large direct
# coefficients on raw environmental measurements. Trigger flags determine
# coverage eligibility, while hazard scores determine frequency among eligible
# records. This avoids the unstable V1 mechanism.
FREQ_OCC = {
    "Hospital": 0.10,
    "Manufacturing": 0.24,
    "Food Processing": 0.18,
}
FREQ_BETA = {
    "intercept": -0.85,
    "air_score": 0.24,
    "water_score": 0.30,
    "temperature_score": 0.08,
    "drought_score": 0.12,
    "wet_score": 0.06,
    "air_filtration": -0.24,
    "water_treatment": -0.30,
    "bcp": -0.18,
}

BASE_RATE = {
    "Hospital": 0.0033,
    "Manufacturing": 0.00285,
    "Food Processing": 0.00305,
}

SEVERITY_OCC = {
    "Hospital": 1.30,
    "Manufacturing": 1.15,
    "Food Processing": 1.00,
}
SEVERITY_TRIGGER = {
    "Air": 0.90,
    "Water": 1.10,
    "Compound": 1.42,
}
SEV_SIGMA_REMEDIATION = 0.62
SEV_SIGMA_BI_DAILY = 0.58


def _digest(*parts: object) -> bytes:
    key = "|".join([SEED, *map(str, parts)]).encode("utf-8")
    return hashlib.sha256(key).digest()


def u01(*parts: object) -> float:
    """Deterministic U(0,1), based on the first 64 SHA-256 bits."""
    x = int.from_bytes(_digest(*parts)[:8], "big")
    return (x + 0.5) / (2**64)


def normal(*parts: object) -> float:
    """Deterministic standard normal via Box-Muller."""
    u1 = max(u01(*parts, "u1"), 1e-15)
    u2 = u01(*parts, "u2")
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def choose(options: Tuple, probs: Tuple[float, ...], *parts: object):
    x = u01(*parts)
    c = 0.0
    for opt, p in zip(options, probs):
        c += p
        if x <= c:
            return opt
    return options[-1]


def poisson(lam: float, *parts: object) -> int:
    """Knuth Poisson sampler; lambdas are intentionally small in this case."""
    if not math.isfinite(lam) or lam < 0.0:
        raise ValueError(f"Invalid Poisson mean: {lam}")
    if lam == 0.0:
        return 0
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= u01(*parts, "pois", k)
    return k - 1


def clamp(x: float, lo: float, hi: float) -> float:
    return min(max(x, lo), hi)


def logistic(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def round_to(x: float, unit: int) -> int:
    return int(round(x / unit) * unit)


def lognormal_with_mean(mean_value: float, sigma: float, *parts: object) -> float:
    """Positive lognormal draw parameterized by arithmetic mean."""
    if mean_value <= 0 or sigma <= 0 or not math.isfinite(mean_value):
        raise ValueError("Lognormal mean and sigma must be positive and finite.")
    z = normal(*parts)
    return mean_value * math.exp(sigma * z - 0.5 * sigma**2)


def make_locations() -> List[dict]:
    locations: List[dict] = []
    region_probs = (0.18, 0.20, 0.25, 0.18, 0.19)
    occ_probs = (0.25, 0.42, 0.33)

    for loc_num in range(1, N_LOCATIONS + 1):
        location_id = f"LOC{loc_num:03d}"
        region = choose(REGIONS, region_probs, location_id, "region")
        occupancy = choose(OCCUPANCIES, occ_probs, location_id, "occupancy")

        size_factor = math.exp(0.38 * normal(location_id, "size"))
        base_value = {
            "Hospital": 28_000_000,
            "Manufacturing": 18_000_000,
            "Food Processing": 13_000_000,
        }[occupancy]
        insured_value_base = clamp(base_value * size_factor, 4_000_000, 85_000_000)

        rp = REGION_PROFILE[region]
        air_p = 0.34 + (0.16 if occupancy == "Hospital" else 0.0) + (0.12 if rp["pm25"] >= 38 else 0.0)
        water_p = 0.31 + (0.16 if occupancy == "Food Processing" else 0.0) + (0.12 if rp["wqi"] <= 63 else 0.0)
        bcp_p = 0.38 + (0.18 if occupancy == "Hospital" else 0.08 if occupancy == "Manufacturing" else 0.0)

        air_filtration = int(u01(location_id, "air_mit") < min(air_p, 0.85))
        water_treatment = int(u01(location_id, "water_mit") < min(water_p, 0.85))
        bcp = int(u01(location_id, "bcp_mit") < min(bcp_p, 0.85))

        air_upgrade_cost = 0 if air_filtration else round_to(
            52_000 + 0.0018 * insured_value_base + 12_000 * u01(location_id, "air_cost"), 1000
        )
        water_upgrade_cost = 0 if water_treatment else round_to(
            65_000 + 0.0022 * insured_value_base + 15_000 * u01(location_id, "water_cost"), 1000
        )
        bcp_upgrade_cost = 0 if bcp else round_to(
            30_000 + 0.0009 * insured_value_base + 9_000 * u01(location_id, "bcp_cost"), 1000
        )

        locations.append({
            "location_id": location_id,
            "region": region,
            "occupancy": occupancy,
            "insured_value_base": insured_value_base,
            "air_filtration": air_filtration,
            "water_treatment": water_treatment,
            "business_continuity_plan": bcp,
            "air_filtration_upgrade_cost": air_upgrade_cost,
            "water_treatment_upgrade_cost": water_upgrade_cost,
            "bcp_upgrade_cost": bcp_upgrade_cost,
        })
    return locations


def make_policy_state(loc: dict, year: int) -> dict:
    """Create policy terms and unstressed environmental state; no claims yet."""
    loc_id = loc["location_id"]
    region = loc["region"]
    occ = loc["occupancy"]
    rp = REGION_PROFILE[region]
    yr_idx = year - 2024

    exposure = clamp(0.68 + 0.36 * u01(loc_id, year, "exposure"), 0.68, 1.00)
    insured_value = loc["insured_value_base"] * (1.035 ** yr_idx) * (0.97 + 0.06 * u01(loc_id, year, "value_noise"))
    insured_value = round_to(insured_value, 10_000)

    limit_ratio = choose((0.25, 0.35, 0.50), (0.25, 0.45, 0.30), loc_id, year, "limit_ratio")
    policy_limit = round_to(insured_value * limit_ratio, 10_000)

    deductible_options = {
        "Hospital": (50_000, 75_000, 100_000),
        "Manufacturing": (40_000, 60_000, 80_000),
        "Food Processing": (25_000, 40_000, 60_000),
    }[occ]
    deductible = choose(deductible_options, (0.35, 0.45, 0.20), loc_id, year, "deductible")
    waiting_days = choose((1, 2, 3), (0.35, 0.45, 0.20), loc_id, year, "waiting")

    # Environmental conditions are generated independently of claim outcomes.
    pm25 = clamp(rp["pm25"] + 1.8 * yr_idx + 5.2 * normal(loc_id, year, "pm25"), 8.0, 78.0)
    ozone = clamp(rp["ozone"] + 1.2 * yr_idx + 7.0 * normal(loc_id, year, "ozone"), 28.0, 105.0)
    turbidity = clamp(rp["turbidity"] + 0.20 * yr_idx + 1.15 * normal(loc_id, year, "turbidity"), 0.4, 11.5)
    wqi = clamp(rp["wqi"] - 1.1 * yr_idx + 6.0 * normal(loc_id, year, "wqi"), 35.0, 92.0)
    temperature = clamp(rp["temperature"] + 0.45 * yr_idx + 2.2 * normal(loc_id, year, "temp"), 16.0, 39.0)
    rainfall = clamp(rp["rainfall"] * (0.92 + 0.18 * u01(loc_id, year, "rain")) + 90.0 * normal(loc_id, year, "rain_n"), 240.0, 2100.0)
    drought = clamp(rp["drought"] + 0.035 * yr_idx + 0.10 * normal(loc_id, year, "drought"), 0.02, 0.95)

    mitigation_credit = 1.0 - 0.06 * loc["air_filtration"] - 0.06 * loc["water_treatment"] - 0.04 * loc["business_continuity_plan"]
    rate = BASE_RATE[occ] * REGION_PROFILE[region]["premium_factor"] * mitigation_credit
    premium_noise = 0.94 + 0.12 * u01(loc_id, year, "premium_noise")
    current_premium = round_to(insured_value * rate * exposure * premium_noise, 100)

    return {
        "policy_id": f"POL{loc_id[3:]}-{year}",
        "location_id": loc_id,
        "year": year,
        "region": region,
        "occupancy": occ,
        "exposure_years": round(exposure, 3),
        "insured_value": insured_value,
        "policy_limit": policy_limit,
        "deductible": deductible,
        "bi_waiting_period_days": waiting_days,
        "current_premium": current_premium,
        "pm25": pm25,
        "ozone": ozone,
        "turbidity": turbidity,
        "water_quality_index": wqi,
        "temperature_c": temperature,
        "annual_rainfall_mm": rainfall,
        "drought_indicator": drought,
        "air_filtration": loc["air_filtration"],
        "water_treatment": loc["water_treatment"],
        "business_continuity_plan": loc["business_continuity_plan"],
        "air_filtration_upgrade_cost": loc["air_filtration_upgrade_cost"],
        "water_treatment_upgrade_cost": loc["water_treatment_upgrade_cost"],
        "bcp_upgrade_cost": loc["bcp_upgrade_cost"],
    }


def build_policy_states() -> List[dict]:
    return [make_policy_state(loc, year) for loc in make_locations() for year in YEARS]


def apply_scenario(state: dict, scenario: str) -> dict:
    """Apply a documented scenario transformation to environmental variables."""
    if scenario not in SCENARIO_RULES:
        raise ValueError(f"Unknown scenario {scenario!r}; choose from {SCENARIOS}.")
    rule = SCENARIO_RULES[scenario]
    x = dict(state)
    x["pm25"] = clamp(state["pm25"] + rule["pm25_add"], 0.0, 120.0)
    x["ozone"] = clamp(state["ozone"] + rule["ozone_add"], 0.0, 150.0)
    x["turbidity"] = clamp(state["turbidity"] * rule["turbidity_mult"], 0.0, 25.0)
    x["water_quality_index"] = clamp(state["water_quality_index"] + rule["wqi_add"], 0.0, 100.0)
    x["scenario"] = scenario
    return x


def hazard_scores(x: dict) -> Tuple[float, float]:
    """Bounded continuous scores used in frequency/trigger probabilities."""
    air = (
        max(x["pm25"] - 25.0, 0.0) / 20.0
        + max(x["ozone"] - 55.0, 0.0) / 35.0
    )
    water = (
        max(x["turbidity"] - 3.0, 0.0) / 5.0
        + max(70.0 - x["water_quality_index"], 0.0) / 25.0
    )
    return clamp(air, 0.0, 3.0), clamp(water, 0.0, 3.0)


def insured_triggers(x: dict) -> Tuple[int, int, int, str]:
    """
    Draw annual insured-trigger eligibility.

    IMPORTANT LIMITATION: air and water draws use separate deterministic streams
    and are conditionally independent given observed covariates. Residual
    dependence is not modelled; compound effects are introduced only after both
    triggers are active.
    """
    air_stress = int(x["pm25"] >= 35.0 or x["ozone"] >= 70.0)
    water_stress = int(x["turbidity"] >= 5.0 or x["water_quality_index"] <= 60.0)
    air_score, water_score = hazard_scores(x)
    occ = x["occupancy"]

    air_lp = -2.05 + 0.92 * air_score + (0.30 if occ == "Hospital" else 0.12 if occ == "Manufacturing" else 0.05)
    air_lp -= 0.48 * x["air_filtration"] + 0.18 * x["business_continuity_plan"]

    water_lp = -2.10 + 1.00 * water_score + (0.35 if occ == "Food Processing" else 0.18 if occ == "Hospital" else 0.10)
    water_lp -= 0.52 * x["water_treatment"] + 0.15 * x["business_continuity_plan"]

    # No insured trigger is possible unless the corresponding screening stress
    # threshold is crossed. Stress alone still does not guarantee a trigger.
    air_p = logistic(air_lp) if air_stress else 0.0
    water_p = logistic(water_lp) if water_stress else 0.0

    # Common random numbers: scenario name intentionally omitted from streams.
    air_trigger = int(u01(x["location_id"], x["year"], "air_trigger_v2") < air_p)
    water_trigger = int(u01(x["location_id"], x["year"], "water_trigger_v2") < water_p)
    compound = int(air_trigger and water_trigger)

    if compound:
        trigger_type = "Compound"
    elif air_trigger:
        trigger_type = "Air"
    elif water_trigger:
        trigger_type = "Water"
    else:
        trigger_type = "None"
    return air_trigger, water_trigger, compound, trigger_type


def frequency_mean(x: dict, air_trigger: int, water_trigger: int, compound: int) -> float:
    """Stable exposure-adjusted Poisson mean for covered claim counts."""
    if not (air_trigger or water_trigger):
        return 0.0

    air_score, water_score = hazard_scores(x)
    temp_score = clamp(max(x["temperature_c"] - 25.0, 0.0) / 10.0, 0.0, 1.5)
    drought_score = clamp(x["drought_indicator"], 0.0, 1.0)
    wet_score = clamp(max(x["annual_rainfall_mm"] - 1000.0, 0.0) / 800.0, 0.0, 1.5)

    eta = (
        FREQ_BETA["intercept"]
        + FREQ_OCC[x["occupancy"]]
        + FREQ_BETA["air_score"] * air_score * air_trigger
        + FREQ_BETA["water_score"] * water_score * water_trigger
        + FREQ_BETA["temperature_score"] * temp_score
        + FREQ_BETA["drought_score"] * drought_score
        + FREQ_BETA["wet_score"] * wet_score
        + FREQ_BETA["air_filtration"] * x["air_filtration"] * air_trigger
        + FREQ_BETA["water_treatment"] * x["water_treatment"] * water_trigger
        + FREQ_BETA["bcp"] * x["business_continuity_plan"]
        + SCENARIO_RULES[x["scenario"]]["compound_freq_log_effect"] * compound
    )

    # Bound eta defensively: keeps lambda finite and avoids pathological counts.
    eta = clamp(eta, -4.0, 0.35)
    lam = x["exposure_years"] * math.exp(eta)
    if not math.isfinite(lam) or lam < 0:
        raise AssertionError("Non-finite frequency mean.")
    return lam


def claim_type_for_sequence(x: dict, seq: int, air_trigger: int, water_trigger: int) -> str:
    if air_trigger and not water_trigger:
        return "Air"
    if water_trigger and not air_trigger:
        return "Water"
    if air_trigger and water_trigger:
        q = u01(x["location_id"], x["year"], "claim_type", seq)
        if q < 0.30:
            return "Air"
        if q < 0.62:
            return "Water"
        return "Compound"
    raise AssertionError("A claim cannot be assigned when no insured trigger is active.")


def simulate_claim(x: dict, seq: int, claim_type: str) -> dict:
    """Generate one claim and apply coverage terms in the documented order."""
    value_mult = (x["insured_value"] / 15_000_000.0) ** 0.32
    air_score, water_score = hazard_scores(x)
    trigger_mult = SEVERITY_TRIGGER[claim_type]
    if x["scenario"] == "Compound stress" and claim_type == "Compound":
        trigger_mult *= SCENARIO_RULES["Compound stress"]["compound_severity_mult"]

    relevant_air = claim_type in ("Air", "Compound")
    relevant_water = claim_type in ("Water", "Compound")

    mitigation_mult = 1.0
    if relevant_air and x["air_filtration"]:
        mitigation_mult *= 0.80
    if relevant_water and x["water_treatment"]:
        mitigation_mult *= 0.76
    if x["business_continuity_plan"]:
        mitigation_mult *= 0.90

    climate_mult = 1.0 + 0.05 * air_score * relevant_air + 0.06 * water_score * relevant_water

    remediation_mean = 52_000.0 * SEVERITY_OCC[x["occupancy"]] * trigger_mult * value_mult * climate_mult * mitigation_mult
    remediation_ground = max(
        2_500.0,
        lognormal_with_mean(remediation_mean, SEV_SIGMA_REMEDIATION, x["location_id"], x["year"], "remediation", seq),
    )

    # BI duration is claim-level. Waiting period removes the first N days from
    # the covered BI component, rather than multiplying all claim severity.
    duration_base = 0.8 + 1.10 * (claim_type == "Water") + 1.65 * (claim_type == "Compound")
    duration_base += 0.35 * air_score * relevant_air + 0.45 * water_score * relevant_water
    if x["business_continuity_plan"]:
        duration_base *= 0.75
    interruption_days = int(clamp(round(duration_base + 1.8 * u01(x["location_id"], x["year"], "duration", seq)), 0, 12))

    daily_bi_mean = 24_000.0 * SEVERITY_OCC[x["occupancy"]] * value_mult * trigger_mult
    if x["business_continuity_plan"]:
        daily_bi_mean *= 0.82
    daily_bi_loss = lognormal_with_mean(
        daily_bi_mean,
        SEV_SIGMA_BI_DAILY,
        x["location_id"], x["year"], "bi_daily", seq,
    )

    ground_up_bi = daily_bi_loss * interruption_days
    covered_bi_days = max(interruption_days - int(x["bi_waiting_period_days"]), 0)
    covered_bi = daily_bi_loss * covered_bi_days
    waiting_met = int(covered_bi_days > 0)

    # Ground-up = full economic loss from the covered event before coverage terms.
    ground_up = remediation_ground + ground_up_bi

    # Covered = covered remediation/extra expense + BI after waiting period.
    covered = remediation_ground + covered_bi

    # Financial terms: deductible exactly once, then per-claim policy limit.
    after_deductible = max(covered - x["deductible"], 0.0)
    paid = min(after_deductible, x["policy_limit"])

    return {
        "claim_id": f"{x['policy_id']}-C{seq:02d}",
        "policy_id": x["policy_id"],
        "location_id": x["location_id"],
        "year": x["year"],
        "claim_sequence": seq,
        "claim_trigger_type": claim_type,
        "interruption_days": interruption_days,
        "bi_waiting_period_days": x["bi_waiting_period_days"],
        "bi_waiting_period_met_flag": waiting_met,
        "ground_up_remediation_loss": round(remediation_ground, 2),
        "ground_up_bi_loss": round(ground_up_bi, 2),
        "ground_up_loss": round(ground_up, 2),
        "covered_bi_loss": round(covered_bi, 2),
        "covered_loss": round(covered, 2),
        "deductible": x["deductible"],
        "loss_after_deductible": round(after_deductible, 2),
        "policy_limit": x["policy_limit"],
        "paid_loss": round(paid, 2),
    }


def simulate_policy_year(state: dict, scenario: str = "Baseline") -> Tuple[dict, List[dict]]:
    x = apply_scenario(state, scenario)
    air_trigger, water_trigger, compound_trigger, trigger_type = insured_triggers(x)
    lam = frequency_mean(x, air_trigger, water_trigger, compound_trigger)
    claim_count = poisson(lam, x["location_id"], x["year"], "claim_count_v2")

    claims: List[dict] = []
    for seq in range(1, claim_count + 1):
        ctype = claim_type_for_sequence(x, seq, air_trigger, water_trigger)
        claims.append(simulate_claim(x, seq, ctype))

    agg_ground = round(sum(c["ground_up_loss"] for c in claims), 2)
    agg_covered = round(sum(c["covered_loss"] for c in claims), 2)
    agg_paid = round(sum(c["paid_loss"] for c in claims), 2)
    waiting_met_any = int(any(c["bi_waiting_period_met_flag"] for c in claims))

    row = {
        "policy_id": x["policy_id"],
        "location_id": x["location_id"],
        "year": x["year"],
        "region": x["region"],
        "occupancy": x["occupancy"],
        "exposure_years": x["exposure_years"],
        "insured_value": x["insured_value"],
        "policy_limit": x["policy_limit"],
        "deductible": x["deductible"],
        "bi_waiting_period_days": x["bi_waiting_period_days"],
        "current_premium": x["current_premium"],
        "pm25": round(x["pm25"], 1),
        "ozone": round(x["ozone"], 1),
        "turbidity": round(x["turbidity"], 2),
        "water_quality_index": round(x["water_quality_index"], 1),
        "temperature_c": round(x["temperature_c"], 1),
        "annual_rainfall_mm": round(x["annual_rainfall_mm"], 1),
        "drought_indicator": round(x["drought_indicator"], 3),
        "air_stress_flag": int(x["pm25"] >= 35.0 or x["ozone"] >= 70.0),
        "water_stress_flag": int(x["turbidity"] >= 5.0 or x["water_quality_index"] <= 60.0),
        "air_trigger_flag": air_trigger,
        "water_trigger_flag": water_trigger,
        "compound_trigger_flag": compound_trigger,
        "insured_trigger_type": trigger_type,
        "bi_waiting_period_met_flag": waiting_met_any,
        "air_filtration": x["air_filtration"],
        "water_treatment": x["water_treatment"],
        "business_continuity_plan": x["business_continuity_plan"],
        "air_filtration_upgrade_cost": x["air_filtration_upgrade_cost"],
        "water_treatment_upgrade_cost": x["water_treatment_upgrade_cost"],
        "bcp_upgrade_cost": x["bcp_upgrade_cost"],
        "claim_count": claim_count,
        "aggregate_ground_up_loss": agg_ground,
        "aggregate_covered_loss": agg_covered,
        "aggregate_paid_loss": agg_paid,
    }
    return row, claims


def generate_dataset(scenario: str = "Baseline") -> Tuple[List[dict], List[dict]]:
    rows: List[dict] = []
    claims: List[dict] = []
    for state in build_policy_states():
        row, row_claims = simulate_policy_year(state, scenario)
        rows.append(row)
        claims.extend(row_claims)
    return rows, claims


def write_csv(rows: List[dict], output_file: Path) -> None:
    if not rows:
        raise ValueError("Cannot write an empty table.")
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validate(rows: List[dict], claims: List[dict]) -> Dict[str, int]:
    """Fail-fast validation of all V2 data-contract invariants."""
    assert len(rows) == N_LOCATIONS * len(YEARS) == 750
    assert len({r["policy_id"] for r in rows}) == len(rows)
    assert all(0.0 < r["exposure_years"] <= 1.0 for r in rows)
    assert all(isinstance(r["claim_count"], int) and r["claim_count"] >= 0 for r in rows)
    assert all(math.isfinite(float(r["aggregate_ground_up_loss"])) for r in rows)
    assert all(math.isfinite(float(r["aggregate_covered_loss"])) for r in rows)
    assert all(math.isfinite(float(r["aggregate_paid_loss"])) for r in rows)
    assert all(r["aggregate_ground_up_loss"] + 0.02 >= r["aggregate_covered_loss"] >= 0 for r in rows)
    assert all(r["aggregate_covered_loss"] + 0.02 >= r["aggregate_paid_loss"] >= 0 for r in rows)
    assert all((r["claim_count"] == 0) or (r["insured_trigger_type"] != "None") for r in rows)
    assert all((r["insured_trigger_type"] != "None") or (r["claim_count"] == 0) for r in rows)

    # Claim-level positive severity target: valid for Gamma/Lognormal modelling.
    assert all(math.isfinite(c["covered_loss"]) and c["covered_loss"] > 0 for c in claims)
    assert all(math.isfinite(c["ground_up_loss"]) and c["ground_up_loss"] > 0 for c in claims)

    # BI waiting-period rule is exact and internally checkable.
    for c in claims:
        expected_met = int(c["interruption_days"] > c["bi_waiting_period_days"])
        assert c["bi_waiting_period_met_flag"] == expected_met
        if not expected_met:
            assert abs(c["covered_bi_loss"]) <= 0.01
        assert c["ground_up_loss"] + 0.02 >= c["covered_loss"] > 0

        # Deductible exactly once; limit then applies to the post-deductible amount.
        expected_after_ded = max(c["covered_loss"] - c["deductible"], 0.0)
        assert abs(c["loss_after_deductible"] - round(expected_after_ded, 2)) <= 0.02
        expected_paid = min(c["loss_after_deductible"], c["policy_limit"])
        assert abs(c["paid_loss"] - round(expected_paid, 2)) <= 0.02
        assert c["paid_loss"] <= c["policy_limit"] + 0.01

    # Annual aggregates must equal the supplementary claim-level table exactly.
    grouped: Dict[str, dict] = defaultdict(lambda: {"n": 0, "g": 0.0, "c": 0.0, "p": 0.0, "bi": 0})
    for c in claims:
        g = grouped[c["policy_id"]]
        g["n"] += 1
        g["g"] += c["ground_up_loss"]
        g["c"] += c["covered_loss"]
        g["p"] += c["paid_loss"]
        g["bi"] = max(g["bi"], c["bi_waiting_period_met_flag"])

    for r in rows:
        g = grouped[r["policy_id"]]
        assert r["claim_count"] == g["n"]
        assert abs(r["aggregate_ground_up_loss"] - round(g["g"], 2)) <= 0.02
        assert abs(r["aggregate_covered_loss"] - round(g["c"], 2)) <= 0.02
        assert abs(r["aggregate_paid_loss"] - round(g["p"], 2)) <= 0.02
        assert r["bi_waiting_period_met_flag"] == g["bi"]

    zero_paid_claims = sum(c["paid_loss"] == 0 for c in claims)
    if claims:
        assert zero_paid_claims > 0, "V2 should retain legitimate zero-paid claims."

    # Reproducibility fingerprint: because streams are keyed, a repeat call must
    # generate identical rows and claims.
    rows2, claims2 = generate_dataset("Baseline")
    assert rows == rows2 and claims == claims2

    return {
        "policy_year_rows": len(rows),
        "claim_rows": len(claims),
        "zero_paid_claims": zero_paid_claims,
        "positive_paid_claims": sum(c["paid_loss"] > 0 for c in claims),
        "max_claim_count": max(r["claim_count"] for r in rows),
    }


def main() -> None:
    rows, claims = generate_dataset("Baseline")
    diagnostics = validate(rows, claims)
    write_csv(rows, DATASET_FILE)
    if claims:
        write_csv(claims, CLAIM_FILE)
    else:
        # Defensive path, not expected for the calibrated V2 generator.
        CLAIM_FILE.write_text("", encoding="utf-8")

    print("ClimateTwin V2 data generated successfully.")
    print(f"  Student dataset: {DATASET_FILE} ({diagnostics['policy_year_rows']} rows)")
    print(f"  Claim-level supplement: {CLAIM_FILE} ({diagnostics['claim_rows']} rows)")
    print(f"  Zero-paid claims retained: {diagnostics['zero_paid_claims']}")
    print(f"  Positive-paid claims: {diagnostics['positive_paid_claims']}")
    print(f"  Maximum annual claim count: {diagnostics['max_claim_count']}")
    print("  All V2 validation checks passed.")


if __name__ == "__main__":
    main()
