import sqlite3
import os

db_path = r'd:\Company Deatils\Rathinam college\Webite\CCTV\CODE MAIN\BE-CCTV\db.sqlite3'
out_path = r'd:\Company Deatils\Rathinam college\Webite\CCTV\CODE MAIN\BE-CCTV\out.txt'

try:
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(cctv_nvr)")
        columns = cursor.fetchall()
        
        with open(out_path, 'w') as f:
            f.write(f"Found {len(columns)} columns.\n")
            for col in columns:
                f.write(str(col) + "\n")
        conn.close()
    else:
        with open(out_path, 'w') as f:
            f.write("DB not found at " + db_path)
except Exception as e:
    with open(out_path, 'w') as f:
        f.write("Error: " + str(e))
