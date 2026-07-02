import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from maintenance.models import Ticket

print("=== TICKETS IN DATABASE ===")
for t in Ticket.objects.all().order_by('-id'):
    print(f"ID: {t.id} | Status: {t.status} | CreatedDate: {t.createdDate} | InProgressDate: {t.inProgressDate} | CompletedDate: {t.completedDate}")
    print(f"  Description: {t.issueDescription}")
    print(f"  CreatedImg: {t.createdImage} | InProgressImg: {t.inProgressImage} | CompletedImg: {t.completedImage}")
