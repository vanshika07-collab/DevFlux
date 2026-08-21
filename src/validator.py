import json
from pathlib import Path
import re
import numpy as np
import pandas as pd

CORE_COLUMNS = ["repo_name", "owner", "repo_url", "language", "topics", "stars"]

COLUMN_ALIASES = {
    "name": "repo_name",
    "repository_name": "repo_name",
    "url": "repo_url",
    "repository_url": "repo_url",
    "link": "repo_url",
    "author": "owner",
    "lang": "language",
    "tags": "topics",
    "star_count": "stars",
    "stargazers": "stars",
}


def get_project_dirs():
  base = (
      Path(__file__).resolve().parent.parent
      if "__file__" in locals()
      else Path(".")
  )
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


def load_file_resiliently(filepath: Path) -> pd.DataFrame:
  """Reads CSV, JSON, or NDJSON files regardless of extension."""
  # 1. Try reading as standard CSV
  try:
    df = pd.read_csv(filepath)
    # Check if first column looks like raw JSON
    first_col = str(df.columns[0])
    if first_col.startswith("{") or "{" in first_col:
      raise ValueError("File appears to be JSON/NDJSON saved with .csv extension")
    return df
  except Exception:
    pass

  # 2. Try reading as NDJSON (newline-delimited JSON)
  try:
    return pd.read_json(filepath, lines=True)
  except Exception:
    pass

  # 3. Try reading as standard JSON array
  try:
    return pd.read_json(filepath)
  except Exception:
    pass

  # 4. Fallback line-by-line JSON parse
  try:
    records = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
      for line in f:
        line_str = line.strip()
        if line_str:
          try:
            records.append(json.loads(line_str))
          except Exception:
            pass
    if records:
      return pd.DataFrame(records)
  except Exception as e:
    print(f"❌ Could not parse {filepath.name}: {e}")

  return None


def validate_and_clean_file(filepath: Path) -> pd.DataFrame:
  df = load_file_resiliently(filepath)
  if df is None or df.empty:
    print(f"⚠️ {filepath.name} is empty or unreadable. Skipped.")
    return None

  # Normalize column headers
  df.columns = [str(c).strip().lower() for c in df.columns]

  # Map aliases to standard names
  for alias, target in COLUMN_ALIASES.items():
    if alias in df.columns and target not in df.columns:
      df.rename(columns={alias: target}, inplace=True)

  # Derive missing owner if repo_name has 'owner/repo' format
  if "owner" not in df.columns and "repo_name" in df.columns:
    df["owner"] = df["repo_name"].apply(
        lambda x: str(x).split("/")[0] if "/" in str(x) else "Unknown"
    )

  if "language" not in df.columns:
    df["language"] = "Unknown"

  if "topics" not in df.columns:
    df["topics"] = "[]"

  if "repo_url" not in df.columns and "repo_name" in df.columns:
    df["repo_url"] = "https://github.com/" + df["repo_name"].astype(str)

  # Check core columns
  missing = [c for c in CORE_COLUMNS if c not in df.columns]
  if missing:
    print(f"⚠️ {filepath.name} missing columns: {missing}. Skipped.")
    return None

  # Clean strings & formatting
  df["repo_name"] = df["repo_name"].astype(str).str.strip()
  df["owner"] = df["owner"].astype(str).str.strip()
  df["repo_url"] = df["repo_url"].astype(str).str.strip()
  df["language"] = df["language"].fillna("Unknown").astype(str).str.strip()
  df["topics"] = df["topics"].apply(
      lambda t: (
          str(t)
          if isinstance(t, (str, list))
          else "[]"
      )
  )

  df["description"] = (
      df["description"].fillna("") if "description" in df.columns else ""
  )
  df["updated_at"] = (
      df["updated_at"].fillna("") if "updated_at" in df.columns else ""
  )

  df["stars"] = (
      pd.to_numeric(df["stars"], errors="coerce").fillna(0).astype(int)
  )

  # Deduplicate within snapshot
  df = df.drop_duplicates(subset=["repo_name"]).copy()

  df["snapshot_id"] = filepath.stem
  df["snapshot_date"] = extract_snapshot_date(filepath.name)

  return df


def validate_all_snapshots():
  raw_dir, processed_dir = get_project_dirs()
  raw_files = sorted(raw_dir.glob("*.csv")) + sorted(raw_dir.glob("*.json"))
  # Deduplicate path list
  raw_files = sorted(list({f.resolve(): f for f in raw_files}.values()))

  if not raw_files:
    print(f"⚠️ No raw files found in: {raw_dir}")
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
    print(
        f"   ✅ Stamped & Cleaned: {filepath.name} -> {output_path.name}"
        f" ({len(df)} records)"
    )
    cleaned_files.append(output_path)

  return cleaned_files


if __name__ == "__main__":
  validate_all_snapshots()