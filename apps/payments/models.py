from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Payment(models.Model):
    METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank transfer'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))],
                                 help_text='Amount in KES')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='mpesa')
    transaction_code = models.CharField(max_length=50, blank=True, help_text='e.g. the M-Pesa confirmation code')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')
    paid_at = models.DateTimeField(help_text='When the payment was received')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-paid_at']
        constraints = [
            models.UniqueConstraint(
                fields=['transaction_code'],
                condition=~Q(transaction_code=''),
                name='unique_nonblank_transaction_code',
            ),
        ]

    def save(self, *args, **kwargs):
        self.transaction_code = self.transaction_code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking.reference} · KES {self.amount:,.0f}"