import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.core.management.color import no_style
from django.apps import apps

def reset_all_sequences():
    print("Synchronizing PostgreSQL sequences with table data...")
    with connection.cursor() as cursor:
        app_labels = ['cctv', 'users', 'maintenance', 'routes', 'reports']
        for label in app_labels:
            try:
                app_config = apps.get_app_config(label)
                models = app_config.get_models()
                sequence_sql = connection.ops.sequence_reset_sql(no_style(), models)
                for sql in sequence_sql:
                    cursor.execute(sql)
                print(f"  ✓ Synchronized app '{label}'")
            except Exception as e:
                print(f"  ✗ App '{label}' error: {e}")

        # Also generic sequence update for any remaining sequences
        cursor.execute("""
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                FOR r IN (
                    SELECT c.relname AS table_name, a.attname AS column_name, s.relname AS seq_name
                    FROM pg_class s
                    JOIN pg_depend d ON d.objid = s.oid
                    JOIN pg_class c ON d.refobjid = c.oid
                    JOIN pg_attribute a ON (d.refobjid, d.refobjsubid) = (a.attrelid, a.attnum)
                    WHERE s.relkind = 'S' AND c.relkind = 'r'
                ) LOOP
                    EXECUTE format('SELECT setval(%L, COALESCE((SELECT MAX(%I) FROM %I), 1) + 1, false)', r.seq_name, r.column_name, r.table_name);
                END LOOP;
            END $$;
        """)
        print("  ✓ All PostgreSQL sequence pointers successfully updated!")

if __name__ == '__main__':
    reset_all_sequences()
