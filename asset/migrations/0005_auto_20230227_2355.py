# Generated by Django 3.2 on 2023-02-27 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset', '0004_remove_assigncylinder_cylinder_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assigncylinder',
            options={'ordering': ('-date_assigned',)},
        ),
        migrations.AlterField(
            model_name='assigncylinder',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_cylinder', to=settings.AUTH_USER_MODEL),
        ),
    ]
