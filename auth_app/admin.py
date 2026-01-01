from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.

    Customizes the Django admin interface to manage users by email
    instead of username, defines displayed and filterable fields,
    configures permission management, and customizes the user
    creation and edit forms.
    """

    model = CustomUser

    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_verified",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_verified",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_verified",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_verified",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
