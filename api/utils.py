from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse


class Utils:
    def __init__(self, request):
        self.current_site = get_current_site(request)

    @staticmethod
    def validate_email_registration(subject, token, is_secure=False):
        send_mail(
            subject='Confirmación de correo electrónico',
            message='Si no logra ver este correo, contacte con algún administrador.',
            from_email=None,
            recipient_list=[subject],
            html_message=render_to_string('emails/confirm-registration.html', context={
                'link_to_confirm': 'http{secure}://{domain}{path}?token={token}'.format(
                    secure='s' if is_secure else '',
                    # domain=self.current_site.domain,
                    domain='localhost:4200',
                    # Cambiar path al de la vista
                    path=reverse('auth-email-verify'),
                    token=token
                )
            })
        )

    @staticmethod
    def reset_password(subject, uidb64, token, name, is_secure=False):
        print('{protocol}://{domain}/{path}?uidb64={uidb64}&token={token}'.format(
            protocol='https' if is_secure else 'http',
            domain='localhost:4200',
            path='new-password',
            uidb64=uidb64,
            token=token
        ))
        send_mail(
            subject='Reinicio de contraseña',
            message='Si no logra ver este correo, contacte con algún administrador.',
            from_email=None,
            recipient_list=[subject],
            html_message=render_to_string('emails/reset-password.html', context={
                'link_to_confirm': '{protocol}://{domain}/{path}?uidb64={uidb64}&token={token}'.format(
                    protocol='https' if is_secure else 'http',
                    # domain=self.current_site.domain,
                    domain='localhost:4200',
                    # Cambiar path al de la vista
                    path='new-password',
                    uidb64=uidb64,
                    token=token
                ),
                'name': f' {name}' if name else ""
            })
        )
