"""
Custom permission classes for role-based access control.

This module provides flexible permission classes that can be used with Django REST Framework
to implement fine-grained access control based on user roles and permissions.

Usage in views:
    from rest_framework.views import APIView
    from api.permissions import HasPermission, IsUserRole
    
    class MyView(APIView):
        permission_classes = [HasPermission('posts.create')]
        
        def post(self, request):
            # Only users with 'posts.create' permission can access this
            pass

Extensibility:
    To create custom permission classes:
    1. Inherit from BaseRolePermission or BasePermission
    2. Override has_permission() or has_object_permission()
    3. Use user.has_permission() method to check permissions
    4. Add your custom logic (e.g., time-based, IP-based restrictions)
"""

from rest_framework import permissions
from typing import List


class BaseRolePermission(permissions.BasePermission):
    """
    Base class for role-based permissions.
    
    Provides common functionality for permission checking.
    All custom role permissions should inherit from this class.
    """
    
    def has_permission_check(self, user, permission_name):
        """
        Check if user has a specific permission.
        
        Args:
            user: User instance
            permission_name: Permission to check (e.g., 'posts.create')
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        if not user or not user.is_authenticated:
            return False
        
        # Superusers always have all permissions
        if user.is_superuser:
            return True
        
        # Check user's permission through roles
        return user.has_permission(permission_name)


class HasPermission(BaseRolePermission):
    """
    Permission class to check if user has a specific permission.
    
    Usage:
        from api.permissions import HasPermission
        
        class MyView(APIView):
            permission_classes = [HasPermission('posts.create')]
    
    The permission name is passed to the constructor and checked against
    the user's roles and their permissions.
    
    Examples:
        HasPermission('posts.create')  # Check simple permission
        HasPermission('posts.delete')  # Check another permission
        HasPermission('admin.users')   # Check admin permission
    """
    
    def __init__(self, permission_name):
        """
        Initialize with permission name.
        
        Args:
            permission_name (str): Permission to check (e.g., 'posts.create')
        """
        self.permission_name = permission_name
        super().__init__()
    
    def has_permission(self, request, view):
        """
        Check if user has the specified permission.
        
        Args:
            request: DRF request object
            view: View being accessed
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return self.has_permission_check(request.user, self.permission_name)
    
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission.
        
        By default, uses the same permission as has_permission.
        Override this method in a subclass for custom object-level logic.
        
        Args:
            request: DRF request object
            view: View being accessed
            obj: Object being accessed
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return self.has_permission(request, view)


class HasAnyPermission(BaseRolePermission):
    """
    Permission class to check if user has ANY of the specified permissions.
    
    Useful when you want to allow access if user has at least one permission
    from a list of permissions.
    
    Usage:
        from api.permissions import HasAnyPermission
        
        class MyView(APIView):
            permission_classes = [
                HasAnyPermission(['posts.create', 'posts.update', 'admin.all'])
            ]
    
    The user only needs to have ONE of the listed permissions to gain access.
    
    Examples:
        HasAnyPermission(['posts.create', 'posts.update'])  # Can create OR update
        HasAnyPermission(['admin.all', 'moderator.all'])    # Admin OR moderator
    """
    
    def __init__(self, permission_list: List[str]):
        """
        Initialize with list of permissions.
        
        Args:
            permission_list (List[str]): List of permissions to check
        """
        self.permission_list = permission_list
        super().__init__()
    
    def has_permission(self, request, view):
        """
        Check if user has ANY of the specified permissions.
        
        Args:
            request: DRF request object
            view: View being accessed
        
        Returns:
            bool: True if user has at least one permission, False otherwise
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusers always have all permissions
        if request.user.is_superuser:
            return True
        
        # Check if user has any of the permissions
        for permission_name in self.permission_list:
            if self.has_permission_check(request.user, permission_name):
                return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission.
        
        By default, uses the same logic as has_permission.
        Override this method in a subclass for custom object-level logic.
        
        Args:
            request: DRF request object
            view: View being accessed
            obj: Object being accessed
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return self.has_permission(request, view)


class HasAllPermissions(BaseRolePermission):
    """
    Permission class to check if user has ALL of the specified permissions.
    
    Useful when you want to ensure user has multiple permissions
    before granting access.
    
    Usage:
        from api.permissions import HasAllPermissions
        
        class MyView(APIView):
            permission_classes = [
                HasAllPermissions(['posts.create', 'posts.publish'])
            ]
    
    The user must have ALL of the listed permissions to gain access.
    
    Examples:
        HasAllPermissions(['posts.create', 'posts.publish'])  # Can create AND publish
        HasAllPermissions(['admin.users', 'admin.roles'])     # Has both admin perms
    """
    
    def __init__(self, permission_list: List[str]):
        """
        Initialize with list of permissions.
        
        Args:
            permission_list (List[str]): List of permissions to check
        """
        self.permission_list = permission_list
        super().__init__()
    
    def has_permission(self, request, view):
        """
        Check if user has ALL of the specified permissions.
        
        Args:
            request: DRF request object
            view: View being accessed
        
        Returns:
            bool: True if user has all permissions, False otherwise
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusers always have all permissions
        if request.user.is_superuser:
            return True
        
        # Check if user has all of the permissions
        for permission_name in self.permission_list:
            if not self.has_permission_check(request.user, permission_name):
                return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission.
        
        By default, uses the same logic as has_permission.
        Override this method in a subclass for custom object-level logic.
        
        Args:
            request: DRF request object
            view: View being accessed
            obj: Object being accessed
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return self.has_permission(request, view)


