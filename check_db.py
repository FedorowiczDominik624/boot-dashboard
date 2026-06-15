import sqlite3

conn = sqlite3.connect("boot_dashboard.db")
cur = conn.cursor()
cur.execute("SELECT * FROM targets")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()