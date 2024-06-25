import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.cluster import KMeans


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)
    query = """
    SELECT user_id, COUNT(*) AS purchases
        FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id
    HAVING COUNT(*) < 30
    ORDER BY purchases DESC;
    """
    data = pd.read_sql(query, engine)

    wss = []
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(data)
        wss.append(kmeans.inertia_)

    plt.plot(range(1, 11), wss)
    plt.xlabel("Number of clusters")
    plt.title("The Elbow Method")
    plt.show()


if __name__ == '__main__':
    main()
