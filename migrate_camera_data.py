import os
import sys
import django
import re

# Setup Django
sys.path.append(r'd:\Rathinam college\cctv\backend_django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Camera

def migrate_data():
    print("Starting data migration for Camera network details...")
    cameras = Camera.objects.all()
    count = 0
    
    for cam in cameras:
        details = cam.dvrNvrDetails or ""
        if not details:
            continue
            
        # Parse existing string format
        gw_match = re.search(r'Gateway:\s*([^|]+)', details)
        sub_match = re.search(r'Subnet:\s*([^|]+)', details)
        mac_match = re.search(r'MAC:\s*([^|]+)', details)
        coll_match = re.search(r'College:\s*([^|]+)', details)
        
        updated = False
        if gw_match and not cam.gateway:
            cam.gateway = gw_match.group(1).strip()
            updated = True
        if sub_match and not cam.subnetMask:
            cam.subnetMask = sub_match.group(1).strip()
            updated = True
        if mac_match and not cam.macAddress:
            cam.macAddress = mac_match.group(1).strip()
            updated = True
        if coll_match and not cam.collegeName:
            cam.collegeName = coll_match.group(1).strip()
            updated = True
            
        if updated:
            cam.save()
            count += 1
            print(f"Updated Camera: {cam.cameraId}")

    print(f"\nMigration complete! {count} records were updated.")

if __name__ == "__main__":
    migrate_data()
