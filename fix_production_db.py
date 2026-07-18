import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def fix_schema():
    # 1. Fix cctv_camera table ('model' column)
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT model FROM cctv_camera LIMIT 1;")
            print("Column 'model' already exists in 'cctv_camera'.")
        except Exception:
            # Re-establish cursor to clear transaction state
            connection.close()
            with connection.cursor() as cursor_alter:
                print("Adding column 'model' to 'cctv_camera'...")
                cursor_alter.execute("ALTER TABLE cctv_camera ADD COLUMN model VARCHAR(100) NULL;")
                print("Successfully added 'model' to 'cctv_camera'.")

    # 2. Fix maintenance_ticket table ('receivedDate' column)
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT "receivedDate" FROM maintenance_ticket LIMIT 1;')
            print("Column 'receivedDate' already exists in 'maintenance_ticket'.")
        except Exception:
            # Re-establish cursor to clear transaction state
            connection.close()
            with connection.cursor() as cursor_alter:
                print("Adding column 'receivedDate' to 'maintenance_ticket'...")
                # Note: Mixed-case column names must be double-quoted in PostgreSQL
                cursor_alter.execute('ALTER TABLE maintenance_ticket ADD COLUMN "receivedDate" DATE NULL;')
                print("Successfully added 'receivedDate' to 'maintenance_ticket'.")

    # 3. Fix maintenance_ticket table ('ticketDevice' column)
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT "ticketDevice" FROM maintenance_ticket LIMIT 1;')
            print("Column 'ticketDevice' already exists in 'maintenance_ticket'.")
        except Exception:
            connection.close()
            with connection.cursor() as cursor_alter:
                print("Adding column 'ticketDevice' to 'maintenance_ticket'...")
                cursor_alter.execute('ALTER TABLE maintenance_ticket ADD COLUMN "ticketDevice" VARCHAR(100) NULL;')
                print("Successfully added 'ticketDevice' to 'maintenance_ticket'.")

    # 4. Fix maintenance_ticket table ('raisedByName' column)
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT "raisedByName" FROM maintenance_ticket LIMIT 1;')
            print("Column 'raisedByName' already exists in 'maintenance_ticket'.")
        except Exception:
            connection.close()
            with connection.cursor() as cursor_alter:
                print("Adding column 'raisedByName' to 'maintenance_ticket'...")
                cursor_alter.execute('ALTER TABLE maintenance_ticket ADD COLUMN "raisedByName" VARCHAR(255) NULL;')
                print("Successfully added 'raisedByName' to 'maintenance_ticket'.")

if __name__ == '__main__':
    fix_schema()
    print("Database schema fix execution complete!")
