from django.db import models
from accounts.models import User
from asset.models import SmartBox, Cylinder

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
		('ongoing', 'ongoing'),
		('delivered', 'delivered')
	)
class RefillOrder(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	smart_box = models.ForeignKey(SmartBox, on_delete=models.CASCADE, related_name='meters')
	cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE, related_name='cylinders')
	quantity_remaining = models.DecimalField(decimal_places=2, max_digits=5)
	status = models.CharField(max_length=20, choices=status_choices, default='pending', blank=True)
	transaction_id = models.CharField(max_length=200, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def approve_order(self):
		if self.status == 'pending':
			self.status = 'approved'
			self.save()

	def start_delivery(self):
		if self.status == 'approved':
			self.status = 'ongoing'
			self.save()

	def complete_delivery(self):
		if self.status == 'ongoing':
			self.status = 'delivered'
			self.save()


	def __str__(self):
		return self.status

	class Meta:
		ordering = ['-date_created']



# new_token: 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
