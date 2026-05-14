from rest_framework import serializers
from .models import Ticket, Project, TicketRemark, MaintenanceStaff
from users.serializers import UserSerializer
from cctv.serializers import CameraSerializer

class MaintenanceStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceStaff
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    ticket_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_ticket_count(self, obj):
        return obj.tickets.count()

class TicketRemarkSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.name')
    class Meta:
        model = TicketRemark
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Ticket
        fields = '__all__'

    def validate_serviceImage(self, value):
        if value:
            # 2MB in bytes
            max_size = 2 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError("Image size must be less than 2MB")
        return value

    def validate_workImage(self, value):
        if value:
            max_size = 2 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError("Image size must be less than 2MB")
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.projectId:
            response['project'] = ProjectSerializer(instance.projectId).data
        if instance.cameraId:
            response['camera'] = CameraSerializer(instance.cameraId).data
        if instance.raisedBy:
            response['raisedBy'] = UserSerializer(instance.raisedBy).data
        if instance.assignedTo:
            response['assignedTo'] = UserSerializer(instance.assignedTo).data
        if instance.assignedStaff:
            response['assignedStaff'] = MaintenanceStaffSerializer(instance.assignedStaff.all(), many=True).data
        
        # Include message history
        remarks = instance.message_history.all().order_by('-createdAt')
        response['message_history'] = TicketRemarkSerializer(remarks, many=True).data
        
        return response
