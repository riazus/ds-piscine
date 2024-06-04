import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


def main():
    """Driver main function"""
    conn_string = "postgresql+psycopg2://jannabel:mysecretpassword@localhost:5432/piscineds"
    engine = create_engine(conn_string)
    query = "SELECT event_type FROM customers"
    df = pd.read_sql(query, engine)

    event_type_counts = df['event_type'].value_counts()

    plt.figure(figsize=(10, 7))
    plt.pie(event_type_counts, labels=event_type_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()
