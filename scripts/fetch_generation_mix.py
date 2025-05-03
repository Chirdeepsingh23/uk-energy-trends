import requests
import pandas as pd
from datetime import datetime
import os


def save_to_history(df):
    history_path = "data/generation_mix_history.csv"

    if os.path.exists(history_path):
        df.to_csv(history_path, mode="a", header=False, index=False)
    else:
        df.to_csv(history_path, index=False)

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

    print("Saved latest and appended to history.")

if __name__ == "__main__":
    fetch_generation_mix()
