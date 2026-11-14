import html as htmllib
import logging
import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.bookings.models import Booking
from apps.contact.models import Enquiry
from .context_processors import site_info

logger = logging.getLogger(__name__)


def send_email(subject, to, template, context, reply_to=None):
    """Render an HTML email (with a plain-text copy) and send it once the database save has committed.
    A failed send is logged and never breaks the page."""
    recipients = [address for address in to if address]
    if not recipients:
        return

    context = {**context, 'SITE': site_info(None)['SITE'], 'SITE_URL': settings.SITE_URL}
    html_body = render_to_string(template, context)
    text_body = htmllib.unescape(strip_tags(html_body))
    text_body = re.sub(r'\n\s*\n+', '\n\n', text_body).strip()

    def _send():
        try:
            message = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL,
                                             recipients, reply_to=reply_to)
            message.attach_alternative(html_body, 'text/html')
            message.send()
        except Exception:
            logger.exception('Could not send email: %s', subject)

    transaction.on_commit(_send)


@receiver(pre_save, sender=Booking)
def remember_old_status(sender, instance, **kwargs):
    if instance.pk:
        instance._old_status = Booking.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
    else:
        instance._old_status = None


@receiver(post_save, sender=Booking)
def booking_emails(sender, instance, created, **kwargs):
    if created:
        send_email(f'New booking {instance.reference}: {instance.full_name}',
                   settings.NOTIFY_EMAILS, 'emails/admin_new_booking.html',
                   {'booking': instance}, reply_to=[instance.email] if instance.email else None)
        send_email(f'We received your booking {instance.reference}',
                   [instance.email], 'emails/booking_received.html', {'booking': instance})
    elif instance.status == 'confirmed' and getattr(instance, '_old_status', None) != 'confirmed':
        send_email(f'Your booking {instance.reference} is confirmed',
                   [instance.email], 'emails/booking_confirmed.html', {'booking': instance})


@receiver(post_save, sender=Enquiry)
def enquiry_email(sender, instance, created, **kwargs):
    if created:
        kind = instance.get_enquiry_type_display().lower()
        send_email(f'New {kind} from {instance.name}',
                   settings.NOTIFY_EMAILS, 'emails/admin_new_enquiry.html',
                   {'enquiry': instance}, reply_to=[instance.email] if instance.email else None)