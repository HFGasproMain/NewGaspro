from django.db import models
from accounts.models import User
from asset.models import SmartBox, Cylinder
from delivery.models import DeliveryOfficer
from django.utils.crypto import get_random_string


# Create your models here.

lagos_lga = (
		('Agege', 'Agege'),
		('Ajeromi-Ifelodun', 'Ajeromi-Ifelodun'),
		('Alimosho', 'Alimosho'),
		('Apapa', 'Apapa'),
		('Amuwo-Odofin', 'Amuwo-Odofin'),
		('Badagry', 'Badagry'),
		('Epe','Epe'),
		('Eti-Osa', 'Eti-Osa'),
		('Ibeju-Lekki','Ibeju-Lekki'),
		('Ifako-Ijaiye','Ifako-Ijaiye'),
		('Ikeja','Ikeja'),
		('Ikorodu','Ikorodu'),
		('Kosofe','Kosofe'),
		('Lagos Island','Lagos Island'),
		('Lagos Mainland','Lagos Mainland'),
		('Mushin','Mushin'),
		('Ojo','Ojo'),
		('Oshodi-Isolo','Oshodi-Isolo'),
		('Somolu','Somolu'),
		('Surulere','Surulere'),
	)

class OnboardingOrder(models.Model):
	cy_type = (
		('new_cylinder','new_cylinder'),
		('existing_cylinder', 'existing_cylinder')) 
	customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='onboard_order')
	cylinder_type = models.CharField(max_length=60, choices=cy_type, blank=True)
	state = models.CharField(max_length=60, default='Lagos')
	lga = models.CharField(max_length=60, choices=lagos_lga)
	home_address = models.TextField()
	order_transaction_id = models.CharField(max_length=200, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']
	
	def __str__(self):
		"""Customer Onboarding Order"""
		return self.cy_type



status_choices = (
		('pending', 'pending'),
		('resheduled', 'rescheduled'),
		('assigned', 'assigned'),
		('approved', 'approved'),
		('in progress', 'in progress'),
		('delivered', 'delivered')
	)

ACTION_CHOICES = [
        ('accept', 'Accept'),
        ('reschedule', 'Reschedule'),
        ('reject', 'Reject')
    ]

class RefillOrder(models.Model):
	order_id = models.CharField(max_length=5, blank=True, null=True, unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	smart_box = models.ForeignKey(SmartBox, on_delete=models.CASCADE, related_name='meters')
	cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, related_name='cylinders')
	quantity_remaining = models.DecimalField(decimal_places=2, max_digits=5)
	status = models.CharField(max_length=20, choices=status_choices, default='pending', blank=True, editable=True)
	transaction_id = models.CharField(max_length=5, blank=True, null=True)
	access_code = models.CharField(max_length=6, null=True, unique=True)
	delivery_officer = models.ForeignKey(DeliveryOfficer, on_delete=models.CASCADE, null=True, related_name='attached_delivery_officer')
	date_created = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=20, choices=ACTION_CHOICES, blank=True, null=True)
	action_date = models.DateField(null=True, blank=True)
	old_cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, null=True, related_name='customer_low_cylinder')
	new_cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, null=True, related_name='delivery_new_cylinder')

    #rescheduled_date = models.DateField(blank=True, null=True)

	def approve_order(self):
		if self.status == 'pending':
			self.status = 'approved'
			self.action_date = action_date
			self.save()

	def start_delivery(self):
		if self.status == 'approved':
			self.status = 'ongoing'
			self.save()

	def complete_delivery(self):
		if self.status == 'ongoing':
			self.status = 'delivered'
			self.save()

	def reschedule_order(self, rescheduled_date):
		if self.status == 'pending':
			self.status = 'rescheduled'
			self.action_date = action_date
			self.save()


	def __str__(self):
		return '{},{}'.format(self.status, self.user)

	def generate_unique_order_id(self):
		order_id = get_random_string(length=5, allowed_chars='0123456789')
		while RefillOrder.objects.filter(order_id=order_id).exists():
			order_id = get_random_string(length=5, allowed_chars='0123456789')
		return order_id

	
	# def generate_unique_order_id(self):
	#     order_id = get_random_string(length=5, allowed_chars='0123456789')
	#     while True:
	#         try:
	#             with transaction.atomic():
	#                 self.order_id = order_id
	#                 self.save()
	#                 break
	#         except IntegrityError:
	#             order_id = get_random_string(length=5, allowed_chars='0123456789')
	#     return order_id



	def generate_unique_access_code(self):
		access_code = get_random_string(length=6, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		while RefillOrder.objects.filter(access_code=access_code).exists():
			access_code = get_random_string(length=6, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		return access_code

	def save(self, *args, **kwargs):
		if not self.order_id:
			self.order_id = self.generate_unique_order_id()
		if not self.access_code:
			self.access_code = self.generate_unique_access_code()
		super().save(*args, **kwargs)

	class Meta:
		ordering = ['-date_created']


# new_token: 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


class RefillOrderAssignDeliveryOfficer(models.Model):
    refill_order = models.ForeignKey(RefillOrder, on_delete=models.CASCADE, related_name="refill_order", blank=True)
    delivery_officer = models.ForeignKey(DeliveryOfficer, on_delete=models.CASCADE, null=True, related_name='assigned_delivery_officer')
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{},{}'.format(str(self.refill_order), str(self.delivery_officer))

    class Meta:
        ordering = ('-assigned_date',)
