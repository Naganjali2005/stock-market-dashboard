# in cleaner.py

import pandas as pd

def clean_data(df: pd.DataFrame, start: str, end: str, method: str = "ffill") -> pd.DataFrame:
    df2 = df.copy()

    # Handle column names: strip spaces / fix MultiIndex
    cols = df2.columns

    # If MultiIndex, flatten it
    if isinstance(cols, pd.MultiIndex):
        # Join levels with underscore or space
        new_cols = []
        for lvl in cols:
            # lvl is a tuple of names, e.g. ("Adj Close", "")
            # convert each part to str, then join
            new_name = "_".join([str(x).strip() for x in lvl if str(x).strip() != ""])
            if new_name == "":
                new_name = "unknown"
            new_cols.append(new_name)
        df2.columns = new_cols
    else:
        # Plain Index: strip spaces
        df2.columns = df2.columns.str.strip()

    # Ensure "Date" exists
    if "Date" not in df2.columns:
        df2 = df2.reset_index()
        if "index" in df2.columns:
            df2 = df2.rename(columns={"index": "Date"})
        else:
            # maybe the first column is date after reset
            possible = df2.columns[0]
            df2 = df2.rename(columns={possible: "Date"})

    # Convert to datetime
    df2["Date"] = pd.to_datetime(df2["Date"], errors="coerce")
    df2 = df2.dropna(subset=["Date"])

    # sort, drop duplicates, filter, fill missing etc.
    df2 = df2.sort_values("Date").reset_index(drop=True)
    df2 = df2.drop_duplicates(subset=["Date"])
    df2 = df2.loc[(df2["Date"] >= pd.to_datetime(start)) & (df2["Date"] <= pd.to_datetime(end))].reset_index(drop=True)

    if method == "ffill":
        df2 = df2.fillna(method="ffill")
    elif method == "bfill":
        df2 = df2.fillna(method="bfill")
    elif method == "drop":
        df2 = df2.dropna()

    return df2
