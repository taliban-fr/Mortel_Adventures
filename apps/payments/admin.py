from django.contrib import admin
from .models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'transaction_code', 'status', 'paid_at')
    list_filter = ('status', 'method', 'paid_at')
    search_fields = ('booking__reference', 'booking__full_name', 'transaction_code')
    autocomplete_fields = ('booking',)
    date_hierarchy = 'paid_at'