from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.
    Configured to work with email-based authentication.
    """

    # Fields to display in the user list
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    # Filters for the sidebar
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    # Fields to search
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    # Default ordering
    ordering = ("-date_joined",)

    # Fieldsets for the user detail/edit page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "updated_at")},
        ),
        # ### EXTENSIBILITY SECTION ###
        # Add additional fieldsets below for new fields
        # Example:
        # (
        #     _("Additional info"),
        #     {"fields": ("phone_number", "avatar", "bio")},
        # ),
        # ### END EXTENSIBILITY SECTION ###
    )

    # Fieldsets for the add user page
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # Read-only fields
    readonly_fields = ("last_login", "date_joined", "updated_at")

    # Enable filtering by date
    date_hierarchy = "date_joined"
