# analyze.py
# Summary: load_factor and km_since_service are the strongest predictors of breakdown.
# Total odometer and age look obvious but are actually weak on their own — high-mileage
# old cars that stay lightly loaded mostly do NOT break down. It is the combination of
# heavy loading AND a long gap since last service that separates the breakdown cars.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# ── 1. Compare column means for the two groups ──────────────────────────────────────
broke = df[df["broke_down"] == 1]
fine  = df[df["broke_down"] == 0]

numeric_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

print("=" * 65)
print("Column-by-column comparison: broke-down vs healthy")
print("=" * 65)
print(f"{'Column':<22} {'Broke mean':>12} {'Fine mean':>12} {'Diff %':>8}")
print("-" * 65)
for col in numeric_cols:
    m_broke = broke[col].mean()
    m_fine  = fine[col].mean()
    diff_pct = (m_broke - m_fine) / m_fine * 100 if m_fine != 0 else float("nan")
    print(f"{col:<22} {m_broke:>12.2f} {m_fine:>12.2f} {diff_pct:>+8.1f}%")

print()

# ── 2. Correlation with broke_down ──────────────────────────────────────────────────
print("Pearson correlation with broke_down:")
corr = df[numeric_cols + ["broke_down"]].corr()["broke_down"].drop("broke_down").sort_values(
    key=abs, ascending=False
)
for col, val in corr.items():
    print(f"  {col:<22} r = {val:+.3f}")

print()

# ── 3. Build a simple 0-100 risk score ──────────────────────────────────────────────
# Factors that showed the clearest separation: load_factor and km_since_service.
# We normalise each to [0, 1] across the whole fleet and combine them equally.

def norm(series: pd.Series) -> pd.Series:
    """Min-max normalise a column to [0, 1]."""
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo) if hi != lo else pd.Series([0.5] * len(series))

df["risk_score"] = (
    0.5 * norm(df["load_factor"])
  + 0.5 * norm(df["km_since_service"])
) * 100

# ── 4. Print cars ranked by risk, highest first ─────────────────────────────────────
print("=" * 65)
print("Fleet ranked by breakdown risk (highest first)")
print("=" * 65)
print(f"{'car_id':<12} {'risk_score':>11} {'load_factor':>12} {'km_since_svc':>14} {'broke_down':>11}")
print("-" * 65)
for _, row in df.sort_values("risk_score", ascending=False).iterrows():
    flag = "  <-- BROKE" if row["broke_down"] == 1 else ""
    print(
        f"{row['car_id']:<12} {row['risk_score']:>11.1f}"
        f" {row['load_factor']:>12.2f} {row['km_since_service']:>14.0f}"
        f" {int(row['broke_down']):>11}{flag}"
    )

print()
print("Done.")
