import os
import subprocess
import json
import sys

def run_cmd(cmd):
    print(f"Running: {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode()}")
        return False
    return True

def migrate():
    # 1. Install psycopg2-binary
    print("Installing psycopg2-binary...")
    run_cmd("pip install psycopg2-binary")

    # 2. Dump data from SQLite
    # We need to temporarily point to SQLite to dump data
    # But since settings.py is already updated, we can use a temporary settings override or just revert it
    
    print("Step 1: Dumping data from SQLite...")
    # This assumes db.sqlite3 exists in the current directory
    # We use a trick: run dumpdata with a temporary settings file or just tell the user to revert
    
    # Actually, the easiest way for the user is:
    print("\n--- MANUAL ACTION REQUIRED ---")
    print("1. Temporarily change settings.py back to 'sqlite3' engine.")
    print("2. Run: python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db_dump.json")
    print("3. Change settings.py back to 'postgresql' engine.")
    print("4. Run: python manage.py migrate")
    print("5. Run: python manage.py loaddata db_dump.json")
    print("------------------------------\n")

if __name__ == "__main__":
    migrate()
