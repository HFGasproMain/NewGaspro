from django.db import models
from accounts.models import User

# Create your models here.
reading_transmit_type = (
        ('time', 'time'),
        ('flow', 'flow')
    )

class SmartBoxReadings(models.Model):
    user = models.CharField(max_length=20, null=True, blank=True)
    smart_box = models.CharField(max_length=20)
    weight = models.FloatField(max_length=10, null=True)
    quantity_supplied = models.FloatField(max_length=10, null=True, blank=True, default="0")
    quantity_used = models.FloatField(max_length=10, null=True, blank=True)
    quantity_remaining = models.FloatField(max_length=10, null=True, blank=True)
    battery_remaining = models.DecimalField(decimal_places=2, max_digits=6)
    cylinder = models.CharField(max_length=20, null=True, blank=True)
    cylinder_tare_weight = models.CharField(max_length=20, null=True, blank=True)
    master = models.CharField(max_length=20, null=True, blank=True, default="0")
    master_battery_level = models.CharField(max_length=20, null=True, blank=True, default="0")
    min_transmit_time = models.CharField(max_length=20, null=True, blank=True, default="4")
    max_transmit_time = models.CharField(max_length=20, null=True, blank=True, default="25")
    min_value = models.CharField(max_length=20, null=True, blank=True, default="0")
    max_value = models.CharField(max_length=20, null=True, blank=True, default="0")
    transmit_type = models.CharField(max_length=20, choices=reading_transmit_type, default='time', blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True, default="0")
    latitude = models.CharField(max_length=20, null=True, blank=True, default="0")
    asset_type = models.CharField(max_length=20, default="smart_box")
    last_push = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-last_push']

    def __str__(self):
        return self.smart_box

#12kg; cylinder = 12kg, cylinder_tare_weight = initial_cylinder_weight


class NewReading(models.Model):
    user = models.CharField(max_length=20, null=True, blank=True)
    smart_scale = models.CharField(max_length=20)
    weight = models.FloatField(max_length=10)
    quantity_supplied = models.FloatField(max_length=10, null=True, blank=True, default="0")
    quantity_used = models.FloatField(max_length=10, null=True, blank=True)
    quantity_remaining = models.FloatField(max_length=10, null=True, blank=True)
    battery_remaining = models.DecimalField(decimal_places=2, max_digits=6)
    cylinder = models.CharField(max_length=20, null=True, blank=True)
    cylinder_tare_weight = models.CharField(max_length=20, null=True, blank=True)
    master = models.CharField(max_length=20, null=True, blank=True, default="0")
    master_battery_level = models.CharField(max_length=20, null=True, blank=True, default="0")
    min_value = models.CharField(max_length=20, null=True, blank=True, default="0")
    max_value = models.CharField(max_length=20, null=True, blank=True, default="0")
    longitude = models.CharField(max_length=20, null=True, blank=True, default="0")
    latitude = models.CharField(max_length=20, null=True, blank=True, default="0")
    asset_type = models.CharField(max_length=20, default="smart scale")
    last_push = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_push']

    def __str__(self):
        return self.smart_scale



class SmartScaleMonitor(models.Model):
    smart_scale = models.CharField(max_length=20)
    value = models.IntegerField()


class SmartBoxMonitor(models.Model):
    smart_box = models.CharField(max_length=20)
    value = models.IntegerField()


class Notification(models.Model):
    user = models.CharField(max_length=10, null=True, blank=True)
    header = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=100)
    notif_type = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.content


class Range(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.start_date)
