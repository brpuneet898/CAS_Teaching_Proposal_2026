"""
ClimateTwin synthetic data generator
====================================

Creates exactly 750 policy-location-year observations for the AquaAir General
Insurance teaching case.

Reproducibility
---------------
The generator deliberately uses only the Python standard library. Pseudo-random
values are derived from SHA-256 using a fixed seed and named streams rather than
from a library RNG. This makes the output deterministic and stable across runs.

Running:
    python data_script.py

Output:
    dataset.csv

Instructor-only design notes
----------------------------
The synthetic relationships are intentional but not written into the student
CSV. Claim occurrence is possible only when a defined insured trigger exists.
Environmental deterioration alone therefore does not automatically create a
claim.

Frequency:
    Poisson with exposure offset and multiplicative effects for occupancy,
    insured air/water triggers, compound triggers, climate, and mitigation.

Severity:
    Claim-level lognormal ground-up losses driven by occupancy, insured value,
    trigger type, compound interaction, climate, and mitigation. Deductible and
    per-claim policy limit are then applied.

The exact coefficient values below are instructor-only.
"""

from __future__ import annotations

import csv
import hashlib
import math
from pathlib import Path

SEED = "ClimateTwin-CAS-2026-v1"
N_LOCATIONS = 250
YEARS = (2024, 2025, 2026)
OUTPUT_FILE = Path(__file__).resolve().with_name("dataset.csv")

REGIONS = (
    "Northgate",
    "Riverbend",
    "Central Metro",
    "Coastview",
    "Drylands",
)
OCCUPANCIES = (
    "Hospital",
    "Manufacturing",
    "Food Processing",
)

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

FREQ_OCC = {
    "Hospital": 0.20,
    "Manufacturing": 0.35,
    "Food Processing": 0.28,
}
FREQ_BETA = {
    "intercept": -1.30,
    "air_trigger": 0.48,
    "water_trigger": 0.62,
    "compound": 0.55,
    "temperature_per_5c_above_25": 0.10,
    "drought": 0.22,
    "rainfall_per_500mm_above_1000": 0.08,
    "air_filtration": -0.34,
    "water_treatment": -0.40,
    "bcp": -0.24,
}

SEV_OCC = {
    "Hospital": 1.35,
    "Manufacturing": 1.15,
    "Food Processing": 1.00,
}
SEV_TRIGGER = {
    "air_only": 0.95,
    "water_only": 1.15,
    "compound": 1.55,
}
SEV_SIGMA = 0.72

BASE_RATE = {
    "Hospital": 0.0033,
    "Manufacturing": 0.00285,
    "Food Processing": 0.00305,
}


def _digest(*parts: object) -> bytes:
    key = "|".join([SEED, *map(str, parts)]).encode("utf-8")
    return hashlib.sha256(key).digest()


def u01(*parts: object) -> float:
    """Deterministic uniform in (0,1), based on the first 64 SHA-256 bits."""
    x = int.from_bytes(_digest(*parts)[:8], "big")
    return (x + 0.5) / (2**64)


def normal(*parts: object) -> float:
    """Deterministic standard normal via Box-Muller."""
    u1 = max(u01(*parts, "u1"), 1e-15)
    u2 = u01(*parts, "u2")
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def choose(options, probs, *parts: object):
    x = u01(*parts)
    c = 0.0
    for opt, p in zip(options, probs):
        c += p
        if x <= c:
            return opt
    return options[-1]


def poisson(lam: float, *parts: object) -> int:
    """Knuth Poisson sampler; fine for the small lambdas used in this case."""
    if lam <= 0.0:
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


def round_to(x: float, unit: int) -> int:
    return int(round(x / unit) * unit)


def make_locations():
    locations = []
    region_probs = (0.18, 0.20, 0.25, 0.18, 0.19)
    occ_probs = (0.25, 0.42, 0.33)

    for loc_num in range(1, N_LOCATIONS + 1):
        location_id = f"LOC{loc_num:03d}"
        region = choose(REGIONS, region_probs, location_id, "region")
        occupancy = choose(OCCUPANCIES, occ_probs, location_id, "occupancy")

        size_factor = math.exp(0.38 * normal(location_id, "size"))
        if occupancy == "Hospital":
            base_value = 28_000_000
        elif occupancy == "Manufacturing":
            base_value = 18_000_000
        else:
            base_value = 13_000_000

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


