# Generated by Django 4.2.2 on 2023-08-01 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_subscriber_activation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='is_active',
        ),
    ]
