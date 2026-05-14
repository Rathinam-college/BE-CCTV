from django.db import models
from django.conf import settings

class Route(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    date = models.DateTimeField()
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='technician')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class SiteVisit(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='sitesToVisit')
    siteName = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
