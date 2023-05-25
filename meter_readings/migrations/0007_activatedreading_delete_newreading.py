# Generated by Django 4.1.7 on 2023-05-23 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0017_alter_gasprice_options_and_more"),
        ("meter_readings", "0006_rename_smart_box_smartboxreadings_smart_box_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivatedReading",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(blank=True, max_length=20, null=True)),
                ("weight", models.FloatField(max_length=10)),
                (
                    "quantity_supplied",
                    models.FloatField(
                        blank=True, default="0", max_length=10, null=True
                    ),
                ),
                (
                    "quantity_used",
                    models.FloatField(blank=True, max_length=10, null=True),
                ),
                (
                    "quantity_remaining",
                    models.FloatField(blank=True, max_length=10, null=True),
                ),
                (
                    "battery_remaining",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                ("cylinder", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "cylinder_tare_weight",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "master",
                    models.CharField(blank=True, default="0", max_length=20, null=True),
                ),
                (
                    "master_battery_level",
                    models.CharField(blank=True, default="0", max_length=20, null=True),
                ),
                (
                    "min_value",
                    models.CharField(blank=True, default="0", max_length=20, null=True),
                ),
                (
                    "max_value",
                    models.CharField(blank=True, default="0", max_length=20, null=True),
                ),
                (
                    "longitude",
                    models.CharField(blank=True, default="0", max_length=20, null=True),
                ),
                (
                    "latitude",
                    models.CharField(blank=True, default="0", max_length=20, null=True),
                ),
                ("asset_type", models.CharField(default="smart_box", max_length=20)),
                ("last_push", models.DateTimeField(auto_now_add=True)),
                (
                    "smart_box",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="asset.retailassigncylinder",
                    ),
                ),
            ],
            options={"ordering": ["-last_push"],},
        ),
        migrations.DeleteModel(name="NewReading",),
    ]