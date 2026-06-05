from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (
    Camera, NVR, Biometric, Barrier, NetworkSwitch, ActivityLog, 
    CameraRemark, NVRRemark, BiometricRemark, SwitchRemark,
    CameraRelocation, NVRRelocation, BiometricRelocation, SwitchRelocation,
    GlobalSiteConfig, MasterLocation,
    Rack, RackRemark, RackRelocation, Occupation
)
from .serializers import (
    CameraSerializer, NVRSerializer, BiometricSerializer, BarrierSerializer, 
    NetworkSwitchSerializer, ActivityLogSerializer, CameraRemarkSerializer, 
    NVRRemarkSerializer, BiometricRemarkSerializer, SwitchRemarkSerializer,
    CameraRelocationSerializer, NVRRelocationSerializer, BiometricRelocationSerializer, SwitchRelocationSerializer,
    GlobalSiteConfigSerializer, MasterLocationSerializer,
    RackSerializer, RackRemarkSerializer, RackRelocationSerializer, OccupationSerializer
)

from django.db import transaction
from django.db.models import Count
import openpyxl
import io

def log_activity(user, action, page, details='', request=None):
    ip = ''
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    
    ActivityLog.objects.create(
        user=user,
        action=action,
        page=page,
        details=details,
        ipAddress=ip
    )

def check_can_edit(user, page):
    if user.role == 'Super Admin':
        return True
    return f"{page}:EDIT" in user.permissions

