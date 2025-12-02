from django.core.mail import send_mail
from django.conf import settings

def send_activation_email(to_email, activation_url):
    subject = "Activate Your Account"
    message = f"Hi!\n\nPlease click the link below to activate your account:\n{activation_url}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)