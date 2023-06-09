# Generated by Django 4.1.7 on 2023-06-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0007_manager_date_created_staff_date_created"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="retailers",
            name="email",
        ),
        migrations.RemoveField(
            model_name="retailers",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="retailers",
            name="last_name",
        ),
        migrations.AddField(
            model_name="retailers",
            name="business_email",
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name="retailers",
            name="business_state",
            field=models.CharField(
                choices=[
                    ("Abia", "Abia"),
                    ("Adamawa", "Adamawa"),
                    ("Akwa Ibom", "Akwa Ibom"),
                    ("Anambra", "Anambra"),
                    ("Bauchi", "Bauchi"),
                    ("Bayelsa", "Bayelsa"),
                    ("Benue", "Benue"),
                    ("Borno", "Borno"),
                    ("Cross River", "Cross River"),
                    ("Delta", "Delta"),
                    ("Ebonyi", "Ebonyi"),
                    ("Edo", "Edo"),
                    ("Ekiti", "Ekiti"),
                    ("Enugu", "Enugu"),
                    ("FCT", "FCT"),
                    ("Gombe", "Gombe"),
                    ("Imo", "Imo"),
                    ("Jigawa", "Jigawa"),
                    ("Kaduna", "Kaduna"),
                    ("Kano", "Kano"),
                    ("Katsina", "Katsina"),
                    ("Kebbi", "Kebbi"),
                    ("Kogi", "Kogi"),
                    ("Kwara", "Kwara"),
                    ("Lagos", "Lagos"),
                    ("Nasarawa", "Nasarawa"),
                    ("Niger", "Niger"),
                    ("Ogun", "Ogun"),
                    ("Ondo", "Ondo"),
                    ("Osun", "Osun"),
                    ("Oyo", "Oyo"),
                    ("Plateau", "Plateau"),
                    ("Rivers", "Rivers"),
                    ("Sokoto", "Sokoto"),
                    ("Taraba", "Taraba"),
                    ("Yobe", "Yobe"),
                    ("Zamfara", "Zamfara"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
