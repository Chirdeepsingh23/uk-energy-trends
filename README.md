# 🇬🇧 UK Energy Trends (2024–2025)

This project analyses the UK's electricity generation mix using real-time and historical data from the [Carbon Intensity API](https://carbon-intensity.github.io/). It combines **data engineering**, **automated scheduling**, and **exploratory analysis** to uncover insights into clean vs fossil fuel usage patterns.

---

## 📦 Project Structure

uk-energy-trends/
├── dags/ # Airflow DAGs
├── data/ # CSV data files (excluded from Git)
├── db/ # SQLite database
├── notebooks/ # Jupyter analysis notebooks
├── scripts/ # Data fetch + backfill scripts
├── .gitignore
├── README.md
└── requirements.txt


---

## 🔧 Tech Stack

- Python (pandas, matplotlib, sqlite3)
- Apache Airflow (hourly scheduling)
- SQLite (structured data storage)
- Jupyter Notebook (exploratory analysis)
- Git + GitHub (version control)

---

## 💡 What This Project Does

### Data Engineering
- Pulls hourly UK generation mix from API
- Stores both latest and historical data
- Backfills 1 year of hourly data on demand
- Schedules automated hourly fetch via Airflow
- Writes data to both CSV and SQLite

### Data Analysis
- Cleans and deduplicates data
- Exploratory insights by:
  - Hour of day
  - Day of week
  - Season and month
  - Clean vs fossil comparison
- Visualised with line plots, bar charts, and pie charts

---

## 📊 Key Insights

- Clean energy consistently contributed over 50% on average
- Wind and gas were the top two fuels, each around 29%
- Gas usage spiked in colder months; solar dominated summer
- Weekends saw increased wind and imports vs weekdays
- Seasonal patterns revealed solar’s summer peak and winter wind strength

---

## 🧠 Summary and Conclusion

This project showcases how public API data can be used to build a reproducible data pipeline and generate meaningful energy sector insights.

It highlights:
- How fuel usage shifts across time
- How renewables compete with traditional sources
- The UK's evolving energy landscape in real terms

---

## 📁 How to Run

1. Clone the repo:
```bash
git clone https://github.com/your-username/uk-energy-trends.git
cd uk-energy-trends

2. Set up virtual environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Backfill historical Data (optional): 
python scripts/backfill_generation_mix.py

4. Start Airflow: 
airflow scheduler
airflow webserver

---

## Full Analysis
View the full Jupyter Notebook here:
energy_trend_visualisation.ipynb

## 📝Credits

Built by Chirdeep Singh Reen.
Data provided by the UK Carbon Intensity API.