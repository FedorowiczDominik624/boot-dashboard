import sqlite3
import json
import pandas as pd

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
    for bucket in data["targets"]:
        row = {
            "week_start":data["week_start"],
            "buckets": bucket,
            "targets": data["targets"][bucket],
            "logged": data["logged"][bucket]
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    result = load_targets("boot_dashboard.db")
    hours_df = load_hours("hours.json")
    print(result)
    print(result.shape)
    print(result.dtypes)
    print(hours_df)
    print(hours_df.shape)
    print(hours_df.dtypes)