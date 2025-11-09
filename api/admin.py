from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role, RefreshToken


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin interface for Role model.
    """
    list_display = ["name", "description", "is_active", "created_at", "user_count"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    
    fieldsets = [
        (None, {
            "fields": ["name", "description", "is_active"]
        }),
        ("Permissions", {
            "fields": ["permissions"],
            "description": "Define permissions as JSON. Example: {\"posts\": [\"create\", \"read\", \"update\", \"delete\"]}"
        }),
        ("Metadata", {
            "fields": ["created_at", "updated_at"],
            "classes": ["collapse"]
        }),
    ]
    
    def user_count(self, obj):
        """Display the number of users with this role."""
        return obj.users.count()
    user_count.short_description = "Users"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for custom User model.
    """
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "date_joined", "role_list"]
    list_filter = ["is_active", "is_staff", "is_superuser", "date_joined", "roles"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-date_joined"]
    readonly_fields = ["date_joined", "updated_at"]
    filter_horizontal = ["roles", "groups", "user_permissions"]
    
    fieldsets = [
        (None, {
            "fields": ["email", "password"]
        }),
        (_("Personal info"), {
            "fields": ["first_name", "last_name"]
        }),
        (_("Roles and Permissions"), {
            "fields": ["roles", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"],
        }),
        (_("Important dates"), {
            "fields": ["date_joined", "updated_at", "last_login"],
            "classes": ["collapse"]
        }),
    ]
    
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": ["email", "password1", "password2", "first_name", "last_name", "roles"],
        }),
    ]
    
    def role_list(self, obj):
        """Display comma-separated list of user's roles."""
        return ", ".join([role.name for role in obj.roles.all()])
    role_list.short_description = "Roles"


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for RefreshToken model.
    """
    list_display = ["user", "token_preview", "created_at", "expires_at", "is_revoked", "is_valid_status"]
    list_filter = ["is_revoked", "created_at", "expires_at"]
    search_fields = ["user__email", "token", "ip_address"]
    ordering = ["-created_at"]
    readonly_fields = ["token", "created_at", "revoked_at", "user_agent", "ip_address"]
    date_hierarchy = "created_at"
    
    fieldsets = [
        ("Token Information", {
            "fields": ["user", "token", "created_at", "expires_at"]
        }),
        ("Status", {
            "fields": ["is_revoked", "revoked_at"]
        }),
        ("Device Information", {
            "fields": ["user_agent", "ip_address"],
            "classes": ["collapse"]
        }),
    ]
    
    def token_preview(self, obj):
        """Display truncated token for security."""
        return f"{obj.token[:20]}..."
    token_preview.short_description = "Token"
    
    def is_valid_status(self, obj):
        """Display whether token is currently valid."""
        return obj.is_valid()
    is_valid_status.boolean = True
    is_valid_status.short_description = "Valid"
    
    def has_add_permission(self, request):
        """Prevent manual creation of tokens through admin."""
        return False
    
    actions = ["revoke_tokens", "delete_expired_tokens"]
    
    def revoke_tokens(self, request, queryset):
        """Action to revoke selected tokens."""
        count = 0
        for token in queryset.filter(is_revoked=False):
            token.revoke()
            count += 1
        self.message_user(request, f"{count} token(s) revoked successfully.")
    revoke_tokens.short_description = "Revoke selected tokens"
    
    def delete_expired_tokens(self, request, queryset):
        """Action to delete expired tokens."""
        from django.utils import timezone
        count = queryset.filter(expires_at__lt=timezone.now()).delete()[0]
        self.message_user(request, f"{count} expired token(s) deleted successfully.")
    delete_expired_tokens.short_description = "Delete expired tokens"
