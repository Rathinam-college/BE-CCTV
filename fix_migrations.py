import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT setval('django_migrations_id_seq', (SELECT MAX(id) FROM django_migrations));")
    print("Migration sequence fixed!")
