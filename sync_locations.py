import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from cctv.models import Camera, NVR, Biometric, NetworkSwitch

def split_site_name(raw):
    if not raw or '|' not in raw:
        return None
    parts = [p.strip() for p in raw.split('|')]
    return {
        'college': parts[0] if len(parts) > 0 else '',
        'block': parts[1] if len(parts) > 1 else '',
        'floor': parts[2] if len(parts) > 2 else '',
        'room': parts[3] if len(parts) > 3 else ''
    }

def migrate_data():
    print("Starting database location synchronization...")

    # 1. Cameras
    print("Processing Cameras...")
    for cam in Camera.objects.all():
        loc = split_site_name(cam.siteName)
        if loc:
            cam.collegeName = loc['college'] or cam.collegeName
            cam.block = loc['block'] or cam.block
            cam.floor = loc['floor'] or cam.floor
            cam.room = loc['room'] or cam.room
            cam.save()
    
    # 2. NVRs
    print("Processing NVRs...")
    for nvr in NVR.objects.all():
        loc = split_site_name(nvr.location)
        if loc:
            nvr.collegeName = loc['college'] or nvr.collegeName
            nvr.block = loc['block'] or nvr.block
            nvr.floor = loc['floor'] or nvr.floor
            nvr.room = loc['room'] or nvr.room
            nvr.save()

    # 3. Biometrics
    print("Processing Biometrics...")
    for bio in Biometric.objects.all():
        loc = split_site_name(bio.location)
        if loc:
            bio.collegeName = loc['college'] or bio.collegeName
            bio.block = loc['block'] or bio.block
            bio.floor = loc['floor'] or bio.floor
            bio.room = loc['room'] or bio.room
            bio.save()

    # 4. Switches
    print("Processing Switches...")
    for sw in NetworkSwitch.objects.all():
        loc = split_site_name(sw.location)
        if loc:
            sw.collegeName = loc['college'] or sw.collegeName
            sw.block = loc['block'] or sw.block
            sw.floor = loc['floor'] or sw.floor
            sw.room = loc['room'] or sw.room
            sw.save()

    print("Database synchronization complete.")

if __name__ == "__main__":
    migrate_data()
