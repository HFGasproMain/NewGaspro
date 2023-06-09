# Generated by Django 3.2 on 2023-03-10 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0010_auto_20230310_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cylinder',
            name='cylinder_status',
            field=models.CharField(blank=True, choices=[('assigned', 'assigned'), ('unassigned', 'unassigned')], default='unassigned', max_length=20),
        ),
        migrations.AlterField(
            model_name='smartbox',
            name='smartbox_status',
            field=models.CharField(blank=True, choices=[('assigned', 'assigned'), ('unassigned', 'unassigned')], default='unassigned', max_length=20),
        ),
        migrations.AlterField(
            model_name='smartscale',
            name='smartscale_status',
            field=models.CharField(blank=True, choices=[('assigned', 'assigned'), ('unassigned', 'unassigned')], default='unassigned', max_length=20),
        ),
    ]
