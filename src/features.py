"""
Feature engineering functions for the SupplyGuard project.
"""

import numpy as np
import pandas as pd


def create_late_delivery_target(df: pd.DataFrame) -> pd.DataFrame:
    """Create binary target for late delivery."""
    df = df.copy()
    df["is_late"] = (df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]).astype(int)
    return df


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Calculate Haversine distance between two geographic points in kilometers."""
    radius_km = 6371

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return radius_km * c
