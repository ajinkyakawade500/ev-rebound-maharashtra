"""Check accounting identities and limiting cases, not an empirical model fit."""
import json
import math
from copy import deepcopy
from reproduce import ROOT, compute

a = json.loads((ROOT / "analysis/assumptions.json").read_text())
r = compute(a)
# Hand-calculated energy costs for a 40 km journey.
assert math.isclose(r["costs"][0]["energy_inr_per_km"] * 40, 84)
assert math.isclose(r["costs"][1]["energy_inr_per_km"] * 40, 12.8)
# At the break-even distance, total impact must equal the old baseline.
for t in r["thresholds"]:
    assert math.isclose(t["intensity_ratio_q"] * t["distance_multiplier_at_break_even"], 1)
# No extra travel means zero take-back, even though the new technology saves resources.
for row in r["impacts"]:
    if row["distance_increase_pct"] == 0:
        assert row["engineering_savings_taken_back_pct"] == 0
    if row["intensity_ratio_q"] == 0.25 and row["distance_increase_pct"] == 25:
        assert math.isclose(row["engineering_savings_taken_back_pct"], 100 / 12)
# The zero-energy-price thought experiment must produce finite demand.
assert all(math.isfinite(row["annual_km"]) for row in r["demand"])
bad = deepcopy(a)
bad["time_inr_per_km"] = bad["variable_nonenergy_inr_per_km"] = 0
try:
    compute(bad)
except ValueError:
    pass
else:
    raise AssertionError("A zero generalized cost must be rejected")
print("PASS: trip arithmetic, impact break-even, rebound definition, finite demand and input boundary.")
