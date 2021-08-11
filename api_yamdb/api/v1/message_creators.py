from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_code(data, code):
    user_email = data['email']
    username = data['username']
    send_mail(
        'Confirmation code for YamDb',
        f'Deer {username}, you confirmation code: {code}',
        settings.EMAIL_HOST_USER,
        user_email,
        fail_silently=False,
    )
