from datetime import date

from django import forms

from apps.tours.models import Package, Service
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'service', 'full_name', 'phone', 'email',
                  'travel_date', 'travelers', 'special_requests']
        labels = {
            'package': 'Package',
            'service': 'Or choose a service',
            'full_name': 'Full name',
            'phone': 'Phone number (WhatsApp if possible)',
            'email': 'Email (optional)',
            'travel_date': 'Preferred travel date',
            'travelers': 'Number of travelers',
            'special_requests': 'Special requests',
        }
        widgets = {
            'package': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'travelers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = Package.objects.filter(is_available=True).select_related('destination')
        self.fields['package'].empty_label = '— Choose a package —'
        self.fields['package'].label_from_instance = lambda p: f"{p.title} — KES {p.price:,.0f}"
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = '— No specific service —'
        self.fields['travel_date'].widget.attrs['min'] = date.today().isoformat()

    def clean_travel_date(self):
        d = self.cleaned_data['travel_date']
        if d < date.today():
            raise forms.ValidationError('Please choose a date that is today or later.')
        return d

    def clean_travelers(self):
        n = self.cleaned_data['travelers']
        if n < 1:
            raise forms.ValidationError('At least one traveler is required.')
        return n

    def clean(self):
        cleaned = super().clean()
        package, service = cleaned.get('package'), cleaned.get('service')
        if not package and not service:
            raise forms.ValidationError('Please choose a package or a service.')
        travelers = cleaned.get('travelers')
        if package and travelers and package.slots_available and travelers > package.slots_available:
            self.add_error('travelers', f'Only {package.slots_available} slots are available for this package.')
        return cleaned