import pandas as pd

def create_lag_features(df, lag_days=3):
    """
    Create lag features for Linear Regression.
    df: pandas DataFrame with 'close' column
    """
    df = df.sort_values("date")
    for i in range(1, lag_days + 1):
        df[f"lag_{i}"] = df["close"].shift(i)
    df = df.dropna().reset_index(drop=True)
    return df
