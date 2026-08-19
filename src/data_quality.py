from pathlib import Path
import pandas as pd

def run_quality_check(filepath: Path) -> dict:
    df = pd.read_csv(filepath)
    total_rows = len(df)
    
    report = {
        "file": filepath.name,
        "total_repos": total_rows,
        "unique_repos": df["repo_name"].nunique(),
        "duplicate_rows": total_rows - df["repo_name"].nunique(),
        "missing_language_pct": round((df["language"].isin(["Unknown", ""]).sum() / total_rows) * 100, 1),
        "missing_description_pct": round((df["description"].isna() | (df["description"] == "")).sum() / total_rows * 100, 1),
        "empty_topics_pct": round((df["topics"].isin(["[]", "", "nan"]).sum() / total_rows) * 100, 1),
        "min_stars": int(df["stars"].min()),
        "max_stars": int(df["stars"].max()),
        "mean_stars": int(df["stars"].mean())
    }
    return report

def audit_all_clean_snapshots():
    base = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path(".")
    processed_dir = base / "data" / "processed"
    clean_files = sorted(processed_dir.glob("clean_*.csv"))

    if not clean_files:
        print("⚠️ No clean snapshots found to audit.")
        return None

    print("=" * 60)
    print("STEP 2: DATA QUALITY AUDIT")
    print("=" * 60)

    reports = [run_quality_check(f) for f in clean_files]
    df_quality = pd.DataFrame(reports)

    report_path = processed_dir / "data_quality_report.csv"
    df_quality.to_csv(report_path, index=False)
    
    print(df_quality.to_string(index=False))
    print(f"\n📊 Quality report saved to: {report_path.name}")
    return df_quality

if __name__ == "__main__":
    audit_all_clean_snapshots()