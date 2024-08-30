import os
import logging
import dask.dataframe as dd
import psycopg2
from google.cloud import storage


logging.basicConfig(filename='logs/data_cleaning.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GCS_BUCKET_NAME = 'my-data-lake-test'
GCS_FILE_NAME = 'sotatek/insurance_claims.csv'
LOCAL_TEMP_FILE = 'insurance_claims.csv'

POSTGRESQL_CONNECTION = {
    'host': 'localhost',
    'database': os.getenv('POSTGRES_DB', 'test'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
}

def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    logging.info(f"Downloaded {source_blob_name} to {destination_file_name}.")


def clean_data(df):
    
    df = df.dropna(subset=['IDpol'])
    logging.info(f"Dropped rows with null IDpol")

    metrics_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    metrics_columns.remove('IDpol')
    
    for column in metrics_columns:
        max_value = df[column].max().compute()
        df[column] = df[column].fillna(0)
        df[column] = df[column].replace([float('inf')], max_value)
        df[column] = df[column].replace([-float('inf')], -max_value)
        logging.info(f"Cleaned column {column}: Filled NaNs with 0 and inf with value {max_value}")
    
    return df


def load_data_to_postgresql(df, conn, batch_size=10000):
    cur = conn.cursor()
    
    for i in range(0, len(df), batch_size):
        start = i
        end = min(i + batch_size, len(df))
        batch = df.loc[start:end].compute()
        
        rows = [tuple(row) for _, row in batch.iterrows()]
        args_str = b','.join(cur.mogrify('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', row) for row in rows)
        insert_query = b'INSERT INTO insurance_claims (IDpol, ClaimNb, Exposure, VehPower, VehAge, DrivAge, BonusMalus, VehBrand, VehGas, Area, Density, Region, ClaimAmount) VALUES ' + args_str
        
        cur.execute(insert_query.decode('utf-8'))
        logging.info(f"Inserted batch {i // batch_size + 1} into PostgreSQL")
    
    conn.commit()
    cur.close()
    
    
def main():
    try:
        # download data from GCS
        download_from_gcs(GCS_BUCKET_NAME, GCS_FILE_NAME, LOCAL_TEMP_FILE)
        
        # Read and clean data using Dask
        df = dd.read_csv(LOCAL_TEMP_FILE, assume_missing=True)
        df = clean_data(df)
        
        # Load data to PostgreSQL
        conn = psycopg2.connect(**POSTGRESQL_CONNECTION)
        load_data_to_postgresql(df, conn)
        
        # clean up
        os.remove(LOCAL_TEMP_FILE)
        logging.info(f"Removed local file {LOCAL_TEMP_FILE}.")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
