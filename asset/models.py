from django.db import models
from accounts.models import User

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
    cylinder_type = models.CharField(max_length=20, choices=cy_types, blank=True)
    cylinder_serial_number = models.CharField(max_length=20, primary_key=True)
    cylinder_weight = models.FloatField()
    cylinder_status = models.CharField(max_length=20, choices=cy_status, blank=True, default='unassigned')
    manufacturer = models.CharField(max_length=30, default="Amaze Gas")
    cylinder_tar_weight = models.DecimalField(max_length=10, max_digits=10, decimal_places=2)
    manufacture_date = models.DateField() # date it was manufactured
    date_added = models.DateField(auto_now_add=True) # date it was added to the warehouse 
    maintenance_date = models.DateField()
    
    def __str__(self):
        return '{},{}'.format(self.cylinder_serial_number, self.cylinder_status)

    class Meta:
        ordering = ['-date_added']


#cy_tare_weight = initial_cy_weight, cy_total_weight = cy_tare_weight + capacity/gas content, 
# qty_gas_left = cy_total_weight - cy_tare_weight
# deduct remnant from old bottle from content/capacity of new bottle => qty delivered & qty billable.

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


class RetailAssignCylinder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retail_assigned_cylinder", blank=True)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, null=True)
    smart_box = models.ForeignKey(SmartBox, on_delete=models.CASCADE, null=True, blank=True)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

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