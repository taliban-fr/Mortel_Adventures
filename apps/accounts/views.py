from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.bookings.models import Booking
from apps.payments.models import Payment
from .forms import EmailLoginForm, ProfileForm, RegisterForm, StyledPasswordChangeForm
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
    today = timezone.localdate()
    bookings = request.user.bookings.select_related('package__destination', 'service')
    upcoming = bookings.filter(travel_date__gte=today, status__in=['pending', 'confirmed']).order_by('travel_date')

    activity = []
    for b in bookings[:10]:
        url = reverse('accounts:booking_detail', args=[b.reference])
        activity.append({'icon': 'bi-calendar-plus', 'tone': 'blue', 'title': 'Booking requested',
                         'detail': b.display_title, 'when': b.created_at, 'url': url})
        if b.status == 'confirmed':
            activity.append({'icon': 'bi-check-circle-fill', 'tone': 'green', 'title': 'Booking confirmed',
                             'detail': b.display_title, 'when': b.confirmed_at or b.updated_at, 'url': url})

    payments = (Payment.objects.filter(booking__user=request.user, status='completed')
                .select_related('booking__package', 'booking__service')[:5])
    for p in payments:
        activity.append({'icon': 'bi-cash-coin', 'tone': 'orange',
                         'title': f'Payment received · KES {p.amount:,.0f}',
                         'detail': p.booking.display_title, 'when': p.paid_at,
                         'url': reverse('accounts:booking_detail', args=[p.booking.reference])})

    activity.sort(key=lambda a: a['when'], reverse=True)

    return render(request, 'accounts/dashboard.html', {
        'next_booking': upcoming.first(),
        'total': bookings.count(),
        'upcoming_count': upcoming.count(),
        'activity': activity[:5],
    })


@login_required
def my_bookings(request):
    today = timezone.localdate()
    bookings = request.user.bookings.select_related('package__destination', 'service')
    upcoming = bookings.filter(travel_date__gte=today, status__in=['pending', 'confirmed']).order_by('travel_date')
    past = bookings.filter(Q(travel_date__lt=today) | Q(status__in=['completed', 'cancelled'])).order_by('-travel_date')

    tab = 'past' if request.GET.get('tab') == 'past' else 'upcoming'
    return render(request, 'accounts/bookings.html', {
        'tab': tab,
        'upcoming_count': upcoming.count(),
        'past_count': past.count(),
        'bookings': past if tab == 'past' else upcoming,
    })

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
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            profile_obj.phone = form.cleaned_data['phone']
            photo = form.cleaned_data.get('photo')
            if photo:
                profile_obj.photo = photo
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

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)  # session ends when the browser closes
        return response