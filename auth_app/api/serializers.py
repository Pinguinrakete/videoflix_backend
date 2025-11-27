from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        pw = self.validated_data["password"]

        account = User(
            email=self.validated_data["email"]
        )
        account.set_password(pw)
        account.save()
        return account


class CookieTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Both fields must be filled out."
                )

        email = authenticate(email=email, password=password)
        if email is None:
            raise serializers.ValidationError(
                "Invalid email or password."
                )

        attrs["email"] = email

        return attrs