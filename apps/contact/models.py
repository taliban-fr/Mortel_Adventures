from django.db import models

# Create your models here.
from django.db import models


class Enquiry(models.Model):
    TYPES = [('quote', 'Quote request'), ('general', 'General enquiry')]

    enquiry_type = models.CharField(max_length=10, choices=TYPES, default='general')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    destination = models.CharField(max_length=100, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    travelers = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.name} · {self.get_enquiry_type_display()}"