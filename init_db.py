import sqlite3


def init_db(db_path: str, schema_path: str) -> None:
    """
    Open (or create) a SQLite database at db_path and execute the SQL
    in schema_path against it. Commit before closing.
    """
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r") as f:
        text = f.read()
    conn.executescript(text)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db("boot_dashboard.db", "schema.sql")
