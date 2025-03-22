# Generated by Django 4.2.2 on 2025-02-04 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_delete_subscriber_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('firstname', models.CharField(blank=True, default='', max_length=100)),
                ('lastname', models.CharField(blank=True, default='', max_length=100)),
                ('phone', models.PositiveBigIntegerField(blank=True, null=True, unique=True)),
                ('subscribed_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('firstname', models.CharField(blank=True, default='', max_length=100)),
                ('lastname', models.CharField(blank=True, default='', max_length=100)),
                ('phone', models.PositiveBigIntegerField(blank=True, null=True, unique=True)),
                ('subscribed_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('activation_token', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
