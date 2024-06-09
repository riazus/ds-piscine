import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, Column, Integer, \
    MetaData, Text, BigInteger


def main():
    """Driver main function"""
    df_list = pd.read_csv("../subject/item/item.csv")

    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)

    metadata = MetaData()
    Table('items', metadata,
          Column('product_id', Integer, nullable=False),
          Column('category_id', BigInteger),
          Column('category_code', Text),
          Column('brand', Text))

    metadata.create_all(engine)
    print("Table items successfully created")

    df_list.to_sql('items', engine, if_exists='append', index=False)
    print("Data successfully writed to items table")


if __name__ == '__main__':
    main()
