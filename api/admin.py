from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from api.models import User, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin interface for Role model.
    Allows easy management of roles and their permissions through Django admin.
    """
    list_display = ['name', 'description', 'is_active', 'user_count', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = [
        (None, {
            'fields': ['name', 'description', 'is_active']
        }),
        (_('Permissions'), {
            'fields': ['permissions'],
            'description': (
                'Define permissions as a JSON object. Examples:<br>'
                '<code>{"posts": ["create", "read", "update", "delete"]}</code><br>'
                '<code>{"posts": {"create": true, "delete": false}}</code><br>'
                'No migration needed when adding new permissions.'
            ),
        }),
        (_('Metadata'), {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    
    def user_count(self, obj):
        """Display number of users with this role."""
        return obj.users.count()
    user_count.short_description = 'Users'
    
    def save_model(self, request, obj, form, change):
        """Save the model and provide feedback."""
        super().save_model(request, obj, form, change)
        if not change:
            self.message_user(
                request,
                f'Role "{obj.name}" created successfully. '
                f'You can now assign this role to users.'
            )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    Extended to include role management.
    """
    list_display = ['email', 'first_name', 'last_name', 'display_roles', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'roles', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    filter_horizontal = ['roles', 'groups', 'user_permissions']
    readonly_fields = ['date_joined', 'updated_at']
    
    fieldsets = [
        (None, {
            'fields': ['email', 'password']
        }),
        (_('Personal info'), {
            'fields': ['first_name', 'last_name']
        }),
        (_('Roles & Permissions'), {
            'fields': ['roles', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
            'description': 'Assign roles to grant permissions. Roles provide flexible, JSON-based permissions.'
        }),
        (_('Important dates'), {
            'fields': ['date_joined', 'updated_at', 'last_login'],
            'classes': ['collapse'],
        }),
    ]
    
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2', 'first_name', 'last_name', 'roles'],
        }),
    ]
    
    def display_roles(self, obj):
        """Display user's roles as comma-separated list."""
        roles = obj.roles.filter(is_active=True)
        if roles.exists():
            return ', '.join([role.name for role in roles])
        return '-'
    display_roles.short_description = 'Roles'
    
    def get_readonly_fields(self, request, obj=None):
        """Make last_login readonly only when editing existing user."""
        if obj:
            return self.readonly_fields + ['last_login']
        return self.readonly_fields
