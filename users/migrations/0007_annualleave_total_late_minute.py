# Generated by Django 4.2.16 on 2024-11-24 01:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_annualleave"),
    ]

    operations = [
        migrations.AddField(
            model_name="annualleave",
            name="total_late_minute",
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]