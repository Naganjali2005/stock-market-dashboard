# src/indicators/moving_average.py

import pandas as pd

def moving_average(df: pd.DataFrame, window: int, column: str = "Close") -> pd.Series:
    """
    Compute simple moving average for the given window size.

    Args:
        df: DataFrame containing at least column `column`
        window: window size in number of periods (days, etc.)
        column: which price column to compute MA over (default "Close")

    Returns:
        Pandas Series with the moving average, same index as df (with NaNs for initial periods)
    """
    return df[column].rolling(window=window).mean()
