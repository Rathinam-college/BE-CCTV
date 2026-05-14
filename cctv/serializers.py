from rest_framework import serializers
from .models import (
    Camera, NVR, Biometric, Barrier, NetworkSwitch, ActivityLog, 
    CameraRemark, NVRRemark, BiometricRemark, SwitchRemark,
    CameraRelocation, NVRRelocation, BiometricRelocation, SwitchRelocation,
    GlobalSiteConfig, MasterLocation
)

class CameraRelocationSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = CameraRelocation
        fields = ['id', 'old_location', 'new_location', 'old_ip', 'new_ip', 'remark', 'userName', 'createdAt']

class CameraRemarkSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = CameraRemark
        fields = ['id', 'remark', 'device_status', 'date', 'time', 'userName', 'createdAt']

class CameraSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    message_history = CameraRemarkSerializer(many=True, read_only=True)
    relocations = CameraRelocationSerializer(many=True, read_only=True)
    class Meta:
        model = Camera
        fields = '__all__'

class NVRRelocationSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = NVRRelocation
        fields = ['id', 'old_location', 'new_location', 'old_ip', 'new_ip', 'remark', 'userName', 'createdAt']

class NVRRemarkSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = NVRRemark
        fields = ['id', 'remark', 'device_status', 'date', 'time', 'userName', 'createdAt']

class NVRSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    message_history = NVRRemarkSerializer(many=True, read_only=True)
    relocations = NVRRelocationSerializer(many=True, read_only=True)
    class Meta:
        model = NVR
        fields = '__all__'

class BiometricRelocationSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = BiometricRelocation
        fields = ['id', 'old_location', 'new_location', 'old_ip', 'new_ip', 'remark', 'userName', 'createdAt']

class BiometricRemarkSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = BiometricRemark
        fields = ['id', 'remark', 'device_status', 'date', 'time', 'userName', 'createdAt']

class BiometricSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    message_history = BiometricRemarkSerializer(many=True, read_only=True)
    relocations = BiometricRelocationSerializer(many=True, read_only=True)
    class Meta:
        model = Biometric
        fields = '__all__'

class BarrierSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Barrier
        fields = '__all__'

class SwitchRelocationSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = SwitchRelocation
        fields = ['id', 'old_location', 'new_location', 'old_ip', 'new_ip', 'remark', 'userName', 'createdAt']

class SwitchRemarkSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = SwitchRemark
        fields = ['id', 'remark', 'device_status', 'date', 'time', 'userName', 'createdAt']

class NetworkSwitchSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    message_history = SwitchRemarkSerializer(many=True, read_only=True)
    relocations = SwitchRelocationSerializer(many=True, read_only=True)
    class Meta:
        model = NetworkSwitch
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    userEmail = serializers.EmailField(source='user.email', read_only=True)
    userName = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = ActivityLog
        fields = '__all__'

class GlobalSiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSiteConfig
        fields = '__all__'

    def to_representation(self, instance):
        from users.serializers import UserSerializer
        response = super().to_representation(instance)
        if instance.assignedTo:
            response['assignedTo'] = UserSerializer(instance.assignedTo).data
        return response

class MasterLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterLocation
        fields = '__all__'

    def to_representation(self, instance):
        from users.serializers import UserSerializer
        response = super().to_representation(instance)
        if instance.assignedTo:
            response['assignedTo'] = UserSerializer(instance.assignedTo).data
        return response
