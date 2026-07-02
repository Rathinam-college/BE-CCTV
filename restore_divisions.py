import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Division, Camera, NVR, Biometric, NetworkSwitch, MasterLocation, Barrier, Rack

def restore_divisions():
    print("Scanning devices and locations for unique divisions...")
    unique_names = set()

    for model in [Camera, NVR, Biometric, NetworkSwitch, MasterLocation, Barrier, Rack]:
        names = model.objects.values_list('collegeName', flat=True).distinct()
        for name in names:
            if name and name.strip():
                unique_names.add(name.strip())

    print(f"Found {len(unique_names)} unique divisions: {unique_names}")

    restored_count = 0
    for name in unique_names:
        division, created = Division.objects.get_or_create(
            name=name,
            defaults={'division_type': 'College'}
        )
        if created:
            restored_count += 1
            print(f"Created Division: {name}")

    print(f"Successfully restored {restored_count} divisions.")

if __name__ == '__main__':
    restore_divisions()
