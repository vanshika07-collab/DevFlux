import pandas as pd

REQUIRED_COLUMNS = ["repo_name", "repo_url", "stars", "topics", "language"]

def validate_snapshot(filepath: str) -> bool:
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

    print(f"✅ Validation Passed: {len(df)} records verified successfully.")
    return True

if __name__ == "__main__":
    sample_path = r"E:\COLLEGE\MyProjects\DevFlux\data\sample\demo_run.csv"
    validate_snapshot(sample_path)