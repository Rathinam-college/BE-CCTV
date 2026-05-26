from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Ticket, Project, TicketRemark, MaintenanceStaff, ProjectDocument, TicketDocument
from .serializers import TicketSerializer, ProjectSerializer, TicketRemarkSerializer, MaintenanceStaffSerializer, ProjectDocumentSerializer, TicketDocumentSerializer
from rest_framework.response import Response
from cctv.views import check_can_edit, log_activity

class MaintenanceStaffViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceStaff.objects.all()
    serializer_class = MaintenanceStaffSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'MaintenanceStaff', f"Added staff: {request.data.get('name')}", request)
        return response

    def update(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        log_activity(request.user, 'EDIT', 'MaintenanceStaff', f"Updated staff ID: {kwargs.get('pk')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        staff_member = self.get_object()
        log_activity(request.user, 'DELETE', 'MaintenanceStaff', f"Deleted staff: {staff_member.name}", request)
        return super().destroy(request, *args, **kwargs)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'Projects', f"Created project: {request.data.get('name')}", request)
        return response

    def update(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        log_activity(request.user, 'EDIT', 'Projects', f"Updated project ID: {kwargs.get('pk')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        log_activity(request.user, 'DELETE', 'Projects', f"Deleted project ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def add_remark(self, request):
        pass # Assuming the original code had this, we leave it as is or delete it if it's incomplete. Let's just append ProjectDocumentViewSet below.

class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'ProjectDocument', f"Uploaded document: {request.data.get('name')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        doc = self.get_object()
        log_activity(request.user, 'DELETE', 'ProjectDocument', f"Deleted document: {doc.name}", request)
        return super().destroy(request, *args, **kwargs)

class TicketViewSet(viewsets.ModelViewSet):
    def bulk_create(self, request):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'BULK_CREATE', 'Projects', f"Bulk created {len(data)} projects", request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'Maintenance', f"Raised ticket: {request.data.get('issueDescription')}", request)
        return response

    def perform_update(self, serializer):
        instance = serializer.save()
        # Create an automatic remark for the update
        custom_remark = self.request.data.get('remark')
        TicketRemark.objects.create(
            ticket=instance,
            remark=custom_remark if custom_remark else f"Ticket updated - Status: {instance.status}",
            device_status=instance.status,
            user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        instance = self.get_object()
        
        # Restriction: Only Super Admin can edit completed tickets
        # Exception: Allow updating billing details on completed tickets
        billing_fields = {'bill_number', 'po_number', 'bill_document', 'po_document'}
        request_keys = set(request.data.keys())
        is_only_billing_update = request_keys.issubset(billing_fields)
        
        if instance.status == 'Completed' and request.user.role != 'Super Admin' and not is_only_billing_update:
            return Response({'message': 'Only Super Admin can modify completed tickets (except for Billing Records)'}, status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        log_activity(request.user, 'EDIT', 'Maintenance', f"Updated ticket ID: {instance.id}", request)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        instance = self.get_object()
        
        # Restriction: Only Super Admin can edit completed tickets
        # Exception: Allow updating billing details on completed tickets
        billing_fields = {'bill_number', 'po_number', 'bill_document', 'po_document'}
        request_keys = set(request.data.keys())
        is_only_billing_update = request_keys.issubset(billing_fields)
        
        if instance.status == 'Completed' and request.user.role != 'Super Admin' and not is_only_billing_update:
            return Response({'message': 'Only Super Admin can modify completed tickets (except for Billing Records)'}, status=status.HTTP_403_FORBIDDEN)

        kwargs['partial'] = True
        response = self.update(request, *args, **kwargs)
        log_activity(request.user, 'STATUS_CHANGE', 'Maintenance', f"Changed status/details of ticket ID: {kwargs.get('pk')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        ticket = self.get_object()
        if ticket.status == 'Completed' and request.user.role != 'Super Admin':
            return Response({'message': 'Completed tickets cannot be deleted to preserve audit integrity'}, status=status.HTTP_403_FORBIDDEN)
            
        log_activity(request.user, 'DELETE', 'Maintenance', f"Deleted ticket ID: {kwargs.get('pk')}", request)
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        if not self.request.data.get('raisedBy'):
            ticket = serializer.save(raisedBy=self.request.user)
        else:
            ticket = serializer.save()
        
        # Create an initial remark for the ticket
        TicketRemark.objects.create(
            ticket=ticket,
            remark=f"Initial Ticket Raised: {ticket.issueDescription}",
            device_status=ticket.status,
            user=self.request.user
        )

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Inject raisedBy if not provided for each ticket
        for item in data:
            if not item.get('raisedBy'):
                item['raisedBy'] = request.user.id

        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            tickets = serializer.save()
            # Create initial remarks for bulk tickets
            remarks = [
                TicketRemark(
                    ticket=t,
                    remark=f"Initial Ticket Raised (Import): {t.issueDescription}",
                    device_status=t.status,
                    user=request.user
                ) for t in tickets
            ]
            TicketRemark.objects.bulk_create(remarks)
            
            log_activity(request.user, 'BULK_CREATE', 'Maintenance', f"Bulk created {len(data)} tickets", request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def add_remark(self, request, pk=None):
        ticket = self.get_object()
        
        # Restriction: Cannot add remarks to completed tickets unless Super Admin
        if ticket.status == 'Completed' and request.user.role != 'Super Admin':
            return Response({'message': 'Cannot add messages to a completed ticket'}, status=status.HTTP_403_FORBIDDEN)

        remark_text = request.data.get('remark')
        
        if not remark_text:
            return Response({'message': 'Remark text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = TicketRemark.objects.create(
            ticket=ticket,
            remark=remark_text,
            device_status=ticket.status,
            user=request.user
        )
        
        serializer = TicketRemarkSerializer(remark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TicketDocumentViewSet(viewsets.ModelViewSet):
    queryset = TicketDocument.objects.all()
    serializer_class = TicketDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'TicketDocument', f"Uploaded document: {request.data.get('name')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        doc = self.get_object()
        log_activity(request.user, 'DELETE', 'TicketDocument', f"Deleted document: {doc.name}", request)
        return super().destroy(request, *args, **kwargs)
