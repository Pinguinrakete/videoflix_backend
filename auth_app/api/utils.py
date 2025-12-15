from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_activation_email(user_email, activation_url):
    html_content = f"""
        <div style="width:500px; font-size:18px; font-family:Arial, Helvetica, sans-serif">    
            <p>Dear videoflix user,<br><br>
            Thank you for registering with <span style="color:blue;">Videoflix</span>. To complete your registration and verify your email address, please click the link below:</p>

            <a href="{activation_url}" style="text-decoration:none;"><b>https://videoflix.de/site/registerConfirm</b></a>

            <p>If you did not create an account with us, please disregard this email.</p>

            <p>Best regards,</p>

            <p>Your Videoflix Team.</p>
        </div>
    """

    email = EmailMultiAlternatives(
        subject="Confirm your email",
        body="Please use an HTML-capable email client.",
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()