# Generated by Django 4.1.7 on 2023-05-23 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0017_alter_gasprice_options_and_more"),
        ("meter_readings", "0007_activatedreading_delete_newreading"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activatedreading",
            name="smart_box",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_smartbox",
                to="asset.retailassigncylinder",
            ),
        ),
    ]
