# Generated by Django 4.1.6 on 2023-10-08 06:02

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
                    2023, 10, 8, 6, 2, 22, 157397, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 10, 8, 6, 2, 22, 157525, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
