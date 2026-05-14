import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import MasterLocation, GlobalSiteConfig
from maintenance.models import Ticket, MaintenanceStaff
from users.models import User

def verify():
    print("\n=== DATABASE INTEGRITY DIAGNOSTIC ===\n")

    # 1. Check MasterLocation Table
    print("1. Site Registry (MasterLocation):")
    ml_fields = [f.name for f in MasterLocation._meta.get_fields()]
    print(f"   - Required Fields Found: {'assignedTo' in ml_fields and 'collegeName' in ml_fields}")
    ml_count = MasterLocation.objects.count()
    print(f"   - Total Registered Locations: {ml_count}")
    if ml_count > 0:
        sample = MasterLocation.objects.first()
        print(f"   - Sample Record: {sample.collegeName} | {sample.block} | Responsible: {sample.assignedTo.name if sample.assignedTo else 'None'}")

    # 2. Check GlobalSiteConfig Table
    print("\n2. Global Site Intelligence:")
    gs_fields = [f.name for f in GlobalSiteConfig._meta.get_fields()]
    print(f"   - Responsibility Field Active: {'assignedTo' in gs_fields}")
    config = GlobalSiteConfig.objects.first()
    if config:
        print(f"   - Active Site: {config.collegeName} | Responsible: {config.assignedTo.name if config.assignedTo else 'None'}")

    # 3. Check Ticket Table
    print("\n3. Maintenance Tickets (New Schema):")
    t_fields = [f.name for f in Ticket._meta.get_fields()]
    new_fields = ['collegeName', 'block', 'floor', 'room', 'assignedTo', 'assignedStaff']
    missing = [f for f in new_fields if f not in t_fields]
    print(f"   - Schema Status: {'OK' if not missing else f'MISSING: {missing}'}")
    t_count = Ticket.objects.count()
    print(f"   - Total Tickets: {t_count}")
    if t_count > 0:
        sample_t = Ticket.objects.latest('id')
        staff_list = ", ".join([s.name for s in sample_t.assignedStaff.all()])
        print(f"   - Latest Ticket: {sample_t.issueDescription[:30]}...")
        print(f"   - Location Data: {sample_t.collegeName} > {sample_t.block}")
        print(f"   - Site Admin: {sample_t.assignedTo.name if sample_t.assignedTo else 'Unlinked'}")
        print(f"   - Technicians: {staff_list if staff_list else 'None'}")

    # 4. Staff Registry
    print("\n4. Technician Registry:")
    staff_count = MaintenanceStaff.objects.count()
    print(f"   - Registered Staff: {staff_count}")
    if staff_count > 0:
        names = ", ".join([s.name for s in MaintenanceStaff.objects.all()])
        print(f"   - Active Names: {names}")

    print("\n=== DIAGNOSTIC COMPLETE ===")

if __name__ == "__main__":
    verify()
