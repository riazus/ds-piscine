import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, MetaData, Text, BigInteger


def main():
    """Driver main function"""
    df_list = pd.read_csv("../subject/item/item.csv")

    conn_string = "postgresql+psycopg2://jannabel:mysecretpassword@localhost:5432/piscineds"
    engine = create_engine(conn_string)

    metadata = MetaData()
    Table('items', metadata,
          Column('product_id', Integer, nullable=False),
          Column('category_id', BigInteger),
          Column('category_code', Text),
          Column('brand', Text))

    # Create table in PostgreSQL if it does not exist
    metadata.create_all(engine)

    # Write data to PostgreSQL
    df_list.to_sql('items', engine, if_exists='append', index=False)

    print("Data from all CSV files has been successfully written")


if __name__ == '__main__':
    main()
