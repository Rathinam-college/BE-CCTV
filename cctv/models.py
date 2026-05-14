from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Camera(models.Model):
    STATUS_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Maintenance', 'Maintenance'),
    ]
    CAMPUS_ZONE_CHOICES = [
        ('INSIDE', 'Inside Campus'),
        ('OUTSIDE', 'Outside Campus'),
    ]

    cameraId = models.CharField(max_length=100, blank=True, null=True, unique=True)
    name = models.CharField(max_length=255)
    siteName = models.CharField(max_length=255)
    ipAddress = models.CharField(max_length=45, blank=True, null=True)
    dvrNvrDetails = models.TextField(blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Online')
    installationDate = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # Location Intelligence
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    campusZone = models.CharField(max_length=10, choices=CAMPUS_ZONE_CHOICES, default='INSIDE')
    
    # Additional Details
    deviceType = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    serialNumber = models.CharField(max_length=255, blank=True, null=True)
    macAddress = models.CharField(max_length=255, blank=True, null=True)
    index = models.CharField(max_length=100, blank=True, null=True)
    subnetMask = models.CharField(max_length=255, blank=True, null=True)
    gateway = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.cameraId})"

class NVR(models.Model):
    STATUS_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Maintenance', 'Maintenance'),
    ]
    CAMPUS_ZONE_CHOICES = [
        ('INSIDE', 'Inside Campus'),
        ('OUTSIDE', 'Outside Campus'),
    ]

    sNo = models.CharField(max_length=50, blank=True, null=True)
    ipAddress = models.CharField(max_length=45, blank=True, null=True)
    nvrName = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    hardDisk = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=50, blank=True, null=True)
    serialNumber = models.CharField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Online')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # Location Intelligence
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    campusZone = models.CharField(max_length=10, choices=CAMPUS_ZONE_CHOICES, default='INSIDE')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nvrName

class Biometric(models.Model):
    STATUS_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Maintenance', 'Maintenance'),
    ]
    CAMPUS_ZONE_CHOICES = [
        ('INSIDE', 'Inside Campus'),
        ('OUTSIDE', 'Outside Campus'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=100, default='Fingerprint')
    brand = models.CharField(max_length=100, blank=True, null=True)
    ipAddress = models.CharField(max_length=45, blank=True, null=True)
    serverIp = models.CharField(max_length=45, blank=True, null=True)
    serialNumber = models.CharField(max_length=100, blank=True, null=True, unique=True)
    syncStatus = models.CharField(max_length=100, default='In Sync')
    lastCheckIn = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Online')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # Location Intelligence
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    campusZone = models.CharField(max_length=10, choices=CAMPUS_ZONE_CHOICES, default='INSIDE')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Barrier(models.Model):
    STATUS_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Maintenance', 'Maintenance'),
    ]
    CAMPUS_ZONE_CHOICES = [
        ('INSIDE', 'Inside Campus'),
        ('OUTSIDE', 'Outside Campus'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=100, default='Boom Barrier')
    gateStatus = models.CharField(max_length=50, default='Closed')
    controller = models.CharField(max_length=100, blank=True, null=True)
    lastUsed = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Online')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # Location Intelligence
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    campusZone = models.CharField(max_length=10, choices=CAMPUS_ZONE_CHOICES, default='INSIDE')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class NetworkSwitch(models.Model):
    STATUS_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Maintenance', 'Maintenance'),
    ]
    CAMPUS_ZONE_CHOICES = [
        ('INSIDE', 'Inside Campus'),
        ('OUTSIDE', 'Outside Campus'),
    ]

    name = models.CharField(max_length=255)
    ipAddress = models.CharField(max_length=45, blank=True, null=True)
    location = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    portCount = models.CharField(max_length=50, blank=True, null=True)
    serialNumber = models.CharField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Online')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # Location Intelligence
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    campusZone = models.CharField(max_length=10, choices=CAMPUS_ZONE_CHOICES, default='INSIDE')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    page = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    ipAddress = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.page}"

class CameraRemark(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='message_history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remark = models.TextField()
    device_status = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class NVRRemark(models.Model):
    nvr = models.ForeignKey(NVR, on_delete=models.CASCADE, related_name='message_history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remark = models.TextField()
    device_status = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class BiometricRemark(models.Model):
    biometric = models.ForeignKey(Biometric, on_delete=models.CASCADE, related_name='message_history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remark = models.TextField()
    device_status = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class SwitchRemark(models.Model):
    switch = models.ForeignKey(NetworkSwitch, on_delete=models.CASCADE, related_name='message_history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remark = models.TextField()
    device_status = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class CameraRelocation(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='relocations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_location = models.CharField(max_length=255)
    new_location = models.CharField(max_length=255)
    old_ip = models.CharField(max_length=45, blank=True, null=True)
    new_ip = models.CharField(max_length=45, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class NVRRelocation(models.Model):
    nvr = models.ForeignKey(NVR, on_delete=models.CASCADE, related_name='relocations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_location = models.CharField(max_length=255)
    new_location = models.CharField(max_length=255)
    old_ip = models.CharField(max_length=45, blank=True, null=True)
    new_ip = models.CharField(max_length=45, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class BiometricRelocation(models.Model):
    biometric = models.ForeignKey(Biometric, on_delete=models.CASCADE, related_name='relocations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_location = models.CharField(max_length=255)
    new_location = models.CharField(max_length=255)
    old_ip = models.CharField(max_length=45, blank=True, null=True)
    new_ip = models.CharField(max_length=45, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class SwitchRelocation(models.Model):
    switch = models.ForeignKey(NetworkSwitch, on_delete=models.CASCADE, related_name='relocations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_location = models.CharField(max_length=255)
    new_location = models.CharField(max_length=255)
    old_ip = models.CharField(max_length=45, blank=True, null=True)
    new_ip = models.CharField(max_length=45, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class GlobalSiteConfig(models.Model):
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    assignedTo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='global_managed_sites')
    updatedAt = models.DateTimeField(auto_now=True)

class MasterLocation(models.Model):
    collegeName = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    assignedTo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_locations')
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collegeName', 'block', 'floor', 'room')

    def __str__(self):
        return f"{self.collegeName} | {self.block} | {self.floor} | {self.room} ({self.brand})"
