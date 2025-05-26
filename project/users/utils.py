# users/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_email_to_profile(user, subject, message):
    # Try notify_email first, then profile email, then user email
    profile = getattr(user, 'profile', None)
    if profile:
        to_email = profile.notify_email or profile.email or user.email
    else:
        to_email = user.email
    
    if to_email:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # sender email from settings.py
            [to_email],                # recipient email list
            fail_silently=False,
        )
