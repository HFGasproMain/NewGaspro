# Generated by Django 4.1.7 on 2023-06-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0011_rename_approved_date_refillorder_action_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="refillorder",
            name="action",
            field=models.CharField(
                blank=True,
                choices=[("accept", "Accept"), ("reschedule", "Reschedule")],
                max_length=20,
                null=True,
            ),
        ),
    ]
