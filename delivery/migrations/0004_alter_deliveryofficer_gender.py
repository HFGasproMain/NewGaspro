# Generated by Django 4.1.7 on 2023-06-21 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0003_rename_ro_deliveryofficer_manager"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveryofficer",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")], max_length=10
            ),
        ),
    ]
