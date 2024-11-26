# Generated by Django 4.2.16 on 2024-11-24 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0007_annualleave_total_late_minute"),
    ]

    operations = [
        migrations.AddField(
            model_name="annualleave",
            name="notify_sent",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="annualleave",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="annual_leave",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="TakenAnnualLeave",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("leave_duration", models.DurationField()),
                (
                    "is_approved",
                    models.BooleanField(blank=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "annual_leave",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="taken_leaves",
                        to="users.annualleave",
                    ),
                ),
            ],
        ),
    ]
