from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, ProjectViewSet, MaintenanceStaffViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'staff', MaintenanceStaffViewSet, basename='staff')
router.register(r'', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
