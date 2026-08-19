import re
from pathlib import Path
import pandas as pd

CORE_COLUMNS = ["repo_name", "owner", "repo_url", "language", "topics", "stars"]

def get_project_dirs():
    base = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path(".")
    raw_dir = base / "data" / "raw"
    processed_dir = base / "data" / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, processed_dir

def extract_snapshot_date(filename: str) -> str:
    match = re.search(r"(\d{4}[_-]\d{2}[_-]\d{2})", filename)
    if match:
        return match.group(1).replace("_", "-")
    return filename

def validate_and_clean_file(filepath: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Failed to read {filepath.name}: {e}")
        return None

    # Check minimum required core columns
    missing = [c for c in CORE_COLUMNS if c not in df.columns]
    if missing:
        print(f"⚠️ {filepath.name} skipped. Missing core columns: {missing}")
        return None

    # Standardize string fields
    df["repo_name"] = df["repo_name"].astype(str).str.strip()
    df["owner"] = df["owner"].astype(str).str.strip()
    df["repo_url"] = df["repo_url"].astype(str).str.strip()
    df["language"] = df["language"].fillna("Unknown").astype(str).str.strip()
    df["topics"] = df["topics"].fillna("[]").astype(str)

    # Optional fields handled gracefully
    df["description"] = df["description"].fillna("") if "description" in df.columns else ""
    df["updated_at"] = df["updated_at"].fillna("") if "updated_at" in df.columns else ""

    # Numeric conversions
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce").fillna(0).astype(int)

    # Deduplicate within this snapshot
    df = df.drop_duplicates(subset=["repo_name"]).copy()

    # Dynamic metadata from filename
    df["snapshot_id"] = filepath.stem
    df["snapshot_date"] = extract_snapshot_date(filepath.name)

    return df

def validate_all_snapshots():
    raw_dir, processed_dir = get_project_dirs()
    raw_files = sorted(raw_dir.glob("*.csv"))

    if not raw_files:
        print(f"⚠️ No CSV files found in: {raw_dir}")
        return []

    print("=" * 60)
    print("STEP 1: VALIDATION & DATA INGESTION")
    print("=" * 60)
    print(f"📂 Found {len(raw_files)} raw snapshot(s)")

    cleaned_files = []
    for filepath in raw_files:
        df = validate_and_clean_file(filepath)
        if df is None:
            continue

        output_path = processed_dir / f"clean_{filepath.stem}.csv"
        df.to_csv(output_path, index=False)
        print(f"   ✅ Stamped & Cleaned: {filepath.name} -> {output_path.name} ({len(df)} records)")
        cleaned_files.append(output_path)

    return cleaned_files

if __name__ == "__main__":
    validate_all_snapshots()