# Generated by Django 3.2 on 2023-03-31 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailer',
            name='email',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
