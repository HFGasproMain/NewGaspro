# Generated by Django 4.1.7 on 2023-06-21 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0010_refillorder_approved_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="refillorder",
            old_name="approved_date",
            new_name="action_date",
        ),
        migrations.RemoveField(
            model_name="refillorder",
            name="rescheduled_date",
        ),
    ]
