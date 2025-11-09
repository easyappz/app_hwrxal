# Generated migration for Role-based authentication system

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        # Create Role model
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text="Unique name for the role (e.g., 'user', 'admin', 'moderator')", max_length=50, unique=True, verbose_name='Role name')),
                ('description', models.TextField(blank=True, help_text='Description of what this role can do', verbose_name='Description')),
                ('permissions', models.JSONField(blank=True, default=dict, help_text='JSON object storing flexible permission structure. Can be extended without schema changes.', verbose_name='Permissions')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this role is currently active. Inactive roles will not grant permissions.', verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'roles',
                'ordering': ['name'],
            },
        ),
        # Create RefreshToken model
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, help_text='Unique refresh token string', max_length=255, unique=True, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When this token was created', verbose_name='Created at')),
                ('expires_at', models.DateTimeField(help_text='When this token expires', verbose_name='Expires at')),
                ('is_revoked', models.BooleanField(db_index=True, default=False, help_text='Whether this token has been manually revoked', verbose_name='Revoked')),
                ('revoked_at', models.DateTimeField(blank=True, help_text='When this token was revoked', null=True, verbose_name='Revoked at')),
                ('user_agent', models.TextField(blank=True, help_text='User agent string from the device that created this token', verbose_name='User agent')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address from which this token was created', null=True, verbose_name='IP address')),
                ('user', models.ForeignKey(help_text='User who owns this refresh token', on_delete=django.db.models.deletion.CASCADE, related_name='refresh_tokens', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Refresh Token',
                'verbose_name_plural': 'Refresh Tokens',
                'db_table': 'refresh_tokens',
                'ordering': ['-created_at'],
            },
        ),
        # Create PasswordResetToken model
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, help_text='Unique password reset token string', max_length=255, unique=True, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When this token was created', verbose_name='Created at')),
                ('expires_at', models.DateTimeField(help_text='When this token expires', verbose_name='Expires at')),
                ('is_used', models.BooleanField(db_index=True, default=False, help_text='Whether this token has been used', verbose_name='Used')),
                ('used_at', models.DateTimeField(blank=True, help_text='When this token was used', null=True, verbose_name='Used at')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address from which reset was requested', null=True, verbose_name='IP address')),
                ('user', models.ForeignKey(help_text='User who requested password reset', on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_tokens', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Password Reset Token',
                'verbose_name_plural': 'Password Reset Tokens',
                'db_table': 'password_reset_tokens',
                'ordering': ['-created_at'],
            },
        ),
        # Add roles field to User model
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, help_text='The roles this user belongs to. A user will get all permissions granted to each of their roles.', related_name='users', to='api.role', verbose_name='Roles'),
        ),
        # Add indexes for Role model
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['name', 'is_active'], name='roles_name_is_active_idx'),
        ),
        # Add indexes for RefreshToken model
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['token', 'is_revoked'], name='refresh_tokens_token_is_revoked_idx'),
        ),
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['user', 'is_revoked', 'expires_at'], name='refresh_tokens_user_is_revoked_expires_idx'),
        ),
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['expires_at'], name='refresh_tokens_expires_at_idx'),
        ),
        # Add indexes for PasswordResetToken model
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['token', 'is_used'], name='password_reset_tokens_token_is_used_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['user', 'is_used', 'expires_at'], name='password_reset_tokens_user_is_used_expires_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['expires_at'], name='password_reset_tokens_expires_at_idx'),
        ),
    ]
