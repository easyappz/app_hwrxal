from django.core.management.base import BaseCommand
from api.models import Role


class Command(BaseCommand):
    """
    Management command to create default roles for the application.
    
    Usage:
        python manage.py create_default_roles
    
    This command is idempotent - it won't create duplicate roles if they already exist.
    """
    
    help = 'Creates default roles (user) for the application'

    def handle(self, *args, **options):
        """
        Create default 'user' role with basic permissions.
        """
        
        # Define default role configuration
        default_roles = [
            {
                'name': 'user',
                'description': 'Default user role with basic permissions',
                'permissions': {
                    # Example permission structure - can be extended as needed
                    # Using grouped by resource structure:
                    'profile': ['read', 'update'],
                    'posts': ['create', 'read'],
                    'comments': ['create', 'read'],
                    
                    # Alternative: simple list structure
                    # 'permissions': [
                    #     'read_profile',
                    #     'update_profile',
                    #     'create_post',
                    #     'read_post',
                    # ]
                },
                'is_active': True,
            },
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
                    self.style.SUCCESS(
                        f"✓ Created role '{role.name}'"
                    )
                )
            else:
                # Update existing role if needed
                updated = False
                if role.description != role_data['description']:
                    role.description = role_data['description']
                    updated = True
                if role.permissions != role_data['permissions']:
                    role.permissions = role_data['permissions']
                    updated = True
                if role.is_active != role_data['is_active']:
                    role.is_active = role_data['is_active']
                    updated = True
                
                if updated:
                    role.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"⟳ Updated role '{role.name}'"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"→ Role '{role.name}' already exists and is up to date"
                        )
                    )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSummary: {created_count} created, {updated_count} updated"
            )
        )
        
        # Show instructions for extending
        if created_count > 0:
            self.stdout.write(
                self.style.NOTICE(
                    "\nTo add more roles or modify permissions:"
                )
            )
            self.stdout.write(
                "  1. Use Django admin panel at /admin/api/role/"
            )
            self.stdout.write(
                "  2. Or modify this management command and run it again"
            )
            self.stdout.write(
                "  3. Or create roles programmatically in your code"
            )
