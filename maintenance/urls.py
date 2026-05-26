from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, ProjectViewSet, MaintenanceStaffViewSet, ProjectDocumentViewSet, TicketDocumentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-documents', ProjectDocumentViewSet, basename='projectdocument')
router.register(r'ticket-documents', TicketDocumentViewSet, basename='ticketdocument')
router.register(r'staff', MaintenanceStaffViewSet, basename='staff')
router.register(r'', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
