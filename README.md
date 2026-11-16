# Largest Banks ETL Pipeline

A Python project that extracts market capitalization data for the world's largest banks, transforms the values into multiple currencies, and stores the results in CSV and SQLite formats.

## Project Overview

This project was completed as part of the IBM Data Engineering course on Coursera.

The objective was to develop an ETL (Extract, Transform, Load) workflow that automates the collection and processing of bank market capitalization data.

The extracted USD values are converted into GBP, EUR, and INR using exchange rates provided in a CSV file.

## Project Workflow

The project follows three main ETL stages:

### 1. Extract
- Retrieve bank market capitalization data from a Wikipedia page using its archived version.
- Parse the HTML content using BeautifulSoup.
- Extract bank names and their market capitalization in USD.
- Store the extracted data in a Pandas DataFrame.

### 2. Transform
- Read currency exchange rates from a CSV file.
- Convert market capitalization values from USD into:
  - GBP (British Pound)
  - EUR (Euro)
  - INR (Indian Rupee)
- Round converted values to two decimal places.

### 3. Load
- Export the transformed data into a CSV file.
- Store the data in an SQLite database.
- Execute SQL queries to retrieve and analyze the results.

## Technologies & Libraries

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation and processing |
| BeautifulSoup | HTML parsing and data extraction |
| Requests | Retrieving webpage content |
| NumPy | Numerical operations and rounding |
| SQLite | Relational database storage |
| SQL | Querying the processed data |

## Project Files

| File | Description |
|---|---|
| `banks_project.py` | Main ETL script |
| `exchange_rate.csv` | Currency exchange rate data |
| `Largest_banks_data.csv` | Transformed output dataset |
| `Banks.db` | SQLite database |
| `code_log.txt` | ETL execution log |

## SQL Queries

The project includes several SQL queries to verify and explore the loaded data:

1. Retrieve all records from the `Largest_banks` table.
2. Calculate the average market capitalization in GBP.
3. Retrieve the names of the first five banks.

## What I Learned

- Extracting structured data from HTML pages.
- Working with Pandas DataFrames.
- Transforming datasets using external reference data.
- Implementing a basic ETL workflow.
- Loading processed data into CSV files and relational databases.
- Executing SQL queries through Python and SQLite.
- Logging execution progress throughout a data pipeline.

## Acknowledgment

Completed as part of the IBM Data Engineering Professional Certificate coursework on Coursera.
