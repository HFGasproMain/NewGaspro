# Generated by Django 4.1.7 on 2023-06-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0011_manager_mobile_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="manager",
            name="dob",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="dob",
        ),
        migrations.AlterField(
            model_name="manager",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")], max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")], max_length=10
            ),
        ),
    ]
