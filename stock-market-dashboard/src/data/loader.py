# src/data/loader.py

import os
import pandas as pd
from src.data.fetcher import fetch_data
from src.data.cleaner import clean_data

CACHE_DIR = "data/cache"

def ensure_cache_dir():
    """Make sure the cache directory exists."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def cache_file_path(ticker: str, start: str, end: str) -> str:
    """
    Generate a filename for caching based on ticker and date range.
    """
    # Clean ticker and dates for filename safety
    ticker_clean = ticker.upper().replace(" ", "")
    fname = f"{ticker_clean}_{start}_{end}.csv"
    return os.path.join(CACHE_DIR, fname)

def load_cached_data(ticker: str, start: str, end: str) -> pd.DataFrame | None:
    """
    Load cached data from CSV if it exists. Returns DataFrame or None.
    """
    path = cache_file_path(ticker, start, end)
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, parse_dates=["Date"])
            return df
        except Exception as e:
            print(f"Error loading cached file {path}: {e}")
            return None
    return None

def save_data_to_cache(ticker: str, start: str, end: str, df: pd.DataFrame):
    """
    Save DataFrame to cache directory. Overwrites if exists.
    """
    path = cache_file_path(ticker, start, end)
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        print(f"Error saving cache to {path}: {e}")

def get_data_cached_or_fetch(ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    """
    Tries to load data from cache; if not found or fails, fetches:
    fetch -> clean -> save to cache -> return DataFrame.
    """
    ensure_cache_dir()
    df_cached = load_cached_data(ticker, start, end)
    if df_cached is not None:
        return df_cached
    # fetch fresh
    df_fetched = fetch_data(ticker, start=start, end=end, interval=interval)
    # clean fetched
    df_clean = clean_data(df_fetched, start, end, method="ffill")
    # save to cache
    save_data_to_cache(ticker, start, end, df_clean)
    return df_clean
