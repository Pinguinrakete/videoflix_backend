from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
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
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active or not user.is_verified:
            raise serializers.ValidationError("Account is not active.")

        return {"user": user}
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("If the email exists, a reset link will be sent.")
        return value
        

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs