# ETL Pipeline (Python)

This project is a complete ETL pipeline built in Python.
It simulates a real workflow for loading raw CSV data, transforming it, enriching it with external sources, 
and saving results into different formats and destinations.
The goal is to show clean project structure, repeatability, testability, and use of 
common data engineering tools such as SQLAlchemy, pandas, Parquet, CI, and logging.
Python ETL pipeline contains additional scripts, testing, and CI.

### What the project does
#### Extract & Transform
The pipeline loads input CSV files and performs simple business transformations.
The results are saved as Parquet into a date-based folder structure (e.g. output/2025-01-12/).
This makes the ETL runs versioned and easy to track.

#### API Integration

A separate component connects to the NBP API (Polish National Bank) using the requests library.
It downloads the EUR exchange rate and stores both:
the raw API response (json)
transformed sales data converted to EUR (parquet)

#### Loading to SQL Server

The pipeline uses SQLAlchemy to: connect to SQL Server via ODBC, create the database if it does not exist
and load transformed Parquet data into a sales table
It running an aggregation query (sales per region) and save its output back to the analysis/date directory

You can run scripts individually by typing:
python scripts/extract_transform.py
python scripts/add_fx.py
python scripts/load_to_sql.py

in terminal

#### Logging

The project includes a custom logging setup with:
- log rotation (so logs don’t grow infinitely)
- console output
- no duplicate log handlers when running inside notebooks
Logs are stored inside logs/pipeline.log.

#### Tests

The repository contains:
- unit tests with edge cases
- integration tests, e2e
- Mocking API calls (requests) and database connections (SQLAlchemy).
The tests avoid touching real external systems — SQLAlchemy engines, Parquet files, and API calls are replaced with mocks (patch, MagicMock)
You can tests by typing: pytest tests -v

#### The CI checks:

- installation of project dependencies
- correctness of the ETL logic via tests
- structure of all modules (imports, project layout)

### Notebook Version
The project also includes a full notebook-based version of the ETL inside:
This folder contains:

- Jupyter version of the entire ETL pipeline

- additional data analysis and visualizations

- exploratory transformations and charts that complement the Python scripts
