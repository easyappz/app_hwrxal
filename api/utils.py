"""
Utility functions for user and role management.

This module provides helper functions for working with users, roles, and permissions.
These functions are used throughout the application to simplify common operations.

Extensibility:
    Add new utility functions here as your application grows.
    Keep functions focused and well-documented for easy maintenance.
"""

from api.models import User, Role
from typing import Dict, List, Optional


def get_user_permissions(user: User) -> Dict:
    """
    Get all permissions from all of a user's active roles.
    
    This function aggregates permissions from all roles assigned to the user.
    It returns a combined dictionary of all permissions.
    
    Args:
        user (User): User instance to get permissions for
    
    Returns:
        dict: Combined permissions from all user's active roles
        
    Example:
        user = User.objects.get(email='user@example.com')
        permissions = get_user_permissions(user)
        # Returns: {
        #     'posts': ['create', 'read', 'update', 'delete'],
        #     'comments': ['create', 'read'],
        #     ...
        # }
    
    Usage in views:
        from api.utils import get_user_permissions
        
        def my_view(request):
            user_perms = get_user_permissions(request.user)
            if 'posts' in user_perms and 'create' in user_perms['posts']:
                # User can create posts
                pass
    
    Note:
        For checking specific permissions, it's better to use user.has_permission()
        method directly. This function is useful for debugging or displaying
        all user permissions in UI.
    """
    if not user or not user.is_authenticated:
        return {}
    
    # Superusers have all permissions
    if user.is_superuser:
        return {"superuser": True, "all_permissions": True}
    
    # Use the model method to get combined permissions
    return user.get_all_permissions()


def assign_default_role(user: User) -> bool:
    """
    Assign the default 'user' role to a user.
    
    This function is called during user registration to assign the default role.
    It checks if the user already has the role before assigning it.
    
    Args:
        user (User): User instance to assign role to
    
    Returns:
        bool: True if role was assigned, False if role doesn't exist or already assigned
    
    Example:
        user = User.objects.create_user(
            email='newuser@example.com',
            password='password123'
        )
        assign_default_role(user)
    
    Usage in signals or serializers:
        from api.utils import assign_default_role
        
        def post_save_user(sender, instance, created, **kwargs):
            if created:
                assign_default_role(instance)
    
    Extensibility:
        To change the default role:
        1. Modify the role_name variable below
        2. Or create additional logic to assign different default roles
           based on user attributes (e.g., email domain, invitation code)
    """
    if not user:
        return False
    
    # Define default role name
    # To change default role, modify this variable
    default_role_name = 'user'
    
    try:
        # Get the default role
        default_role = Role.objects.get(name=default_role_name, is_active=True)
        
        # Check if user already has this role
        if user.roles.filter(id=default_role.id).exists():
            return False
        
        # Assign role to user
        user.roles.add(default_role)
        return True
        
    except Role.DoesNotExist:
        # Default role doesn't exist
        # This should be created by the create_default_roles management command
        return False


def assign_role(user: User, role_name: str) -> bool:
    """
    Assign a specific role to a user.
    
    Helper function to assign any role by name.
    Wrapper around user.add_role() for convenience.
    
    Args:
        user (User): User instance to assign role to
        role_name (str): Name of the role to assign
    
    Returns:
        bool: True if role was assigned, False otherwise
    
    Example:
        from api.utils import assign_role
        
        user = User.objects.get(email='user@example.com')
        assign_role(user, 'moderator')
    
    Extensibility:
        This function can be extended to:
        - Send notifications when roles are assigned
        - Log role changes for audit trail
        - Validate business rules before assigning roles
    """
    if not user:
        return False
    
    return user.add_role(role_name)


def remove_role(user: User, role_name: str) -> bool:
    """
    Remove a specific role from a user.
    
    Helper function to remove any role by name.
    Wrapper around user.remove_role() for convenience.
    
    Args:
        user (User): User instance to remove role from
        role_name (str): Name of the role to remove
    
    Returns:
        bool: True if role was removed, False otherwise
    
    Example:
        from api.utils import remove_role
        
        user = User.objects.get(email='user@example.com')
        remove_role(user, 'moderator')
    
    Extensibility:
        This function can be extended to:
        - Prevent removal of certain roles (e.g., don't allow removing last role)
        - Send notifications when roles are removed
        - Log role changes for audit trail
    """
    if not user:
        return False
    
    return user.remove_role(role_name)


def get_users_with_role(role_name: str) -> List[User]:
    """
    Get all users that have a specific role.
    
    Args:
        role_name (str): Name of the role to search for
    
    Returns:
        List[User]: List of users with the specified role
    
    Example:
        from api.utils import get_users_with_role
        
        moderators = get_users_with_role('moderator')
        for user in moderators:
            print(user.email)
    
    Usage:
        - Send notifications to all users with a specific role
        - Generate reports on role distribution
        - Admin dashboard showing user counts by role
    """
    try:
        role = Role.objects.get(name=role_name)
        return list(role.users.filter(is_active=True))
    except Role.DoesNotExist:
        return []


