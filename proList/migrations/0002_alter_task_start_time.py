# Generated by Django 5.0.4 on 2024-05-06 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proList', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 6, 7, 24, 11, 631934, tzinfo=datetime.timezone.utc)),
        ),
    ]
