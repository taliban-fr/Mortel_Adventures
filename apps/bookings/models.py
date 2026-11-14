import secrets
import string
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum


def make_reference():
    alphabet = string.ascii_uppercase + string.digits
    return 'MA-' + ''.join(secrets.choice(alphabet) for _ in range(6))


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    reference = models.CharField(max_length=12, unique=True, editable=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='bookings')
    package = models.ForeignKey('tours.Package', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='bookings')
    service = models.ForeignKey('tours.Service', null=True, blank=True, on_delete=models.SET_NULL)

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    travel_date = models.DateField()
    travelers = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                      help_text='Estimated total (KES). You can adjust it after agreeing a final price.')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference:
            ref = make_reference()
            while Booking.objects.filter(reference=ref).exists():
                ref = make_reference()
            self.reference = ref
        super().save(*args, **kwargs)

    @property
    def amount_paid(self):
        total = self.payments.filter(status='completed').aggregate(total=Sum('amount'))['total']
        return total or Decimal('0')

    @property
    def balance(self):
        if self.total_price is None:
            return None
        return self.total_price - self.amount_paid

    @property
    def payment_status(self):
        paid = self.amount_paid
        if paid <= 0:
            return 'unpaid'
        if self.total_price and paid >= self.total_price:
            return 'paid'
        return 'partial'

    def __str__(self):
        return f"{self.reference} · {self.full_name}"