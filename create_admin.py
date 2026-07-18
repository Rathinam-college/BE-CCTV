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
    }
]

for u_data in default_users:
    user, created = User.objects.get_or_create(
        email=u_data['email'],
        defaults={
            'name': u_data['name'],
            'role': u_data['role'],
            'is_staff': u_data['is_staff'],
            'is_superuser': u_data['is_superuser']
        }
    )
    if created:
        user.set_password(u_data['password'])
        user.raw_password = u_data['password']
        user.save()
        print(f"User {u_data['email']} created successfully!")
    else:
        print(f"User {u_data['email']} already exists.")
