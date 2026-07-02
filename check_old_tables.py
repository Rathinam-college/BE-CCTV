import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def check_old_tickets():
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT count(*) FROM cctv_ticket")
            count = cursor.fetchone()[0]
            print(f"cctv_ticket count: {count}")
        except Exception as e:
            print(f"cctv_ticket error: {e}")
            connection.rollback()
            
        try:
            cursor.execute("SELECT count(*) FROM maintenance_ticket")
            count = cursor.fetchone()[0]
            print(f"maintenance_ticket count: {count}")
        except Exception as e:
            print(f"maintenance_ticket error: {e}")
            connection.rollback()

if __name__ == '__main__':
    check_old_tickets()
