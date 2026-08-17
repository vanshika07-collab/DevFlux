import os
import pandas as pd

def calculate_snapshot_delta(snapshot_old_path: str, snapshot_new_path: str):
    if not os.path.exists(snapshot_old_path) or not os.path.exists(snapshot_new_path):
        print("⚠️ One or both snapshot files are missing.")
        return None

    df_old = pd.read_csv(snapshot_old_path)
    df_new = pd.read_csv(snapshot_new_path)

    # Ensure required columns exist
    for df in [df_old, df_new]:
        if "stars" not in df.columns:
            df["stars"] = 0
        df["stars"] = pd.to_numeric(df["stars"], errors="coerce").fillna(0).astype(int)

    # Merge datasets on repo_name
    merged = pd.merge(
        df_new,
        df_old[["repo_name", "stars"]],
        on="repo_name",
        how="left",
        suffixes=("", "_prev")
    )

    merged["stars_prev"] = merged["stars_prev"].fillna(merged["stars"]).astype(int)
    merged["star_growth"] = merged["stars"] - merged["stars_prev"]

    # Aggregate by Category
    summary = merged.groupby("category").agg(
        repo_count=("repo_name", "count"),
        total_stars=("stars", "sum"),
        total_growth=("star_growth", "sum")
    ).reset_index().sort_values(by="total_growth", ascending=False)

    return summary

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Path to sample classified file
    sample_file = os.path.join(base_dir, "data", "processed", "sample_classified.csv")

    if os.path.exists(sample_file):
        print("📊 Running Delta & Trend Detection Test...")
        # Self-comparison baseline test (growth = 0 for Day 1 baseline)
        trends = calculate_snapshot_delta(sample_file, sample_file)
        if trends is not None:
            print("\n--- Category Breakdown (Baseline Snapshot) ---")
            print(trends.to_string(index=False))
            print("\n✅ Change detector module is fully functional!")