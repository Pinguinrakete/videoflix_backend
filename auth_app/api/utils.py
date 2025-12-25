from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_activation_email(user_email, activation_url):
    """Send an account activation email to the user."""
    html_content = (
        '<div style="width:500px; font-size:18px; '
        'font-family:Arial, Helvetica, sans-serif">'
        '<p>Dear videoflix user,<br><br>'
        'Thank you for registering with '
        '<span style="color:blue;">Videoflix</span>. '
        'To complete your registration and verify your email, '
        'please click the link below:</p>'
        f'<a href="{activation_url}" style="text-decoration:none;">'
        '<b>https://videoflix.de/site/registerConfirm</b></a>'
        '<p>If you did not create an account with us, '
        'please disregard this email.</p>'
        '<p>Best regards,</p>'
        '<p>Your Videoflix Team</p>'
        '</div>'
    )

    email = EmailMultiAlternatives(
        subject="Confirm your email",
        body="Please use an HTML-capable email client.",
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_reset_password_email(user_email, reset_pw_url):
    """Send a password reset email to the user."""
    html_content = (
        '<div style="width:500px; font-size:18px; '
        'font-family:Arial, Helvetica, sans-serif">'
        '<p>Hello videoflix user,<br><br>'
        'We recently received a request to reset your password. '
        'If you made this request, please click the link below:</p>'
        f'<a href="{reset_pw_url}" style="text-decoration:none;">'
        '<b>https://videoflix.de/site/resetPassword</b></a>'
        '<p>Please note that for security reasons, this link is '
        'only valid für 24 hours.</p>'
        '<p>If you did not request a password reset, please ignore this email.'
        '</p>'
        '<p>Best regards,</p>'
        '<p>Your Videoflix Team</p>'
        '</div>'
    )

    email = EmailMultiAlternatives(
        subject="Reset your Password",
        body="Please use an HTML-capable email client.",
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
