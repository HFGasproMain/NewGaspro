from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Notifications(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message')
	message = models.CharField(max_length=200, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message

	class Meta:
		ordering = ('-date_created',)
