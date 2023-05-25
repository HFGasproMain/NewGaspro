import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string
from .managers import CustomUserManager

phone_regex = RegexValidator(regex=r"^[0]\d{10}$", message="must be a valid phone number")

class User(AbstractBaseUser, PermissionsMixin):
    SME = 1
    ADMIN = 2
    DELIVERY = 3
    RETAIL_OUTLETS = 4
    RESIDENT_CUSTOMERS = 5

    ROLE_CHOICES = (
        (SME, 'Sme'), # sme_users
        (ADMIN, 'Admin'), # admin_users
        (DELIVERY, 'Delivery'), # delivery_users
        (RETAIL_OUTLETS, 'Retail_outlets'), # retail_outlets
        (RESIDENT_CUSTOMERS, 'Residential') # retail_users
    )

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(unique=True, validators=[phone_regex], max_length=11, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    models.ImageField(default='default.jpeg', upload_to='profile_pics', null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=5)
    referral_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    any_referral_code = models.CharField(max_length=7, null=True, blank=True)
    user_class = models.CharField(max_length=30, null=True, blank=True, default='Residential Customers')
    date_to_onboard = models.DateField(null=True)
    address = models.TextField(null=True)
    lga = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    is_staff = models.BooleanField(default=False)
    date_for_your_onboarding = models.DateField()
    date_joined = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-date_joined',)

    def __str__(self):
        return '{},{},{}'.format(str(self.first_name), str(self.last_name), str(self.user_class))

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_random_string(length=6, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        return super().save(*args, **kwargs)


class SMEUser2(User):
    #which_user = models.CharField(max_length=100, blank=True, default='sme_new_user', null=True)
    business_name = models.CharField(max_length=100, default="Homefort SME", blank=True)
    business_type = models.CharField(max_length=30, null=True, blank=True, default='Business Pro')
    business_address = models.CharField(max_length=100, default="1, Faneye Street, Alagomeji, Yaba")
    business_lga = models.CharField(max_length=20, default="Yaba")
    business_state = models.CharField(max_length=20, default="Lagos")
    has_new_shop = models.CharField(max_length=30, null=True, blank=True)
    asset_type = models.CharField(max_length=30, null=True, blank=True)
    has_cylinder = models.CharField(max_length=30, blank=True, null=True)
    cylinder_size = models.CharField(max_length=30, blank=True, null=True)
    cylinder_position = models.CharField(max_length=30, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ('-date_created',)