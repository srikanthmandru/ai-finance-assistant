import pandas as pd
import plotly.express as px


def portfolio_pie_chart(allocations):
    df = pd.DataFrame(allocations)
    if df.empty:
        return None

    fig = px.pie(df, names="symbol", values="allocation_pct", title="Portfolio Allocation")
    return fig


def market_line_chart(history):
    df = pd.DataFrame(history)
    if df.empty:
        return None

    fig = px.line(df, x="date", y="close", title="Market Trend")
    return fig