# src/indicators/rsi.py

import pandas as pd

def compute_rsi(df: pd.DataFrame, period: int = 14, column: str = "Close") -> pd.Series:
    """
    Compute the Relative Strength Index (RSI) for a given DataFrame.

    Args:
      df: DataFrame with price data (must include `column`)
      period: lookback period for RSI (default 14)
      column: column to compute RSI from (default "Close")

    Returns:
      Pandas Series of RSI values (0-100), same index as df
    """
    delta = df[column].diff()  # differences between consecutive close prices
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Use exponential weighted average (EWMA) for smoothing
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