def make_row(loc: dict, year: int) -> dict:
    loc_id = loc["location_id"]
    region = loc["region"]
    occ = loc["occupancy"]
    rp = REGION_PROFILE[region]
    yr_idx = year - 2024

    exposure = clamp(0.68 + 0.36 * u01(loc_id, year, "exposure"), 0.68, 1.00)
    insured_value = loc["insured_value_base"] * (1.035 ** yr_idx) * (
        0.97 + 0.06 * u01(loc_id, year, "value_noise")
    )
    insured_value = round_to(insured_value, 10_000)

    limit_ratio = choose((0.25, 0.35, 0.50), (0.25, 0.45, 0.30), loc_id, year, "limit_ratio")
    policy_limit = round_to(insured_value * limit_ratio, 10_000)

    if occ == "Hospital":
        deductible_options = (50_000, 75_000, 100_000)
    elif occ == "Manufacturing":
        deductible_options = (40_000, 60_000, 80_000)
    else:
        deductible_options = (25_000, 40_000, 60_000)
    deductible = choose(deductible_options, (0.35, 0.45, 0.20), loc_id, year, "deductible")
    bi_waiting_days = choose((1, 2, 3), (0.35, 0.45, 0.20), loc_id, year, "waiting")

    pm25 = rp["pm25"] + 1.8 * yr_idx + 5.2 * normal(loc_id, year, "pm25")
    ozone = rp["ozone"] + 1.2 * yr_idx + 7.0 * normal(loc_id, year, "ozone")
    turbidity = rp["turbidity"] + 0.20 * yr_idx + 1.15 * normal(loc_id, year, "turbidity")
    wqi = rp["wqi"] - 1.1 * yr_idx + 6.0 * normal(loc_id, year, "wqi")
    temperature = rp["temperature"] + 0.45 * yr_idx + 2.2 * normal(loc_id, year, "temp")
    rainfall = rp["rainfall"] * (0.92 + 0.18 * u01(loc_id, year, "rain")) + 90.0 * normal(loc_id, year, "rain_n")
    drought = rp["drought"] + 0.035 * yr_idx + 0.10 * normal(loc_id, year, "drought")

    pm25 = clamp(pm25, 8.0, 78.0)
    ozone = clamp(ozone, 28.0, 105.0)
    turbidity = clamp(turbidity, 0.4, 11.5)
    wqi = clamp(wqi, 35.0, 92.0)
    temperature = clamp(temperature, 16.0, 39.0)
    rainfall = clamp(rainfall, 240.0, 2100.0)
    drought = clamp(drought, 0.02, 0.95)

    air_stress = int(pm25 >= 35.0 or ozone >= 70.0)
    water_stress = int(turbidity >= 5.0 or wqi <= 60.0)

    air_qual_p = (
        0.16
        + 0.18 * air_stress
        + 0.10 * (pm25 >= 45.0)
        + 0.07 * (ozone >= 80.0)
        + (0.08 if occ == "Hospital" else 0.04 if occ == "Manufacturing" else 0.02)
        - 0.10 * loc["air_filtration"]
        - 0.05 * loc["business_continuity_plan"]
    )
    water_qual_p = (
        0.14
        + 0.20 * water_stress
        + 0.10 * (turbidity >= 6.5)
        + 0.08 * (wqi <= 52.0)
        + (0.09 if occ == "Food Processing" else 0.05 if occ == "Hospital" else 0.04)
        - 0.11 * loc["water_treatment"]
        - 0.04 * loc["business_continuity_plan"]
    )
    air_qual_p = clamp(air_qual_p, 0.02, 0.78)
    water_qual_p = clamp(water_qual_p, 0.02, 0.80)

    air_trigger = int(air_stress and u01(loc_id, year, "air_trigger") < air_qual_p)
    water_trigger = int(water_stress and u01(loc_id, year, "water_trigger") < water_qual_p)
    compound_trigger = int(air_trigger and water_trigger)

    if compound_trigger:
        trigger_type = "Compound"
    elif air_trigger:
        trigger_type = "Air"
    elif water_trigger:
        trigger_type = "Water"
    else:
        trigger_type = "None"

    if trigger_type == "None":
        bi_waiting_met = 0
    else:
        duration_score = (
            0.55
            + 0.12 * air_trigger
            + 0.15 * water_trigger
            + 0.16 * compound_trigger
            + 0.04 * max(pm25 - 35.0, 0.0) / 10.0
            + 0.04 * max(60.0 - wqi, 0.0) / 10.0
            - 0.08 * (bi_waiting_days - 1)
            - 0.08 * loc["business_continuity_plan"]
        )
        bi_waiting_met = int(u01(loc_id, year, "bi_wait") < clamp(duration_score, 0.10, 0.93))

    if trigger_type == "None":
        lam = 0.0
    else:
        climate_term = (
            FREQ_BETA["temperature_per_5c_above_25"] * max(temperature - 25.0, 0.0) / 5.0
            + FREQ_BETA["drought"] * drought
            + FREQ_BETA["rainfall_per_500mm_above_1000"] * max(rainfall - 1000.0, 0.0) / 500.0
        )
        eta = (
            FREQ_BETA["intercept"]
            + FREQ_OCC[occ]
            + FREQ_BETA["air_trigger"] * air_trigger
            + FREQ_BETA["water_trigger"] * water_trigger
            + FREQ_BETA["compound"] * compound_trigger
            + climate_term
            + FREQ_BETA["air_filtration"] * loc["air_filtration"] * air_trigger
            + FREQ_BETA["water_treatment"] * loc["water_treatment"] * water_trigger
            + FREQ_BETA["bcp"] * loc["business_continuity_plan"]
        )
        lam = exposure * math.exp(eta)

    claim_count = poisson(lam, loc_id, year, "count")

    aggregate_ground_up = 0.0
    aggregate_covered = 0.0
    aggregate_paid = 0.0

    for c in range(1, claim_count + 1):
        if trigger_type == "Compound":
            trigger_mult = SEV_TRIGGER["compound"]
        elif trigger_type == "Water":
            trigger_mult = SEV_TRIGGER["water_only"]
        else:
            trigger_mult = SEV_TRIGGER["air_only"]

        value_mult = (insured_value / 15_000_000.0) ** 0.38
        climate_mult = (
            1.0
            + 0.06 * max(temperature - 28.0, 0.0) / 5.0
            + 0.07 * drought
            + 0.05 * max(turbidity - 5.0, 0.0) / 3.0
        )
        mitigation_mult = (
            (0.78 if (air_trigger and loc["air_filtration"]) else 1.0)
            * (0.74 if (water_trigger and loc["water_treatment"]) else 1.0)
            * (0.84 if loc["business_continuity_plan"] else 1.0)
        )
        waiting_mult = 1.10 if bi_waiting_met else 0.88

        mean_scale = 165_000.0 * SEV_OCC[occ] * trigger_mult * value_mult * climate_mult * mitigation_mult * waiting_mult
        z = normal(loc_id, year, "sev", c)
        ground = mean_scale * math.exp(SEV_SIGMA * z - 0.5 * SEV_SIGMA**2)
        ground = max(8_000.0, ground)

        covered = ground
        paid = min(max(covered - deductible, 0.0), policy_limit)

        aggregate_ground_up += ground
        aggregate_covered += covered
        aggregate_paid += paid

    aggregate_ground_up = round(aggregate_ground_up, 2)
    aggregate_covered = round(aggregate_covered, 2)
    aggregate_paid = round(aggregate_paid, 2)

    mitigation_credit = (
        1.0
        - 0.06 * loc["air_filtration"]
        - 0.06 * loc["water_treatment"]
        - 0.04 * loc["business_continuity_plan"]
    )
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
        "bi_waiting_period_days": bi_waiting_days,
        "current_premium": current_premium,
        "pm25": round(pm25, 1),
        "ozone": round(ozone, 1),
        "turbidity": round(turbidity, 2),
        "water_quality_index": round(wqi, 1),
        "temperature_c": round(temperature, 1),
        "annual_rainfall_mm": round(rainfall, 1),
        "drought_indicator": round(drought, 3),
        "air_stress_flag": air_stress,
        "water_stress_flag": water_stress,
        "air_trigger_flag": air_trigger,
        "water_trigger_flag": water_trigger,
        "compound_trigger_flag": compound_trigger,
        "insured_trigger_type": trigger_type,
        "bi_waiting_period_met_flag": bi_waiting_met,
        "air_filtration": loc["air_filtration"],
        "water_treatment": loc["water_treatment"],
        "business_continuity_plan": loc["business_continuity_plan"],
        "air_filtration_upgrade_cost": loc["air_filtration_upgrade_cost"],
        "water_treatment_upgrade_cost": loc["water_treatment_upgrade_cost"],
        "bcp_upgrade_cost": loc["bcp_upgrade_cost"],
        "claim_count": claim_count,
        "aggregate_ground_up_loss": aggregate_ground_up,
        "aggregate_covered_loss": aggregate_covered,
        "aggregate_paid_loss": aggregate_paid,
    }


def generate_rows():
    rows = []
    for loc in make_locations():
        for year in YEARS:
            rows.append(make_row(loc, year))
    return rows


def write_csv(rows, output_file=OUTPUT_FILE):
    fieldnames = list(rows[0].keys())
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = generate_rows()
    assert len(rows) == 750
    assert all(0.0 < r["exposure_years"] <= 1.0 for r in rows)
    assert all(r["aggregate_paid_loss"] <= r["aggregate_covered_loss"] + 1e-9 for r in rows)
    assert all((r["claim_count"] > 0) <= (r["insured_trigger_type"] != "None") for r in rows)
    write_csv(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
