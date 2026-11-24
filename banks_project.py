
# Code for ETL operations on Banks data

# Importing the required libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime


# Initialize the required variables

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

table_attribs = ["Name", "MC_USD_Billion"]

db_name = 'Banks.db'
table_name = 'Largest_banks'

csv_path = './Largest_banks_data.csv'
exchange_rate_csv_path = './exchange_rate.csv'


# Task 1: Logging function

def log_progress(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open("./code_log.txt", "a") as f:
        f.write(timestamp + " : " + message + "\n")


# First log entry

log_progress('Preliminaries complete. Initiating ETL process')


# Task 2: Extraction function

def extract(url, table_attribs):

    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')

    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')

        if len(col) >= 3:
            data_dict = {
                "Name": col[1].get_text(strip=True),
                "MC_USD_Billion": float(col[2].get_text(strip=True))
            }

            df1 = pd.DataFrame([data_dict])
            df = pd.concat([df, df1], ignore_index=True)

    return df
    
# Calling extract function

df = extract(url, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')

#print(df)

# Task 3: Transformation function

def transform(df):

    exchange_rate_df = pd.read_csv(exchange_rate_csv_path)

    exchange_rate = exchange_rate_df.set_index('Currency').to_dict()['Rate']

    # Convert USD to GBP
    gbp_rate = float(exchange_rate['GBP'])
    df['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in df['MC_USD_Billion']]

    # Convert USD to EUR
    eur_rate = float(exchange_rate['EUR'])
    df['MC_EUR_Billion'] = [np.round(x * eur_rate, 2) for x in df['MC_USD_Billion']]

    # Convert USD to INR
    inr_rate = float(exchange_rate['INR'])
    df['MC_INR_Billion'] = [np.round(x * inr_rate, 2) for x in df['MC_USD_Billion']]

    return df

# Calling transform function

df = transform(df)

log_progress('Data transformation complete')

print(df)

# Print market capitalization of 5th largest bank in EUR
print(df['MC_EUR_Billion'][4])


# Task 4: Loading to CSV

def load_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)


# Calling load_to_csv function

load_to_csv(df, csv_path)

log_progress('Data loaded to CSV file')

# Task 5: Loading to Database

def load_to_db(df, conn, table_name):
    df.to_sql(table_name, conn, if_exists='replace', index=False)


# Calling load_to_db function

conn = sqlite3.connect(db_name)

load_to_db(df, conn, table_name)

log_progress('Data loaded to Database successfully')



# Task 6: Function to run queries on Database

def run_queries(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


# Query 1: Print the entire table

query_statement = "SELECT * FROM Largest_banks"
run_queries(query_statement, conn)


# Query 2: Average market capitalization in GBP

query_statement = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_queries(query_statement, conn)


# Query 3: Print names of top 5 banks

query_statement = "SELECT Name FROM Largest_banks LIMIT 5"
run_queries(query_statement, conn)


# Log completion

log_progress('Process Complete')

# Close database connection after all queries
conn.close()
