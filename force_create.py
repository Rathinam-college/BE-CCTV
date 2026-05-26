import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Occupation, MasterLocation

def force_create():
    print("--- ATTEMPTING TO FORCE-CREATE TABLES FOR OCCUPATION & ONBOARDING ---")
    try:
        # 1. Drop existing tables if they exist to start fresh
        with connection.cursor() as cursor:
            print("Dropping cctv_occupation and cctv_masterlocation if they exist...")
            cursor.execute("DROP TABLE IF EXISTS cctv_occupation CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS cctv_masterlocation CASCADE;")
        
        # 2. Use Django's internal schema editor to create tables EXACTLY as defined in models
        with connection.schema_editor() as schema_editor:
            print("Creating cctv_occupation table...")
            schema_editor.create_model(Occupation)
            
            print("Creating cctv_masterlocation table...")
            schema_editor.create_model(MasterLocation)
            
        print("Tables created successfully!")
        
        # 3. Fix the migration history so Django doesn't get confused later
        with connection.cursor() as cursor:
            print("Updating django_migrations...")
            # Delete any records that might cause conflicts
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cctv' AND name = '0021_masterlocation';")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cctv' AND name = '0024_globalsiteconfig_assignedto_and_more';")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cctv' AND name = '0031_occupation';")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cctv' AND name = '0032_alter_occupation_occupation_type';")
            
            # Re-insert them as applied
            cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('cctv', '0021_masterlocation', NOW());")
            cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('cctv', '0024_globalsiteconfig_assignedto_and_more', NOW());")
            cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('cctv', '0031_occupation', NOW());")
            cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('cctv', '0032_alter_occupation_occupation_type', NOW());")
            
        print("--- SUCCESS! Both tables are recreated completely clean. ---")
            
    except Exception as e:
        print(f"--- ERROR: {e} ---")

if __name__ == '__main__':
    force_create()
