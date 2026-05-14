import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
try:
    django.setup()
except Exception as e:
    print(f"ERROR: Could not setup Django. Make sure you are in the correct directory and venv is active.\nDetail: {e}")
    sys.exit(1)

def check_database():
    print("Checking database connection...")
    db_conn = connections['default']
    try:
        db_conn.cursor()
        print("SUCCESS: Database connection established!")
        
        # Check if tables exist
        from django.db import connection
        tables = connection.introspection.table_names()
        if not tables:
            print("WARNING: Database is connected but no tables found. Did you run 'python manage.py migrate'?")
        else:
            print(f"INFO: Database is ready with {len(tables)} tables.")
            
    except OperationalError as e:
        print(f"ERROR: Could not connect to the database.\nDetail: {e}")
        print("\nPlease check:")
        print("1. Is PostgreSQL service running?")
        print("2. Does the database 'cctv' exist?")
        print("3. Are the credentials in core/settings.py correct?")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_database()
