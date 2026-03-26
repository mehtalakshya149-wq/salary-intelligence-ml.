"""
salary_trends.py -- Salary Trend Forecast
==========================================
Analyzes historical salary data by year and projects future
salary trends using weighted moving average with linear
trend extrapolation.

No external time-series libraries required -- uses numpy
for lightweight, interpretable forecasting.
"""

import os
import logging
import numpy as np
import pandas as pd

from ml.src.preprocess import load_config, load_data, clean_data

logger = logging.getLogger(__name__)


# -- Historical Statistics ----------------------------------

def compute_yearly_stats(
    df: pd.DataFrame,
    target_col: str = "salary_in_usd",
    year_col: str = "work_year",
) -> pd.DataFrame:
    """
    Compute salary statistics grouped by year.

    Metrics per year:
    - count, mean, median, std
    - p10 (10th percentile), p90 (90th percentile)
    - year-over-year growth %

    Args:
        df: Cleaned salary DataFrame.
        target_col: Salary column name.
        year_col: Year column name.

    Returns:
        DataFrame with one row per year, sorted chronologically.
    """
    stats = df.groupby(year_col)[target_col].agg(
        count="count",
        mean="mean",
        median="median",
        std="std",
        p10=lambda x: np.percentile(x, 10),
        p90=lambda x: np.percentile(x, 90),
    ).reset_index()

    stats = stats.sort_values(year_col).reset_index(drop=True)

    # Year-over-year growth (on median)
    stats["yoy_growth_pct"] = stats["median"].pct_change() * 100
    stats["yoy_growth_pct"] = stats["yoy_growth_pct"].round(2)

    # Round all numeric columns
    for col in ["mean", "median", "std", "p10", "p90"]:
        stats[col] = stats[col].round(2)

    logger.info(f"Computed yearly stats for {len(stats)} years")
    return stats


# -- Trend Fitting ------------------------------------------

