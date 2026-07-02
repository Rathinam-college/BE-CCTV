from django.contrib import admin
from .models import (
    Project, ProjectDocument, Ticket, TicketRemark, TicketDocument, 
    TicketCompletedImage, GeneralBillingInfo, GeneralBillingDocument, 
    ProjectBillingRecord, TicketBillingRecord
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_name', 'status', 'po_number', 'createdAt')
    search_fields = ('name', 'po_number', 'client_name')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'projectId', 'cameraId', 'issueDescription', 'status', 'assignedTo', 'createdAt')
    list_filter = ('status', 'createdAt')
    search_fields = ('id', 'issueDescription')

admin.site.register(ProjectDocument)
admin.site.register(TicketRemark)
admin.site.register(TicketDocument)
admin.site.register(TicketCompletedImage)
admin.site.register(GeneralBillingInfo)
admin.site.register(GeneralBillingDocument)
admin.site.register(ProjectBillingRecord)
admin.site.register(TicketBillingRecord)
