import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def fix_nvr_postgres():
    with connection.cursor() as cursor:
        try:
            # For postgres, adding a column:
            cursor.execute('ALTER TABLE cctv_nvr ADD COLUMN "portNumber" varchar(50) NULL;')
            print("Successfully added portNumber to PostgreSQL.")
        except Exception as e:
            print("Error adding portNumber:", e)

if __name__ == '__main__':
    fix_nvr_postgres()
