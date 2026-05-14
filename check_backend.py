import os
import sys
import django

def check_backend():
    print("=== Backend Diagnostic Tool ===")
    
    # 1. Check Python Version
    print(f"Python Version: {sys.version}")
    
    # 2. Check Environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        django.setup()
        print("Django Setup: OK")
    except Exception as e:
        print(f"Django Setup: FAILED - {str(e)}")
        return

    # 3. Check Database
    from django.db import connection
    try:
        connection.ensure_connection()
        print(f"Database Connection: OK (Engine: {connection.vendor})")
        print(f"Database Name: {connection.settings_dict['NAME']}")
    except Exception as e:
        print(f"Database Connection: FAILED - {str(e)}")
        print("TIP: If you are using Postgres, make sure the database exists and the service is running.")

    # 4. Check Installed Apps
    from django.conf import settings
    print(f"Installed Apps: {len(settings.INSTALLED_APPS)}")

    # 5. Check User Model
    from users.models import User
    try:
        user_count = User.objects.count()
        print(f"Users in Database: {user_count}")
        if user_count == 0:
            print("WARNING: No users found. Run 'python create_admin.py' to create an admin.")
    except Exception as e:
        print(f"User Check: FAILED - {str(e)}")

    print("\n=== End of Diagnostic ===")

if __name__ == "__main__":
    check_backend()
