# Generated by Django 3.2 on 2023-03-09 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20230308_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_onboarding',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
