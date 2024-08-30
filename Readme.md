# GCS to PostgreSQL ETL Project

## Overview

This project provides a solution to extract insurance claim data from Google Cloud Storage (GCS), load it into PostgreSQL, and perform data analysis tasks, including calculating summary statistics

### Setup and Usage

- Set up and upload your CSV file to Google Cloud Storage (GCS).
- Run PostgreSQL using Docker:
  ```bash
  docker-compose up

- Install the required Python packages

  ```bash 
  pip install dask[complete] google-cloud-storage sqlalchemy psycopg2

- Add the following environment variables
  - `GOOGLE_APPLICATION_CREDENTIALS`:  Path to your Google Cloud service account JSON file.
  - `POSTGRES_USER`: Your PostgreSQL username.
  - `POSTGRES_PASSWORD`: Your PostgreSQL password.
- Run the data extraction and loading script
  ``python scripts/extract_gcp.py``

## Explanation of Approach
1. **Data Extraction**

- Download CSV from GCS: The script uses the google-cloud-storage library to download the CSV file from Google Cloud Storage.
- Read Data with Dask: Dask is used to read the data, allowing efficient handling of potentially large datasets.
2. **Data Cleaning**

- The IDpol column is assumed to be the primary key, and rows with null values in IDpol are dropped
- For the remaining metric columns, null values are filled with 0. Positive infinity (inf) is replaced with maximum value and negatve infinity (-inf) is replaced with -maximum
3. **Data Loading**

- Batch Loading: The cleaned data is loaded into PostgreSQL in batches to optimize memory usage and improve performance.
## Next Steps


- **Optimize Data Loading**: Explore multithreading or multiprocessing to further optimize the data loading process into PostgreSQL.
- **Encrypt Sensitive Data**: Implement encryption for sensitive data to enhance security.
- **Data Validation**: Add more comprehensive data validation checks before loading the data into PostgreSQL.
