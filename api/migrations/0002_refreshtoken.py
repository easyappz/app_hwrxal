# Generated migration for RefreshToken model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
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
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['token', 'is_revoked'], name='refresh_tok_token_idx'),
        ),
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['user', 'is_revoked', 'expires_at'], name='refresh_tok_user_idx'),
        ),
        migrations.AddIndex(
            model_name='refreshtoken',
            index=models.Index(fields=['expires_at'], name='refresh_tok_expires_idx'),
        ),
    ]
