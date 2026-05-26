import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from cctv.models import Location
print("Deleting test locations...")
Location.objects.filter(collegeName__in=['DATA', 'DMEO123', 'SADSADSDB', 'UIUIOUIO123']).delete()
print("Done.")
