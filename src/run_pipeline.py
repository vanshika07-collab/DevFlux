from pathlib import Path
import sys

# Add src/ to system path
sys.path.append(str(Path(__file__).resolve().parent))

from change_detector import compute_longitudinal_deltas
from classifier import classify_all_snapshots
from data_quality import audit_all_clean_snapshots
from validator import validate_all_snapshots


def cleanup_stale_processed_files(processed_dir: Path):
  """Removes stale intermediate files before a fresh run."""
  patterns = [
      "clean_*.csv",
      "classified_*.csv",
      "longitudinal_*.csv",
      "latest_*.csv",
      "*trends*.csv",
      "*breakout*.csv",
  ]
  for pattern in patterns:
    for f in processed_dir.glob(pattern):
      try:
        f.unlink()
      except Exception:
        pass


def main():
  print("\n" + "=" * 70)
  print("⚡ DEVFLUX AUTOMATED DATA INTELLIGENCE PIPELINE")
  print("=" * 70 + "\n")

  base = (
      Path(__file__).resolve().parent.parent
      if "__file__" in locals()
      else Path(".")
  )
  processed_dir = base / "data" / "processed"
  processed_dir.mkdir(parents=True, exist_ok=True)

  # Clear stale intermediate files
  cleanup_stale_processed_files(processed_dir)

  # Step 1: Validation & Ingestion
  clean_files = validate_all_snapshots()
  if not clean_files:
    print("❌ Pipeline stopped: No valid raw files found.")
    return

  # Step 2: Quality Audit
  print("\n")
  audit_all_clean_snapshots()

  # Step 3: Classification
  print("\n")
  classified_files = classify_all_snapshots()
  if not classified_files:
    print("❌ Pipeline stopped: Classification failed.")
    return

  # Step 4: Longitudinal Deltas & Momentum
  print("\n")
  compute_longitudinal_deltas()

  print("\n" + "=" * 70)
  print("✅ PIPELINE EXECUTION COMPLETE (IDEMPOTENT & REPRODUCIBLE)")
  print("=" * 70)
  print("Clean datasets updated in 'data/processed/'\n")


if __name__ == "__main__":
  main()