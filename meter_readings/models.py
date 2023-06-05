from django.db import models
from accounts.models import User
from asset.models import ResidentialAssignCylinder, SmartBox, Cylinder

# Create your models here.
class CollectGasReading(models.Model):
    smart_box_id = models.CharField(max_length=20, null=True, blank=True)
    quantity_used = models.FloatField(null=True, blank=True)
    quantity_remaining = models.FloatField(null=True, blank=True)
    battery_remaining = models.DecimalField(decimal_places=2, max_digits=6)
    longitude = models.CharField(max_length=20, null=True, blank=True, default="0")
    latitude = models.CharField(max_length=20, null=True, blank=True, default="0")
    residential_assign_meter = models.ForeignKey("asset.ResidentialAssignCylinder", on_delete=models.PROTECT, null=True, related_name='meter_readings')
    last_push = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # New instance, deduct from original quantity
            self.quantity_remaining -= self.gas_quantity_used
        else:  # Existing instance, deduct from current quantity
            previous_instance = MeterReadings.objects.get(pk=self.pk)
            previous_gas_quantity_used = previous_instance.gas_quantity_used
            self.quantity_remaining = previous_instance.quantity_remaining - (self.gas_quantity_used - previous_gas_quantity_used)

        super().save(*args, **kwargs)

    def create(self, validated_data):
        gas_quantity_used = validated_data.get('quantity_used')
        cylinder = validated_data.get('residential_assign_meter').cylinder

        # Calculate the remaining quantity
        quantity_remaining = cylinder.cylinder_total_weight - gas_quantity_used

        # Update the validated data with the calculated quantity_left
        validated_data['quantity_remaining'] = self.quantity_remaining

        return super().create(validated_data)

    def __str__(self):
        return self.smart_box_id


class GasMeterStatus(models.Model):
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    smart_box = models.CharField(max_length=30, blank=True)
    cylinder_serial_number = models.CharField(max_length=30, blank=True)
    quantity_supplied = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    quantity_used = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    battery_remaining = models.CharField(max_length=10,null=True)
    quantity_gas_left = models.DecimalField(decimal_places=2, max_digits=6)
    last_push = models.DateTimeField()

    def __str__(self):
        return self.smart_box

    class Meta:
        ordering = ('-last_push',)




reading_transmit_type = (
        ('time', 'time'),
        ('flow', 'flow')
    )

class SmartBoxReadings(models.Model):
    user = models.CharField(max_length=20, null=True, blank=True)
    smart_box_id = models.CharField(max_length=20)
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


class ActivatedSmartBoxReading(models.Model):
    user = models.CharField(max_length=20, null=True, blank=True)
    smart_box = models.ForeignKey(ResidentialAssignCylinder, on_delete=models.SET_NULL, null=True, related_name="activated_smartbox")
    cylinder = models.ForeignKey(ResidentialAssignCylinder, on_delete=models.SET_NULL, null=True, related_name="activated_cylinder")
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
    asset_type = models.CharField(max_length=20, default="smart_box")
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
