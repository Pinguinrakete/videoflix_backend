from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from pathlib import Path


def send_activation_email(user_email, activation_url):
    """Send an account activation email to the user."""

    html_content = f"""
        <div style="width:500px; font-size:18px; font-family:Arial, Helvetica, sans-serif"; text-align:center;>

            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td align="center">
                        <img src="cid:videoflix_logo" alt="Videoflix Logo" style="max-width:200px; margin-top: 18px; display:block;" />
                    </td>
                </tr>
            </table>

            <p style="font-size:18px;">Dear videoflix user,<br><br>
            Thank you for registering with <span style="color:blue;">Videoflix</span>. To complete your registration and verify your email address, please click the link below:</p>

            <a href="{activation_url}" style="text-decoration:none;"><b>https://videoflix.de/site/registerConfirm</b></a>

            <p>If you did not create an account with us, please disregard this email.</p>

            <p>Best regards,</p>

            <p>Your Videoflix Team</p>
        </div>
    """

    email = EmailMultiAlternatives(
        subject="Confirm your email",
        body="Please use an HTML-capable email client.",
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.attach_alternative(html_content, "text/html")

    image_path = Path(settings.BASE_DIR) / "assets/image/videoflix.png"

    with open(image_path, "rb") as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header("Content-ID", "<videoflix_logo>")
        mime_image.add_header("Content-Disposition", "inline", filename="videoflix.png")
        email.attach(mime_image)

    email.send()


def send_reset_password_email(user_email, reset_pw_url):
    """Send a password reset email to the user."""

    html_content = f"""
        <div style="width:500px; font-size:18px; font-family:Arial, Helvetica, sans-serif">    
            <p>Hello videoflix user,<br><br>
            We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:</p>

            <a href="{reset_pw_url}" style="text-decoration:none;"><b>https://videoflix.de/site/resetPassword</b></a>

            <p>Please note that for security reasons, this link is only valid für 24 hours.</p>

            <p>If you did not request a password reset, please ignore this email.</p>

            <p>Best regards,</p>

            <p>Your Videoflix Team</p>

            <img src="cid:videoflix_logo" alt="Videoflix Logo" style="max-width:200px; display:block; margin:0 auto;" />
        </div>
    """

    email = EmailMultiAlternatives(
        subject="Reset your Password",
        body="Please use an HTML-capable email client.",
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
