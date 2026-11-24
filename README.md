# Largest Banks ETL Pipeline

## Overview
Developed an end-to-end ETL pipeline using Python to extract bank market capitalization data, convert USD values into GBP, EUR and INR, and load the results into CSV and SQLite databases.

## Technologies
Python | Pandas | NumPy | BeautifulSoup | Requests | SQLite | SQL

## Workflow
- **Extract:** Scraped bank data from an archived Wikipedia page using BeautifulSoup.
- **Transform:** Applied currency exchange rates to convert USD into GBP, EUR and INR.
- **Load:** Stored transformed data in CSV and SQLite.
- **Analyse:** Executed SQL queries to retrieve bank records and calculate average market capitalization.
- **Logging:** Tracked ETL execution using timestamps.

## Project Files
- `banks_project.py` – Main ETL script
- `exchange_rate.csv` – Exchange-rate input
- `Largest_banks_data.csv` – Transformed output

## Run the Project

```bash
pip install requests beautifulsoup4 pandas numpy
python banks_project.py
```

## Data Sources
- [Wikipedia – Largest Banks](https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks)
- [IBM Skills Network – Exchange Rates](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv)
