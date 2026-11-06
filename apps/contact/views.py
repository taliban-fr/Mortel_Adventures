from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import QuoteForm


def contact(request):
    return HttpResponse("Contact")


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