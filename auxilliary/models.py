from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model

#from retailer.models import Retailer

User = get_user_model()

phone_regex = RegexValidator(
    regex=r"^[0]\d{10}$", message="must be a valid phone number"
)


class Auxiliary(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_auxiliary")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date_created']


# class RetailerAuxiliary(models.Model):
#     customer = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name="retailer_auxiliary"
#     )
#     retailer = models.OneToOneField(
#         Retailer, on_delete=models.CASCADE, related_name="retailer_object_auxiliary"
#     )
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     image = models.ImageField()
#     phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True)

#     def __str__(self):
#         return str(self.id)
