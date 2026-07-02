import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def check_cols():
    cursor = connection.cursor()
    
    # 1. cctv_camera
    try:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='cctv_camera'")
        camera_cols = [row[0] for row in cursor.fetchall()]
        print("Columns in 'cctv_camera' database table:")
        print(camera_cols)
    except Exception as e:
        print("Failed to query 'cctv_camera':", e)
        
    # 2. cctv_biometric
    try:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='cctv_biometric'")
        biometric_cols = [row[0] for row in cursor.fetchall()]
        print("\nColumns in 'cctv_biometric' database table:")
        print(biometric_cols)
    except Exception as e:
        print("Failed to query 'cctv_biometric':", e)

if __name__ == "__main__":
    check_cols()
