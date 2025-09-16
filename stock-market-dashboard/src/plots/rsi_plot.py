# src/plots/rsi_plot.py

import plotly.express as px

def plot_rsi(df, rsi_series, ticker: str, period: int = 14):
    """
    Plot RSI ensuring y is 1-dimensional
    """
    # Ensure rsi_series is 1D
    y = rsi_series
    # If it's a DataFrame or shape (n,1), convert:
    try:
        y = y.squeeze()
    except:
        pass

    # If still 2D with second dim = 1, flatten
    import numpy as np
    if hasattr(y, "shape") and len(y.shape) == 2 and y.shape[1] == 1:
        y = y.values.flatten()

    fig = px.line(
        x=df["Date"],
        y=y,
        title=f"{ticker} RSI (Period = {period})",
        labels={"x": "Date", "y": "RSI"}
    )

    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought", annotation_position="top left")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold", annotation_position="bottom left")
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(hovermode="x unified", margin=dict(l=40, r=40, t=50, b=40))

    return fig
