import re
from pathlib import Path
import numpy as np
import pandas as pd


def assign_momentum_signal(score: float) -> str:
  if score >= 60.0:
    return "🔥 BREAKOUT"
  elif score >= 40.0:
    return "⚡ ACCELERATING"
  elif score >= 20.0:
    return "🌱 STEADY"
  else:
    return "💤 LOW VELOCITY"


def compute_longitudinal_deltas():
  base = (
      Path(__file__).resolve().parent.parent
      if "__file__" in locals()
      else Path(".")
  )
  processed_dir = base / "data" / "processed"
  classified_files = sorted(processed_dir.glob("classified_*.csv"))

  if not classified_files:
    print("⚠️ No classified files found.")
    return None

  print("=" * 60)
  print("STEP 4: LONGITUDINAL MOMENTUM & INTELLIGENCE ENGINE")
  print("=" * 60)

  dfs = []
  for f in classified_files:
    df_temp = pd.read_csv(f)
    if "snapshot_date" not in df_temp.columns or df_temp[
        "snapshot_date"
    ].isna().all():
      match = re.search(r"(\d{4}[_-]\d{2}[_-]\d{2})", f.name)
      df_temp["snapshot_date"] = (
          match.group(1).replace("_", "-") if match else "2026-08-19"
      )
    dfs.append(df_temp)

  all_data = pd.concat(dfs, ignore_index=True)
  all_data["snapshot_date"] = all_data["snapshot_date"].astype(str)
  all_data["snapshot_dt"] = pd.to_datetime(
      all_data["snapshot_date"], errors="coerce"
  )
  all_data["stars"] = (
      pd.to_numeric(all_data["stars"], errors="coerce").fillna(0).astype(int)
  )

  # Sort deterministically
  all_data = all_data.sort_values(
      by=["repo_name", "snapshot_dt"]
  ).reset_index(drop=True)

  # Time-series delta metrics
  all_data["stars_prev"] = all_data.groupby("repo_name")["stars"].shift(1)
  all_data["star_growth"] = (
      all_data["stars"] - all_data["stars_prev"].fillna(all_data["stars"])
  ).astype(int)

  denom = all_data["stars_prev"].replace(0, np.nan)
  all_data["star_growth_rate"] = (
      ((all_data["star_growth"] / denom) * 100).round(2).fillna(0.0)
  )

  # Compound Momentum Scoring
  vol_score = np.log1p(np.maximum(0, all_data["star_growth"]))
  vel_score = np.log1p(np.maximum(0, all_data["star_growth_rate"]))
  all_data["momentum_score"] = (
      (vol_score * 0.5 + vel_score * 0.5) * 20
  ).round(1)
  all_data["signal"] = all_data["momentum_score"].apply(assign_momentum_signal)

  # Latest snapshot evaluation
  latest_dt = all_data["snapshot_dt"].max()
  latest_data = all_data[all_data["snapshot_dt"] == latest_dt].copy()

  # Normalized Category Velocity Summary
  category_velocity = (
      latest_data.groupby("primary_category")
      .agg(
          total_repos=("repo_name", "count"),
          total_stars=("stars", "sum"),
          net_star_growth=("star_growth", "sum"),
          avg_growth_per_repo=("star_growth", "mean"),
          median_growth_per_repo=("star_growth", "median"),
          avg_growth_rate=("star_growth_rate", "mean"),
          avg_momentum=("momentum_score", "mean"),
      )
      .reset_index()
  )

  # Round metrics for readability
  category_velocity["avg_growth_per_repo"] = category_velocity[
      "avg_growth_per_repo"
  ].round(2)
  category_velocity["median_growth_per_repo"] = category_velocity[
      "median_growth_per_repo"
  ].round(2)
  category_velocity["avg_growth_rate"] = category_velocity[
      "avg_growth_rate"
  ].round(2)
  category_velocity["avg_momentum"] = category_velocity["avg_momentum"].round(1)

  # Sort by average growth per repo to surface high-velocity clusters fairly
  category_velocity = category_velocity.sort_values(
      by="avg_growth_per_repo", ascending=False
  )

  # Top Breakout Repositories Leaderboard
  top_breakouts = latest_data.sort_values(
      by="momentum_score", ascending=False
  ).head(10)

  # Save processed datasets
  all_data = all_data.drop(columns=["snapshot_dt"])
  latest_data = latest_data.drop(columns=["snapshot_dt"])

  all_data.to_csv(
      processed_dir / "longitudinal_all_snapshots.csv", index=False
  )
  latest_data.to_csv(processed_dir / "latest_repo_deltas.csv", index=False)
  category_velocity.to_csv(
      processed_dir / "category_velocity.csv", index=False
  )
  top_breakouts.to_csv(
      processed_dir / "top_breakout_repositories.csv", index=False
  )

  print(
      f"\n📊 Snapshot Range: {all_data['snapshot_date'].min()} ->"
      f" {all_data['snapshot_date'].max()}"
  )
  print(
      f"Total Observations: {len(all_data)} records across"
      f" {len(classified_files)} snapshot(s)"
  )

  print("\n" + "-" * 75)
  print("🔥 TOP BREAKOUT LEADERBOARD (MOMENTUM SCORED)")
  print("-" * 75)
  display_cols = [
      "repo_name",
      "primary_category",
      "stars",
      "star_growth",
      "star_growth_rate",
      "momentum_score",
      "signal",
  ]
  print(top_breakouts[display_cols].head(5).to_string(index=False))

  print("\n" + "-" * 75)
  print("📈 NORMALIZED CATEGORY VELOCITY & MOMENTUM")
  print("-" * 75)
  print(category_velocity.to_string(index=False))

  return all_data


if __name__ == "__main__":
  compute_longitudinal_deltas()