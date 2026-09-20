"""Reproduce transparent scenarios. No data downloads or fitted parameters.

Run from the repository root: python analysis/reproduce.py
Only Python's standard library is required for the calculations and CSV output.
"""

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def compute(a):
    positive = ("baseline_km_per_year", "petrol_inr_per_litre",
                "petrol_km_per_litre", "ev_wall_kwh_per_km")
    for key in positive:
        if not math.isfinite(a[key]) or a[key] <= 0:
            raise ValueError(f"{key} must be finite and positive")
    for key in ("grid_inr_per_kwh", "solar_opportunity_inr_per_kwh",
                "variable_nonenergy_inr_per_km", "time_inr_per_km"):
        if not math.isfinite(a[key]) or a[key] < 0:
            raise ValueError(f"{key} must be finite and nonnegative")
    other = a["variable_nonenergy_inr_per_km"] + a["time_inr_per_km"]
    if other <= 0:
        raise ValueError("Positive non-energy cost is required for the zero-energy-cost case")
    energy_costs = {
        "Petrol two-wheeler": a["petrol_inr_per_litre"] / a["petrol_km_per_litre"],
        "Grid-charged EV": a["ev_wall_kwh_per_km"] * a["grid_inr_per_kwh"],
        "Solar EV, opportunity cost": a["ev_wall_kwh_per_km"] * a["solar_opportunity_inr_per_kwh"],
        "EV, zero energy cost thought experiment": 0.0,
    }
    costs = [{"case": case, "energy_inr_per_km": energy,
              "variable_nonenergy_inr_per_km": a["variable_nonenergy_inr_per_km"],
              "time_inr_per_km": a["time_inr_per_km"],
              "generalized_inr_per_km": energy + other}
             for case, energy in energy_costs.items()]
    c0 = costs[0]["generalized_inr_per_km"]
    demand = []
    for row in costs[1:]:
        for elasticity in a["generalized_cost_elasticities"]:
            if not math.isfinite(elasticity) or elasticity >= 0:
                raise ValueError("Use finite, negative illustrative elasticities")
            ratio = (row["generalized_inr_per_km"] / c0) ** elasticity
            demand.append({"case": row["case"], "elasticity": elasticity,
                           "distance_multiplier": ratio,
                           "distance_increase_pct": 100 * (ratio - 1),
                           "annual_km": a["baseline_km_per_year"] * ratio})
    impacts, thresholds = [], []
    for q in a["impact_intensity_ratios"]:
        if not 0 < q < 1:
            raise ValueError("Impact intensity ratios must lie strictly between zero and one")
        thresholds.append({"intensity_ratio_q": q,
                           "distance_multiplier_at_break_even": 1 / q,
                           "extra_distance_pct_at_break_even": 100 * (1 / q - 1)})
        for r in a["distance_increases"]:
            if not math.isfinite(r) or r < 0:
                raise ValueError("Distance increases must be finite and nonnegative")
            impacts.append({"intensity_ratio_q": q, "distance_increase_pct": 100 * r,
                            "total_impact_pct_of_old_baseline": 100 * q * (1 + r),
                            "engineering_savings_taken_back_pct": 100 * q * r / (1 - q)})
    return {"costs": costs, "demand": demand, "impacts": impacts, "thresholds": thresholds}


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for row in rows:
            w.writerow({k: round(v, 9) if isinstance(v, float) else v for k, v in row.items()})


def main():
    a = json.loads((ROOT / "analysis/assumptions.json").read_text())
    result = compute(a)
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    for name, rows in result.items():
        write_csv(out / f"{name}.csv", rows)
    print("Illustrative results written to results/. No empirical rebound estimate was computed.")
    for row in result["demand"]:
        print(f"{row['case']} | elasticity {row['elasticity']:.1f} | extra travel {row['distance_increase_pct']:.1f}%")


if __name__ == "__main__":
    main()
