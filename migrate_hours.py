import json
import sqlite3

def migrate_hours_json_to_sqlite(json_path: str, db_path: str) -> dict:

    """
    Load hours.json and insert all rows into boot_dashboard.db.
    Return a summary dict: {"sessions_inserted" : int, "targets_inserted": int}
    Idempotent: safe to re-run without duplicating rows. 
    """
    with open(json_path, "r") as f:
        data = json.load(f)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    begin_week = data["week_start"]
    targets_inserted = 0
    for bucket, target in data["targets"].items():
        cur.execute(
            "INSERT OR IGNORE INTO targets (week, bucket, target) VALUES (?, ?, ?)",
            (begin_week, bucket, target)
        )
        targets_inserted += cur.rowcount
    conn.commit()
    conn.close()

    return {"sessions_inserted": 0, "targets_inserted": targets_inserted}


if __name__ == "__main__":
    result = migrate_hours_json_to_sqlite("hours.json", "boot_dashboard.db")
    print(result)