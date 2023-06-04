# Generated by Django 4.1.7 on 2023-06-02 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0027_rename_retailassigncylinder_residentialassigncylinder"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meter_readings", "0013_collectgasreading_residential_assign_meter"),
    ]

    operations = [
        migrations.CreateModel(
            name="GasMeterStatus",
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
                ("first_name", models.CharField(blank=True, max_length=50)),
                ("last_name", models.CharField(blank=True, max_length=50)),
                ("battery_remaining", models.CharField(max_length=10, null=True)),
                (
                    "quantity_remaining",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                ("last_push", models.DateTimeField()),
                (
                    "cylinder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="asset.cylinder"
                    ),
                ),
                (
                    "smart_box",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="asset.smartbox"
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-last_push",),
            },
        ),
    ]