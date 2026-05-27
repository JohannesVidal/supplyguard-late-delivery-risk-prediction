from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

current = Path.cwd().resolve()
for path in [current, *current.parents]:
    if (path / "data" / "processed").exists():
        PROJECT_ROOT = path
        break
else:
    raise FileNotFoundError("Project root not found. Expected data/processed folder.")

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_port = os.getenv("MYSQL_PORT", "3306")
mysql_database = os.getenv("MYSQL_DATABASE", "supplyguard")

if not all([mysql_user, mysql_password, mysql_database]):
    raise ValueError("Missing MySQL credentials. Check MYSQL_USER, MYSQL_PASSWORD and MYSQL_DATABASE in .env.")

engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4")

load_plan = [
    {"table": "category_translation", "file": "category_translation_clean.csv", "date_cols": []},
    {"table": "geolocation_zip_prefix", "file": "geolocation_zip_prefix_clean.csv", "date_cols": []},
    {"table": "geolocation_clean", "file": "geolocation_clean.csv", "date_cols": []},
    {"table": "customers", "file": "customers_clean.csv", "date_cols": []},
    {"table": "sellers", "file": "sellers_clean.csv", "date_cols": []},
    {"table": "products", "file": "products_clean.csv", "date_cols": []},
    {"table": "orders", "file": "orders_clean.csv", "date_cols": ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]},
    {"table": "order_items", "file": "order_items_clean.csv", "date_cols": ["shipping_limit_date"]},
    {"table": "order_payments", "file": "order_payments_clean.csv", "date_cols": []},
    {"table": "order_reviews", "file": "order_reviews_clean.csv", "date_cols": ["review_creation_date", "review_answer_timestamp"]}
]

with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    for item in reversed(load_plan):
        conn.execute(text(f"TRUNCATE TABLE {item['table']};"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

for item in load_plan:
    file_path = PROCESSED_DIR / item["file"]
    print(f"Loading {item['file']} into {item['table']}...")

    df = pd.read_csv(file_path, low_memory=False)

    for col in item["date_cols"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df = df.where(pd.notna(df), None)
    df.to_sql(item["table"], con=engine, if_exists="append", index=False, chunksize=5000, method="multi")

    print(f"Loaded {len(df):,} rows into {item['table']}.")

row_count_query = """
SELECT 'category_translation' AS table_name, COUNT(*) AS rows_count FROM category_translation
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'geolocation_clean', COUNT(*) FROM geolocation_clean
UNION ALL SELECT 'geolocation_zip_prefix', COUNT(*) FROM geolocation_zip_prefix
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'sellers', COUNT(*) FROM sellers
ORDER BY table_name;
"""

row_counts = pd.read_sql(row_count_query, engine)
print("\nFinal row counts:")
print(row_counts.to_string(index=False))