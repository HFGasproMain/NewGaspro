# Generated by Django 4.1.7 on 2023-06-02 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meter_readings", "0015_gasmeterstatus_quantity_supplied_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gasmeterstatus",
            name="user_id",
        ),
    ]