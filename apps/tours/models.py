from django.db import models



class Destination(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    duration_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per person (KES)')
    slots_available = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='packages/')

    def __str__(self):
        return self.title


class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.package.title} photo"

