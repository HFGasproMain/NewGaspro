# Generated by Django 4.1.7 on 2023-06-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meter_readings", "0016_remove_gasmeterstatus_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="gasmeterstatus",
            name="user_id",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="gasmeterstatus",
            name="cylinder",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="gasmeterstatus",
            name="smart_box",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
