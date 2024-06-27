import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import numpy as np


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)
    query = """
    SELECT user_id, COUNT(*) AS frequency
        FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id;
    """
    data_frequency = pd.read_sql(query, engine)

    query1 = """
    SELECT user_id, SUM(price) as price
        FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id
    HAVING SUM(price) < 225;
    """
    data_monetary = pd.read_sql(query1, engine)

    frequency = data_frequency["frequency"]
    monetary = data_monetary["price"]

    _, axs = plt.subplots(1, 2, figsize=(15, 6))
    axs[0].grid(True, zorder=-1)
    axs[0].hist(frequency, bins=5, edgecolor='k')
    axs[0].set_ylabel('customers')
    axs[0].set_xlabel('frequency')
    axs[0].set_xticks(range(0, 39, 10))
    axs[0].set_ylim(0, 60000)
    axs[0].set_title('Frequency distribution of the number of orders per customer')

    axs[1].grid(True, zorder=-1)
    axs[1].hist(monetary, bins=5, edgecolor='k')
    axs[1].set_ylabel('Count of customers')
    axs[1].set_xlabel('Monetary value in Altairian Dollars (A$)')
    axs[1].set_title('Frequency distribution of the purchase prices per customer')

    for ax in axs:
        ax.yaxis.grid(True, linestyle='-', alpha=0.7)
        ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
