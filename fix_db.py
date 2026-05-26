import os
import django
from django.db import connection
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def fix_database():
    with connection.cursor() as cursor:
        # Check if the cctv_occupation table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'cctv_occupation'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if not exists:
            print("cctv_occupation table is missing! Fixing django_migrations table...")
            # Remove the migration records so Django knows it needs to run them again
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cctv' AND name = '0031_occupation';")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cctv' AND name = '0032_alter_occupation_occupation_type';")
            print("Migration records deleted. Running 'python manage.py migrate'...")
            
            # Run migrate to recreate the table
            call_command('migrate', 'cctv')
            print("Database fixed successfully! The cctv_occupation table should now exist.")
        else:
            print("cctv_occupation table already exists. No fix needed.")

if __name__ == '__main__':
    fix_database()
