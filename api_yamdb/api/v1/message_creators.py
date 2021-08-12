from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_code(username, user_email, code):
    send_mail(
        'Confirmation code from YamDb',
        f'Dear {username}, you confirmation code: {code}',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
