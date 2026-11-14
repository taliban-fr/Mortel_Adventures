from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking


# Create your views here.
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            if request.user.is_authenticated:
                b.user = request.user
            if b.package:
                b.total_price = b.package.price * b.travelers
            b.save()
            return redirect('bookings:success', reference=b.reference)
    else:
        initial = {}
        for key in ('package', 'service'):
            value = request.GET.get(key)
            if value and value.isdigit():
                initial[key] = value
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name() or request.user.get_username()
            initial['email'] = request.user.email
        form = BookingForm(initial=initial)

    return render(request, 'bookings/booking.html', {'form': form})


def booking_success(request, reference):
    b = get_object_or_404(Booking, reference=reference)
    return render(request, 'bookings/success.html', {'booking': b})