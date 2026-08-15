import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(connection_url)


def get_business_metrics():
    query = text("""
        SELECT
            SUM("Weekly_Sales") AS total_sales,
            AVG("Weekly_Sales") AS avg_weekly_sales,
            COUNT(DISTINCT "Store") AS total_stores,
            COUNT(DISTINCT "Dept") AS total_departments
        FROM sales_fact;
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().one()

    return dict(result)

def get_top_stores(limit=5):
    query = text("""
        SELECT
            "Store" AS store,
            SUM("Weekly_Sales") AS total_sales
        FROM sales_fact
        GROUP BY "Store"
        ORDER BY total_sales DESC
        LIMIT :limit;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    return [dict(row) for row in result]

if __name__ == "__main__":
    print(get_business_metrics())
    print(get_top_stores())