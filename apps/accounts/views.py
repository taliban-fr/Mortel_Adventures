from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from apps.bookings.models import Booking
from .forms import ProfileForm, RegisterForm, StyledPasswordChangeForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('accounts:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    bookings = request.user.bookings.select_related('package', 'service')
    context = {
        'bookings': bookings,
        'total': bookings.count(),
        'pending': bookings.filter(status='pending').count(),
        'confirmed': bookings.filter(status='confirmed').count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def booking_detail(request, reference):
    booking = get_object_or_404(Booking, reference=reference, user=request.user)
    return render(request, 'accounts/booking_detail.html', {'booking': booking})


@login_required
@require_POST
def cancel_booking(request, reference):
    booking = get_object_or_404(Booking, reference=reference, user=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Your booking request has been cancelled.')
    else:
        messages.error(request, 'Only pending requests can be cancelled online. Please call us to change this booking.')
    return redirect('accounts:booking_detail', reference=booking.reference)


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            profile_obj.phone = form.cleaned_data['phone']
            profile_obj.save()
            messages.success(request, 'Your details have been updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


class PasswordChange(SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = StyledPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Your password has been updated.'