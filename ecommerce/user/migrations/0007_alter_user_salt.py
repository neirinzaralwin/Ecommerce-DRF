# Generated by Django 4.1.6 on 2024-01-11 08:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0006_alter_user_salt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="salt",
            field=models.CharField(default="wCtRwnuaKysw", max_length=12),
        ),
    ]
