from django.contrib import admin
from .models import (
    Camera, NVR, Biometric, Barrier, NetworkSwitch, ActivityLog,
    GlobalSiteConfig, Rack, Division, Brand,
    CameraRemark, NVRRemark, BiometricRemark, SwitchRemark,
    CameraRelocation, NVRRelocation, BiometricRelocation, SwitchRelocation,
    Block, Floor, Room, RackRemark, RackRelocation
)

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('cameraId', 'name', 'siteName', 'ipAddress', 'status', 'brand', 'model', 'divisionName')
    list_filter = ('status', 'brand', 'divisionName', 'campusZone')
    search_fields = ('cameraId', 'name', 'ipAddress', 'serialNumber', 'macAddress')

@admin.register(NVR)
class NVRAdmin(admin.ModelAdmin):
    list_display = ('nvrName', 'location', 'ipAddress', 'brand', 'model', 'status', 'channel')
    list_filter = ('status', 'brand', 'channel')
    search_fields = ('nvrName', 'ipAddress', 'serialNumber', 'macAddress')

@admin.register(Biometric)
class BiometricAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'ipAddress', 'status', 'brand', 'model', 'serialNumber')
    list_filter = ('status', 'brand', 'type')
    search_fields = ('name', 'ipAddress', 'serialNumber', 'hardwareSerial', 'macAddress')

@admin.register(Barrier)
class BarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'gateStatus', 'controller', 'status')
    list_filter = ('status', 'type', 'campusZone')
    search_fields = ('name', 'controller')

@admin.register(NetworkSwitch)
class NetworkSwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'ipAddress', 'location', 'brand', 'model', 'status', 'portCount')
    list_filter = ('status', 'brand')
    search_fields = ('name', 'ipAddress', 'serialNumber')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'page', 'details', 'timestamp')
    list_filter = ('action', 'page', 'timestamp')
    search_fields = ('user__email', 'details')

@admin.register(GlobalSiteConfig)
class GlobalSiteConfigAdmin(admin.ModelAdmin):
    list_display = ('divisionName', 'block', 'floor', 'room', 'brand', 'assignedTo')
    search_fields = ('divisionName',)

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'brand', 'model', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'location')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'createdAt')
    search_fields = ('name',)

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'block', 'createdAt')
    list_filter = ('block',)
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'block', 'floor', 'createdAt')
    list_filter = ('block', 'floor')
    search_fields = ('name',)

admin.site.register(Division)
admin.site.register(Brand)
admin.site.register(CameraRemark)
admin.site.register(NVRRemark)
admin.site.register(BiometricRemark)
admin.site.register(SwitchRemark)
admin.site.register(CameraRelocation)
admin.site.register(NVRRelocation)
admin.site.register(BiometricRelocation)
admin.site.register(SwitchRelocation)
admin.site.register(RackRemark)
admin.site.register(RackRelocation)
