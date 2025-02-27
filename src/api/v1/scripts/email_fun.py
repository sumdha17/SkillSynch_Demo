from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.core.cache import cache

def send_mail_to_reset_password(email,message, subject):
    token = str(uuid.uuid4())
    reset_link = f"http://127.0.0.1:8000/{token}/"
    message =  f"{message} {reset_link}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)
    return token