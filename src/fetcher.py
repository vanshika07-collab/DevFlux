from datetime import datetime, timezone
import os
from pathlib import Path
import time
import pandas as pd
import requests

# Your Bright Data Collector ID
COLLECTOR_ID = "c_msyw70buwjvpywmh0"

# Fetch API Token securely from local environment variable
API_TOKEN = os.getenv("BRIGHT_DATA_API_TOKEN", "")

BASE_DIR = (
    Path(__file__).resolve().parent.parent if "__file__" in locals() else Path(".")
)
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def trigger_and_download_snapshot(
    search_query: str = "topic:machine-learning stars:>50", max_pages: int = 15
) -> Path:
  """Triggers the Bright Data Collector via API and downloads the snapshot.

  Skips execution if today's snapshot already exists locally.
  """
  today_str = datetime.now(timezone.utc).strftime("%Y_%m_%d")
  output_filepath = RAW_DIR / f"raw_{today_str}.csv"

  # Check if today's snapshot was already collected
  if output_filepath.exists():
    print(
        f"ℹ️ [Fetcher] Snapshot for today ({output_filepath.name}) already"
        " exists. Skipping API call."
    )
    return output_filepath

  if not API_TOKEN:
    print(
        "ℹ️ [Fetcher] No BRIGHT_DATA_API_TOKEN found in environment. Using"
        " existing raw files."
    )
    return None

  url = f"https://api.brightdata.com/dca/trigger?collector={COLLECTOR_ID}&queue_next=1"
  headers = {
      "Authorization": f"Bearer {API_TOKEN}",
      "Content-Type": "application/json",
  }
  payload = [{
      "url": "https://github.com/search?q=topic%3Amachine-learning+stars%3A%3E50&type=repositories&s=updated&o=desc",
      "query": search_query,
      "max_pages": max_pages,
  }]

  print(f"🚀 Triggering Bright Data Collector Endpoint [{COLLECTOR_ID}]...")
  try:
    res = requests.post(url, json=payload, headers=headers, timeout=30)
    if res.status_code not in [200, 202]:
      print(f"❌ API Trigger Error ({res.status_code}): {res.text}")
      return None

    response_data = res.json()
    collection_id = response_data.get("collection_id") or response_data.get(
        "response_id"
    )
    print(f"✅ Collector Triggered! Job ID: {collection_id}")
  except Exception as e:
    print(f"❌ Error triggering collector: {e}")
    return None

  # Poll for results
  dataset_url = f"https://api.brightdata.com/dca/dataset?id={collection_id}"
  print("⏳ Polling Bright Data endpoint for completed snapshot...")

  for attempt in range(25):
    time.sleep(12)
    try:
      r = requests.get(dataset_url, headers=headers)
      if r.status_code == 200 and len(r.content) > 0:
        with open(output_filepath, "wb") as f:
          f.write(r.content)
        print(f"🎉 Live Snapshot Saved: {output_filepath.name}")
        return output_filepath
      elif r.status_code in [202, 204]:
        print(f"   ... collection in progress (attempt {attempt + 1}/25)")
      else:
        print(f"⚠️ Polling status ({r.status_code})")
    except Exception as err:
      print(f"⚠️ Polling attempt error: {err}")
      break

  return None


if __name__ == "__main__":
  trigger_and_download_snapshot()