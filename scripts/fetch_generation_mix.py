import requests
import pandas as pd
from datetime import datetime
import os
import sqlite3

def save_to_history(df):
    history_path = "data/generation_mix_history.csv"

    if os.path.exists(history_path):
        df.to_csv(history_path, mode="a", header=False, index=False)
    else:
        df.to_csv(history_path, index=False)

def save_to_sqlite(df):
    db_path = "db/generation_mix.sqlite"
    os.makedirs("db", exist_ok=True)  # Ensure db/ folder exists

    conn = sqlite3.connect(db_path)
    df.to_sql("generation_mix", conn, if_exists="append", index=False)
    conn.close()

def fetch_generation_mix():
    url = "https://api.carbonintensity.org.uk/generation"
    response = requests.get(url)
    data = response.json()

    mix = data["data"]["generationmix"]
    timestamp = data["data"]["from"]

    df = pd.DataFrame(mix)
    df["timestamp"] = pd.to_datetime(timestamp)

    # Save both latest and historical
    df.to_csv("data/generation_mix_latest.csv", index=False)
    save_to_history(df)
    save_to_sqlite(df)

    print("Saved latest, appended to history, and stored in SQLite.")

if __name__ == "__main__":
    fetch_generation_mix()
