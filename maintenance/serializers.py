from rest_framework import serializers

class DateCleanupMixin:
    def to_internal_value(self, data):
        if hasattr(data, 'copy'):
            data = data.copy()
        elif isinstance(data, dict):
            data = dict(data)
            
        for field_name, field in self.fields.items():
            if isinstance(field, (serializers.DateField, serializers.DateTimeField)):
                if field_name in data and data[field_name] in ['', 'null', 'None']:
                    data[field_name] = None
        return super().to_internal_value(data)
from .models import Ticket, Project, TicketRemark, ProjectDocument, TicketDocument, GeneralBillingInfo, GeneralBillingDocument, TicketBillingRecord, ProjectBillingRecord
from users.serializers import UserSerializer
from cctv.serializers import CameraSerializer
from .models import TicketCompletedImage



class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = '__all__'

    def validate_file(self, value):
        from .utils import compress_file
        return compress_file(value)

class TicketDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDocument
        fields = '__all__'

    def validate_file(self, value):
        from .utils import compress_file
        return compress_file(value)

class TicketCompletedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCompletedImage
        fields = '__all__'

    def validate_image(self, value):
        from .utils import compress_file
        return compress_file(value)

class ProjectBillingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBillingRecord
        fields = '__all__'

    def validate_file(self, value):
        from .utils import compress_file
        return compress_file(value)

class TicketBillingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBillingRecord
        fields = '__all__'

    def validate_file(self, value):
        from .utils import compress_file
        return compress_file(value)

class ProjectSerializer(DateCleanupMixin, serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    ticket_count = serializers.SerializerMethodField()
    documents = ProjectDocumentSerializer(many=True, read_only=True)
    billing_records = ProjectBillingRecordSerializer(many=True, read_only=True)

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

    def validate_image(self, value):
        from .utils import compress_file
        return compress_file(value)

class TicketSerializer(DateCleanupMixin, serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    documents = TicketDocumentSerializer(many=True, read_only=True)
    completed_images = TicketCompletedImageSerializer(many=True, read_only=True)
    billing_records = TicketBillingRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ticket
        fields = '__all__'

    def validate_serviceImage(self, value):
        from .utils import compress_file
        return compress_file(value)

    def validate_workImage(self, value):
        from .utils import compress_file
        return compress_file(value)

    def validate_createdImage(self, value):
        from .utils import compress_file
        return compress_file(value)

    def validate_inProgressImage(self, value):
        from .utils import compress_file
        return compress_file(value)

    def validate_completedImage(self, value):
        from .utils import compress_file
        return compress_file(value)

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
            response['assignedStaff'] = UserSerializer(instance.assignedStaff.all(), many=True).data
        
        # Include message history
        remarks = instance.message_history.all().order_by('-createdAt')
        response['message_history'] = TicketRemarkSerializer(remarks, many=True).data
        
        return response

class GeneralBillingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralBillingDocument
        fields = '__all__'

    def validate_file(self, value):
        from .utils import compress_file
        return compress_file(value)

class GeneralBillingInfoSerializer(DateCleanupMixin, serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    documents = GeneralBillingDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = GeneralBillingInfo
        fields = '__all__'
