# src/plots/price_plot.py

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def plot_price_ma_volume_rsi(
    df: pd.DataFrame,
    ma_series: pd.Series = None,
    rsi_series: pd.Series = None,
    ticker: str = "TICK",
    ma_label: str = "MA",
    use_candles: bool = True,
):
    """
    Returns a Plotly figure with:
      - Price (candles or line) + MA overlay
      - Volume subplot
      - RSI subplot (if provided)

    df: DataFrame must have "Date", and price columns like "Close"/"Adj Close" + "Volume"
    ma_series: pd.Series aligned with df (optional, for Moving Average)
    rsi_series: pd.Series aligned with df (optional, for RSI)
    """

    # Pick price column safely
    price_col = None
    if "Close" in df.columns:
        price_col = "Close"
    elif "Adj Close" in df.columns:
        price_col = "Adj Close"
    else:
        # fallback: detect first column containing "Close"
        close_candidates = [c for c in df.columns if "Close" in c]
        if close_candidates:
            price_col = close_candidates[0]
        else:
            raise KeyError(f"No Close/Adj Close column found in DataFrame. Columns: {list(df.columns)}")

    # Figure rows: 3 (Price, Volume, RSI)
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        vertical_spacing=0.03, row_heights=[0.6, 0.2, 0.2]
    )

    # --- Price chart ---
    if use_candles and all(col in df.columns for col in ["Open", "High", "Low", price_col]):
        fig.add_trace(
            go.Candlestick(
                x=df["Date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df[price_col],
                name=f"{ticker} OHLC"
            ),
            row=1, col=1
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df["Date"], y=df[price_col],
                mode="lines",
                name=f"{ticker} {price_col}"
            ),
            row=1, col=1
        )

    # MA overlay
    if ma_series is not None:
        fig.add_trace(
            go.Scatter(
                x=df["Date"], y=ma_series,
                mode="lines",
                line=dict(width=1.5, dash="dash"),
                name=f"{ma_label}"
            ),
            row=1, col=1
        )

    # --- Volume subplot ---
    if "Volume" in df.columns:
        fig.add_trace(
            go.Bar(x=df["Date"], y=df["Volume"], showlegend=False, name="Volume"),
            row=2, col=1
        )

    # --- RSI subplot ---
    if rsi_series is not None:
        fig.add_trace(
            go.Scatter(
                x=df["Date"], y=rsi_series,
                mode="lines",
                line=dict(color="orange", width=1.5),
                name="RSI"
            ),
            row=3, col=1
        )
        # Add 30/70 reference lines
        fig.add_hline(y=70, line_dash="dot", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dot", line_color="green", row=3, col=1)

    # --- Layout tweaks ---
    fig.update_layout(
        title=f"{ticker} Price, MA, Volume & RSI",
        hovermode="x unified",
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
        xaxis2=dict(type="date"),
        xaxis3=dict(type="date"),
        margin=dict(t=40, b=20)
    )

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])

    return fig


# Wrapper (for backward compatibility)
def plot_price_with_ma(df, ma_series, ticker: str, ma_label: str = "MA"):
    """
    Wrapper to just plot price + MA (line), without volume or RSI.
    """
    return plot_price_ma_volume_rsi(
        df, ma_series, rsi_series=None, ticker=ticker, ma_label=ma_label, use_candles=False
    )
