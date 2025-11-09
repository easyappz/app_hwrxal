from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import User, Role, RefreshToken, PasswordResetToken


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin interface for Role model.
    Allows management of roles and their permissions through Django admin.
    
    To extend:
    - Modify list_display to show additional fields
    - Add custom actions for bulk operations
    - Override save_model() for custom save logic
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
            "description": (
                "<strong>Define permissions as JSON object. The structure is flexible and can be extended.</strong><br><br>"
                "<strong>Example 1 - Simple list:</strong><br>"
                '<code>{"permissions": ["create_post", "edit_post", "delete_post"]}</code><br><br>'
                "<strong>Example 2 - Grouped by resource:</strong><br>"
                '<code>{"posts": ["create", "read", "update", "delete"], "comments": ["create", "read"]}</code><br><br>'
                "<strong>Example 3 - With conditions:</strong><br>"
                '<code>{"posts": {"create": true, "edit": {"condition": "own_only"}, "delete": false}}</code><br><br>'
                "<strong>To extend permissions:</strong> Just add new keys to the JSON - no migration needed!"
            )
        }),
        ("Metadata", {
            "fields": ["created_at", "updated_at"],
            "classes": ["collapse"]
        }),
    ]
    
    def user_count(self, obj):
        """Display the number of users with this role."""
        count = obj.users.count()
        return format_html('<strong>{}</strong>', count)
    user_count.short_description = "Users"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for custom User model.
    Provides comprehensive user management with role-based access control.
    
    ### HOW TO EXTEND THIS ADMIN:
    
    1. To add new fields to the user model:
       - Add the field to User model in models.py (in EXTENSIBILITY SECTION)
       - Add the field name to 'list_display' below to show in list view
       - Add the field to appropriate fieldset (e.g., "Personal info")
       - Add to 'search_fields' if you want it searchable
    
    2. To add custom filters:
       - Add filter name to 'list_filter'
       - For complex filters, create custom filter class
    
    3. To add custom actions:
       - Define method with (self, request, queryset) signature
       - Add method name to 'actions' list
    
    Example of adding 'phone_number' field:
       - In models.py: phone_number = models.CharField(max_length=20, blank=True)
       - In list_display: add "phone_number" to the list
       - In Personal info fieldset: add "phone_number" to fields
       - In search_fields: add "phone_number"
    """
    
    # Fields displayed in the user list view
    list_display = [
        "email", 
        "first_name", 
        "last_name", 
        "is_active", 
        "is_staff", 
        "date_joined", 
        "role_list"
        # ### ADD NEW FIELDS HERE FOR LIST VIEW ###
        # Example: "phone_number", "birth_date"
    ]
    
    # Filters in the right sidebar
    list_filter = [
        "is_active", 
        "is_staff", 
        "is_superuser", 
        "date_joined", 
        "roles"
        # ### ADD NEW FILTERS HERE ###
        # Example: "created_at", "country"
    ]
    
    # Fields that can be searched
    search_fields = [
        "email", 
        "first_name", 
        "last_name"
        # ### ADD NEW SEARCHABLE FIELDS HERE ###
        # Example: "phone_number", "bio"
    ]
    
    ordering = ["-date_joined"]
    readonly_fields = ["date_joined", "updated_at", "last_login"]
    filter_horizontal = ["roles", "groups", "user_permissions"]
    
    # Field organization for the edit/view user page
    fieldsets = [
        (None, {
            "fields": ["email", "password"]
        }),
        (_("Personal Info"), {
            "fields": [
                "first_name", 
                "last_name"
                # ### ADD NEW PERSONAL FIELDS HERE ###
                # Example: "phone_number", "birth_date", "avatar", "bio"
            ],
            "description": "Basic personal information. Add more fields here as needed."
        }),
        (_("Permissions"), {
            "fields": [
                "is_active", 
                "is_staff", 
                "is_superuser"
            ],
            "description": "User account status and administrative permissions."
        }),
        (_("Roles"), {
            "fields": ["roles"],
            "description": (
                "Assign roles to grant permissions. Users inherit all permissions from their roles. "
                "For fine-grained control, use groups and user_permissions below."
            )
        }),
        (_("Advanced Permissions"), {
            "fields": ["groups", "user_permissions"],
            "classes": ["collapse"],
            "description": "Django's built-in permission system. Use roles for custom permissions."
        }),
        (_("Important Dates"), {
            "fields": ["date_joined", "updated_at", "last_login"],
            "classes": ["collapse"]
        }),
    ]
    
    # Fields shown when creating a new user
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": [
                "email", 
                "password1", 
                "password2", 
                "first_name", 
                "last_name", 
                "roles"
                # ### ADD NEW FIELDS FOR USER CREATION HERE ###
                # Example: "phone_number"
            ],
        }),
    ]
    
    def role_list(self, obj):
        """Display comma-separated list of user's roles with color coding."""
        roles = obj.roles.all()
        if not roles:
            return format_html('<span style="color: #999;">No roles</span>')
        
        role_badges = []
        for role in roles:
            color = "#28a745" if role.is_active else "#dc3545"
            role_badges.append(
                f'<span style="background-color: {color}; color: white; '
                f'padding: 2px 8px; border-radius: 3px; margin-right: 4px; '
                f'font-size: 11px;">{role.name}</span>'
            )
        return format_html("".join(role_badges))
    role_list.short_description = "Roles"


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for RefreshToken model.
    Allows viewing and managing JWT refresh tokens.
    
    Features:
    - View all refresh tokens with their status
    - Revoke tokens individually or in bulk
    - Delete expired tokens
    - Track token usage by device and IP
    
    Note: Token creation is handled programmatically, not through admin.
    """
    
    list_display = [
        "user", 
        "token_preview", 
        "created_at", 
        "expires_at", 
        "is_revoked", 
        "is_valid_status"
    ]
    list_filter = [
        "is_revoked", 
        "created_at", 
        "expires_at"
    ]
    search_fields = [
        "user__email", 
        "token", 
        "ip_address"
    ]
    ordering = ["-created_at"]
    readonly_fields = [
        "user",
        "token", 
        "created_at", 
        "expires_at",
        "revoked_at", 
        "user_agent", 
        "ip_address"
    ]
    date_hierarchy = "created_at"
    
    fieldsets = [
        ("Token Information", {
            "fields": ["user", "token", "created_at", "expires_at"],
            "description": "Basic token information. Tokens are automatically generated."
        }),
        ("Status", {
            "fields": ["is_revoked", "revoked_at"],
            "description": "Token revocation status. Revoked tokens cannot be used."
        }),
        ("Device Information", {
            "fields": ["user_agent", "ip_address"],
            "classes": ["collapse"],
            "description": "Information about the device/session that created this token."
        }),
    ]
    
    def token_preview(self, obj):
        """Display truncated token for security."""
        return format_html(
            '<code style="background: #f5f5f5; padding: 2px 6px; border-radius: 3px;">{}</code>',
            f"{obj.token[:20]}..."
        )
    token_preview.short_description = "Token"
    
    def is_valid_status(self, obj):
        """Display whether token is currently valid with visual indicator."""
        is_valid = obj.is_valid()
        if is_valid:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Valid</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">✗ Invalid</span>'
            )
    is_valid_status.short_description = "Status"
    
    def has_add_permission(self, request):
        """Prevent manual creation of tokens through admin."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow viewing but limit editing to revocation only."""
        return True
    
    actions = ["revoke_tokens", "delete_expired_tokens"]
    
    def revoke_tokens(self, request, queryset):
        """Action to revoke selected tokens."""
        count = 0
        for token in queryset.filter(is_revoked=False):
            token.revoke()
            count += 1
        self.message_user(
            request, 
            f"{count} token(s) revoked successfully.",
            level="success" if count > 0 else "warning"
        )
    revoke_tokens.short_description = "Revoke selected tokens"
    
    def delete_expired_tokens(self, request, queryset):
        """Action to delete expired tokens from selection."""
        from django.utils import timezone
        expired_queryset = queryset.filter(expires_at__lt=timezone.now())
        count = expired_queryset.count()
        expired_queryset.delete()
        self.message_user(
            request, 
            f"{count} expired token(s) deleted successfully.",
            level="success" if count > 0 else "warning"
        )
    delete_expired_tokens.short_description = "Delete expired tokens"


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for PasswordResetToken model.
    Allows viewing and managing password reset tokens.
    
    Features:
    - View all password reset requests
    - Track token usage and expiration
    - Revoke tokens if needed
    - Monitor security with IP tracking
    
    Note: Token creation is handled programmatically, not through admin.
    """
    
    list_display = [
        "user", 
        "token_preview", 
        "created_at", 
        "expires_at", 
        "is_used", 
        "is_valid_status",
        "ip_address"
    ]
    list_filter = [
        "is_used", 
        "created_at", 
        "expires_at"
    ]
    search_fields = [
        "user__email", 
        "token", 
        "ip_address"
    ]
    ordering = ["-created_at"]
    readonly_fields = [
        "user",
        "token", 
        "created_at", 
        "expires_at",
        "used_at", 
        "ip_address"
    ]
    date_hierarchy = "created_at"
    
    fieldsets = [
        ("Token Information", {
            "fields": ["user", "token", "created_at", "expires_at"],
            "description": "Password reset token details. Tokens are single-use and time-limited."
        }),
        ("Usage Status", {
            "fields": ["is_used", "used_at"],
            "description": "Whether this token has been used to reset password."
        }),
        ("Security Information", {
            "fields": ["ip_address"],
            "description": "IP address from which reset was requested."
        }),
    ]
    
    def token_preview(self, obj):
        """Display truncated token for security."""
        return format_html(
            '<code style="background: #f5f5f5; padding: 2px 6px; border-radius: 3px;">{}</code>',
            f"{obj.token[:20]}..."
        )
    token_preview.short_description = "Token"
    
    def is_valid_status(self, obj):
        """Display whether token is currently valid with visual indicator."""
        is_valid = obj.is_valid()
        if is_valid:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Valid</span>'
            )
        else:
            reason = "Used" if obj.is_used else "Expired"
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">✗ {} </span>',
                reason
            )
    is_valid_status.short_description = "Status"
    
    def has_add_permission(self, request):
        """Prevent manual creation of tokens through admin."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow viewing but prevent editing."""
        return True
    
    actions = ["mark_as_used", "delete_expired_tokens"]
    
    def mark_as_used(self, request, queryset):
        """Action to mark selected tokens as used (effectively revoking them)."""
        count = 0
        for token in queryset.filter(is_used=False):
            token.mark_as_used()
            count += 1
        self.message_user(
            request, 
            f"{count} token(s) marked as used successfully.",
            level="success" if count > 0 else "warning"
        )
    mark_as_used.short_description = "Mark selected tokens as used"
    
    def delete_expired_tokens(self, request, queryset):
        """Action to delete expired tokens from selection."""
        from django.utils import timezone
        expired_queryset = queryset.filter(expires_at__lt=timezone.now())
        count = expired_queryset.count()
        expired_queryset.delete()
        self.message_user(
            request, 
            f"{count} expired token(s) deleted successfully.",
            level="success" if count > 0 else "warning"
        )
    delete_expired_tokens.short_description = "Delete expired tokens"


# ############################################################################
# ### HOW TO ADD ADMIN FOR NEW MODELS:
# ###
# ### 1. Import your model at the top:
# ###    from .models import YourModel
# ###
# ### 2. Create admin class:
# ###    @admin.register(YourModel)
# ###    class YourModelAdmin(admin.ModelAdmin):
# ###        list_display = ['field1', 'field2', 'created_at']
# ###        list_filter = ['status', 'created_at']
# ###        search_fields = ['name', 'description']
# ###        ordering = ['-created_at']
# ###
# ### 3. For complex admin interfaces, use fieldsets to organize fields:
# ###    fieldsets = [
# ###        ('Basic Info', {'fields': ['name', 'description']}),
# ###        ('Advanced', {'fields': ['options'], 'classes': ['collapse']}),
# ###    ]
# ###
# ### 4. Add custom actions if needed:
# ###    actions = ['activate_items']
# ###    def activate_items(self, request, queryset):
# ###        queryset.update(is_active=True)
# ###
# ############################################################################
