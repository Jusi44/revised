# Generated by Django 5.2.1 on 2025-05-26 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_is_verified_profile_verification_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='verification_token',
        ),
    ]
