import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def show_box_plot(df):
    """Show box plot of price"""
    df.boxplot(column='price')


def main():
    """Driver main function"""
    load_dotenv("../.env")

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql+psycopg2://{pg_user}:{pg_pass}@localhost:5432/{pg_db}"
    engine = create_engine(conn_string)
    query = """
    SELECT
      price
    FROM customers
    WHERE event_type = 'purchase'
    """
    df = pd.read_sql(query, engine)

    prices = df['price']
    print(f"count\t{prices.count()}")
    print(f"mean\t{prices.mean()}")
    print(f"std\t{prices.std()}")
    print(f"min\t{prices.min()}")
    print(f"25%\t{prices.quantile(0.25)}")
    print(f"50%\t{prices.quantile(0.5)}")
    print(f"75%\t{prices.quantile(0.75)}")
    print(f"max\t{prices.max()}")

    # Show box plots

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.boxplot(prices, vert=False, widths=0.5, notch=True,
                boxprops=dict(facecolor='lightgray', edgecolor='none'),
                flierprops=dict(marker='D', markersize=8, markerfacecolor='lightgray', markeredgecolor='none'),
                patch_artist=True)
    ax1.set_yticks([])
    ax1.set_xlabel("Price")
    ax1.set_title("Full Box Plot")

    boxprops = dict(facecolor='green', edgecolor='black')
    medianprops = dict(linestyle='-', linewidth=2, color='black')
    ax2.boxplot(prices, vert=False, widths=0.5, notch=True,
                boxprops=boxprops, medianprops=medianprops, showfliers=False,
                patch_artist=True)
    ax2.set_yticks([])
    ax2.set_xlabel("Price")
    ax2.set_title("Interquartile range (IQR)")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
