from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    """
    Role model for implementing role-based access control (RBAC).
    
    The permissions field uses JSONField for maximum flexibility.
    It can store permissions in various structures:
    
    Example 1 - Simple list:
    {
        "permissions": ["create_post", "edit_post", "delete_post"]
    }
    
    Example 2 - Grouped by resource:
    {
        "posts": ["create", "read", "update", "delete"],
        "comments": ["create", "read", "delete"],
        "users": ["read"]
    }
    
    Example 3 - With conditions:
    {
        "posts": {
            "create": true,
            "edit": {"condition": "own_only"},
            "delete": {"condition": "own_only"},
            "publish": false
        }
    }
    
    To extend permissions:
    1. Add new permission keys to the JSON structure
    2. No database migration needed
    3. Update the has_permission() method logic if needed
    4. Use admin panel to configure role permissions
    """
    
    name = models.CharField(
        verbose_name="Role name",
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique name for the role (e.g., 'user', 'admin', 'moderator')"
    )
    
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        help_text="Description of what this role can do"
    )
    
    permissions = models.JSONField(
        verbose_name="Permissions",
        default=dict,
        blank=True,
        help_text="JSON object storing flexible permission structure. "
                  "Can be extended without schema changes."
    )
    
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text="Designates whether this role is currently active. "
                  "Inactive roles will not grant permissions."
    )
    
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
    )
    
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["name"]
        db_table = "roles"
        indexes = [
            models.Index(fields=["name", "is_active"]),
        ]
    
    def __str__(self):
        return self.name
    
    def has_permission(self, permission_name):
        """
        Check if this role has a specific permission.
        
        This method supports multiple permission structures:
        - Simple list: checks if permission_name is in the list
        - Nested dict: checks if permission exists in any resource
        - Complex structures: can be extended for custom logic
        
        Args:
            permission_name (str): Permission to check (e.g., 'create_post' or 'posts.create')
        
        Returns:
            bool: True if permission is granted, False otherwise
        """
        if not self.is_active:
            return False
        
        if not self.permissions:
            return False
        
        # Support dot notation (e.g., 'posts.create')
        if '.' in permission_name:
            parts = permission_name.split('.', 1)
            resource = parts[0]
            action = parts[1]
            
            if resource in self.permissions:
                resource_perms = self.permissions[resource]
                
                # Handle list of permissions
                if isinstance(resource_perms, list):
                    return action in resource_perms
                
                # Handle dict of permissions
                if isinstance(resource_perms, dict):
                    if action in resource_perms:
                        perm_value = resource_perms[action]
                        # Simple boolean
                        if isinstance(perm_value, bool):
                            return perm_value
                        # Complex permission (with conditions, etc.)
                        if isinstance(perm_value, dict):
                            # Default to True if permission exists but condition handling
                            # can be implemented in application logic
                            return True
                        return True
            return False
        
        # Simple permission check
        # Check if it's a simple list structure
        if 'permissions' in self.permissions:
            perms = self.permissions['permissions']
            if isinstance(perms, list):
                return permission_name in perms
        
        # Check in root level
        if permission_name in self.permissions:
            perm_value = self.permissions[permission_name]
            if isinstance(perm_value, bool):
                return perm_value
            # If it exists and is not False, consider it granted
            return True
        
        return False


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the username field.
    Designed to be easily extensible for additional fields and role-based access control.
    """

    # Basic authentication field
    email = models.EmailField(
        verbose_name="Email address",
        max_length=255,
        unique=True,
        db_index=True,
    )

    # Personal information fields
    first_name = models.CharField(
        verbose_name="First name",
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=150,
        blank=True,
    )

    # Status fields
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_staff = models.BooleanField(
        verbose_name="Staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    # Timestamp fields
    date_joined = models.DateTimeField(
        verbose_name="Date joined",
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )

    # ### EXTENSIBILITY SECTION ###
    # Add additional profile fields below this comment
    # Examples:
    # phone_number = models.CharField(max_length=20, blank=True)
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # bio = models.TextField(blank=True)
    # birth_date = models.DateField(blank=True, null=True)
    # ### END EXTENSIBILITY SECTION ###

    # ### ROLE-BASED ACCESS CONTROL SECTION ###
    roles = models.ManyToManyField(
        Role,
        verbose_name="Roles",
        blank=True,
        related_name="users",
        help_text="The roles this user belongs to. A user will get all permissions "
                  "granted to each of their roles."
    )
    # ### END RBAC SECTION ###

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email is already required by default

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        db_table = "users"
        indexes = [
            models.Index(fields=["email", "is_active"]),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name or self.email
    
    def has_permission(self, permission_name):
        """
        Check if user has a specific permission through any of their active roles.
        Superusers always have all permissions.
        
        Args:
            permission_name (str): Permission to check (e.g., 'create_post' or 'posts.create')
        
        Returns:
            bool: True if user has the permission, False otherwise
        
        Example usage:
            if user.has_permission('posts.create'):
                # Allow user to create post
                pass
        """
        # Superusers have all permissions
        if self.is_superuser:
            return True
        
        # Inactive users have no permissions
        if not self.is_active:
            return False
        
        # Check if any of user's active roles has this permission
        for role in self.roles.filter(is_active=True):
            if role.has_permission(permission_name):
                return True
        
        return False
    
    def add_role(self, role_name):
        """
        Add a role to the user by role name.
        
        Args:
            role_name (str): Name of the role to add
        
        Returns:
            bool: True if role was added, False if role doesn't exist or already assigned
        
        Example:
            user.add_role('moderator')
        """
        try:
            role = Role.objects.get(name=role_name, is_active=True)
            if not self.roles.filter(id=role.id).exists():
                self.roles.add(role)
                return True
            return False
        except Role.DoesNotExist:
            return False
    
    def remove_role(self, role_name):
        """
        Remove a role from the user by role name.
        
        Args:
            role_name (str): Name of the role to remove
        
        Returns:
            bool: True if role was removed, False if role doesn't exist or not assigned
        
        Example:
            user.remove_role('moderator')
        """
        try:
            role = Role.objects.get(name=role_name)
            if self.roles.filter(id=role.id).exists():
                self.roles.remove(role)
                return True
            return False
        except Role.DoesNotExist:
            return False
    
    def get_all_permissions(self):
        """
        Get all permissions from all user's active roles.
        
        Returns:
            dict: Combined permissions from all roles
        
        Note: This is a helper method for debugging or displaying user permissions.
        For checking specific permissions, use has_permission() instead.
        """
        if self.is_superuser:
            return {"superuser": True}
        
        combined_permissions = {}
        for role in self.roles.filter(is_active=True):
            if role.permissions:
                # Merge permissions (simple merge, can be extended for complex merging logic)
                for key, value in role.permissions.items():
                    if key not in combined_permissions:
                        combined_permissions[key] = value
                    else:
                        # If both are lists, combine them
                        if isinstance(combined_permissions[key], list) and isinstance(value, list):
                            combined_permissions[key] = list(set(combined_permissions[key] + value))
                        # If both are dicts, merge them
                        elif isinstance(combined_permissions[key], dict) and isinstance(value, dict):
                            combined_permissions[key].update(value)
        
        return combined_permissions
