from django.core.management.base import BaseCommand
from api.models import Role


class Command(BaseCommand):
    """
    DEPRECATED: This command is replaced by 'init_roles'.
    
    Please use: python manage.py init_roles
    
    This command is kept for backward compatibility but redirects to init_roles.
    """
    
    help = 'DEPRECATED: Use "python manage.py init_roles" instead'

    def handle(self, *args, **options):
        """
        Display deprecation warning and redirect to init_roles.
        """
        self.stdout.write(
            self.style.WARNING(
                '\n' + '='*70
            )
        )
        self.stdout.write(
            self.style.WARNING(
                'DEPRECATION WARNING'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '='*70
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nThe "create_default_roles" command is deprecated.'
            )
        )
        self.stdout.write(
            self.style.NOTICE(
                'Please use: python manage.py init_roles'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nThis command will be removed in a future version.'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '='*70 + '\n'
            )
        )
        
        # Import and call the new command
        from django.core.management import call_command
        call_command('init_roles')
