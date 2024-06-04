import os
import enum
import pandas as pd
from sqlalchemy import create_engine


class event_type_enum(enum.Enum):
    """Enum for event types"""
    view = 'view'
    cart = 'cart'
    purchase = 'purchase'
    remove_from_cart = 'remove_from_cart'


def get_db_engine():
    """Return a PostgreSQL database engine"""
    return create_engine('postgresql://{}:{}@{}/{}'.format(
        'jannabel', 'mysecretpassword', 'localhost:5432', 'piscineds'))


def csv_to_postgres(engine, csv_file_path, table_name):
    """Write data from a CSV file to a PostgreSQL table"""
    data = pd.read_csv(csv_file_path)
    data.to_sql(table_name, engine, if_exists='append', index=False)

    print(f"Data from {csv_file_path} has been written to {table_name}")


def main():
    """Driver main function"""
    folder_path = "../subject/customer"
    engine = get_db_engine().connect()

    for filename in os.listdir(folder_path):
        if not filename.endswith(".csv"):
            continue

        table_name = filename.split(".")[0]
        csv_file_path = os.path.join(folder_path, filename)
        csv_to_postgres(engine, csv_file_path, table_name)

    engine.close()


if __name__ == '__main__':
    main()
