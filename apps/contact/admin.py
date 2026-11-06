from django.contrib import admin
from .models import Enquiry

# Register your models here.
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'enquiry_type', 'destination', 'travel_date', 'created_at', 'is_read')
    list_filter = ('enquiry_type', 'is_read')
    list_editable = ('is_read',)
    search_fields = ('name', 'phone', 'email', 'destination')
    readonly_fields = ('created_at',)