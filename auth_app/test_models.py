from django.contrib.auth.tokens import default_token_generator
# from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from .api.serializers import RegisterSerializer
from .api.utils import send_activation_email
from .api.utils import send_reset_password_email
from .models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Test suite for the CustomUser model.

    Verifies that standard users and superusers are created correctly,
    checks the validity of authentication tokens, and ensures
    the string representation of the user is correct.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_verified)

    def test_superuser_creation(self):
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_verified)

    def test_token_validity(self):
        self.user.token_created_at = timezone.now()
        self.assertTrue(self.user.token_is_valid())

        self.user.token_created_at -= timezone.timedelta(hours=25)
        self.assertFalse(self.user.token_is_valid())

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "test@example.com")


class RegisterSerializerTest(TestCase):
    """
    Test suite for the RegisterSerializer.

    Verifies that user registration works correctly with valid data,
    checks for password mismatch errors, and ensures duplicate
    emails are not allowed.
    """

    def test_valid_data(self):
        data = {
            "email": "newuser@example.com",
            "password": "password123",
            "confirmed_password": "password123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("password123"))

    def test_password_mismatch(self):
        data = {
            "email": "newuser2@example.com",
            "password": "password123",
            "confirmed_password": "wrongpass"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("confirmed_password", serializer.errors)

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            email="duplicate@example.com",
            password="pass"
            )
        data = {
            "email": "duplicate@example.com",
            "password": "pass123",
            "confirmed_password": "pass123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class RegisterViewTest(APITestCase):
    """
    Test suite for the RegisterView API endpoint.

    Verifies that a user can be successfully registered through the API,
    and that the user is properly created in the database.
    """

    def test_register_user(self):
        url = reverse("auth_app:register")
        data = {
            "email": "viewtest@example.com",
            "password": "pass1234",
            "confirmed_password": "pass1234"
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CustomUser.objects.filter(email="viewtest@example.com").exists()
            )


class ActivationViewTest(APITestCase):
    """
    Test suite for the ActivationView API endpoint.

    Verifies that a user can activate their account
    using a valid UID and token,
    and that invalid tokens are correctly rejected.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="activate@example.com",
            password="pass123"
            )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_activation_success(self):
        url = reverse(
            "auth_app:activation_via_email",
            args=[self.uid, self.token]
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_verified)

    def test_activation_invalid_token(self):
        url = reverse(
            "auth_app:activation_via_email",
            args=[self.uid, "wrongtoken"]
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)


class UtilsEmailTest(TestCase):
    """
    Test suite for email utility functions.

    Verifies that activation and password reset emails
    are sent correctly using the email utility functions.
    """

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_send_activation_email(self, mock_send):
        send_activation_email("test@example.com", "http://activation-link")
        self.assertTrue(mock_send.called)

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_send_reset_password_email(self, mock_send):
        send_reset_password_email("test@example.com", "http://reset-link")
        self.assertTrue(mock_send.called)
