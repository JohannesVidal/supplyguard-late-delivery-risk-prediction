"""
Data cleaning functions for the SupplyGuard project.
"""

import pandas as pd


def convert_to_datetime(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to datetime."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df
