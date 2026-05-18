"""
Database connection utilities for the SupplyGuard project.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


def get_mysql_engine():
    """Create a SQLAlchemy engine using environment variables."""
    load_dotenv()

    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "supplyguard_db")

    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)
