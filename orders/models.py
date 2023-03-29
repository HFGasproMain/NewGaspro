from django.db import models
from accounts.models import User

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

	# def get_cost(self):
	# 	return Decimal(self.price) * Decimal(self.quantity)

	# def get_cost(self):
	# 	if cylinder_type = 'new_cylinder':
	# 		return Decimal(self.)

			

