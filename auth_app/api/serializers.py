from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user account.

    Validates the email and password fields, ensures that the password
    and confirmed_password match,
    and creates a new user with a hashed password.
    """

    confirmed_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirmed_password"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
        }

    def validate_confirmed_password(self, value):
        password = self.initial_data.get("password")
        if password and value and password != value:
            raise serializers.ValidationError("Passwords do not match")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Invalid credentials.")
        return value

    def save(self):
        user = User(
            email=self.validated_data["email"],
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class CookieTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer for authenticating a user via email and password.

    Validates the provided credentials, checks that the user account
    is active and the email address is verified, and returns the
    authenticated user instance on success.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")

        user = authenticate(
            request=request,
            username=attrs.get("email"),
            password=attrs.get("password")
        )

        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid email or password."}
                )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "Account is disabled."}
                )

        if not user.is_verified:
            raise serializers.ValidationError(
                {"detail": "Email address is not verified."}
                )

        return {"user": user}


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for initiating a password reset process.

    Validates the provided email address and attempts to retrieve
    the corresponding user. The user instance is stored for further
    processing (e.g. sending a password reset email), even if the
    email does not exist in the system.
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        self.user = User.objects.filter(email=value).first()

        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.

    Validates that the new password and confirmation password match
    before allowing the password update to proceed.
    """

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
