from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse


class Utils:
    def __init__(self, request):
        self.current_site = get_current_site(request)

    def validate_email_registration(self, subject, token, is_secure=False):
        send_mail(
            subject='Confirmación de correo electrónico',
            message='Si no logra ver este correo, contacte con algún administrador.',
            from_email=None,
            recipient_list=[subject],
            html_message=render_to_string('emails/confirm-registration.html', context={
                'link_to_confirm': 'http{secure}://{domain}{path}?token={token}'.format(
                    secure='s' if is_secure else '',
                    domain=self.current_site.domain,
                    path=reverse('auth-email-verify'),
                    token=token
                )
            })
        )
