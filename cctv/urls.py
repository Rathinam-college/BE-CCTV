from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CameraViewSet, NVRViewSet, BiometricViewSet, BarrierViewSet, 
    NetworkSwitchViewSet, ActivityLogViewSet,
    CameraRemarkViewSet, NVRRemarkViewSet, BiometricRemarkViewSet, SwitchRemarkViewSet,
    GlobalSiteConfigViewSet, MasterLocationViewSet,
    RackViewSet, RackRemarkViewSet, OccupationViewSet
)

router = DefaultRouter()
router.register(r'nvrs', NVRViewSet, basename='nvr')
router.register(r'biometrics', BiometricViewSet, basename='biometric')
router.register(r'barriers', BarrierViewSet, basename='barrier')
router.register(r'switches', NetworkSwitchViewSet, basename='switch')
router.register(r'racks', RackViewSet, basename='rack')
router.register(r'logs', ActivityLogViewSet, basename='activitylog')

# Master Location Routes
router.register(r'master_locations', MasterLocationViewSet, basename='master_location')
router.register(r'global-site-config', GlobalSiteConfigViewSet, basename='globalsiteconfig')
router.register(r'occupations', OccupationViewSet, basename='occupation')

router.register(r'', CameraViewSet, basename='camera')

urlpatterns = [
    path('', include(router.urls)),
]
