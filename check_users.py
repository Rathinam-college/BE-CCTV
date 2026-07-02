import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

print("=== USERS IN DATABASE ===")
for u in User.objects.all():
    print(f"Name: {u.name} | Email: {u.email} | Role: {u.role} | IsStaff: {u.is_staff} | IsSuperuser: {u.is_superuser}")
