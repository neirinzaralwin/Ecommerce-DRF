# Generated by Django 4.1.6 on 2023-10-10 17:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 10, 10, 17, 41, 30, 503522, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 10, 10, 17, 41, 30, 503652, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
