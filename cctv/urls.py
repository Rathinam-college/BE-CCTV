from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CameraViewSet, NVRViewSet, BiometricViewSet, BarrierViewSet, 
    NetworkSwitchViewSet, ActivityLogViewSet,
    CameraRemarkViewSet, NVRRemarkViewSet, BiometricRemarkViewSet, SwitchRemarkViewSet,
    GlobalSiteConfigViewSet,
    RackViewSet, RackRemarkViewSet, DivisionViewSet, BrandViewSet,
    DatabaseBackupView
)

router = DefaultRouter()
router.register(r'nvrs', NVRViewSet, basename='nvr')
router.register(r'biometrics', BiometricViewSet, basename='biometric')
router.register(r'barriers', BarrierViewSet, basename='barrier')
router.register(r'switches', NetworkSwitchViewSet, basename='switch')
router.register(r'racks', RackViewSet, basename='rack')
router.register(r'logs', ActivityLogViewSet, basename='activitylog')

from .views import LocationViewSet
router.register(r'locations', LocationViewSet, basename='location')

router.register(r'global-site-config', GlobalSiteConfigViewSet, basename='globalsiteconfig')
router.register(r'divisions', DivisionViewSet, basename='division')
router.register(r'brands', BrandViewSet, basename='brand')

router.register(r'', CameraViewSet, basename='camera')

urlpatterns = [
    path('', include(router.urls)),
]
