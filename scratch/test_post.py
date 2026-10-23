import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User
admin_user = User.objects.get(email='admin@mail.com')

from rest_framework.test import APIClient
client = APIClient()
client.force_authenticate(user=admin_user)

for val in ['null', 'undefined', 'None']:
    payload = {
        'issueDescription': f'Test issue description with {val} assignedTo',
        'status': 'Open',
        'divisionName': 'RGI',
        'block': 'NEW CONTROL ROOM',
        'floor': 'G',
        'room': 'CONTROL ROOM',
        'location': 'RGI | NEW CONTROL ROOM | G | CONTROL ROOM',
        'category': 'Repair',
        'ticketDevice': 'Camera',
        'assignedTo': val,
    }
    response = client.post('/cctv/api/tickets/', payload)
    print(f"Val: {val} | Status code: {response.status_code} | Content: {response.content.decode()[:150]}")
