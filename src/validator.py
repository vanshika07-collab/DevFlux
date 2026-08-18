import os
import pandas as pd

REQUIRED_COLUMNS = ["repo_name", "repo_url", "stars", "topics", "language"]

def validate_snapshot(filepath: str) -> bool:
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Failed to load file: {e}")
        return False

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        print(f"⚠️ Validation Warning: Missing columns {missing}")
        return False

    if len(df) == 0:
        print("⚠️ Validation Warning: Dataset is empty.")
        return False

    print(f"✅ Validation Passed: {len(df)} records verified successfully from {os.path.basename(filepath)}.")
    return True

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "__file__" in locals() else "."
    raw_path = os.path.join(base_dir, "data", "raw", "raw_2026_08_19.csv")
    validate_snapshot(raw_path)