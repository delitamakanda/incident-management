# Generated by Django 4.1.4 on 2024-07-21 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(choices=[('text', 'Text'), ('heading', 'Heading'), ('image', 'Image'), ('link', 'Link'), ('video', 'Video'), ('audio', 'Audio'), ('quote', 'Quote'), ('code', 'Code'), ('document', 'Document'), ('todo_list', 'Todo List')], default='text', max_length=20)),
                ('content', models.TextField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_blocks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Block',
                'verbose_name_plural': 'Blocks',
                'ordering': ['page', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_databases', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Database',
                'verbose_name_plural': 'Databases',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('members', models.ManyToManyField(blank=True, related_name='workspaces', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_workspaces', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Workspace',
                'verbose_name_plural': 'Workspaces',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('property_type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('dropdown', 'Dropdown'), ('multi_select', 'Multi-Select')], default='text', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='workspaces.database')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_pages', to=settings.AUTH_USER_MODEL)),
                ('parent_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='workspaces.page')),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='workspaces.workspace')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DatabaseRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_database_rows', to=settings.AUTH_USER_MODEL)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='workspaces.database')),
            ],
            options={
                'verbose_name': 'Database Row',
                'verbose_name_plural': 'Database Rows',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='database',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='databases', to='workspaces.workspace'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.block')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='block',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='workspaces.page'),
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted')], max_length=20)),
                ('action', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.block')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Activity Log',
                'verbose_name_plural': 'Activity Logs',
                'ordering': ['-id'],
            },
        ),
    ]
