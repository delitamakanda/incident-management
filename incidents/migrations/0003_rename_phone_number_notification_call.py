# Generated by Django 4.1.4 on 2023-04-16 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_incidents_notes_incidents_statut_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='phone_number',
            new_name='call',
        ),
    ]