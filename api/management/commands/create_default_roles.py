from django.core.management.base import BaseCommand
from api.models import Role


class Command(BaseCommand):
    help = 'Create default roles for the application'

    def handle(self, *args, **options):
        """
        Create default 'user' role with full permissions.
        This can be extended to create additional roles.
        """
        
        # Define default roles and their permissions
        default_roles = [
            {
                'name': 'user',
                'description': 'Default user role with full basic permissions',
                'permissions': {
                    # Full permissions for basic user
                    # Using grouped structure for better organization
                    'profile': ['read', 'update'],
                    'posts': ['create', 'read', 'update', 'delete'],
                    'comments': ['create', 'read', 'update', 'delete'],
                },
                'is_active': True,
            },
            # You can add more default roles here:
            # {
            #     'name': 'moderator',
            #     'description': 'Moderator with extended permissions',
            #     'permissions': {
            #         'profile': ['read', 'update'],
            #         'posts': ['create', 'read', 'update', 'delete'],
            #         'comments': ['create', 'read', 'update', 'delete'],
            #         'users': ['read', 'moderate'],
            #         'reports': ['read', 'resolve'],
            #     },
            #     'is_active': True,
            # },
            # {
            #     'name': 'admin',
            #     'description': 'Administrator with full permissions',
            #     'permissions': {
            #         'all': True,  # Simple flag for full access
            #     },
            #     'is_active': True,
            # },
        ]
        
        created_count = 0
        updated_count = 0
        
        for role_data in default_roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions'],
                    'is_active': role_data['is_active'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created role: {role.name}")
                )
            else:
                # Optionally update existing role
                # Uncomment the following lines to update existing roles
                # role.description = role_data['description']
                # role.permissions = role_data['permissions']
                # role.is_active = role_data['is_active']
                # role.save()
                # updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Role already exists: {role.name}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSummary: {created_count} role(s) created, {updated_count} role(s) updated"
            )
        )
        
        # Display instructions
        self.stdout.write(
            self.style.SUCCESS(
                "\nTo extend permissions in the future:"
                "\n1. Add new permission keys to the JSON structure in admin panel"
                "\n2. Or modify the default_roles list in this command"
                "\n3. Run this command again to create new roles"
                "\n4. No database migration needed for permission changes"
            )
        )
