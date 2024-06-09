import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)

    csv_paths = [
        '../subject/customer/data_2022_oct.csv',
        '../subject/customer/data_2022_nov.csv',
        '../subject/customer/data_2022_dec.csv',
        '../subject/customer/data_2023_jan.csv',
    ]

    for path in csv_paths:
        data = pd.read_csv(path)
        file_name_with_extension = path.split('/')[-1]
        table_name = file_name_with_extension.split('.')[0]
        data.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data from {path} has been written to {table_name}")


if __name__ == '__main__':
    main()
