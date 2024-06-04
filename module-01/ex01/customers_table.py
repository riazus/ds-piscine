import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, DateTime
from sqlalchemy.dialects.postgresql import ENUM


def main():
    """Driver main function"""
    csv_file_paths = [
        '../../module-00/subject/customer/data_2022_oct.csv',
        '../../module-00/subject/customer/data_2022_nov.csv',
        '../../module-00/subject/customer/data_2022_dec.csv',
        '../../module-00/subject/customer/data_2023_jan.csv'
    ]

    df_list = [pd.read_csv(file) for file in csv_file_paths]
    combined_df = pd.concat(df_list, ignore_index=True)

    conn_string = "postgresql+psycopg2://jannabel:mysecretpassword@localhost:5432/piscineds"
    engine = create_engine(conn_string)

    # Connect to the database to create ENUM type
    # with engine.connect() as conn:
    #     conn.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_type_enum') THEN CREATE TYPE event_type_enum AS ENUM ('remove_from_cart', 'view', 'cart', 'purchase'); END IF; END $$;")

    metadata = MetaData()
    Table('customers', metadata,
          Column('event_time', DateTime),
          Column('event_type',
                 ENUM('remove_from_cart',
                      'view',
                      'cart',
                      'purchase',
                      name='event_type_enum')),
          Column('product_id', Integer),
          Column('price', Float),
          Column('user_id', Integer),
          Column('user_session', String))

    # Create table in PostgreSQL if it does not exist
    metadata.create_all(engine)

    # Write data to PostgreSQL
    combined_df.to_sql('customers', engine, if_exists='append', index=False)

    print("Data from all CSV files has been successfully written")


if __name__ == '__main__':
    main()