class IsUserRole(BaseRolePermission):
    """
    Permission class to check if user has the default 'user' role.
    
    This is a convenience permission for checking if a user has the basic user role.
    Useful for endpoints that should be accessible to all registered users.
    
    Usage:
        from api.permissions import IsUserRole
        
        class MyView(APIView):
            permission_classes = [IsUserRole]
    
    Note: This checks for the role name 'user', not a specific permission.
    For permission-based checks, use HasPermission instead.
    """
    
    def has_permission(self, request, view):
        """
        Check if user has 'user' role.
        
        Args:
            request: DRF request object
            view: View being accessed
        
        Returns:
            bool: True if user has 'user' role or is superuser, False otherwise
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusers always pass
        if request.user.is_superuser:
            return True
        
        # Check if user has 'user' role
        return request.user.roles.filter(name='user', is_active=True).exists()
    
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission.
        
        By default, uses the same logic as has_permission.
        Override this method in a subclass for custom object-level logic.
        
        Args:
            request: DRF request object
            view: View being accessed
            obj: Object being accessed
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return self.has_permission(request, view)


# ============================================================
# CUSTOM PERMISSION EXAMPLES
# ============================================================
# Below are examples of how to create custom permission classes.
# Uncomment and modify as needed for your application.
# ============================================================

class IsOwnerOrReadOnly(BaseRolePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only access is allowed for any authenticated user.
    
    Usage:
        from api.permissions import IsOwnerOrReadOnly
        
        class PostDetailView(APIView):
            permission_classes = [IsOwnerOrReadOnly]
    
    This permission requires the object to have a 'user' or 'owner' field.
    Modify the field name in has_object_permission if your model uses different naming.
    """
    
    def has_permission(self, request, view):
        """
        Allow access to authenticated users.
        
        Args:
            request: DRF request object
            view: View being accessed
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any authenticated user.
        Write permissions are only allowed to the owner of the object.
        
        Args:
            request: DRF request object
            view: View being accessed
            obj: Object being accessed
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Superusers can edit anything
        if request.user.is_superuser:
            return True
        
        # Write permissions are only allowed to the owner of the object
        # Adjust this to match your model's owner field name
        # Common field names: 'user', 'owner', 'created_by', 'author'
        owner_field = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        return owner_field == request.user


# ============================================================
# HOW TO ADD CUSTOM PERMISSION CLASSES
# ============================================================
# 
# 1. Create a new class inheriting from BaseRolePermission or permissions.BasePermission
# 2. Override has_permission() for view-level checks
# 3. Override has_object_permission() for object-level checks
# 4. Use user.has_permission() to check role-based permissions
# 5. Add custom logic (time checks, IP restrictions, etc.)
# 
# Example - Time-based permission:
# 
# class BusinessHoursOnly(BaseRolePermission):
#     """
#     Only allow access during business hours (9 AM - 5 PM).
#     """
#     
#     def has_permission(self, request, view):
#         from datetime import datetime
#         current_hour = datetime.now().hour
#         return 9 <= current_hour < 17
# 
# 
# Example - IP-based permission:
# 
# class AllowedIPOnly(BaseRolePermission):
#     """
#     Only allow access from specific IP addresses.
#     """
#     
#     ALLOWED_IPS = ['127.0.0.1', '192.168.1.1']
#     
#     def has_permission(self, request, view):
#         ip = request.META.get('REMOTE_ADDR')
#         return ip in self.ALLOWED_IPS
# 
# 
# Example - Complex permission combining role and object ownership:
# 
# class CanEditPost(BaseRolePermission):
#     """
#     Allow editing if user is owner OR has 'posts.edit_any' permission.
#     """
#     
#     def has_object_permission(self, request, view, obj):
#         # Owner can always edit
#         if obj.user == request.user:
#             return True
#         
#         # Or user has special permission to edit any post
#         return self.has_permission_check(request.user, 'posts.edit_any')
# 
# ============================================================
