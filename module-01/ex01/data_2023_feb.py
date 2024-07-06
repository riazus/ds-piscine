import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, Column, Integer, String, \
      Float, MetaData, DateTime
from sqlalchemy.dialects.postgresql import ENUM


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)

    metadata = MetaData()
    event_type_enum = ENUM(
        'remove_from_cart',
        'view',
        'cart',
        'purchase',
        name='event_type_enum'
    )

    Table('data_2023_feb', metadata,
        Column('event_time', DateTime),
        Column('event_type', event_type_enum),
        Column('product_id', Integer),
        Column('price', Float),
        Column('user_id', Integer),
        Column('user_session', String))

    metadata.create_all(engine)

    data = pd.read_csv("../data_2023_feb.csv")
    data.to_sql('data_2023_feb', engine, if_exists='append', index=False)

    print("data_2023_feb.py was successfully writed to db.")


if __name__ == '__main__':
    main()