def get_users_with_permission(permission_name: str) -> List[User]:
    """
    Get all users that have a specific permission (through any of their roles).
    
    Note: This is a helper function for admin/reporting purposes.
    It may be slow for large user bases as it checks each user's permissions.
    
    Args:
        permission_name (str): Permission to search for (e.g., 'posts.create')
    
    Returns:
        List[User]: List of users with the specified permission
    
    Example:
        from api.utils import get_users_with_permission
        
        users_can_publish = get_users_with_permission('posts.publish')
        for user in users_can_publish:
            print(user.email)
    
    Performance note:
        For large user bases, consider caching this result or using database-level
        JSON queries if your database supports them (PostgreSQL, MySQL 8+).
    """
    users_with_permission = []
    
    # Get all active users (you may want to add pagination for large datasets)
    active_users = User.objects.filter(is_active=True).prefetch_related('roles')
    
    for user in active_users:
        if user.has_permission(permission_name):
            users_with_permission.append(user)
    
    return users_with_permission


def create_default_roles() -> Dict[str, int]:
    """
    Create default roles in the database.
    
    This function is called during initial setup (migrations or management command)
    to create the default role structure.
    
    Returns:
        dict: Dictionary with counts of created and updated roles
              {'created': int, 'updated': int, 'errors': int}
    
    Example:
        from api.utils import create_default_roles
        
        result = create_default_roles()
        print(f"Created {result['created']} roles")
    
    Extensibility:
        To add new default roles:
        1. Add role definition to the default_roles list below
        2. Define permissions structure
        3. Run this function or the management command
    """
    # Define default roles
    default_roles = [
        {
            'name': 'user',
            'description': 'Default user role with full basic permissions',
            'permissions': {
                'profile': ['read', 'update'],
                'posts': ['create', 'read', 'update', 'delete'],
                'comments': ['create', 'read', 'update', 'delete'],
            },
            'is_active': True,
        },
        # Add more default roles here:
        # {
        #     'name': 'moderator',
        #     'description': 'Moderator with extended permissions',
        #     'permissions': {
        #         'profile': ['read', 'update'],
        #         'posts': ['create', 'read', 'update', 'delete', 'moderate'],
        #         'comments': ['create', 'read', 'update', 'delete', 'moderate'],
        #         'users': ['read', 'moderate'],
        #         'reports': ['read', 'resolve'],
        #     },
        #     'is_active': True,
        # },
    ]
    
    result = {'created': 0, 'updated': 0, 'errors': 0}
    
    for role_data in default_roles:
        try:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions'],
                    'is_active': role_data['is_active'],
                }
            )
            
            if created:
                result['created'] += 1
            else:
                # Optionally update existing role
                # Uncomment to update on each run:
                # role.description = role_data['description']
                # role.permissions = role_data['permissions']
                # role.is_active = role_data['is_active']
                # role.save()
                # result['updated'] += 1
                pass
                
        except Exception as e:
            result['errors'] += 1
    
    return result


def has_any_role(user: User, role_names: List[str]) -> bool:
    """
    Check if user has any of the specified roles.
    
    Args:
        user (User): User instance to check
        role_names (List[str]): List of role names to check
    
    Returns:
        bool: True if user has at least one of the roles, False otherwise
    
    Example:
        from api.utils import has_any_role
        
        if has_any_role(user, ['admin', 'moderator']):
            # User is either admin or moderator
            pass
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    return user.roles.filter(name__in=role_names, is_active=True).exists()


def has_all_roles(user: User, role_names: List[str]) -> bool:
    """
    Check if user has all of the specified roles.
    
    Args:
        user (User): User instance to check
        role_names (List[str]): List of role names to check
    
    Returns:
        bool: True if user has all of the roles, False otherwise
    
    Example:
        from api.utils import has_all_roles
        
        if has_all_roles(user, ['verified', 'premium']):
            # User is both verified and premium
            pass
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    user_role_names = set(
        user.roles.filter(is_active=True).values_list('name', flat=True)
    )
    
    return all(role_name in user_role_names for role_name in role_names)


# ============================================================
# HOW TO EXTEND UTILITIES
# ============================================================
#
# Add new utility functions below this section.
# Keep functions focused on a single responsibility.
# Always add docstrings with examples.
#
# Examples of useful utilities to add:
#
# def bulk_assign_role(users: List[User], role_name: str) -> int:
#     """Assign role to multiple users at once."""
#     pass
#
# def get_role_statistics() -> Dict:
#     """Get statistics about role distribution."""
#     pass
#
# def sync_permissions_from_config(config_file: str) -> bool:
#     """Sync roles and permissions from external config file."""
#     pass
#
# def audit_user_permissions(user: User) -> Dict:
#     """Generate audit report of user's permissions."""
#     pass
#
# ============================================================
