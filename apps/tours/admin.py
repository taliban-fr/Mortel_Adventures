from django.contrib import admin
from django.utils.html import format_html

from .models import Destination, GalleryImage, Package, PackageImage, Service


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


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'caption', 'category', 'order', 'is_published')
    list_editable = ('category', 'order', 'is_published')
    list_filter = ('category', 'is_published')

    @admin.display(description='Photo')
    def thumb(self, obj):
        return format_html('<img src="{}" style="height:50px; border-radius:6px;">', obj.image.url)