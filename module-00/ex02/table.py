from sqlalchemy import create_engine, Table, Column, Integer, String, \
      Float, MetaData, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from dotenv import load_dotenv
import os


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}\
        @localhost:5432/{pg_db}"
    engine = create_engine(conn_string)

    table_names = [
        'data_2022_oct',
        'data_2022_nov',
        'data_2022_dec',
        'data_2023_jan',
    ]

    event_type_enum = ENUM(
        'remove_from_cart',
        'view',
        'cart',
        'purchase',
        name='event_type_enum'
    )

    metadata = MetaData()

    for name in table_names:
        Table(name, metadata,
              Column('event_time', DateTime),
              Column('event_type', event_type_enum),
              Column('product_id', Integer),
              Column('price', Float),
              Column('user_id', Integer),
              Column('user_session', String))

    metadata.create_all(engine)

    print("Tables were successfully created")


if __name__ == '__main__':
    main()
