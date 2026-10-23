import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

# List of default users to ensure exist in the database
default_users = [
    {
        'email': 'admin@mail.com',
        'name': 'Administrator',
        'role': 'Super Admin',
        'is_staff': True,
        'is_superuser': True,
        'password': 'admin123'
    },
    {
        'email': 'karthik_it@rathinam.in',
        'name': 'Karthik K N',
        'role': 'Super Admin',
        'is_staff': True,
        'is_superuser': True,
        'password': 'password123'
    },
    {
        'email': 'cctv@rathinam.in',
        'name': 'Manimaran',
        'role': 'Super Admin',
        'is_staff': True,
        'is_superuser': True,
        'password': 'password123'
    },
    {
        'email': 'saraths.ict@rathinam.in',
        'name': 'Sarath',
        'role': 'Admin',
        'is_staff': True,
        'is_superuser': False,
        'password': 'password123'
    },
    {
        'email': 'gm@rathinam.com',
        'name': 'GM',
        'role': 'Super Admin',
        'is_staff': True,
        'is_superuser': True,
        'password': 'password123'
    },
    {
        'email': 'staff@rathinam.in',
        'name': 'Staff User',
        'role': 'Staff',
        'is_staff': True,
        'is_superuser': False,
        'password': 'password123',
        'permissions': ['Dashboard:VIEW', 'Assets:VIEW', 'Maintenance:VIEW', 'Projects:VIEW']
    }
]

for u_data in default_users:
    user, created = User.objects.get_or_create(
        email=u_data['email'],
        defaults={
            'name': u_data['name'],
            'role': u_data['role'],
            'is_staff': u_data['is_staff'],
            'is_superuser': u_data['is_superuser'],
            'permissions': u_data.get('permissions', [])
        }
    )
    if created:
        user.set_password(u_data['password'])
        user.raw_password = u_data['password']
        user.save()
        print(f"User {u_data['email']} created successfully!")
    else:
        # Update permissions/role if needed
        if 'permissions' in u_data:
            user.permissions = u_data['permissions']
            user.save()
        print(f"User {u_data['email']} already exists.")

# Now, connect this staff user to tickets
from maintenance.models import Ticket
try:
    staff_user = User.objects.get(email='staff@rathinam.in')
    # Filter tickets where assignedStaff is empty (M2M relation count is 0)
    tickets_to_link = Ticket.objects.filter(assignedStaff=None)
    linked_count = 0
    for ticket in tickets_to_link:
        ticket.assignedStaff.add(staff_user)
        # Also assign it as primary assignedTo user if not set
        if not ticket.assignedTo:
            ticket.assignedTo = staff_user
            ticket.save()
        linked_count += 1
    if linked_count > 0:
        print(f"Connected staff user to {linked_count} tickets successfully.")
    else:
        print("No tickets required staff connection.")
except Exception as e:
    print(f"Failed to connect staff user to tickets: {e}")

