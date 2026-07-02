import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Division

count, _ = Division.objects.all().delete()
print(f"Successfully deleted {count} Divisions from the database.")
