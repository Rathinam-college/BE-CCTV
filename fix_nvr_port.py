import sqlite3
import os

db_path = r'd:\Company Deatils\Rathinam college\Webite\CCTV\CODE MAIN\BE-CCTV\db.sqlite3'
print("Connecting to DB:", db_path)
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE cctv_nvr ADD COLUMN portNumber varchar(50) NULL;")
        conn.commit()
        print("Successfully added portNumber column!")
    except Exception as e:
        print("Error or column already exists:", str(e))
    conn.close()
else:
    print("DB not found at", db_path)
