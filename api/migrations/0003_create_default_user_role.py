# Data migration to create default 'user' role with basic permissions
# This migration is part of the initial authentication system setup

from django.db import migrations


def create_default_role(apps, schema_editor):
    """
    Create the default 'user' role with all basic permissions.
    
    The 'user' role is the base role for all regular users in the system.
    By default, users have full permissions to interact with the application.
    
    Permission structure can be extended by:
    1. Adding new keys to the permissions JSON in the admin panel
    2. No code or migration changes required
    3. The permission checking logic in User.has_permission() will automatically
       recognize new permissions
    
    To restrict permissions for specific features:
    1. Create a new role (e.g., 'restricted_user')
    2. Define granular permissions in the JSON structure
    3. Assign the appropriate role to users
    """
    Role = apps.get_model('api', 'Role')
    
    # Create default 'user' role with all permissions
    # Using a simple permissions list structure that can be easily extended
    Role.objects.get_or_create(
        name='user',
        defaults={
            'description': 'Default user role with basic permissions. All registered users are assigned this role by default.',
            'permissions': {
                # Simple list structure - easy to check and extend
                'permissions': [
                    'view_profile',
                    'edit_profile',
                    'change_password',
                ]
                # To add resource-based permissions, you can use this structure:
                # 'posts': ['create', 'read', 'update', 'delete'],
                # 'comments': ['create', 'read', 'delete'],
                # 'profile': ['read', 'update'],
            },
            'is_active': True,
        }
    )


def reverse_create_default_role(apps, schema_editor):
    """
    Remove the default 'user' role.
    This reverse migration is provided for completeness but should be used with caution
    as it will remove the role from all users who have it assigned.
    """
    Role = apps.get_model('api', 'Role')
    Role.objects.filter(name='user').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_role_refreshtoken_passwordresettoken_user_roles'),
    ]

    operations = [
        migrations.RunPython(
            create_default_role,
            reverse_create_default_role,
        ),
    ]
