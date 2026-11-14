from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ContactForm, QuoteForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('website'):  # bots fill the hidden field, so skip saving
                enquiry = form.save(commit=False)
                enquiry.enquiry_type = 'general'
                enquiry.save()
            messages.success(request, "Thank you! Your message has been sent. We'll get back to you shortly.")
            return redirect('contact:contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})


@require_POST
def quote_request(request):
    form = QuoteForm(request.POST)
    if form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.enquiry_type = 'quote'
        enquiry.save()
        messages.success(request, "Thank you! We've received your request and will contact you shortly.")
    else:
        messages.error(request, 'Please check the form. Name and phone number are required.')
    return redirect(f"{reverse('core:home')}#quote")