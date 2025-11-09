from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import User, Role
import getpass
import sys


class Command(BaseCommand):
    """
    Create a superuser with all permissions and optional role assignment.
    
    This command creates a Django superuser that has:
    - is_superuser=True (bypasses all permission checks)
    - is_staff=True (can access admin panel)
    - Optional role assignment for application-level permissions
    
    Usage:
        # Interactive mode
        python manage.py create_superuser_with_role
        
        # Non-interactive mode
        python manage.py create_superuser_with_role \
            --email admin@example.com \
            --password mysecurepassword \
            --first-name Admin \
            --last-name User \
            --role admin \
            --noinput
    
    The superuser will have all permissions regardless of role assignment.
    Role assignment is optional and useful for:
    - Testing role-based permissions
    - Maintaining consistency in user management
    - Displaying role information in admin panel
    """
    
    help = 'Create a superuser with all permissions and optional role assignment'
    
    def add_arguments(self, parser):
        """
        Add command line arguments.
        """
        parser.add_argument(
            '--email',
            type=str,
            help='Email address for the superuser',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser',
        )
        parser.add_argument(
            '--first-name',
            type=str,
            default='',
            help='First name of the superuser',
        )
        parser.add_argument(
            '--last-name',
            type=str,
            default='',
            help='Last name of the superuser',
        )
        parser.add_argument(
            '--role',
            type=str,
            help='Role name to assign to the superuser (optional)',
        )
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_true',
            help='Do not prompt for any input',
        )
        parser.add_argument(
            '--create-admin-role',
            action='store_true',
            help='Create an admin role if it does not exist',
        )

    def handle(self, *args, **options):
        """
        Execute the command to create a superuser with role.
        """
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name', '')
        last_name = options.get('last_name', '')
        role_name = options.get('role')
        no_input = options.get('noinput', False)
        create_admin_role = options.get('create_admin_role', False)
        
        self.stdout.write(
            self.style.MIGRATE_HEADING('\n=== Create Superuser with Role ===')
        )
        
        # Interactive mode
        if not no_input:
            if not email:
                email = self._get_input('Email address: ')
            
            if not password:
                password = self._get_password()
            
            if not first_name:
                first_name = self._get_input('First name (optional): ', required=False)
            
            if not last_name:
                last_name = self._get_input('Last name (optional): ', required=False)
            
            if not role_name:
                self._display_available_roles()
                role_name = self._get_input(
                    'Role name to assign (optional, press Enter to skip): ',
                    required=False
                )
        
        # Validate required fields
        if not email:
            raise CommandError('Email address is required')
        
        if not password:
            raise CommandError('Password is required')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise CommandError(f"User with email '{email}' already exists")
        
        try:
            with transaction.atomic():
                # Create superuser
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Superuser created: {user.email}")
                )
                self.stdout.write(
                    f"  Name: {user.get_full_name() or 'Not provided'}"
                )
                self.stdout.write(
                    f"  Superuser: Yes"
                )
                self.stdout.write(
                    f"  Staff: Yes"
                )
                
                # Assign role if specified
                if role_name:
                    role = self._get_or_create_role(role_name, create_admin_role)
                    if role:
                        user.roles.add(role)
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ Assigned role: '{role.name}'")
                        )
                        if role.permissions:
                            self.stdout.write(
                                f"  Role permissions: {role.permissions}"
                            )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ Role '{role_name}' not found and not created"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.NOTICE('→ No role assigned')
                    )
                
                self.stdout.write(
                    self.style.MIGRATE_HEADING('\n=== Important Notes ===')
                )
                self.stdout.write(
                    "• This superuser has ALL permissions (is_superuser=True)"
                )
                self.stdout.write(
                    "• Superuser status bypasses all role-based permission checks"
                )
                self.stdout.write(
                    "• The assigned role is for organizational purposes only"
                )
                self.stdout.write(
                    "• This user can access the Django admin panel"
                )
                self.stdout.write(
                    self.style.SUCCESS('\n=== Superuser Creation Complete ===')
                )
                
        except Exception as e:
            raise CommandError(f"Error creating superuser: {str(e)}")
    
    def _get_input(self, prompt, required=True):
        """
        Get input from user with validation.
        """
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            self.stdout.write(
                self.style.ERROR('This field is required')
            )
    
    def _get_password(self):
        """
        Get password from user with confirmation.
        """
        while True:
            password = getpass.getpass('Password: ')
            if not password:
                self.stdout.write(
                    self.style.ERROR('Password cannot be empty')
                )
                continue
            
            password_confirm = getpass.getpass('Password (again): ')
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('Passwords do not match')
                )
                continue
            
            if len(password) < 8:
                self.stdout.write(
                    self.style.WARNING(
                        'Warning: Password is short (less than 8 characters)'
                    )
                )
                confirm = input('Continue anyway? (y/N): ')
                if confirm.lower() != 'y':
                    continue
            
            return password
    
    def _display_available_roles(self):
        """
        Display available roles to the user.
        """
        roles = Role.objects.filter(is_active=True)
        if roles.exists():
            self.stdout.write('\nAvailable roles:')
            for role in roles:
                self.stdout.write(f"  • {role.name}: {role.description}")
            self.stdout.write('')
        else:
            self.stdout.write(
                self.style.WARNING('\nNo active roles found in the database')
            )
            self.stdout.write(
                'Run "python manage.py init_roles" to create default roles\n'
            )
    
    def _get_or_create_role(self, role_name, create_if_missing=False):
        """
        Get an existing role or optionally create it.
        """
        try:
            return Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            if create_if_missing and role_name.lower() == 'admin':
                # Create admin role with all permissions
                role = Role.objects.create(
                    name='admin',
                    description='Administrator role with full system permissions',
                    permissions={'all': True},
                    is_active=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created admin role")
                )
                return role
            return None