def sync_location_to_master(college, block, floor, room, brand):
    if college and block:
        try:
            MasterLocation.objects.get_or_create(
                collegeName=college,
                block=block,
                floor=floor if floor else '',
                room=room if room else '',
                defaults={'brand': brand}
            )
        except Exception as e:
            print(f"MasterLocation Registry update skipped: {str(e)}")

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Cameras'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'Cameras', f"Created camera: {request.data.get('name')}", request)
        return response

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Cameras'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        log_activity(request.user, 'CREATE', 'Cameras', f"Bulk created {len(data)} cameras", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'])
    def upload_excel(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Cameras'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Handle both .xlsx and .csv if needed, but primarily .xlsx
            if file_obj.name.endswith('.xlsx') or file_obj.name.endswith('.xls'):
                wb = openpyxl.load_workbook(file_obj)
                ws = wb.active
                
                headers = [str(cell.value).strip().lower() if cell.value else "" for cell in ws[1]]
                rows_data = []
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if not any(row): continue
                    rows_data.append(dict(zip(headers, row)))
            elif file_obj.name.endswith('.csv'):
                import csv
                decoded_file = file_obj.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                rows_data = [ {k.lower(): v for k, v in row.items()} for row in reader]
            else:
                return Response({'message': 'Unsupported file format. Please upload .xlsx or .csv'}, status=status.HTTP_400_BAD_REQUEST)

            created_count = 0
            updated_count = 0
            with transaction.atomic():
                for data in rows_data:
                    # Mapping
                    name_val = data.get('device type') or data.get('devicetype') or data.get('camera type') or data.get('name') or 'Unknown Camera'
                    camera_data = {
                        'ipAddress': data.get('ip address') or data.get('ipaddress'),
                        'name': name_val,
                        'deviceType': data.get('device type') or data.get('devicetype') or data.get('camera type') or name_val,
                        'status': data.get('status') or 'Online',
                        'campusZone': data.get('campus zone') or data.get('campuszone') or 'INSIDE',
                        'block': data.get('block'),
                        'floor': data.get('floor'),
                        'brand': data.get('brand'),
                        'remarks': data.get('remarks'),
                    }
                    
                    # Reconstruct siteName and dvrNvrDetails
                    block = camera_data['block'] or ''
                    floor = camera_data['floor'] or ''
                    camera_data['siteName'] = f"{block} - {floor}" if block or floor else 'Unknown'
                    
                    gateway = data.get('ipv4 gateway') or data.get('gateway') or ''
                    subnet = data.get('subnet mask') or data.get('subnet') or ''
                    mac = data.get('mac address') or data.get('mac') or ''
                    college = data.get('college name') or data.get('college') or ''
                    room = data.get('room') or ''
                    
                    # Special fields that are also in the model
                    camera_data['gateway'] = gateway
                    camera_data['subnetMask'] = subnet
                    camera_data['macAddress'] = mac
                    camera_data['collegeName'] = college
                    camera_data['room'] = room
                    
                    # Sync to Master Location Registry
                    sync_location_to_master(college, camera_data['block'], camera_data['floor'], room, camera_data['brand'])
                    
                    # cameraId will be auto-generated by the model's save method if not provided
                    serial = data.get('serial number') or data.get('cameraid') or data.get('device serial number')
                    
                    if serial:
                        # Update existing or create new with this serial
                        obj, created = Camera.objects.update_or_create(
                            cameraId=serial,
                            defaults=camera_data
                        )
                        if created: created_count += 1
                        else: updated_count += 1
                    else:
                        # Create new, let save() handle sequential cameraId generation
                        Camera.objects.create(**camera_data)
                        created_count += 1
            
            log_activity(request.user, 'UPLOAD', 'Cameras', f"Uploaded file {file_obj.name}: {created_count} created, {updated_count} updated", request)
            return Response({
                'message': 'Import Complete',
                'created': created_count,
                'updated': updated_count,
                'total': len(rows_data)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'message': f'Error processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_remark(self, request, pk=None):
        camera = self.get_object()
        remark_text = request.data.get('remark')
        if not remark_text:
            return Response({'message': 'Remark is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = CameraRemark.objects.create(
            camera=camera,
            remark=remark_text,
            device_status=camera.status,
            user=request.user
        )
        
        log_activity(request.user, 'REMARK', 'Cameras', f"Added remark to camera: {camera.name}", request)
        return Response(CameraRemarkSerializer(remark).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_relocation(self, request, pk=None):
        camera = self.get_object()
        serializer = CameraRelocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(camera=camera, user=request.user)
        log_activity(request.user, 'RELOCATE', 'Cameras', f"Relocated camera: {camera.name}", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Cameras'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        instance = self.get_object()
        old_status = instance.status
        
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            instance.refresh_from_db()
            new_status = instance.status
            if old_status != new_status:
                log_activity(request.user, 'STATUS_CHANGE', 'Cameras', f"Status changed from {old_status} to {new_status} for camera: {instance.name}", request)
                CameraRemark.objects.create(
                    camera=instance,
                    remark=f"System: Status changed from {old_status} to {new_status}",
                    device_status=new_status,
                    user=request.user
                )
            else:
                log_activity(request.user, 'EDIT', 'Cameras', f"Updated camera: {instance.name}", request)
        
        return response

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Cameras'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        log_activity(request.user, 'DELETE', 'Cameras', f"Deleted camera ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

class NVRViewSet(viewsets.ModelViewSet):
    queryset = NVR.objects.all()
    serializer_class = NVRSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Storage'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'NVR', f"Created NVR: {request.data.get('nvrName')}", request)
        return response

    @action(detail=False, methods=['post'])
    def upload_excel(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Storage'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if file_obj.name.endswith('.xlsx') or file_obj.name.endswith('.xls'):
                wb = openpyxl.load_workbook(file_obj)
                ws = wb.active
                headers = [str(cell.value).strip().lower() if cell.value else "" for cell in ws[1]]
                rows_data = [dict(zip(headers, row)) for row in ws.iter_rows(min_row=2, values_only=True) if any(row)]
            elif file_obj.name.endswith('.csv'):
                import csv
                decoded_file = file_obj.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                rows_data = [{k.lower(): v for k, v in row.items()} for row in reader]
            else:
                return Response({'message': 'Unsupported format'}, status=status.HTTP_400_BAD_REQUEST)

            created_count = 0
            updated_count = 0
            with transaction.atomic():
                for data in rows_data:
                    college = data.get('college name') or data.get('college') or ''
                    block = data.get('block') or ''
                    floor = data.get('floor') or ''
                    room = data.get('room') or ''
                    
                    nvr_data = {
                        'ipAddress': data.get('ip address') or data.get('ipaddress'),
                        'nvrName': data.get('nvr name') or data.get('name') or 'Unknown NVR',
                        'location': data.get('location') or f"{college} | {block} | {floor} | {room}",
                        'brand': data.get('brand'),
                        'hardDisk': data.get('hard disk') or data.get('harddisk'),
                        'channel': data.get('channel'),
                        'status': data.get('status') or 'Online',
                        'collegeName': college,
                        'block': block,
                        'floor': floor,
                        'room': room,
                    }
                    
                    # Sync to Master Location Registry
                    sync_location_to_master(college, block, floor, room, nvr_data['brand'])
                    serial = data.get('serial number') or data.get('serialnumber') or data.get('sno')
                    
                    if serial:
                        obj, created = NVR.objects.update_or_create(serialNumber=serial, defaults=nvr_data)
                        if created: created_count += 1
                        else: updated_count += 1
                    else:
                        NVR.objects.create(**nvr_data)
                        created_count += 1
            
            log_activity(request.user, 'UPLOAD', 'NVR', f"Uploaded {file_obj.name}", request)
            return Response({'message': 'Import Complete', 'created': created_count, 'updated': updated_count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Storage'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        log_activity(request.user, 'CREATE', 'NVR', f"Bulk created {len(data)} NVRs", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_remark(self, request, pk=None):
        nvr = self.get_object()
        remark_text = request.data.get('remark')
        if not remark_text:
            return Response({'message': 'Remark is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = NVRRemark.objects.create(
            nvr=nvr,
            remark=remark_text,
            device_status=nvr.status,
            user=request.user
        )
        
        log_activity(request.user, 'REMARK', 'NVR', f"Added remark to NVR: {nvr.nvrName}", request)
        return Response(NVRRemarkSerializer(remark).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_relocation(self, request, pk=None):
        nvr = self.get_object()
        serializer = NVRRelocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(nvr=nvr, user=request.user)
        log_activity(request.user, 'RELOCATE', 'NVR', f"Relocated NVR: {nvr.nvrName}", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Storage'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        instance = self.get_object()
        old_status = instance.status
        
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            instance.refresh_from_db()
            new_status = instance.status
            if old_status != new_status:
                log_activity(request.user, 'STATUS_CHANGE', 'NVR', f"Status changed from {old_status} to {new_status} for NVR: {instance.nvrName}", request)
                NVRRemark.objects.create(
                    nvr=instance,
                    remark=f"System: Status changed from {old_status} to {new_status}",
                    device_status=new_status,
                    user=request.user
                )
            else:
                log_activity(request.user, 'EDIT', 'NVR', f"Updated NVR: {instance.nvrName}", request)
                
        return response

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Storage'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        log_activity(request.user, 'DELETE', 'NVR', f"Deleted NVR ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

class BiometricViewSet(viewsets.ModelViewSet):
    queryset = Biometric.objects.all()
    serializer_class = BiometricSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Biometrics'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'Biometrics', f"Created Biometric: {request.data.get('name')}", request)
        return response

    @action(detail=False, methods=['post'])
    def upload_excel(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Biometrics'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if file_obj.name.endswith('.xlsx') or file_obj.name.endswith('.xls'):
                wb = openpyxl.load_workbook(file_obj)
                ws = wb.active
                headers = [str(cell.value).strip().lower() if cell.value else "" for cell in ws[1]]
                rows_data = [dict(zip(headers, row)) for row in ws.iter_rows(min_row=2, values_only=True) if any(row)]
            elif file_obj.name.endswith('.csv'):
                import csv
                decoded_file = file_obj.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                rows_data = [{k.lower(): v for k, v in row.items()} for row in reader]
            else:
                return Response({'message': 'Unsupported format'}, status=status.HTTP_400_BAD_REQUEST)

            created_count = 0
            updated_count = 0
            with transaction.atomic():
                for data in rows_data:
                    college = data.get('college name') or data.get('college') or ''
                    block = data.get('block') or ''
                    floor = data.get('floor') or ''
                    room = data.get('room') or ''
                    
                    bio_data = {
                        'name': data.get('name') or 'Unknown Biometric',
                        'location': data.get('location') or f"{college} | {block} | {floor} | {room}",
                        'type': data.get('type') or 'Fingerprint',
                        'brand': data.get('brand'),
                        'ipAddress': data.get('ip address') or data.get('ipaddress'),
                        'serverIp': data.get('server ip') or data.get('serverip'),
                        'status': data.get('status') or 'Online',
                        'collegeName': college,
                        'block': block,
                        'floor': floor,
                        'room': room,
                    }
                    
                    # Sync to Master Location Registry
                    sync_location_to_master(college, block, floor, room, bio_data['brand'])
                    serial = data.get('serial number') or data.get('serialnumber')
                    
                    if serial:
                        obj, created = Biometric.objects.update_or_create(serialNumber=serial, defaults=bio_data)
                        if created: created_count += 1
                        else: updated_count += 1
                    else:
                        Biometric.objects.create(**bio_data)
                        created_count += 1
            
            log_activity(request.user, 'UPLOAD', 'Biometrics', f"Uploaded {file_obj.name}", request)
            return Response({'message': 'Import Complete', 'created': created_count, 'updated': updated_count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Biometrics'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        log_activity(request.user, 'CREATE', 'Biometrics', f"Bulk created {len(data)} Biometric devices", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_remark(self, request, pk=None):
        biometric = self.get_object()
        remark_text = request.data.get('remark')
        if not remark_text:
            return Response({'message': 'Remark is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = BiometricRemark.objects.create(
            biometric=biometric,
            remark=remark_text,
            device_status=biometric.status,
            user=request.user
        )
        
        log_activity(request.user, 'REMARK', 'Biometrics', f"Added remark to Biometric: {biometric.name}", request)
        return Response(BiometricRemarkSerializer(remark).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_relocation(self, request, pk=None):
        biometric = self.get_object()
        serializer = BiometricRelocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(biometric=biometric, user=request.user)
        log_activity(request.user, 'RELOCATE', 'Biometrics', f"Relocated Biometric: {biometric.name}", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Biometrics'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        instance = self.get_object()
        old_status = instance.status
        
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            instance.refresh_from_db()
            new_status = instance.status
            if old_status != new_status:
                log_activity(request.user, 'STATUS_CHANGE', 'Biometrics', f"Status changed from {old_status} to {new_status} for Biometric: {instance.name}", request)
                BiometricRemark.objects.create(
                    biometric=instance,
                    remark=f"System: Status changed from {old_status} to {new_status}",
                    device_status=new_status,
                    user=request.user
                )
            else:
                log_activity(request.user, 'EDIT', 'Biometrics', f"Updated Biometric: {instance.name}", request)
                
        return response

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Biometrics'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        log_activity(request.user, 'DELETE', 'Biometrics', f"Deleted Biometric ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

class BarrierViewSet(viewsets.ModelViewSet):
    queryset = Barrier.objects.all()
    serializer_class = BarrierSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class NetworkSwitchViewSet(viewsets.ModelViewSet):
    queryset = NetworkSwitch.objects.all()
    serializer_class = NetworkSwitchSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Network Switches'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'Switches', f"Created Switch: {request.data.get('name')}", request)
        return response

    @action(detail=False, methods=['post'])
    def upload_excel(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Network Switches'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if file_obj.name.endswith('.xlsx') or file_obj.name.endswith('.xls'):
                wb = openpyxl.load_workbook(file_obj)
                ws = wb.active
                headers = [str(cell.value).strip().lower() if cell.value else "" for cell in ws[1]]
                rows_data = [dict(zip(headers, row)) for row in ws.iter_rows(min_row=2, values_only=True) if any(row)]
            elif file_obj.name.endswith('.csv'):
                import csv
                decoded_file = file_obj.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                rows_data = [{k.lower(): v for k, v in row.items()} for row in reader]
            else:
                return Response({'message': 'Unsupported format'}, status=status.HTTP_400_BAD_REQUEST)

            created_count = 0
            updated_count = 0
            with transaction.atomic():
                for data in rows_data:
                    college = data.get('college name') or data.get('college') or ''
                    block = data.get('block') or ''
                    floor = data.get('floor') or ''
                    room = data.get('room') or ''
                    
                    switch_data = {
                        'name': data.get('name') or 'Unknown Switch',
                        'ipAddress': data.get('ip address') or data.get('ipaddress'),
                        'location': data.get('location') or f"{college} | {block} | {floor} | {room}",
                        'brand': data.get('brand'),
                        'model': data.get('model'),
                        'portCount': data.get('port count') or data.get('portcount'),
                        'status': data.get('status') or 'Online',
                        'collegeName': college,
                        'block': block,
                        'floor': floor,
                        'room': room,
                    }
                    
                    # Sync to Master Location Registry
                    sync_location_to_master(college, block, floor, room, switch_data['brand'])
                    serial = data.get('serial number') or data.get('serialnumber')
                    
                    if serial:
                        obj, created = NetworkSwitch.objects.update_or_create(serialNumber=serial, defaults=switch_data)
                        if created: created_count += 1
                        else: updated_count += 1
                    else:
                        NetworkSwitch.objects.create(**switch_data)
                        created_count += 1
            
            log_activity(request.user, 'UPLOAD', 'Switches', f"Uploaded {file_obj.name}", request)
            return Response({'message': 'Import Complete', 'created': created_count, 'updated': updated_count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Network Switches'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        log_activity(request.user, 'CREATE', 'Network Switches', f"Bulk created {len(data)} switches", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_remark(self, request, pk=None):
        switch = self.get_object()
        remark_text = request.data.get('remark')
        if not remark_text:
            return Response({'message': 'Remark is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = SwitchRemark.objects.create(
            switch=switch,
            remark=remark_text,
            device_status=switch.status,
            user=request.user
        )
        
        log_activity(request.user, 'REMARK', 'Network Switches', f"Added remark to Switch: {switch.name}", request)
        return Response(SwitchRemarkSerializer(remark).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_relocation(self, request, pk=None):
        switch = self.get_object()
        serializer = SwitchRelocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(switch=switch, user=request.user)
        log_activity(request.user, 'RELOCATE', 'Network Switches', f"Relocated Switch: {switch.name}", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Network Switches'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        instance = self.get_object()
        old_status = instance.status
        
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            instance.refresh_from_db()
            new_status = instance.status
            if old_status != new_status:
                log_activity(request.user, 'STATUS_CHANGE', 'Switches', f"Status changed from {old_status} to {new_status} for Switch: {instance.name}", request)
                SwitchRemark.objects.create(
                    switch=instance,
                    remark=f"System: Status changed from {old_status} to {new_status}",
                    device_status=new_status,
                    user=request.user
                )
            else:
                log_activity(request.user, 'EDIT', 'Switches', f"Updated Switch: {instance.name}", request)
                
        return response

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Network Switches'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        log_activity(request.user, 'DELETE', 'Switches', f"Deleted Switch ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

class CameraRemarkViewSet(viewsets.ModelViewSet):
    queryset = CameraRemark.objects.all()
    serializer_class = CameraRemarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NVRRemarkViewSet(viewsets.ModelViewSet):
    queryset = NVRRemark.objects.all()
    serializer_class = NVRRemarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BiometricRemarkViewSet(viewsets.ModelViewSet):
    queryset = BiometricRemark.objects.all()
    serializer_class = BiometricRemarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SwitchRemarkViewSet(viewsets.ModelViewSet):
    queryset = SwitchRemark.objects.all()
    serializer_class = SwitchRemarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityLogViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Super Admin':
            return ActivityLog.objects.all().order_by('-timestamp')
        return ActivityLog.objects.filter(user=user).order_by('-timestamp')

    def create(self, request, *args, **kwargs):
        action = request.data.get('action', 'VIEW')
        page = request.data.get('page', 'Unknown')
        details = request.data.get('details', '')
        log_activity(request.user, action, page, details, request)
        return Response({'status': 'logged'})

class MasterLocationViewSet(viewsets.ModelViewSet):
    queryset = MasterLocation.objects.all()
    serializer_class = MasterLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MasterLocation.objects.all().order_by('collegeName', 'block')

    def perform_create(self, serializer):
        serializer.save()
        log_activity(self.request.user, 'CREATE', 'Location', f"Added master location: {self.request.data.get('collegeName')}", self.request)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_activity(self.request.user, 'EDIT', 'Location', f"Updated master location: {instance.collegeName}", self.request)

    def perform_destroy(self, instance):
        log_activity(self.request.user, 'DELETE', 'Location', f"Deleted master location: {instance.collegeName} {instance.block}", self.request)
        
        college = instance.collegeName
        block = instance.block
        floor = instance.floor
        room = instance.room
        
        if not floor and not room:
            # Deleting a Block -> Delete block, all its floors, and all its rooms
            MasterLocation.objects.filter(collegeName=college, block=block).delete()
        elif not room:
            # Deleting a Floor -> Delete the floor and all its rooms
            MasterLocation.objects.filter(collegeName=college, block=block, floor=floor).delete()
        else:
            # Deleting a specific Room
            instance.delete()

class GlobalSiteConfigViewSet(viewsets.ModelViewSet):
    queryset = GlobalSiteConfig.objects.all()
    serializer_class = GlobalSiteConfigSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        config = GlobalSiteConfig.objects.first()
        if not config:
            return Response({})
        return Response(GlobalSiteConfigSerializer(config).data)

    @action(detail=False, methods=['post'])
    def apply_site(self, request):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        config = GlobalSiteConfig.objects.first()
        if not config:
            config = GlobalSiteConfig.objects.create()
        
        serializer = self.get_serializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        log_activity(request.user, 'CONFIG_UPDATE', 'Global', f"Updated global site config: {config.collegeName}", request)
        
        # Also ensure it exists in MasterLocation registry
        try:
            if config.collegeName and config.block:
                MasterLocation.objects.update_or_create(
                    collegeName=config.collegeName,
                    block=config.block,
                    floor=config.floor if config.floor else '',
                    room=config.room if config.room else '',
                    defaults={
                        'brand': config.brand,
                        'assignedTo': config.assignedTo
                    }
                )
        except Exception as e:
            print(f"MasterLocation Registry update skipped: {str(e)}")
            
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_locations(self, request):
        locations = MasterLocation.objects.all().order_by('collegeName', 'block')
        return Response(MasterLocationSerializer(locations, many=True).data)

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        from maintenance.models import Ticket
        
        return Response({
            'cameras': {
                'total': Camera.objects.count(),
                'online': Camera.objects.filter(status='Online').count(),
                'offline': Camera.objects.filter(status='Offline').count(),
            },
            'nvrs': {
                'total': NVR.objects.count(),
                'online': NVR.objects.filter(status='Online').count(),
                'offline': NVR.objects.filter(status='Offline').count(),
            },
            'biometrics': {
                'total': Biometric.objects.count(),
                'online': Biometric.objects.filter(status='Online').count(),
                'offline': Biometric.objects.filter(status='Offline').count(),
            },
            'switches': {
                'total': NetworkSwitch.objects.count(),
                'online': NetworkSwitch.objects.filter(status='Online').count(),
                'offline': NetworkSwitch.objects.filter(status='Offline').count(),
            },
            'tickets': {
                'total': Ticket.objects.count(),
                'open': Ticket.objects.filter(status='Open').count(),
                'inProgress': Ticket.objects.filter(status='In Progress').count(),
                'completed': Ticket.objects.filter(status='Completed').count(),
                'upgrade': Ticket.objects.filter(category__icontains='Upgrade').count(),
                'project': Ticket.objects.filter(category__icontains='Project').count(),
            },
            'distribution': [
                {'name': c['collegeName'] or 'Unassigned', 'count': c['count']}
                for c in Camera.objects.values('collegeName').annotate(count=Count('id'))
            ]
        })

class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Racks'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'Racks', f"Created Rack: {request.data.get('name')}", request)
        return response

    @action(detail=True, methods=['post'])
    def add_remark(self, request, pk=None):
        rack = self.get_object()
        remark_text = request.data.get('remark')
        if not remark_text:
            return Response({'message': 'Remark is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = RackRemark.objects.create(
            rack=rack,
            remark=remark_text,
            device_status=rack.status,
            user=request.user
        )
        
        log_activity(request.user, 'REMARK', 'Racks', f"Added remark to Rack: {rack.name}", request)
        return Response(RackRemarkSerializer(remark).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_relocation(self, request, pk=None):
        rack = self.get_object()
        serializer = RackRelocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rack=rack, user=request.user)
        log_activity(request.user, 'RELOCATE', 'Racks', f"Relocated Rack: {rack.name}", request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Racks'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        instance = self.get_object()
        old_status = instance.status
        
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            instance.refresh_from_db()
            new_status = instance.status
            if old_status != new_status:
                log_activity(request.user, 'STATUS_CHANGE', 'Racks', f"Status changed from {old_status} to {new_status} for Rack: {instance.name}", request)
                RackRemark.objects.create(
                    rack=instance,
                    remark=f"System: Status changed from {old_status} to {new_status}",
                    device_status=new_status,
                    user=request.user
                )
            else:
                log_activity(request.user, 'EDIT', 'Racks', f"Updated Rack: {instance.name}", request)
                
        return response

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin'] and not check_can_edit(request.user, 'Racks'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        log_activity(request.user, 'DELETE', 'Racks', f"Deleted Rack ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

class RackRemarkViewSet(viewsets.ModelViewSet):
    queryset = RackRemark.objects.all()
    serializer_class = RackRemarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all().order_by('-createdAt')
    serializer_class = OccupationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        log_activity(self.request.user, 'CREATE', 'Occupation', f"Created occupation: {self.request.data.get('name')}", self.request)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_activity(self.request.user, 'EDIT', 'Occupation', f"Updated occupation: {instance.name}", self.request)

    def perform_destroy(self, instance):
        log_activity(self.request.user, 'DELETE', 'Occupation', f"Deleted occupation: {instance.name}", self.request)
        instance.delete()

    @action(detail=False, methods=['post'])
    def merge(self, request):
        old_names = request.data.get('old_names', [])
        new_name = request.data.get('new_name')
        occupation_type = request.data.get('occupation_type', 'College')

        if not old_names or not new_name:
            return Response({"error": "old_names and new_name are required."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create or update the master occupation
            occupation, created = Occupation.objects.get_or_create(
                name=new_name,
                defaults={'occupation_type': occupation_type}
            )
            
            # Store merged legacy names
            existing_merged = occupation.merged_from if occupation.merged_from else []
            merged_set = set(existing_merged)
            merged_set.update(old_names)
            occupation.merged_from = list(merged_set)
            occupation.save()

            # Update all standard CCTV devices
            Camera.objects.filter(collegeName__in=old_names).update(collegeName=new_name)
            NVR.objects.filter(collegeName__in=old_names).update(collegeName=new_name)
            Biometric.objects.filter(collegeName__in=old_names).update(collegeName=new_name)
            NetworkSwitch.objects.filter(collegeName__in=old_names).update(collegeName=new_name)
            Rack.objects.filter(collegeName__in=old_names).update(collegeName=new_name)

            # Update Tickets in maintenance app
            try:
                from maintenance.models import Ticket
                Ticket.objects.filter(collegeName__in=old_names).update(collegeName=new_name)
            except ImportError:
                pass # Maintenance app might not be installed or available

            # (User requested to KEEP the old occupations A and B in the registry after merging)
            # Occupation.objects.filter(name__in=old_names).exclude(name=new_name).delete()

        log_activity(request.user, 'MERGE', 'Occupation', f"Merged {len(old_names)} legacy colleges into {new_name}", request)
        return Response({"message": "Successfully merged colleges.", "new_name": new_name}, status=status.HTTP_200_OK)
