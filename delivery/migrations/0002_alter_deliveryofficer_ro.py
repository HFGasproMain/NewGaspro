# Generated by Django 4.1.7 on 2023-06-21 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0016_alter_manager_options"),
        ("delivery", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveryofficer",
            name="ro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="retail_outlet",
                to="retailers.retailers",
            ),
        ),
    ]
