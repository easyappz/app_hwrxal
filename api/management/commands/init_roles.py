from django.core.management.base import BaseCommand
from api.models import Role


class Command(BaseCommand):
    """
    Initialize default roles for the application.
    
    This command is idempotent - it can be run multiple times safely.
    It will only create roles that don't exist yet.
    
    Usage:
        python manage.py init_roles
    
    To add new default roles:
    1. Add a new dictionary to the DEFAULT_ROLES list below
    2. Define the role name, description, and permissions structure
    3. Run this command again - it will only create new roles
    
    Permission Structure Best Practices:
    - Use grouped structure by resource (e.g., 'posts', 'comments', 'users')
    - Define actions as lists (e.g., ['create', 'read', 'update', 'delete'])
    - For complex permissions, use nested dicts with conditions
    - Keep permission names consistent across roles
    - Document custom permission logic in the has_permission() method
    
    Example permission structures:
    
    1. Simple grouped permissions:
    {
        'posts': ['create', 'read', 'update', 'delete'],
        'comments': ['create', 'read', 'update', 'delete'],
    }
    
    2. With conditions:
    {
        'posts': {
            'create': True,
            'read': True,
            'update': {'condition': 'own_only'},
            'delete': {'condition': 'own_only'},
        }
    }
    
    3. Global permission:
    {
        'all': True  # Administrator with all permissions
    }
    """
    
    help = 'Initialize default roles with permissions (idempotent operation)'
    
    # ### DEFAULT ROLES CONFIGURATION ###
    # Define all default roles here
    # This list can be extended without modifying the command logic
    DEFAULT_ROLES = [
        {
            'name': 'user',
            'description': 'Standard user role with basic permissions for profile management and content creation',
            'permissions': {
                # Profile permissions
                'profile': {
                    'view': True,
                    'edit': True,
                },
                # Content permissions - user has full control
                # These are examples - adjust based on your application needs
                'content': {
                    'create': True,
                    'read': True,
                    'update': True,
                    'delete': True,
                },
            },
            'is_active': True,
        },
        
        # ### EXAMPLE: Additional roles (uncomment and modify as needed) ###
        
        # {
        #     'name': 'moderator',
        #     'description': 'Moderator role with permissions to manage user content and handle reports',
        #     'permissions': {
        #         'profile': {
        #             'view': True,
        #             'edit': True,
        #         },
        #         'content': {
        #             'create': True,
        #             'read': True,
        #             'update': True,
        #             'delete': True,
        #         },
        #         'moderation': {
        #             'view_reports': True,
        #             'resolve_reports': True,
        #             'moderate_content': True,
        #             'suspend_users': False,  # Only admins can suspend
        #         },
        #         'users': {
        #             'view': True,
        #             'view_details': True,
        #         },
        #     },
        #     'is_active': True,
        # },
        
        # {
        #     'name': 'admin',
        #     'description': 'Administrator role with full system permissions',
        #     'permissions': {
        #         # Simple flag for full access - all permissions granted
        #         'all': True,
        #         # Or you can define granular permissions:
        #         # 'profile': ['view', 'edit', 'delete'],
        #         # 'content': ['create', 'read', 'update', 'delete', 'publish', 'unpublish'],
        #         # 'users': ['view', 'create', 'update', 'delete', 'suspend', 'activate'],
        #         # 'roles': ['view', 'create', 'update', 'delete', 'assign'],
        #         # 'settings': ['view', 'update'],
        #         # 'moderation': ['view_reports', 'resolve_reports', 'moderate_content'],
        #     },
        #     'is_active': True,
        # },
        
        # {
        #     'name': 'viewer',
        #     'description': 'Read-only role with limited permissions',
        #     'permissions': {
        #         'profile': {
        #             'view': True,
        #             'edit': False,
        #         },
        #         'content': {
        #             'create': False,
        #             'read': True,
        #             'update': False,
        #             'delete': False,
        #         },
        #     },
        #     'is_active': True,
        # },
        
        # {
        #     'name': 'premium_user',
        #     'description': 'Premium user with extended permissions',
        #     'permissions': {
        #         'profile': {
        #             'view': True,
        #             'edit': True,
        #         },
        #         'content': {
        #             'create': True,
        #             'read': True,
        #             'update': True,
        #             'delete': True,
        #         },
        #         'premium_features': {
        #             'advanced_analytics': True,
        #             'priority_support': True,
        #             'custom_branding': True,
        #         },
        #     },
        #     'is_active': True,
        # },
    ]
    # ### END DEFAULT ROLES CONFIGURATION ###

    def add_arguments(self, parser):
        """
        Add command line arguments.
        """
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing roles with new permissions (use with caution)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed information about each role',
        )

    def handle(self, *args, **options):
        """
        Execute the command to initialize default roles.
        """
        update_existing = options.get('update', False)
        verbose = options.get('verbose', False)
        
        self.stdout.write(
            self.style.MIGRATE_HEADING('\n=== Initializing Default Roles ===')
        )
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for role_data in self.DEFAULT_ROLES:
            role_name = role_data['name']
            
            try:
                role, created = Role.objects.get_or_create(
                    name=role_name,
                    defaults={
                        'description': role_data['description'],
                        'permissions': role_data['permissions'],
                        'is_active': role_data['is_active'],
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Created role: '{role.name}'")
                    )
                    if verbose:
                        self.stdout.write(
                            f"  Description: {role.description}"
                        )
                        self.stdout.write(
                            f"  Permissions: {role.permissions}"
                        )
                else:
                    if update_existing:
                        # Update existing role
                        role.description = role_data['description']
                        role.permissions = role_data['permissions']
                        role.is_active = role_data['is_active']
                        role.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"↻ Updated role: '{role.name}'")
                        )
                        if verbose:
                            self.stdout.write(
                                f"  New permissions: {role.permissions}"
                            )
                    else:
                        skipped_count += 1
                        self.stdout.write(
                            self.style.NOTICE(f"→ Role already exists: '{role.name}' (skipped)")
                        )
                        if verbose:
                            self.stdout.write(
                                f"  Current permissions: {role.permissions}"
                            )
                            self.stdout.write(
                                f"  Use --update flag to update existing roles"
                            )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Error creating role '{role_name}': {str(e)}")
                )
        
        # Summary
        self.stdout.write(
            self.style.MIGRATE_HEADING('\n=== Summary ===')
        )
        self.stdout.write(
            self.style.SUCCESS(f"Roles created: {created_count}")
        )
        if update_existing:
            self.stdout.write(
                self.style.WARNING(f"Roles updated: {updated_count}")
            )
        if skipped_count > 0:
            self.stdout.write(
                self.style.NOTICE(f"Roles skipped: {skipped_count}")
            )
        
        # Instructions
        self.stdout.write(
            self.style.MIGRATE_HEADING('\n=== Usage Instructions ===')
        )
        self.stdout.write(
            "To add new default roles:"
        )
        self.stdout.write(
            "  1. Edit api/management/commands/init_roles.py"
        )
        self.stdout.write(
            "  2. Add a new role dictionary to DEFAULT_ROLES list"
        )
        self.stdout.write(
            "  3. Run: python manage.py init_roles"
        )
        self.stdout.write(
            "\nTo update existing roles:"
        )
        self.stdout.write(
            "  python manage.py init_roles --update"
        )
        self.stdout.write(
            "\nTo view detailed information:"
        )
        self.stdout.write(
            "  python manage.py init_roles --verbose"
        )
        self.stdout.write(
            "\nPermission naming best practices:"
        )
        self.stdout.write(
            "  - Use resource-based grouping: 'posts', 'comments', 'users'"
        )
        self.stdout.write(
            "  - Use standard CRUD actions: 'create', 'read', 'update', 'delete'"
        )
        self.stdout.write(
            "  - Add custom actions as needed: 'publish', 'moderate', 'export'"
        )
        self.stdout.write(
            "  - Use consistent naming across all roles"
        )
        self.stdout.write(
            self.style.SUCCESS('\n=== Initialization Complete ===')
        )
