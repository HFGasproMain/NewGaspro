from django.db import models
from accounts.models import User
from django.utils import timezone
from decimal import Decimal

# Create your models here.

# Unassigned Cylinder
class Cylinder(models.Model):
    cy_types = (
		('12kg', '12kg'),
		('25kg', '25kg'),
		('50kg', '50kg'),)
    cy_status = (
        ('assigned', 'assigned'),
        ('unassigned', 'unassigned'))
    location_choices = (
        ('storage', 'storage'),
        ('plant','plant'),
        ('maintenance_hub', 'maintenance_hub'),
        ('logistic_officer', 'logistic_officer')
        )
    actor_choices = (
        ('DO','DO'),
        ('RO', 'RO'),
        ('HQ', 'HQ'),
        ('RU', 'RU')
        )
    gas_content_choices = (
        ('contentF', 'contentF'),
        ('remnant', 'remnant')
        )
    cylinder_capacity = models.CharField(max_length=5, choices=cy_types, blank=True)
    cylinder_serial_number = models.CharField(max_length=10, primary_key=True)
    cylinder_gas_content = models.DecimalField(decimal_places=2, max_digits=5, null=True, default=12.00) # two types of gas_content => contentF & gas_remnant (contentF - 0.3kg)
    cylinder_total_weight = models.DecimalField(max_digits=5, decimal_places=2)
    cylinder_status = models.CharField(max_length=20, choices=cy_status, blank=True, default='unassigned')
    manufacturer = models.CharField(max_length=30, default="Homefort Energy")
    cylinder_tare_weight = models.DecimalField(max_digits=5, decimal_places=2)
    manufactured_date = models.DateField() # date it was manufactured
    date_added = models.DateField(auto_now_add=True) # date it was added to the warehouse 
    maintenance_date = models.DateField()
    current_actor = models.CharField(max_length=2, choices=actor_choices, default='HQ')
    location = models.CharField(max_length=20, choices=location_choices, null=True, blank=True, default='storage')
    expiry_status = models.BooleanField(default=False)
    gas_content_type = models.CharField(max_length=10, choices=gas_content_choices, null=True, default='contentF')

    # actor that register it, total_weight & actor/location of the cyinder are what you're tracking.
    # actors: customer, DO, RO, HQ--> Logistic officer, plant, maintenance hub, storage
    #RO audit DO. LO audit RO
    
    # cy_tare_weight = initial_cy_weight, cy_total_weight = cy_tare_weight + capacity/gas content, 
    # qty_gas_left = cy_total_weight - cy_tare_weight
    # deduct remnant from old bottle from content/capacity of new bottle => qty delivered & qty billable.



    def __str__(self):
        return '{},{}'.format(self.cylinder_serial_number, self.cylinder_status)

    def save(self, *args, **kwargs):
        # Sum cylinder_wotal_weight
        self.cylinder_total_weight = self.cylinder_tare_weight + self.cylinder_gas_content
        
        # Calculate the maintenance_date and expiry_status
        self.maintenance_date = self.manufactured_date + timezone.timedelta(days=365 * 10)
        if self.maintenance_date < timezone.now().date():
            self.expiry_status = True

        # Find gas_content_level
        if self.pk is None:
            # New instance being created
            self.gas_content_type = 'contentF'
        else:
            try:
                existing_instance = Cylinder.objects.get(pk=self.pk)
            except Cylinder.DoesNotExist:
                # Existing instance not found
                print('Cylinder DoesNotExist!')
                pass
            else:
                if self.cylinder_gas_content < existing_instance.cylinder_gas_content - Decimal(0.3):
                    self.gas_content_type = 'remnant'
                else:
                    self.gas_content_type = 'contentF'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_added']



# Smart Scale     
class SmartScale(models.Model):
    ss_status = (
        ('assigned', 'assigned'),
        ('unassigned', 'unassigned'))
    scale_id = models.CharField(max_length=10, primary_key=True)
    manufacturer = models.CharField(max_length=100, default="Homefort Energy")
    smartscale_status = models.CharField(max_length=20, choices=ss_status, blank=True, default='unassigned')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.scale_id

# Smart Box
class SmartBox(models.Model):
    sb_status = (
        ('assigned', 'assigned'),
        ('unassigned', 'unassigned'))
    box_id = models.CharField(max_length=10, primary_key=True)
    manufacturer = models.CharField(max_length=100, default="Homefort Energy")
    smartbox_status = models.CharField(max_length=20, choices=sb_status, blank=True, default='unassigned')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{},{}'.format(self.box_id, self.smartbox_status)

    class Meta:
        ordering = ['-date_created']


# Assigned Cylinders
class SMEAssignCylinder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_cylinder", blank=True)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, null=True)
    smart_scale = models.ForeignKey(SmartScale, on_delete=models.CASCADE, null=True, blank=True)
    smart_box = models.ForeignKey(SmartBox, on_delete=models.CASCADE, null=True, blank=True)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
    	ordering = ('-assigned_date',)


class ResidentialAssignCylinder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retail_assigned_cylinder", blank=True)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, null=True)
    smart_box = models.ForeignKey(SmartBox, on_delete=models.CASCADE, null=True, blank=True)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{},{},{}'.format(str(self.user), str(self.cylinder), str(self.smart_box))

    class Meta:
        ordering = ('-assigned_date',)


# Is this not redundant?
class CylinderMovement(models.Model):
    operations_staff = models.CharField(max_length=20)
    operations_staff_name = models.CharField(max_length=50)
    cylinder = models.CharField(max_length=30)
    from_location = models.CharField(max_length=30, null=True, blank=True)
    to_location = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=30, null=True, blank=True)
    history_type = models.CharField(max_length=30, default="Regular")
    cylinder_status = models.CharField(max_length=30, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.operations_staff


class GasPrice(models.Model):
    current_price = models.DecimalField(max_length=10, max_digits=10, default='0.00', decimal_places=2)
    user = models.CharField(max_length=30, default='Homefort Admin', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)


class OtherBillableAssets(models.Model):
    low_pressure_regulator_price_per_yard = models.DecimalField(max_length=10, max_digits=10, default='0.00kg', decimal_places=2)
    high_pressure_regulator_price_per_yard = models.DecimalField(max_length=10, max_digits=10, default='0.00kg', decimal_places=2)
    low_pressure_hose_price_per_yard = models.DecimalField(max_length=10, max_digits=10, default='0.00kg', decimal_places=2)
    high_pressure_hose_price_per_yard = models.DecimalField(max_length=10, max_digits=10, default='0.00kg', decimal_places=2)
    subsidized_cylinder_price = models.DecimalField(max_length=10, max_digits=10, default='0.00kg', decimal_places=2)
    user = models.CharField(max_length=30, default='Homefort Admin', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
