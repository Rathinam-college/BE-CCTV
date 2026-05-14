from rest_framework import serializers
from .models import Route, SiteVisit
from users.serializers import UserSerializer

class SiteVisitSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = SiteVisit
        fields = ['_id', 'siteName', 'status', 'remarks']

class RouteSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    sitesToVisit = SiteVisitSerializer(many=True)

    class Meta:
        model = Route
        fields = ['_id', 'date', 'technician', 'sitesToVisit', 'status', 'createdAt', 'updatedAt']

    def create(self, validated_data):
        sites_data = validated_data.pop('sitesToVisit', [])
        route = Route.objects.create(**validated_data)
        for site_data in sites_data:
            SiteVisit.objects.create(route=route, **site_data)
        return route

    def update(self, instance, validated_data):
        sites_data = validated_data.pop('sitesToVisit', None)
        instance.date = validated_data.get('date', instance.date)
        instance.technician = validated_data.get('technician', instance.technician)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if sites_data is not None:
            instance.sitesToVisit.all().delete()
            for site_data in sites_data:
                SiteVisit.objects.create(route=instance, **site_data)

        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.technician:
            response['technician'] = UserSerializer(instance.technician).data
        return response
