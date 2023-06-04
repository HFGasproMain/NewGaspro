from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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

class Waitlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_waitlist', null=True)
	first_name = models.CharField(max_length=50, blank=True, null=True)
	last_name = models.CharField(max_length=50, blank=True, null=True)
	phone = models.CharField(max_length=11, blank=True, null=True)
	email = models.CharField(max_length=30, blank=True, null=True)
	state = models.CharField(max_length=30, blank=True, null=True)
	lga = models.CharField(max_length=50, blank=True, null=True)
	city = models.CharField(max_length=30, blank=True, null=True)
	subscribtion_status = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

