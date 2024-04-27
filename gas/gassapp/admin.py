from django.contrib import admin
from gassapp.models import ServiceRequest

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['customer', 'request_type', 'status', 'submitted_at', 'resolved_at']
    list_filter = ['status', 'submitted_at', 'resolved_at']
    search_fields = ['customer__username', 'request_type', 'details']

admin.site.register(ServiceRequest, ServiceRequestAdmin)
