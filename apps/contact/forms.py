from django import forms
from .models import Enquiry


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'destination', 'travel_date', 'travelers', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name', 'aria-label': 'Full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number', 'aria-label': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)', 'aria-label': 'Email'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where to?', 'list': 'dest-list', 'autocomplete': 'off', 'aria-label': 'Destination'}),
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'aria-label': 'Travel date'}),
            'travelers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'aria-label': 'Number of travelers'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us more: budget, interests, special requests', 'aria-label': 'Message'}),
        }

class ContactForm(forms.ModelForm):
    # Hidden trap for spam bots: real visitors never see or fill it
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}))

    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'message']
        labels = {
            'name': 'Full name',
            'phone': 'Phone number',
            'email': 'Email (optional)',
            'message': 'How can we help?',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].required = True