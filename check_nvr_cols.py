import sqlite3
import os

db_path = 'd:/Rathinam college/cctv/backend_django/db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(cctv_nvr)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)
    conn.close()
else:
    print("DB not found")
