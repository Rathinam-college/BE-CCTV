from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'role', 'branch', 'permissions', 'is_active', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims
        data['_id'] = self.user.id
        data['name'] = self.user.name
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['branch'] = self.user.branch
        data['permissions'] = self.user.permissions
        # Rename access token to token for frontend compatibility
        data['token'] = data.pop('access')
        return data
