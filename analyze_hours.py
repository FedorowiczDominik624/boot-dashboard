import sqlite3
import json
import pandas as pd
import numpy as np

def load_targets(db_path: str) -> pd.DataFrame:
    """Read the 'targets' table from the boot dashboard SQLite DB and
    return as a Pandas DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM targets" , conn)
    conn.close()
    return df

def load_hours(json_path: str) -> pd.DataFrame:
    """Read the boot-dashboard hours.json file and return as a Pandas DataFrame
    with columns (week_start, buckets, targets, logged)."""
    with open(json_path) as f:
        data = json.load(f)
    rows = []
    for week in data:
        for bucket in week["targets"]:
            row = {
                "week_start":week["week_start"],
                "buckets": bucket,
                "targets": week["targets"][bucket],
                "logged": week["logged"][bucket]
            }
            rows.append(row)
    df = pd.DataFrame(rows)
    return df

def add_progress_column(hours_df: pd.DataFrame) -> pd.DataFrame:
    """Add 'delta' and 'pct_of_target' columns to hours DataFrame."""
    hours_df['delta'] = hours_df['logged'] - hours_df['targets']
    hours_df['pct_of_target'] = hours_df['logged'] / hours_df['targets'] * 100
    return hours_df

def compute_rolling_avg(hours_df: pd.DataFrame, bucket: str, window: int = 2) -> pd.Series:
    """For one bucket, return rolling N-week average of logged hours."""
    bucket_df = hours_df[hours_df['buckets'] == bucket]
    return bucket_df['logged'].rolling(window=window).mean()
    
def compute_basic_stats(hours_df: pd.DataFrame, bucket: str) -> dict:
    """Compute mean, std, and median of logged hours for a given
    bucket using NumPy. Returns dict with keys: 'mean', 'std', 'median'."""
    bucket_df = hours_df[hours_df['buckets'] == bucket]
    arr = bucket_df['logged'].values
    results = {
    "mean": np.mean(arr),
    "std": np.std(arr),
    "median": np.median(arr),
    }
    return results

def fit_trend(hours_df: pd.DataFrame, bucket: str) -> tuple[float, float]:
    """For one bucket, fit a first degree polynomial to weekly logged hours.
    Returns (slope, intercept) as floats"""
    bucket_df = hours_df[hours_df['buckets'] == bucket]
    y = bucket_df['logged'].values
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

def interpret_slope(slope: float) -> str:
    """Convert a regression slope into a human-readable sentence about the
    trend."""
    if abs(slope) < 0.5:
        return "Flat (no significant trend)"
    elif slope > 0:
        return f"Trending up by {abs(slope):.1f} hours per week."
    else:
        return f"Trending down by {abs(slope):.1f} hours per week."



if __name__ == "__main__":
    result = load_targets("boot_dashboard.db")
    hours_df = load_hours("hours.json")
    progress_df = add_progress_column(hours_df)
    print(result)
    print(result.shape)
    print(result.dtypes)
    print(hours_df)
    print(hours_df.shape)
    print(hours_df.dtypes)
    print(progress_df)

    print("\n --- Rolling 2-week avg by bucket ---")
    for b in ["py", "pj", "fi"]:
        avg_series = compute_rolling_avg(progress_df, b)
        print(f"{b}:")
        print(avg_series)
    
    print("\n --- Basic Stats by Bucket (NumPy) ---")
    for b in ["py", "pj", "fi"]:
        stats = compute_basic_stats(progress_df, b)
        print(f"{b}: {stats}")

    print("\n --- Linear Trend per Bucket (NumPy Polyfit) ---")
    for b in ["py", "pj", "fi"]:
        slope, intercept = fit_trend(progress_df, b)
        print(f"{b}: slope={slope:.3f}, intercept={intercept:.3f}")

    print("\n --- Trend interpretation per bucket ---")
    for b in ["py", "pj", "fi"]:
        slope, intercept = fit_trend(progress_df, b)
        interpretation = interpret_slope(slope)
        print(f"{b}: {interpretation}")