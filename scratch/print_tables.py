import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from maintenance.models import Ticket
from users.models import User

print("=== USERS ===")
for u in User.objects.all():
    print(f"ID: {u.id} | Email: {u.email} | Name: {u.name} | Role: {u.role}")

print("\n=== TICKETS ===")
for t in Ticket.objects.all():
    staff_emails = [s.email for s in t.assignedStaff.all()]
    print(f"Ticket ID: {t.id} | Status: {t.status} | AssignedTo: {t.assignedTo.email if t.assignedTo else 'None'} | AssignedStaff: {staff_emails}")
