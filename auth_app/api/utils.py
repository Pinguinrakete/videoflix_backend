from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = "Confirm your email"
    message = (
        f"Dear,\n\nThank you for registering with Videoflix. To complete your registration "
        f"and verify your email address, please click the link below:\n\n"
        f"If you did not create an account with us, please disregard this email.\n\n"
        f"Best regards,\n"
        f"Your Videoflix Team."
    )

    send_mail(subject, message, None, [user.email])