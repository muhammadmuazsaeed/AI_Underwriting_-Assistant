

import pandas as pd
import plotly.graph_objects as go
from ml_model.data_prep import load_and_clean, COL_PRICE, COL_CITY, COL_LOCATION

DATA_PATH = "data/zameen_data.csv"

_cached_df = None


def _get_data() -> pd.DataFrame:
    global _cached_df
    if _cached_df is None:
        _cached_df = load_and_clean(DATA_PATH)
    return _cached_df


def get_price_trend_chart(city: str, location: str | None = None) -> go.Figure:
    """
    Returns a line chart of average price per Marla, grouped by year,
    for the given city (optionally filtered further by location).
    """
    df = _get_data()
    subset = df[df[COL_CITY] == city].copy()
    if location:
        subset = subset[subset[COL_LOCATION] == location]

    subset = subset.dropna(subset=["year_added"])
    subset["price_per_marla"] = subset[COL_PRICE] / subset["area_marla"]

    trend = (
        subset.groupby("year_added")["price_per_marla"]
        .mean()
        .reset_index()
        .sort_values("year_added")
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["year_added"],
        y=trend["price_per_marla"],
        mode="lines+markers",
        line=dict(color="#2E75B6", width=3),
    ))
    title = f"Average Price per Marla Over Time — {city}"
    if location:
        title += f" ({location})"
    fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Avg. Price per Marla (PKR)", height=350)
    return fig


def get_trend_summary(city: str, location: str | None = None) -> dict:
    """
    Returns a simple summary: did the average price go up or down
    across the years available in the dataset for this city/location.
    """
    df = _get_data()
    subset = df[df[COL_CITY] == city].copy()
    if location:
        subset = subset[subset[COL_LOCATION] == location]

    subset = subset.dropna(subset=["year_added"])
    subset["price_per_marla"] = subset[COL_PRICE] / subset["area_marla"]

    trend = subset.groupby("year_added")["price_per_marla"].mean().sort_index()

    if len(trend) < 2:
        return {"direction": "Not enough data", "change_pct": None, "years": trend.index.tolist()}

    first_val = trend.iloc[0]
    last_val = trend.iloc[-1]
    change_pct = ((last_val - first_val) / first_val) * 100

    direction = "Increased" if change_pct > 0 else "Decreased" if change_pct < 0 else "No change"

    return {
        "direction": direction,
        "change_pct": change_pct,
        "years": trend.index.tolist(),
        "first_year": int(trend.index[0]),
        "last_year": int(trend.index[-1]),
    }
