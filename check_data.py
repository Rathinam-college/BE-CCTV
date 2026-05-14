import os
import sys
import django

# Setup Django environment
sys.path.append(r'd:\Rathinam college\cctv\backend_django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Camera, NVR, Biometric, NetworkSwitch

def analyze_model(model, name):
    print(f"\n=== Analyzing {name} ===")
    records = model.objects.all()
    print(f"Total Records: {records.count()}")
    
    # Check Locations
    if name == 'Camera':
        # Cameras use block/floor/campusZone mostly, but let's check what we have
        unique_blocks = list(model.objects.values_list('block', flat=True).distinct())
        unique_zones = list(model.objects.values_list('campusZone', flat=True).distinct())
        print(f"Unique Blocks: {unique_blocks}")
        print(f"Unique Zones: {unique_zones}")
    else:
        unique_locs = list(model.objects.values_list('location', flat=True).distinct())
        print(f"Unique Locations: {unique_locs}")

    # Check for empty fields
    empty_locs = records.filter(location='').count() if name != 'Camera' else records.filter(block=None).count()
    if empty_locs > 0:
        print(f"WARNING: Found {empty_locs} records with missing location/block data.")

    # Check for suspicious IP addresses
    invalid_ips = [r.ipAddress for r in records if r.ipAddress and not r.ipAddress.startswith('192.168.') and not r.ipAddress.startswith('10.') and r.ipAddress != '—']
    if invalid_ips:
        print(f"Suspicious IPs found: {invalid_ips[:5]}...")

if __name__ == "__main__":
    analyze_model(Camera, 'Camera')
    analyze_model(NVR, 'NVR')
    analyze_model(Biometric, 'Biometric')
    analyze_model(NetworkSwitch, 'NetworkSwitch')
