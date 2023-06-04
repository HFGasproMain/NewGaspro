# Generated by Django 4.1.7 on 2023-06-03 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_refillorder_delete_bottleswaporder"),
    ]

    operations = [
        migrations.AlterField(
            model_name="refillorder",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("pending", "pending"),
                    ("approved", "approved"),
                    ("ongoing", "ongoing"),
                    ("delivered", "delivered"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]