# Generated by Django 4.1.4 on 2024-11-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='expiry_date',
            field=models.DateTimeField(null=True),
        ),
    ]