def fit_trend(
    yearly_stats: pd.DataFrame,
    year_col: str = "work_year",
    value_col: str = "median",
) -> dict:
    """
    Fit a linear trend to yearly salary medians.

    Uses numpy polyfit (degree=1) for a simple, interpretable
    trend line: salary = slope * year + intercept.

    Args:
        yearly_stats: DataFrame from compute_yearly_stats.
        year_col: Year column.
        value_col: Value column to trend on.

    Returns:
        Dict with slope, intercept, r_squared, and trend direction.
    """
    years = yearly_stats[year_col].values.astype(float)
    values = yearly_stats[value_col].values.astype(float)

    if len(years) < 2:
        return {
            "slope": 0.0,
            "intercept": float(values[0]) if len(values) > 0 else 0.0,
            "r_squared": 0.0,
            "direction": "insufficient_data",
        }

    # Linear fit
    coeffs = np.polyfit(years, values, 1)
    slope = float(coeffs[0])
    intercept = float(coeffs[1])

    # R-squared
    predicted = np.polyval(coeffs, years)
    ss_res = np.sum((values - predicted) ** 2)
    ss_tot = np.sum((values - np.mean(values)) ** 2)
    r_squared = float(1 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0

    # Direction
    if slope > 500:
        direction = "strong_upward"
    elif slope > 0:
        direction = "upward"
    elif slope > -500:
        direction = "flat"
    else:
        direction = "downward"

    result = {
        "slope": round(slope, 2),
        "intercept": round(intercept, 2),
        "r_squared": round(r_squared, 4),
        "direction": direction,
        "interpretation": (
            f"Salaries change by ~${abs(slope):,.0f}/year "
            f"({'increasing' if slope > 0 else 'decreasing'})"
        ),
    }

    logger.info(f"Trend: {result['interpretation']} (R2={r_squared:.4f})")
    return result


# -- Forecasting --------------------------------------------

def forecast(
    yearly_stats: pd.DataFrame,
    n_years: int = 3,
    year_col: str = "work_year",
    value_col: str = "median",
) -> list[dict]:
    """
    Extrapolate salary trend forward N years with confidence bands.

    Method:
    - Use the fitted linear trend for point estimates
    - Compute historical volatility (std of residuals)
    - Confidence band = point estimate +/- 1.5 * volatility
    - Wider bands for further-out years (multiplied by sqrt(year_offset))

    Args:
        yearly_stats: DataFrame from compute_yearly_stats.
        n_years: Number of years to forecast.
        year_col: Year column.
        value_col: Value column.

    Returns:
        List of forecast dicts, one per future year.
    """
    trend = fit_trend(yearly_stats, year_col, value_col)
    slope = trend["slope"]
    intercept = trend["intercept"]

    # Historical volatility (std of residuals from trend line)
    years = yearly_stats[year_col].values.astype(float)
    values = yearly_stats[value_col].values.astype(float)
    predicted = slope * years + intercept
    residuals = values - predicted
    volatility = float(np.std(residuals)) if len(residuals) > 1 else 0.0

    last_year = int(yearly_stats[year_col].max())

    forecasts = []
    for offset in range(1, n_years + 1):
        future_year = last_year + offset
        point_estimate = slope * future_year + intercept

        # Widen confidence band for further years
        band_width = 1.5 * volatility * np.sqrt(offset)

        forecasts.append({
            "year": future_year,
            "predicted_median": round(float(point_estimate), 2),
            "confidence_low": round(float(point_estimate - band_width), 2),
            "confidence_high": round(float(point_estimate + band_width), 2),
            "band_width": round(float(band_width), 2),
        })

    logger.info(f"Generated {n_years}-year forecast from {last_year}")
    return forecasts


# -- Filtered Trends ----------------------------------------

def compute_filtered_trends(
    df: pd.DataFrame,
    filter_col: str,
    filter_value: str,
    target_col: str = "salary_in_usd",
    year_col: str = "work_year",
    n_forecast_years: int = 3,
) -> dict:
    """
    Compute trends for a specific segment (e.g., a role or location).

    Args:
        df: Cleaned salary DataFrame.
        filter_col: Column to filter on.
        filter_value: Value to filter for.
        target_col: Salary column.
        year_col: Year column.
        n_forecast_years: Years to forecast.

    Returns:
        Dict with filtered stats, trend, and forecast.
    """
    # Filter (case-insensitive for string columns)
    if df[filter_col].dtype == object:
        mask = df[filter_col].str.lower() == filter_value.lower()
    else:
        mask = df[filter_col] == filter_value
    filtered = df[mask]

    if len(filtered) < 5:
        return {
            "filter": {filter_col: filter_value},
            "error": f"Insufficient data ({len(filtered)} rows)",
        }

    stats = compute_yearly_stats(filtered, target_col, year_col)
    trend = fit_trend(stats, year_col)
    fcast = forecast(stats, n_forecast_years, year_col)

    return {
        "filter": {filter_col: filter_value},
        "yearly_stats": stats.to_dict(orient="records"),
        "trend": trend,
        "forecast": fcast,
    }


# -- Orchestrator -------------------------------------------

def get_trend_report(
    config_path: str = "ml/config.yaml",
    n_forecast_years: int = 3,
) -> dict:
    """
    Full salary trend report:
    1. Load and clean historical data
    2. Compute yearly statistics
    3. Fit linear trend
    4. Generate multi-year forecast

    Args:
        config_path: Path to config YAML.
        n_forecast_years: Years to forecast ahead.

    Returns:
        Dict with historical stats, trend, and forecast.
    """
    config = load_config(config_path)

    # Load data
    df = load_data(config["paths"]["raw_data"])
    df = clean_data(df, config)

    target = config["features"]["target"]
    year_col = config.get("drift", {}).get("year_column", "work_year")

    # Overall stats
    stats = compute_yearly_stats(df, target, year_col)
    trend = fit_trend(stats, year_col)
    fcast = forecast(stats, n_forecast_years, year_col)

    return {
        "yearly_stats": stats.to_dict(orient="records"),
        "trend": trend,
        "forecast": fcast,
        "data_summary": {
            "total_records": len(df),
            "year_range": f"{int(stats[year_col].min())}-{int(stats[year_col].max())}",
            "overall_median": round(float(df[target].median()), 2),
        },
    }
