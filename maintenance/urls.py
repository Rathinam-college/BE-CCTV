from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, ProjectViewSet, ProjectDocumentViewSet, TicketDocumentViewSet, GeneralBillingInfoViewSet, GeneralBillingDocumentViewSet, ProjectBillingRecordViewSet, TicketBillingRecordViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-documents', ProjectDocumentViewSet, basename='projectdocument')
router.register(r'project-billing-records', ProjectBillingRecordViewSet, basename='projectbillingrecord')
router.register(r'ticket-documents', TicketDocumentViewSet, basename='ticketdocument')
router.register(r'ticket-billing-records', TicketBillingRecordViewSet, basename='ticketbillingrecord')

router.register(r'general-billing', GeneralBillingInfoViewSet, basename='generalbilling')
router.register(r'general-billing-documents', GeneralBillingDocumentViewSet, basename='generalbillingdocument')
router.register(r'', TicketViewSet, basename='ticket')

from django.http import HttpResponse

def debug_error_log(request):
    try:
        with open("error_log.txt", "r") as f:
            return HttpResponse(f.read(), content_type="text/plain")
    except Exception as e:
        return HttpResponse(str(e), content_type="text/plain")

urlpatterns = [
    path('', include(router.urls)),
    path('debug/', debug_error_log),
]

from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "createdVideo" varchar(100) NULL;')
        cursor.execute('ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "inProgressVideo" varchar(100) NULL;')
        cursor.execute('ALTER TABLE "maintenance_ticket" ADD COLUMN IF NOT EXISTS "completedVideo" varchar(100) NULL;')
        cursor.execute('ALTER TABLE "cctv_camera" ADD COLUMN IF NOT EXISTS "model" varchar(100) NULL;')
        cursor.execute('DROP TABLE IF EXISTS "maintenance_ticket_assignedstaff" CASCADE;')
        cursor.execute('DROP TABLE IF EXISTS "maintenance_ticket_assignedStaff" CASCADE;')
        cursor.execute('''
            CREATE TABLE "maintenance_ticket_assignedStaff" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED,
                "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED,
                UNIQUE ("ticket_id", "user_id")
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "maintenance_projectbillingrecord" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "record_type" varchar(10) NOT NULL,
                "number" varchar(255) NOT NULL,
                "amount" varchar(255) NULL,
                "file" varchar(100) NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "project_id" bigint NOT NULL REFERENCES "maintenance_project" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "maintenance_ticketbillingrecord" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "record_type" varchar(10) NOT NULL,
                "number" varchar(255) NOT NULL,
                "amount" varchar(255) NULL,
                "file" varchar(100) NULL,
                "uploaded_at" timestamp with time zone NOT NULL,
                "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        ''')
except Exception as e:
    pass
