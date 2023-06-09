# Generated by Django 4.1.7 on 2023-06-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="wallet",
            name="debt",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
