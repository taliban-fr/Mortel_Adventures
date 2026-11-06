from django.contrib import admin
from .models import Destination, Service, Package, PackageImage

# Register your models here.

class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'is_featured')
    list_filter = ('is_featured',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'slots_available', 'is_available', 'is_featured')
    list_filter = ('is_available', 'is_featured', 'destination')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PackageImageInline]