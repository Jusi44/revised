# Generated by Django 5.2.1 on 2025-05-25 09:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0015_remove_workoutsession_duration_minutes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutsession',
            name='completed_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
