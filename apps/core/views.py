from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Min
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.contact.forms import QuoteForm
from apps.tours.models import Destination, Package, Service
from .models import FAQ, Subscriber, Testimonial


# Create your views here.
def home(request):
    context = {
        'all_destinations': Destination.objects.all(),
        'destinations': Destination.objects.filter(is_featured=True)
                        .annotate(from_price=Min('packages__price'))[:4],
        'packages': Package.objects.filter(is_featured=True, is_available=True)[:3],
        'services': Service.objects.filter(is_active=True)[:6],
        'testimonials': Testimonial.objects.filter(is_published=True)[:6],
        'faqs': FAQ.objects.filter(is_published=True),
        'quote_form': QuoteForm(),
    }
    return render(request, 'core/home.html', context)


@require_POST
def subscribe(request):
    email = request.POST.get('email', '').strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Please enter a valid email address.')
    else:
        _, created = Subscriber.objects.get_or_create(email=email)
        messages.success(request, 'Thanks for subscribing!' if created else "You're already subscribed.")
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))