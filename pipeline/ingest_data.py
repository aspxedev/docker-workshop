
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

pg_user = 'root'
pg_password = 'root'
pg_host = 'localhost'
pg_db = 'ny_taxi'
pg_port = '5432'
year = 2021
month = 1
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

def download_data(url: str, dtype: dict, parse_dates: list) -> pd.DataFrame:

    # Read a sample of the data
    df = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates
    )

    return df

def create_iterator() -> pd.DataFrame:

    df_iterator = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000,
    )

    return df_iterator

def create_table(engine, df):

    df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


def insert_data(engine, df_iterator):
    first = True

    for df_chunk in tqdm(df_iterator):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name="yellow_taxi_data",
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))

def run():
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    df = download_data(url, dtype, parse_dates)

    create_table(engine, df)

    df_iterator = create_iterator()

    insert_data(engine, df_iterator)        

        
if __name__ == "__main__":

    run()



