"""
load_data.py
------------
Phase 4 — ETL Script
Reads the raw CSV and loads it into MySQL customer_data table.

Requirements:
    pip install pandas sqlalchemy pymysql

Usage:
    python load_data.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ── Configuration ──────────────────────────────────────────────────────────────
# Credentials are read from a local .env file (see .env.example). Never hardcode
# secrets — .env is git-ignored so it stays off GitHub.
load_dotenv()
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = int(os.getenv("DB_PORT", "3306"))
DB_NAME     = os.getenv("DB_NAME", "data_quality")

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "raw_data", "customer_data.csv")

# ── Load CSV ───────────────────────────────────────────────────────────────────
print("Loading CSV...")
df = pd.read_csv(CSV_PATH)
print(f"  Rows read: {len(df)}")
print(df.head())

# ── Connect to MySQL ───────────────────────────────────────────────────────────
connection_string = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(connection_string)

# ── Insert into customer_data ──────────────────────────────────────────────────
df.to_sql(
    name      = "customer_data",
    con       = engine,
    if_exists = "append",   # append so multiple runs accumulate data
    index     = False
)

print("Data loaded successfully into customer_data table.")
