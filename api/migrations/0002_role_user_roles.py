# Generated migration for Role model and User.roles relationship

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, help_text='The roles this user belongs to. A user will get all permissions granted to each of their roles.', related_name='users', to='api.role', verbose_name='Roles'),
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['name', 'is_active'], name='roles_name_f0c4e1_idx'),
        ),
    ]
