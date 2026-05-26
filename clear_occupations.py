import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Occupation

count, _ = Occupation.objects.all().delete()
print(f"Successfully deleted {count} Occupations from the database.")
