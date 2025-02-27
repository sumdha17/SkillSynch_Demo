from django.db.models.signals import post_save, post_delete
from user.models import CustomUser
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=CustomUser)
def send_email_to_user(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to The Organization"
        message = f"""Hello {instance.first_name} {instance.last_name},
        Your account has been Created successfully!"""
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
        
    
@receiver(post_delete, sender=CustomUser)
def send_email_on_deletion(sender, instance, **kwargs):
    subject = "Account Deleted"
    message = f"Hello {instance.first_name} {instance.last_name},\n\nYour account has been successfully deleted."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [instance.email]
    send_mail(subject, message, from_email, recipient_list)
