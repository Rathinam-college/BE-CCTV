import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from cctv.models import GlobalSiteConfig

table_name = GlobalSiteConfig._meta.db_table
with connection.cursor() as cursor:
    tables = connection.introspection.table_names()
    if table_name in tables:
        print(f"Table '{table_name}' exists.")
    else:
        print(f"Table '{table_name}' DOES NOT exist.")
