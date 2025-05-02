import requests
import pandas as pd
from datetime import datetime

def fetch_generation_mix():
    url = "https://api.carbonintensity.org.uk/generation"
    response = requests.get(url)
    data = response.json()

    mix = data["data"]["generationmix"]
    timestamp = data["data"]["from"]

    df = pd.DataFrame(mix)
    df["timestamp"] = pd.to_datetime(timestamp)

    # Save to CSV
    df.to_csv("data/generation_mix_latest.csv", index=False)
    print("Saved generation mix to data/generation_mix_latest.csv")

if __name__ == "__main__":
    fetch_generation_mix()
