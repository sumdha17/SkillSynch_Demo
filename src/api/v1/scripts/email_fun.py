from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.core.cache import cache

"""
    Sends a password reset email with a unique token.
    Args:
        email: Recipient's email address.
        message: Custom message to include in the email.
        subject: Email subject line.
        user: The user requesting the password reset.

    Returns:
        str: The generated reset token.
    """

def send_mail_to_reset_password(email,message, subject, user):
    token = str(uuid.uuid4())
    reset_link = f"http://127.0.0.1:8000/v1/reset-password/{token}/"
    cache.set(token, user.id, timeout=3600)        # Store token for 1 hour
    message =  f"{message} {reset_link}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list, user)
    return token