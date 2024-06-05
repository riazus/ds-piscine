import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns


def show_average_spend(engine):
    query = """
      SELECT
        event_time::date AS day,
        AVG(spend::NUMERIC) AS average_spend
      FROM (
        SELECT
          event_time,
          user_id,
          SUM(price) AS spend
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY event_time, user_id
      ) AS daily_spend
      GROUP BY day
      ORDER BY day;
    """
    df = pd.read_sql(query, engine)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.fill_between(df['day'], df['average_spend'], color="skyblue", alpha=0.4)
    plt.plot(df['day'], df['average_spend'], color="Slateblue", alpha=0.6)

    plt.title('average spend/cusotmers in Æ')
    plt.xlabel('Date')
    plt.ylabel('Average Spent')
    plt.grid(True)

    plt.show()


def show_total_sales(engine):
    query = """
        SELECT
          DATE_TRUNC('month', event_time) AS month,
          SUM(CAST(price AS NUMERIC)) AS total_revenue
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY month
        ORDER BY month;
    """
    df = pd.read_sql(query, engine)
    df['month'] = pd.to_datetime(df['month'])

    df['Month'] = df['month'].dt.strftime('%b')
    df['Year'] = df['month'].dt.strftime('%Y')

    df['MonthYear'] = df['Month'] + ' ' + df['Year']

    sns.set_theme(style="darkgrid")

    plt.figure(figsize=(12, 6))
    sns.barplot(x='MonthYear', y='total_revenue', data=df, color="skyblue", alpha=0.7)

    plt.title('Total Sales per Month')
    plt.xlabel('Month')
    plt.ylabel('Total Sales in Million of $')
    plt.yticks([0, 0.5e6, 1e6, 1.5e6, 2e6], ['0', '0.5', '1.0', '1.5', '2.0'])
    plt.ylim(0, 1.6e6)

    # Show the plot
    plt.show()


def show_number_of_customers(engine):
    query = """
      SELECT
          event_time::date AS day,
          COUNT(*) AS purchase_count
      FROM customers
      WHERE event_type = 'purchase'
      GROUP BY day
      ORDER BY day;
    """
    df = pd.read_sql(query, engine)
    df.set_index('day', inplace=True)

    sns.set_theme(style="darkgrid")

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x=df.index, y='purchase_count', color="blue", alpha=0.7)

    plt.title('Number of Customers per Day')
    plt.xlabel('')
    plt.ylabel('Number of Customers')

    plt.show()


def main():
    """Driver main function"""
    conn_string = "postgresql+psycopg2://jannabel:mysecretpassword@localhost:5432/piscineds"
    engine = create_engine(conn_string)

    show_average_spend(engine)
    show_total_sales(engine)
    show_number_of_customers(engine)


if __name__ == '__main__':
    main()
