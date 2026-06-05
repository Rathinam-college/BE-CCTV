from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from cctv.models import Camera, NVR, NetworkSwitch, Biometric
from maintenance.models import Ticket, Project

try:
    import pandas as pd
except ImportError:
    pd = None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_excel(request):
    if request.user.role not in ['Super Admin', 'Admin']:
        return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
    if pd is None:
        return Response({'message': 'Pandas is not installed. Excel upload is disabled.'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        
    if 'file' not in request.FILES:
        return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    try:
        df = pd.read_excel(file)
        def clean(val):
            if pd.isna(val):
                return ''
            return str(val).strip()

        for index, row in df.iterrows():
            block = clean(row.get('BLOCK'))
            floor = clean(row.get('FLOOR'))
            idx = clean(row.get('INDEX'))
            device_type = clean(row.get('DEVICE TYPE'))
            ip = clean(row.get('IP ADDRESS'))
            gateway = clean(row.get('IPv4 GATE WAY'))
            serial = clean(row.get('DEVICE SERIAL NUMBER'))
            subnet = clean(row.get('SUBNET MASK'))
            mac = clean(row.get('MAC ADDRESS'))

            cam_id = serial or clean(row.get('cameraId')) or clean(row.get('Camera ID')) or f"CAM-{index}"
            name = device_type or clean(row.get('name')) or clean(row.get('Camera Name')) or 'Unknown Device'
            
            site_name = f"{block} - {floor}" if block else (clean(row.get('siteName')) or clean(row.get('Site Name')) or '')
            dvr_details = f"Gateway: {gateway} | Subnet: {subnet} | MAC: {mac} | Index: {idx}"

            Camera.objects.update_or_create(
                cameraId=cam_id,
                defaults={
                    'name': name,
                    'siteName': site_name,
                    'ipAddress': ip or clean(row.get('ipAddress')) or clean(row.get('IP Address')) or '',
                    'dvrNvrDetails': dvr_details,
                    'status': clean(row.get('status')) or clean(row.get('Status')) or 'Online',
                    'block': block,
                    'floor': floor,
                    'index': idx,
                    'deviceType': device_type,
                    'gateway': gateway,
                    'serialNumber': serial,
                    'subnetMask': subnet,
                    'macAddress': mac
                }
            )
        return Response({'message': 'Data imported successfully'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_report(request):
    if request.user.role not in ['Super Admin', 'Admin']:
        return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
    # Dummy endpoint for exporting reports
    # In a real scenario, generate a PDF or Excel and return as FileResponse
    return Response({'message': 'Report export endpoint'})

@api_view(['GET'])
@permission_classes([])
def gm_dashboard_api(request):
    """
    API endpoint for external GM View integration.
    Returns aggregated stats for Tickets, Projects, and Devices.
    """
    
    # 1. Ticket Statistics
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='Open').count()
    in_progress_tickets = Ticket.objects.filter(status='In Progress').count()
    completed_tickets = Ticket.objects.filter(status='Completed').count()
    
    # 2. Project Statistics
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='Active').count()
    completed_projects = Project.objects.filter(status='Completed').count()
    on_hold_projects = Project.objects.filter(status='On Hold').count()
    
    # 3. Device Inventory
    total_cameras = Camera.objects.count()
    total_nvrs = NVR.objects.count()
    total_switches = NetworkSwitch.objects.count()
    total_biometrics = Biometric.objects.count()
    
    # 4. Recent Active Issues (Top 10 Open/In Progress)
    recent_tickets = Ticket.objects.filter(status__in=['Open', 'In Progress']).order_by('-createdAt')[:10]
    recent_tickets_data = [
        {
            'id': t.id,
            'issueDescription': t.issueDescription,
            'location': t.location or f"{t.collegeName} {t.block} {t.floor} {t.room}".strip(),
            'status': t.status,
            'category': t.category,
            'createdAt': t.createdAt.strftime('%Y-%m-%d %H:%M:%S') if t.createdAt else None
        } for t in recent_tickets
    ]
    
    # 5. Active Projects (Top 5 Active)
    active_projects_list = Project.objects.filter(status='Active').order_by('-createdAt')[:5]
    active_projects_data = [
        {
            'id': p.id,
            'name': p.name,
            'client_name': p.client_name,
            'status': p.status,
            'start_date': p.start_date.strftime('%Y-%m-%d') if p.start_date else None,
            'end_date': p.end_date.strftime('%Y-%m-%d') if p.end_date else None,
            'ticket_count': p.tickets.count()
        } for p in active_projects_list
    ]
    
    data = {
        'tickets': {
            'total': total_tickets,
            'open': open_tickets,
            'in_progress': in_progress_tickets,
            'completed': completed_tickets
        },
        'projects': {
            'total': total_projects,
            'active': active_projects,
            'completed': completed_projects,
            'on_hold': on_hold_projects
        },
        'devices': {
            'cameras': total_cameras,
            'nvrs': total_nvrs,
            'switches': total_switches,
            'biometrics': total_biometrics
        },
        'recent_issues': recent_tickets_data,
        'active_projects': active_projects_data
    }
    
    return Response(data, status=status.HTTP_200_OK)
