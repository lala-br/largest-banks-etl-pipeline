from bs4 import BeautifulSoup  # Parse HTML and extract webpage content
import requests                # Send HTTP requests to websites
import pandas as pd            # Data manipulation using DataFrames
import numpy as np              # Numerical operations and rounding
import sqlite3                  # Connect to and interact with SQLite databases
from datetime import datetime   # Generate timestamps for logging

# Code for ETL operations on Country-GDP data

# Importing the required libraries

def log_progress(message):
    timestamp_format = '%Y-%m-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open("./code_log.txt", "a") as f:
        f.write(timestamp + " : " + message + "\n")

def extract(url, table_attribs):

    # Send HTTP request
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    page = response.text
    data = BeautifulSoup(page, 'html.parser')

    # Display diagnostics
    print("Status code:", response.status_code)
    print("Final URL:", response.url)
    print("Content type:", response.headers.get("Content-Type"))
    print("Page title:", data.title)
    print("Number of tables:", len(data.find_all('table')))
    print("Number of tbody elements:", len(data.find_all('tbody')))

    # Find the heading "By market capitalization"
    heading = next(
        (
            h for h in data.find_all(['h2', 'h3'])
            if "By market capitalization" in h.get_text(" ", strip=True)
        ),
        None
    )

    if heading is None:
        raise ValueError("Could not find the market capitalization heading.")

    # Find the table immediately following the heading
    table = heading.find_next('table')

    if table is None:
        raise ValueError("Could not find the market capitalization table.")

    rows = table.find_all('tr')

    # Initialize DataFrame
    df = pd.DataFrame(columns=table_attribs)

    # Extract bank information
    for row in rows:

        col = row.find_all('td')

        if len(col) < 3:
            continue

        bank_name = col[1].get_text(" ", strip=True)

        market_cap_text = col[2].get_text(strip=True)
        market_cap_text = market_cap_text.replace(',', '').replace('$', '')

        try:
            market_cap = float(market_cap_text)
        except ValueError:
            continue

        data_dict = {
            "Name": bank_name,
            "MC_USD_Billion": market_cap
        }

        df1 = pd.DataFrame([data_dict])
        df = pd.concat([df, df1], ignore_index=True)

    # Keep the top 10 banks
    df = df.head(10)

    if df.empty:
        raise ValueError("No bank records were extracted.")

    print("\nExtracted bank data:")
    print(df)

    return df

def transform(df, csv_path):
    exchange_rate = pd.read_csv(csv_path)

    exchange_rate = exchange_rate.set_index('Currency').to_dict()['Rate']

    df['MC_USD_Billion'] = pd.to_numeric(df['MC_USD_Billion'])

    gbp_rate = float(exchange_rate['GBP'])
    df['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in df['MC_USD_Billion']]

    eur_rate = float(exchange_rate['EUR'])
    df['MC_EUR_Billion'] = [np.round(x * eur_rate, 2) for x in df['MC_USD_Billion']]

    inr_rate = float(exchange_rate['INR'])
    df['MC_INR_Billion'] = [np.round(x * inr_rate, 2) for x in df['MC_USD_Billion']]

    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_queries(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

# Main execution

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"

table_attribs = ["Name", "MC_USD_Billion"]

db_name = 'Banks.db'
table_name = 'Largest_banks'

csv_path = "./exchange_rate.csv"
output_path = "./Largest_banks_data.csv"

# Task 1: Declaring known values
log_progress("Preliminaries complete. Initiating ETL process")

# Task 2: Extract data
extracted_data = extract(url, table_attribs)
print(extracted_data)

log_progress("Data extraction complete. Initiating Transformation process")

# Task 3: Transform data
transformed_data = transform(extracted_data, csv_path)
print(transformed_data)

# Print EUR market capitalization of the 5th largest bank
print(transformed_data['MC_EUR_Billion'][4])

log_progress("Data transformation complete. Initiating Loading process")

# Task 4: Load data to CSV
load_to_csv(transformed_data, output_path)

log_progress("Data saved to CSV file")

# Task 5: Connect to SQLite database
sql_connection = sqlite3.connect(db_name)

log_progress("SQL Connection initiated")

# Load data to database
load_to_db(transformed_data, sql_connection, table_name)

log_progress("Data loaded to Database as a table, Executing queries")

# Task 6: Run SQL queries

# Query 1: Print entire table
query_statement = "SELECT * FROM Largest_banks"
run_queries(query_statement, sql_connection)

# Query 2: Calculate average market capitalization
query_statement = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_queries(query_statement, sql_connection)

# Query 3: Print names of top 5 banks
query_statement = "SELECT Name FROM Largest_banks LIMIT 5"
run_queries(query_statement, sql_connection)

log_progress("Process Complete")

# Close database connection
sql_connection.close()

log_progress("Server Connection closed")