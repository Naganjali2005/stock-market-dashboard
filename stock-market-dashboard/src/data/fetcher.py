# src/data/fetcher.py

import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker and date range.
    Ensures clean column names like 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'.
    """
    df = yf.download(ticker, start=start, end=end, interval=interval)

    if df.empty:
        return df

    # --- Fix multi-index columns like ('Close', 'AAPL') -> 'Close'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    # --- Fix suffixed columns like 'Close_AAPL' -> 'Close'
    df.columns = [col.split("_")[0] for col in df.columns]

    df.reset_index(inplace=True)  # keep Date as column
    return df
