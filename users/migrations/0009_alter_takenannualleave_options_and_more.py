# Generated by Django 4.2.16 on 2024-11-24 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_annualleave_notify_sent_alter_annualleave_user_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="takenannualleave",
            options={"ordering": ["-id"]},
        ),
        migrations.AddField(
            model_name="takenannualleave",
            name="description",
            field=models.TextField(default=123),
            preserve_default=False,
        ),
    ]
