from django.db import models
from django.conf import settings
from cctv.models import Camera

class MaintenanceStaff(models.Model):
    name = models.CharField(max_length=255, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]
    name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    # Billing & PO Details
    bill_number = models.CharField(max_length=255, blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=True, null=True)
    bill_document = models.FileField(upload_to='maintenance/projects/bills/', blank=True, null=True)
    po_document = models.FileField(upload_to='maintenance/projects/pos/', blank=True, null=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='maintenance/projects/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets', db_column='projectId')
    cameraId = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True, db_column='cameraId')
    raisedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='raised_tickets', db_column='raisedBy')
    assignedTo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', db_column='assignedTo')
    assignedStaff = models.ManyToManyField(MaintenanceStaff, blank=True, related_name='tickets')
    issueDescription = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    remarks = models.TextField(blank=True, null=True)
    
    # New separate fields
    operationDate = models.DateField(null=True, blank=True)
    # Location Intelligence
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True) # Legacy display field
    category = models.CharField(max_length=100, null=True, blank=True)
    actionTaken = models.TextField(null=True, blank=True)
    instructionBy = models.CharField(max_length=255, null=True, blank=True)
    receivedTime = models.CharField(max_length=20, null=True, blank=True)
    endTime = models.CharField(max_length=20, null=True, blank=True)
    totalTime = models.CharField(max_length=50, null=True, blank=True)

    serviceImage = models.ImageField(upload_to='maintenance/service_images/', blank=True, null=True)
    workImage = models.ImageField(upload_to='maintenance/work_images/', blank=True, null=True)
    workRemarks = models.TextField(blank=True, null=True)
    replacedParts = models.TextField(blank=True, null=True)
    nextServiceDate = models.DateTimeField(blank=True, null=True)
    
    # Billing & PO Details
    bill_number = models.CharField(max_length=255, blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=True, null=True)
    bill_document = models.FileField(upload_to='maintenance/tickets/bills/', blank=True, null=True)
    po_document = models.FileField(upload_to='maintenance/tickets/pos/', blank=True, null=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.status}"

from django.utils import timezone

class TicketRemark(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='message_history', on_delete=models.CASCADE)
    remark = models.TextField()
    device_status = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark for Ticket {self.ticket.id} on {self.date}"

class TicketDocument(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='maintenance/tickets/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
