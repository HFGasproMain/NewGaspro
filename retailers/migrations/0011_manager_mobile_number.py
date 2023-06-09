# Generated by Django 4.1.7 on 2023-06-07 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0010_manager_manager_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="manager",
            name="mobile_number",
            field=models.CharField(
                blank=True,
                max_length=11,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="must be a valid phone number", regex="^[0]\\d{10}$"
                    )
                ],
            ),
        ),
    ]
