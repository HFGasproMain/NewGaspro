# Generated by Django 4.1.7 on 2023-05-25 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0019_cylinder_current_actor_cylinder_gas_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cylinder",
            name="current_actor",
            field=models.CharField(
                choices=[("DO", "DO"), ("RO", "RO"), ("HQ", "HQ"), ("RU", "RU")],
                default="HQ",
                max_length=2,
            ),
        ),
    ]
