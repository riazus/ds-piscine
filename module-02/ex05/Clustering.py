import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)
    query = """
    SELECT DISTINCT
        CASE
            WHEN purchase_months = 5 THEN 'loyal platinum'
            WHEN purchase_months = 4 THEN 'loyal gold'
            WHEN purchase_months = 3 THEN 'loyal silver'
            WHEN purchase_months = 2 THEN 'new customer'
            WHEN purchase_months = 1 AND NOT (purchase_month = 1 OR purchase_month = 2) THEN 'inactive'
            WHEN purchase_months = 1 THEN 'new customer'
        END AS purchase_months_category,
        COUNT(DISTINCT user_id) AS customer_count
    FROM (
        SELECT
            user_id,
            COUNT(DISTINCT EXTRACT(MONTH FROM event_time)) AS purchase_months,
            EXTRACT(MONTH FROM MIN(event_time)) AS purchase_month
        FROM
            customers
        WHERE
            event_type = 'purchase'
        GROUP BY
            user_id
    ) AS purchase_counts
    GROUP BY
        purchase_months_category
    ORDER BY
        customer_count;
    """

    # TODO
    data = pd.read_sql(query, engine)

    group_names = {
        0: "loyal gold",
        1: "inactive",
        2: "new customer",
        3: "loyal silver",
        4: "loyal platinum"
    }

    data_for_clustering = np.array([[row[1]] for row in data])

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_for_clustering)

    num_clusters = 5
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_data)

    cluster_averages = []
    for i in range(num_clusters):
        cluster_points = np.array([data[j][1] for j in range(len(data)) if cluster_labels[j] == i])
        cluster_averages.append(np.mean(cluster_points))
    sorted_indices = np.argsort(cluster_averages)

    sorted_data = [data[idx] for idx in sorted_indices]

    plt.figure(figsize=(10, 6))
    for i, idx in enumerate(sorted_indices):
        cluster_points = np.array([data[j][1] for j in range(len(data)) if cluster_labels[j] == idx])
        color = plt.cm.viridis(i / num_clusters)
        plt.barh(i, np.mean(cluster_points), color=color, alpha=0.7)
        plt.text(np.mean(cluster_points) + 0.8, i, f'{group_names[idx]}', ha='left', va='center', fontsize=10, color='black', weight='bold')

    plt.ylabel("Clusters")
    plt.xlabel("Number of Customers")
    plt.title("Cluster Visualization")
    plt.yticks(range(num_clusters), [f'Cluster {i+1}' for i in range(num_clusters)])
    plt.grid(True)
    plt.show()

    query2 = """
    SELECT
        purchase_months_category,
        customer_count,
        avg_purchase_months,
        avg_purchase_frequency,
        purchase_frequency
    FROM (
        SELECT
            CASE
                WHEN purchase_months = 5 THEN 'loyal platinum'
                WHEN purchase_months = 4 THEN 'loyal gold'
                WHEN purchase_months = 3 THEN 'loyal silver'
                WHEN purchase_months = 2 THEN 'new customer'
                WHEN purchase_months = 1 AND NOT (purchase_month = 1 OR purchase_month = 2) THEN 'inactive'
                WHEN purchase_months = 1 THEN 'new customer'
            END AS purchase_months_category,
            COUNT(DISTINCT user_id) AS customer_count,
            AVG(purchase_months) AS avg_purchase_months,
            AVG(purchase_frequency) AS avg_purchase_frequency,
            AVG(purchase_frequency) AS purchase_frequency
        FROM (
            SELECT
                user_id,
                COUNT(*) AS purchase_months,
                EXTRACT(MONTH FROM MIN(event_time)) AS purchase_month,
                COUNT(*) * 1.0 / COUNT(DISTINCT user_id) AS purchase_frequency
            FROM
                customers
            WHERE
                event_type = 'purchase'
            GROUP BY
                user_id
        ) AS purchase_counts
        GROUP BY
            purchase_months_category
        HAVING
            AVG(purchase_months) BETWEEN 0 AND 6
    ) AS final_result
    ORDER BY
        customer_count;
    """

    # TODO
    data2 = pd.read_sql(query2, engine)

    categories = [row[0] for row in data2]
    user_counts = [int(row[1]) for row in data2]
    months_purchased = [int(row[2]) for row in data2]
    avg_purchase_frequency = [float(row[3]) for row in data2]

    circle_sizes = [count * 10 for count in user_counts]

    unique_colors = plt.cm.tab20(np.linspace(0, 1, len(categories)))

    normalized_circle_sizes = [count / max(user_counts) * 300 for count in user_counts]

    plt.figure(figsize=(10, 6))
    for i, category in enumerate(categories):
        plt.scatter(months_purchased[i], avg_purchase_frequency[i], s=normalized_circle_sizes[i], c=[unique_colors[i]], alpha=0.7)
        plt.annotate(f"{category}\n{user_counts[i]} user", (months_purchased[i] - 0.5, avg_purchase_frequency[i] - 0.1),
                    fontsize=10, ha='center')

    plt.xticks(np.arange(0, max(months_purchased) + 1, step=1))
    plt.xlabel("Months Purchased In")
    plt.ylabel("Average Purchase Frequency")
    plt.title("Groups Visualization")
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
