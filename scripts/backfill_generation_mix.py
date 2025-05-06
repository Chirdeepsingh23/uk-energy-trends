import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import sqlite3
import os
import time

# Constants
BASE_URL = "https://api.carbonintensity.org.uk/generation"
OUTPUT_CSV = "data/generation_mix_history.csv"
OUTPUT_DB = "db/generation_mix.sqlite"
TABLE_NAME = "generation_mix"

# Set time range (last 365 days, hour-by-hour)
end_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
start_time = end_time - timedelta(days=365)

# Create folders if needed
os.makedirs("data", exist_ok=True)
os.makedirs("db", exist_ok=True)

# Load existing timestamps to avoid duplication
existing_timestamps = set()
if os.path.exists(OUTPUT_CSV):
    existing_df = pd.read_csv(OUTPUT_CSV, usecols=["timestamp"])
    existing_timestamps = set(existing_df["timestamp"].unique())

print(f"Backfilling from {start_time} to {end_time}...")

# Loop through hourly intervals
current = start_time
all_data = []

while current < end_time:
    next_hour = current + timedelta(hours=1)
    from_str = current.strftime("%Y-%m-%dT%H:00Z")
    to_str = next_hour.strftime("%Y-%m-%dT%H:00Z")

    url = f"{BASE_URL}/{from_str}/{to_str}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        generation_data = data["data"]

        if isinstance(generation_data, list) and generation_data:
            first_entry = generation_data[0]
            mix = first_entry["generationmix"]
            timestamp = first_entry["from"]

            if timestamp in existing_timestamps:
                print(f"Skipping {timestamp} (already exists)")
            else:
                df = pd.DataFrame(mix)
                df["timestamp"] = pd.to_datetime(timestamp)
                all_data.append(df)
                print(f"Fetched {timestamp}")
        else:
            print(f"No generation data found for {from_str}")

    except Exception as e:
        print(f"Failed at {from_str}: {e}")

    current = next_hour
    time.sleep(0.2)  # Be kind to the API

# Save combined data
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)

    # Save to CSV
    if os.path.exists(OUTPUT_CSV):
        combined_df.to_csv(OUTPUT_CSV, mode="a", header=False, index=False)
    else:
        combined_df.to_csv(OUTPUT_CSV, index=False)

    # Save to SQLite
    conn = sqlite3.connect(OUTPUT_DB)
    combined_df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    conn.close()

    print(f"Saved {len(combined_df)} new records to CSV and SQLite.")
else:
    print("No new data fetched.")
