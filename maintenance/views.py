from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
import threading
from .models import Ticket, Project, TicketRemark, ProjectDocument, TicketDocument, GeneralBillingInfo, GeneralBillingDocument, TicketBillingRecord, ProjectBillingRecord
from .serializers import TicketSerializer, ProjectSerializer, TicketRemarkSerializer, ProjectDocumentSerializer, TicketDocumentSerializer, GeneralBillingInfoSerializer, GeneralBillingDocumentSerializer, TicketBillingRecordSerializer, ProjectBillingRecordSerializer
from rest_framework.response import Response
from cctv.views import check_can_edit, log_activity

def send_ticket_email(subject, message, recipient_list, html_message=None):
    try:
        if settings.EMAIL_HOST_USER and recipient_list:
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER, 
                recipient_list, 
                fail_silently=True,
                html_message=html_message
            )
    except Exception as e:
        print(f"Failed to send email: {e}")



class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT "createdVideo" FROM "maintenance_ticket" LIMIT 1;')
                cursor.execute('SELECT 1 FROM "maintenance_ticket_assignedstaff" LIMIT 1;')
        except Exception:
            connection.rollback()
            sql = """
            CREATE TABLE IF NOT EXISTS "maintenance_generalbillingdocument" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "name" varchar(255) NOT NULL,
                "file" varchar(100) NOT NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "general_billing_id" bigint NOT NULL REFERENCES "maintenance_generalbillinginfo" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE TABLE IF NOT EXISTS "maintenance_projectbillingrecord" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "record_type" varchar(10) NOT NULL,
                "number" varchar(255) NOT NULL,
                "amount" varchar(255) NULL,
                "file" varchar(100) NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "project_id" bigint NOT NULL REFERENCES "maintenance_project" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE TABLE IF NOT EXISTS "maintenance_ticketbillingrecord" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "record_type" varchar(10) NOT NULL,
                "number" varchar(255) NOT NULL,
                "amount" varchar(255) NULL,
                "file" varchar(100) NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE TABLE IF NOT EXISTS "maintenance_ticket_assignedstaff" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED,
                "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED,
                UNIQUE ("ticket_id", "user_id")
            );
            ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "createdVideo" varchar(100) NULL;
            ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "inProgressVideo" varchar(100) NULL;
            ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "completedVideo" varchar(100) NULL;
            """
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
            except Exception as e:
                print("Failed to auto-create billing tables:", e)
                connection.rollback()
        return Project.objects.all().order_by('-id')

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
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT "createdVideo" FROM "maintenance_ticket" LIMIT 1;')
                cursor.execute('SELECT "receivedDate" FROM "maintenance_ticket" LIMIT 1;')
                cursor.execute('SELECT "raisedByName" FROM "maintenance_ticket" LIMIT 1;')
                cursor.execute('SELECT "ticketDevice" FROM "maintenance_ticket" LIMIT 1;')
                cursor.execute('SELECT 1 FROM "maintenance_ticket_assignedStaff" LIMIT 1;')
        except Exception:
            connection.rollback()
            statements = [
                'ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "createdVideo" varchar(100) NULL;',
                'ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "receivedDate" date NULL;',
                'ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "raisedByName" varchar(255) NULL;',
                'ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "ticketDevice" varchar(100) NULL;',
                'ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "inProgressVideo" varchar(100) NULL;',
                'ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "completedVideo" varchar(100) NULL;',
                '''CREATE TABLE IF NOT EXISTS "maintenance_ticket_assignedStaff" (
                    "id" bigserial NOT NULL PRIMARY KEY,
                    "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED,
                    "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED,
                    UNIQUE ("ticket_id", "user_id")
                );''',
                '''CREATE TABLE IF NOT EXISTS "maintenance_generalbillingdocument" (
                    "id" bigserial NOT NULL PRIMARY KEY,
                    "name" varchar(255) NOT NULL,
                    "file" varchar(100) NOT NULL,
                    "uploaded_at" timestamp with time zone NOT NULL,
                    "general_billing_id" bigint NOT NULL REFERENCES "maintenance_generalbillinginfo" ("id") DEFERRABLE INITIALLY DEFERRED
                );''',
                '''CREATE TABLE IF NOT EXISTS "maintenance_projectbillingrecord" (
                    "id" bigserial NOT NULL PRIMARY KEY,
                    "record_type" varchar(10) NOT NULL,
                    "number" varchar(255) NOT NULL,
                    "amount" varchar(255) NULL,
                    "file" varchar(100) NULL,
                    "uploaded_at" timestamp with time zone NOT NULL,
                    "project_id" bigint NOT NULL REFERENCES "maintenance_project" ("id") DEFERRABLE INITIALLY DEFERRED
                );''',
                '''CREATE TABLE IF NOT EXISTS "maintenance_ticketbillingrecord" (
                    "id" bigserial NOT NULL PRIMARY KEY,
                    "record_type" varchar(10) NOT NULL,
                    "number" varchar(255) NOT NULL,
                    "amount" varchar(255) NULL,
                    "file" varchar(100) NULL,
                    "uploaded_at" timestamp with time zone NOT NULL,
                    "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED
                );'''
            ]
            for stmt in statements:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(stmt)
                except Exception as e:
                    connection.rollback()
        return Ticket.objects.all().order_by('-createdAt', '-id')

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            return Response({"error_debug": traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        category = request.data.get('category')
        page_name = 'Upgrades' if category == 'Upgrade' else 'Maintenance'
        action_name = 'upgrade' if category == 'Upgrade' else 'ticket'
        log_activity(request.user, 'CREATE', page_name, f"Raised {action_name}: {request.data.get('issueDescription')}", request)
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
        
        # Handle multiple completed images
        completed_images = request.FILES.getlist('completedImages')
        if completed_images:
            from .models import TicketCompletedImage
            for img in completed_images:
                TicketCompletedImage.objects.create(ticket=instance, image=img)
        
        category = instance.category
        page_name = 'Upgrades' if category == 'Upgrade' else 'Maintenance'
        action_name = 'upgrade' if category == 'Upgrade' else 'ticket'
        log_activity(request.user, 'EDIT', page_name, f"Updated {action_name} ID: {instance.id}", request)
        return Response(self.get_serializer(instance).data)

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
        
        instance.refresh_from_db()
        category = instance.category
        page_name = 'Upgrades' if category == 'Upgrade' else 'Maintenance'
        action_name = 'upgrade' if category == 'Upgrade' else 'ticket'
        log_activity(request.user, 'STATUS_CHANGE', page_name, f"Changed status/details of {action_name} ID: {kwargs.get('pk')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        ticket = self.get_object()
        if ticket.status == 'Completed' and request.user.role != 'Super Admin':
            return Response({'message': 'Completed tickets cannot be deleted to preserve audit integrity'}, status=status.HTTP_403_FORBIDDEN)
            
        category = ticket.category
        page_name = 'Upgrades' if category == 'Upgrade' else 'Maintenance'
        action_name = 'upgrade' if category == 'Upgrade' else 'ticket'
        log_activity(request.user, 'DELETE', page_name, f"Deleted {action_name} ID: {kwargs.get('pk')}", request)
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

        # Send Email Notification asynchronously
        subject = f"New Ticket Raised: {ticket.divisionName or 'Unknown'} - {ticket.block or 'Unknown'}"
        message = f"A new maintenance ticket has been raised by {self.request.user.name}.\n\n"
        message += f"Location: {ticket.location or 'N/A'}\n"
        message += f"Description: {ticket.issueDescription}\n"
        message += f"Status: {ticket.status}\n\n"
        
        # HTML Email Template
        html_message = f"""
        <html>
          <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.05);">
              <div style="background: linear-gradient(135deg, #0b1c3e 0%, #1a3673 100%); padding: 30px 20px; text-align: center;">
                <h2 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 600; letter-spacing: 1px;">New Maintenance Ticket</h2>
              </div>
              <div style="padding: 35px;">
                <p style="font-size: 16px; color: #444444; margin-bottom: 25px; line-height: 1.5;">
                  A new maintenance ticket has been raised by <strong style="color: #0b1c3e;">{self.request.user.name}</strong>.
                </p>
                
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px;">
                  <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f0f0f0; width: 30%; color: #888888; font-weight: 600; font-size: 14px; text-transform: uppercase;">Location</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f0f0f0; color: #222222; font-weight: 500; font-size: 15px;">{ticket.location or 'N/A'}</td>
                  </tr>
                  <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f0f0f0; color: #888888; font-weight: 600; font-size: 14px; text-transform: uppercase;">Priority</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f0f0f0;">
                      <span style="display: inline-block; padding: 4px 10px; border-radius: 20px; background-color: #ffebee; color: #c62828; font-size: 13px; font-weight: bold;">{getattr(ticket, 'priority', 'Medium')}</span>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f0f0f0; color: #888888; font-weight: 600; font-size: 14px; text-transform: uppercase;">Status</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f0f0f0;">
                      <span style="display: inline-block; padding: 4px 10px; border-radius: 20px; background-color: #e3f2fd; color: #1565c0; font-size: 13px; font-weight: bold;">{ticket.status}</span>
                    </td>
                  </tr>
                </table>
                
                <div style="background-color: #f8fafc; padding: 20px; border-left: 4px solid #3b82f6; border-radius: 6px;">
                  <h4 style="margin-top: 0; color: #334155; font-size: 14px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Issue Description</h4>
                  <p style="margin-bottom: 0; color: #475569; font-size: 15px; line-height: 1.6;">{ticket.issueDescription}</p>
                </div>
              </div>
              <div style="background-color: #f8fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="margin: 0; color: #94a3b8; font-size: 13px;">This is an automated notification from the Rathinam Command Center.</p>
              </div>
            </div>
          </body>
        </html>
        """
        
        recipient_list = []
        if ticket.assignedTo and hasattr(ticket.assignedTo, 'email') and ticket.assignedTo.email:
            recipient_list.append(ticket.assignedTo.email)
            
        for staff in ticket.assignedStaff.all():
            if getattr(staff, 'email', None):
                recipient_list.append(staff.email)
            
        if recipient_list:
            threading.Thread(target=send_ticket_email, args=(subject, message, recipient_list, html_message)).start()

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from .models import Project
        
        # Inject raisedBy if not provided for each ticket
        for item in data:
            if not item.get('raisedBy'):
                item['raisedBy'] = request.user.id

            # Map assignedToName to assignedTo ID
            assigned_name = item.pop('assignedToName', None)
            if assigned_name:
                user_obj = User.objects.filter(name__iexact=assigned_name).first()
                if user_obj:
                    item['assignedTo'] = user_obj.id

            # Map project name to project ID if project field exists
            project_name = item.pop('project', None)
            if project_name and project_name.lower() != 'independent':
                proj_obj = Project.objects.filter(name__iexact=project_name).first()
                if proj_obj:
                    item['projectId'] = proj_obj.id

            # Handle extra metadata for remarks
            meta = {}
            if item.get('location'): meta['location'] = item.get('location')
            if item.get('category'): meta['category'] = item.get('category')
            if item.get('actionTaken'): meta['actionTaken'] = item.get('actionTaken')
            if item.get('instructionBy'): meta['instructionBy'] = item.get('instructionBy')
            if item.get('receivedTime'): meta['receivedTime'] = item.get('receivedTime')
            if item.get('endTime'): meta['endTime'] = item.get('endTime')
            if item.get('totalTime'): meta['totalTime'] = item.get('totalTime')
            if item.get('operationDate'): meta['manualDate'] = item.get('operationDate')
            
            import json
            item['remarks'] = json.dumps(meta)

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
        image = request.FILES.get('image')
        
        if not remark_text:
            return Response({'message': 'Remark text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark = TicketRemark.objects.create(
            ticket=ticket,
            remark=remark_text,
            image=image,
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

class GeneralBillingInfoViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralBillingInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1 FROM "maintenance_generalbillingdocument" LIMIT 1;')
        except Exception:
            # Table doesn't exist or error occurred. Rollback the transaction and create tables.
            connection.rollback()
            sql = """
            CREATE TABLE IF NOT EXISTS "maintenance_generalbillingdocument" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "name" varchar(255) NOT NULL,
                "file" varchar(100) NOT NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "general_billing_id" bigint NOT NULL REFERENCES "maintenance_generalbillinginfo" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE TABLE IF NOT EXISTS "maintenance_projectbillingrecord" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "record_type" varchar(10) NOT NULL,
                "number" varchar(255) NOT NULL,
                "amount" varchar(255) NULL,
                "file" varchar(100) NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "project_id" bigint NOT NULL REFERENCES "maintenance_project" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE TABLE IF NOT EXISTS "maintenance_ticketbillingrecord" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "record_type" varchar(10) NOT NULL,
                "number" varchar(255) NOT NULL,
                "amount" varchar(255) NULL,
                "file" varchar(100) NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            """
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
            except Exception as e:
                print("Failed to auto-create billing tables:", e)
                connection.rollback()
        
        return GeneralBillingInfo.objects.all().order_by('-createdAt')

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'GeneralBilling', f"Added General Billing: {request.data.get('work')}", request)
        return response

    def update(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        log_activity(request.user, 'EDIT', 'GeneralBilling', f"Updated General Billing ID: {kwargs.get('pk')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object()
        log_activity(request.user, 'DELETE', 'GeneralBilling', f"Deleted General Billing: {record.work}", request)
        return super().destroy(request, *args, **kwargs)

class GeneralBillingDocumentViewSet(viewsets.ModelViewSet):
    queryset = GeneralBillingDocument.objects.all()
    serializer_class = GeneralBillingDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'GeneralBillingDocument', f"Uploaded document: {request.data.get('name')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        doc = self.get_object()
        log_activity(request.user, 'DELETE', 'GeneralBillingDocument', f"Deleted document: {doc.name}", request)
        return super().destroy(request, *args, **kwargs)

class ProjectBillingRecordViewSet(viewsets.ModelViewSet):
    queryset = ProjectBillingRecord.objects.all()
    serializer_class = ProjectBillingRecordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'ProjectBillingRecord', f"Added {request.data.get('record_type')}: {request.data.get('number')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Projects'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object()
        log_activity(request.user, 'DELETE', 'ProjectBillingRecord', f"Deleted {record.record_type}: {record.number}", request)
        return super().destroy(request, *args, **kwargs)

class TicketBillingRecordViewSet(viewsets.ModelViewSet):
    queryset = TicketBillingRecord.objects.all()
    serializer_class = TicketBillingRecordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        response = super().create(request, *args, **kwargs)
        log_activity(request.user, 'CREATE', 'TicketBillingRecord', f"Added {request.data.get('record_type')}: {request.data.get('number')}", request)
        return response

    def destroy(self, request, *args, **kwargs):
        if not check_can_edit(request.user, 'Maintenance'):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object()
        log_activity(request.user, 'DELETE', 'TicketBillingRecord', f"Deleted {record.record_type}: {record.number}", request)
        return super().destroy(request, *args, **kwargs)
