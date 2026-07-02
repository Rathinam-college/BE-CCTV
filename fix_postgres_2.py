import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def fix_nvr_postgres():
    output = []
    with connection.cursor() as cursor:
        try:
            cursor.execute('ALTER TABLE cctv_nvr ADD COLUMN "portNumber" varchar(50) NULL;')
            output.append("Successfully added portNumber to PostgreSQL.")
        except Exception as e:
            output.append("Error adding portNumber: " + str(e))
            output.append(traceback.format_exc())
    
    with open('fix_pg_out.txt', 'w') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    fix_nvr_postgres()
