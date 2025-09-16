# app.py

import streamlit as st
from datetime import date
from src.data.fetcher import fetch_data
from src.indicators.moving_average import moving_average
from src.indicators.rsi import compute_rsi

# ✅ new combined plot
from src.plots.price_plot import plot_price_ma_volume_rsi  

# Optional: caching data fetches to speed up
@st.cache_data(ttl=60*5)
def get_data(ticker, start, end, interval="1d"):
    return fetch_data(ticker, start, end, interval)

st.title("📊 Stock Dashboard with RSI")

# Sidebar inputs
ticker = st.sidebar.text_input("Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start date", value=date(2023, 1, 1))
end_date = st.sidebar.date_input("End date", value=date.today())
ma_window = st.sidebar.slider("Moving Average Window (days)", min_value=5, max_value=100, value=20, step=5)

# RSI options
show_rsi = st.sidebar.checkbox("Show RSI", value=True)
rsi_period = st.sidebar.slider("RSI Period (days)", min_value=5, max_value=30, value=14, step=1)

if ticker:
    if start_date > end_date:
        st.error("Error: Start date must be before end date.")
    else:
        with st.spinner("Fetching data..."):
            df = get_data(ticker, start=start_date.isoformat(), end=end_date.isoformat(), interval="1d")

        if df.empty:
            st.error("No data found for this ticker / date range.")
        else:
            # --- Moving Average
            ma_series = moving_average(df, window=ma_window, column="Close")

            # --- RSI
            rsi_series = None
            if show_rsi:
                rsi_series = compute_rsi(df, period=rsi_period, column="Close")

            # --- Combined Plot (Price + MA + Volume + RSI)
            fig = plot_price_ma_volume_rsi(
                df,
                ma_series=ma_series,
                rsi_series=rsi_series,
                ticker=ticker,
                ma_label=f"MA{ma_window}",
                use_candles=True,
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- Recent Data Table
            st.subheader("Recent Data")
            st.dataframe(df.tail(10))
