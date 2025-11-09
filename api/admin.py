from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin interface for Role model.
    Allows easy management of roles and permissions through Django admin.
    """
    
    list_display = ['name', 'description', 'is_active', 'user_count', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        (None, {
            'fields': ['name', 'description', 'is_active']
        }),
        ('Permissions', {
            'fields': ['permissions'],
            'description': (
                'Define permissions as JSON. Examples:<br>'
                '<b>Simple list:</b> {"permissions": ["create_post", "edit_post"]}<br>'
                '<b>Grouped:</b> {"posts": ["create", "read", "update"], "comments": ["read"]}<br>'
                '<b>Complex:</b> {"posts": {"create": true, "edit": {"condition": "own_only"}}}'
            )
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def user_count(self, obj):
        """Display number of users with this role."""
        return obj.users.count()
    user_count.short_description = 'Users'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.
    Extended to support role-based access control.
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
            'fields': ['roles', 'is_active', 'is_staff', 'is_superuser'],
            'description': 'Assign roles to grant permissions. Superuser has all permissions.'
        }),
        (_('Django Permissions (Advanced)'), {
            'fields': ['groups', 'user_permissions'],
            'classes': ['collapse'],
            'description': 'Django built-in permissions system. Use roles instead for custom permissions.'
        }),
        (_('Important dates'), {
            'fields': ['last_login', 'date_joined', 'updated_at'],
            'classes': ['collapse']
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
        roles = obj.roles.filter(is_active=True).values_list('name', flat=True)
        return ', '.join(roles) if roles else '-'
    display_roles.short_description = 'Active Roles'
