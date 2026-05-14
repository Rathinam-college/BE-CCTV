import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

email = 'Admin@gmail.com'
password = 'admin'

user, created = User.objects.get_or_create(
    email=email,
    defaults={
        'name': 'Administrator',
        'role': 'Super Admin',
        'is_staff': True,
        'is_superuser': True
    }
)
user.set_password(password)
user.save()
print(f"User {email} password updated successfully to: {password}")
