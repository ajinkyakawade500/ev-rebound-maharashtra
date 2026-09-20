"""Create original scenario figures. Run after reproduce.py; requires matplotlib."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.labelcolor": "#293949", "text.color": "#182b3a",
                     "axes.edgecolor": "#c6cfd5", "xtick.color": "#52616d",
                     "ytick.color": "#293949", "svg.fonttype": "none"})

with (ROOT / "results/costs.csv").open() as f:
    rows = list(csv.DictReader(f))
labels = ["Petrol two-wheeler", "Grid-charged EV", "Solar EV\n(opportunity value)",
          "Zero energy cost\n(thought experiment)"]
fig, ax = plt.subplots(figsize=(9.8, 4.6))
left = [0.0] * len(rows)
for key, label, color in [
    ("energy_inr_per_km", "Energy / opportunity cost", "#147d92"),
    ("variable_nonenergy_inr_per_km", "Other variable cost", "#dfab52"),
    ("time_inr_per_km", "Value of time", "#bac9d1"),
]:
    vals = [float(r[key]) for r in rows]
    ax.barh(range(4), vals, left=left, label=label, color=color, height=.58)
    left = [a+b for a,b in zip(left, vals)]
for i, total in enumerate(left):
    ax.text(total + .065, i, f"{total:.2f}", va="center", fontsize=11, fontweight="bold")
ax.set_yticks(range(4), labels)
ax.invert_yaxis()
ax.set_xlim(0, 5.1)
ax.set_xlabel("Assumed generalized cost (INR per km)", labelpad=11)
ax.set_title("Cheap energy does not remove time and wear", loc="left", fontsize=16, pad=32, fontweight="bold")
ax.xaxis.grid(True, color="#e7ecef", linewidth=.7)
ax.set_axisbelow(True)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.015), ncol=3, frameon=False, fontsize=9)
fig.text(.02, .016, "Illustrative inputs only. Solar opportunity value: INR 3/kWh. Not official tariffs or measured travel costs.", fontsize=9, color="#52616d")
fig.subplots_adjust(left=.26, right=.95, top=.76, bottom=.19)
for ext in ["png", "svg"]:
    fig.savefig(OUT / f"cost_components.{ext}", dpi=220, facecolor="white")
plt.close(fig)

a = json.loads((ROOT / "analysis/assumptions.json").read_text())
fig, ax = plt.subplots(figsize=(9.8, 5.0))
extra = list(range(301))
for q, color, style in zip(a["impact_intensity_ratios"], ["#147d92", "#db9c36", "#705890"], ["-", "--", "-."]):
    totals = [100*q*(1+x/100) for x in extra]
    ax.plot(extra, totals, color=color, linestyle=style, linewidth=2.6,
            label=f"New per-km impact = {q:.0%} of old")
    at = 100*(1/q-1)
    ax.scatter([at], [100], color=color, s=36, zorder=4)
ax.axhline(100, color="#243b4c", linestyle=":", linewidth=1.5)
ax.text(290, 107, "Old total impact", ha="right", fontsize=10)
ax.set_xlim(0, 305)
ax.set_ylim(0, 315)
ax.set_xlabel("Additional distance relative to the old baseline", labelpad=10)
ax.set_ylabel("Total impact relative to the old baseline", labelpad=10)
ax.xaxis.set_major_formatter(PercentFormatter(100))
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.grid(color="#e7ecef", linewidth=.7)
ax.set_axisbelow(True)
ax.set_title("The per-km advantage determines the break-even point", loc="left", fontsize=15, fontweight="bold", pad=18)
ax.legend(loc="upper left", frameon=False, ncol=1, fontsize=9)
fig.text(.02, .016, "Accounting sensitivity: total impact ratio = intensity ratio x distance multiplier. Ratios are hypothetical.", fontsize=9, color="#52616d")
fig.subplots_adjust(left=.12, right=.97, top=.85, bottom=.18)
for ext in ["png", "svg"]:
    fig.savefig(OUT / f"impact_sensitivity.{ext}", dpi=220, facecolor="white")
plt.close(fig)
print("Wrote PNG and SVG versions of both scenario figures.")
