# Generated by Django 4.1.6 on 2023-11-28 03:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_alter_user_salt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="salt",
            field=models.CharField(default="awxd3LPcwe82", max_length=12),
        ),
    ]
