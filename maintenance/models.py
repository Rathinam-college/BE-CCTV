from django.db import models
from django.conf import settings
from cctv.models import Camera



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
    instructionBy = models.CharField(max_length=255, null=True, blank=True)
    
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
    assignedStaff = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='tickets_assigned_as_staff')
    issueDescription = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    remarks = models.TextField(blank=True, null=True)
    
    # New separate fields
    operationDate = models.DateField(null=True, blank=True)
    # Location Intelligence
    divisionName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True) # Legacy display field
    category = models.CharField(max_length=100, null=True, blank=True)
    ticketDevice = models.CharField(max_length=100, null=True, blank=True)
    actionTaken = models.TextField(null=True, blank=True)
    instructionBy = models.CharField(max_length=255, null=True, blank=True)
    receivedDate = models.DateField(null=True, blank=True)
    receivedTime = models.CharField(max_length=20, null=True, blank=True)
    endTime = models.CharField(max_length=20, null=True, blank=True)
    totalTime = models.CharField(max_length=50, null=True, blank=True)

    serviceImage = models.ImageField(upload_to='maintenance/service_images/', blank=True, null=True)
    workImage = models.ImageField(upload_to='maintenance/work_images/', blank=True, null=True)
    
    createdImage = models.ImageField(upload_to='maintenance/created_images/', blank=True, null=True)
    createdVideo = models.FileField(upload_to='maintenance/created_videos/', blank=True, null=True)
    createdDate = models.DateField(null=True, blank=True)
    createdTime = models.CharField(max_length=20, null=True, blank=True)
    
    inProgressImage = models.ImageField(upload_to='maintenance/inprogress_images/', blank=True, null=True)
    inProgressVideo = models.FileField(upload_to='maintenance/inprogress_videos/', blank=True, null=True)
    inProgressDate = models.DateField(null=True, blank=True)
    inProgressTime = models.CharField(max_length=20, null=True, blank=True)
    
    completedImage = models.ImageField(upload_to='maintenance/completed_images/', blank=True, null=True)
    completedVideo = models.FileField(upload_to='maintenance/completed_videos/', blank=True, null=True)
    completedDate = models.DateField(null=True, blank=True)
    completedTime = models.CharField(max_length=20, null=True, blank=True)
    
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

    def save(self, *args, **kwargs):
        from django.utils import timezone
        today = timezone.now().date()
        
        if not self.operationDate:
            self.operationDate = today
            
        if not self.receivedDate:
            self.receivedDate = today
            
        if not self.createdDate:
            self.createdDate = today
            
        if self.status == 'In Progress' and not self.inProgressDate:
            self.inProgressDate = today
            
        if self.status == 'Completed':
            if not self.inProgressDate:
                self.inProgressDate = self.createdDate or today
            if not self.completedDate:
                self.completedDate = today
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.id} - {self.status}"

    class Meta:
        ordering = ['-createdAt', '-id']

from django.utils import timezone

class TicketRemark(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='message_history', on_delete=models.CASCADE)
    remark = models.TextField()
    image = models.ImageField(upload_to='maintenance/ticket_remarks/', blank=True, null=True)
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

class TicketCompletedImage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='completed_images')
    image = models.ImageField(upload_to='maintenance/completed_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Completed Image for Ticket {self.ticket.id}"

class GeneralBillingInfo(models.Model):
    work = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    area_budget = models.CharField(max_length=255, blank=True, null=True)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    
    bill_no = models.CharField(max_length=255, blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    bill_status = models.CharField(max_length=255, blank=True, null=True)
    
    pr_no = models.CharField(max_length=255, blank=True, null=True)
    po_no = models.CharField(max_length=255, blank=True, null=True)
    po_value = models.CharField(max_length=255, blank=True, null=True)
    
    opex_no = models.CharField(max_length=255, blank=True, null=True)
    opex_value = models.CharField(max_length=255, blank=True, null=True)
    opex_status = models.CharField(max_length=255, blank=True, null=True)
    
    payment_status = models.CharField(max_length=255, blank=True, null=True)
    handover_to = models.CharField(max_length=255, blank=True, null=True)

    bill_document = models.FileField(upload_to='maintenance/general/bills/', blank=True, null=True)
    po_document = models.FileField(upload_to='maintenance/general/pos/', blank=True, null=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from django.utils import timezone
        if not self.bill_date:
            self.bill_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.work

class GeneralBillingDocument(models.Model):
    general_billing = models.ForeignKey(GeneralBillingInfo, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='maintenance/general/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectBillingRecord(models.Model):
    RECORD_TYPES = [('Bill', 'Bill'), ('PO', 'PO')]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='billing_records')
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    number = models.CharField(max_length=255)
    amount = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='maintenance/projects/billing_records/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record_type} - {self.number}"

class TicketBillingRecord(models.Model):
    RECORD_TYPES = [('Bill', 'Bill'), ('PO', 'PO')]
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='billing_records')
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    number = models.CharField(max_length=255)
    amount = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='maintenance/tickets/billing_records/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record_type} - {self.number}"
