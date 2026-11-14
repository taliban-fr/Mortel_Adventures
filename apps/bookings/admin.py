from django.contrib import admin

from apps.payments.models import Payment
from .models import Booking


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ('amount', 'method', 'transaction_code', 'status', 'paid_at', 'notes')


@admin.action(description='Mark selected as confirmed')
def mark_confirmed(modeladmin, request, queryset):
    for booking in queryset:
        booking.status = 'confirmed'
        booking.save()


@admin.action(description='Mark selected as cancelled')
def mark_cancelled(modeladmin, request, queryset):
    queryset.update(status='cancelled')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference', 'full_name', 'phone', 'package', 'service', 'travel_date',
                    'travelers', 'total_price', 'amount_paid', 'payment_status', 'status')
    list_filter = ('status', 'travel_date', 'package')
    list_editable = ('status',)
    search_fields = ('reference', 'full_name', 'phone', 'email')
    date_hierarchy = 'travel_date'
    readonly_fields = ('reference', 'created_at', 'updated_at', 'amount_paid', 'balance', 'payment_status')
    inlines = [PaymentInline]
    actions = [mark_confirmed, mark_cancelled]