from django.db.models import Count, Min, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Destination, GalleryImage, Package, Service

# Create your views here.

def services(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'tours/services.html', {'services': services})


def destinations(request):
    live = Q(packages__is_available=True)
    destinations = Destination.objects.annotate(
        from_price=Min('packages__price', filter=live),
        package_count=Count('packages', filter=live),
    )
    return render(request, 'tours/destinations.html', {'destinations': destinations})


def packages(request):
    selected = request.GET.get('destination', '')
    sort = request.GET.get('sort', '')

    qs = Package.objects.filter(is_available=True).select_related('destination')
    if selected:
        qs = qs.filter(destination__slug=selected)

    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    else:
        qs = qs.order_by('-is_featured', 'title')

    return render(request, 'tours/packages.html', {
        'packages': qs,
        'destinations': Destination.objects.all(),
        'selected': selected,
        'sort': sort,
    })


def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug, is_available=True)
    related = (Package.objects.filter(destination=package.destination, is_available=True)
               .exclude(pk=package.pk)[:3])
    return render(request, 'tours/package_detail.html', {'package': package, 'related': related})


def gallery(request):
    images = GalleryImage.objects.filter(is_published=True)
    used = set(images.values_list('category', flat=True))
    categories = [(value, label) for value, label in GalleryImage.CATEGORY_CHOICES if value in used]
    return render(request, 'tours/gallery.html', {'images': images, 'categories': categories})