from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

#from cylinder.models import Cylinder
#from delivery.models import Delivery

phone_regex = RegexValidator(regex=r"^[0]\d{10}$", message="must be a valid phone number")

states = [
    ['AB', 'Abia'],
    ['AD', 'Adamawa'],
    ['AK', 'Akwa Ibom'],
    ['AN', 'Anambra'],
    ['BA', 'Bauchi'],
    ['BY', 'Bayelsa'],
    ['BE', 'Benue'],
    ['BO', 'Borno'],
    ['CR', 'Cross River'],
    ['DE', 'Delta'],
    ['EB', 'Ebonyi'],
    ['ED', 'Edo'],
    ['EK', 'Ekiti'],
    ['EN', 'Enugu'],
    ['GO', 'Gombe'],
    ['IM', 'Imo'],
    ['JI', 'Jigawa'],
    ['KA', 'Kaduna'],
    ['KN', 'Kano'],
    ['KT', 'Katsina'],
    ['KE', 'Kebbi'],
    ['KO', 'Kogi'],
    ['KW', 'Kwara'],
    ['LG', 'Lagos'],
    ['NA', 'Nasarawa'],
    ['NI', 'Niger'],
    ['OG', 'Ogun'],
    ['ON', 'Ondo'],
    ['OS', 'Osun'],
    ['OY', 'Oyo'],
    ['PL', 'Plateau'],
    ['RI', 'Rivers'],
    ['SO', 'Sokoto'],
    ['TA', 'Taraba'],
    ['YO', 'Yobe'],
    ['ZA', 'Zamfara'],
]


lagos_lga = [
    ['Agege', 'Agege'],
    ['Ajeromi-Ifelodun', 'Ajeromi-Ifelodun'],
    ['Alimosho', 'Alimosho'],
    ['Apapa', 'Apapa'],
    ['Amuwo-Odofin', 'Amuwo-Odofin'],
    ['Badagry', 'Badagry'],
    ['Epe', 'Epe'],
    ['Eti-Osa', 'Eti-Osa'],
    ['Ibeju-Lekki', 'Ibeju-Lekki'],
    ['Ifako-Ijaiye', 'Ifako-Ijaiye'],
    ['Ikeja', 'Ikeja'],
    ['Ikorodu', 'Ikorodu'],
    ['Kosofe', 'Kosofe'],
    ['Lagos Island', 'Lagos Island'],
    ['Lagos Mainland', 'Lagos Mainland'],
    ['Mushin', 'Mushin'],
    ['Ojo', 'Ojo'],
    ['Oshodi-Isolo', 'Oshodi-Isolo'],
    ['Somolu', 'Somolu'],
    ['Surulere', 'Surulere'],
]


# class CustomUserManager(UserManager):
#     def create_ro_user(self, username):
#         user = self.model(username=username)
#         password = "hf00002023"  # Set the default password
#         user.set_password(password)
#         user.save()
#         return user

#     objects = CustomUserManager()


class Retailers(models.Model):
    # first_name = models.CharField(max_length=60, blank=True)
    # last_name = models.CharField(max_length=60, blank=True)
    business_name = models.CharField(max_length=100, unique=True)
    business_email = models.CharField(max_length=60, blank=True, null=True)
    business_address = models.TextField(null=True)
    business_lga = models.CharField(max_length=60, choices=lagos_lga)
    business_state = models.CharField(max_length=100, choices=states, null=True)
    state_code = models.PositiveIntegerField(null=True)
    lga_code = models.PositiveIntegerField(null=True)
    business_phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    image = models.CharField(max_length=200)
    first_reference = models.CharField(max_length=30)
    second_reference = models.CharField(max_length=30)
    is_online = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.business_name)

    class Meta:
        ordering = ('-business_lga',)
        verbose_name = 'Retailers'


    def save(self, *args, **kwargs):
        if self.business_state:
            # Assign the state code based on the unique index of the state in the `states` list
            for index, state in enumerate(states):
                if state[0] == self.business_state:
                    self.state_code = index + 1
                    print(f'state code => {self.state_code}')
            # else:
            #     self.state_code = None

        if self.business_lga:
            # Assign the LGA code based on the unique index of the LGA in the `lagos_lga` list
            for index, lga in enumerate(lagos_lga):
                if lga[0] == self.business_lga:
                    self.lga_code = index + 1
                    print(f'business code => {self.state_code}')
            # else:
            #     self.lga_code = None
        
        super().save(*args, **kwargs)

    def get_retailers_code(self):
        return [self.state_code ,self.business_lga]


gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female')
    )
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')
    retailer = models.ForeignKey(Retailers, on_delete=models.CASCADE, related_name='managers')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    #mobile_number = models.CharField(validators=[phone_regex], max_length=11, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    manager_code = models.CharField(max_length=8, unique=True)
    dob = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    def get_full_name(self):
        """ Return the manager's full name """
        return f"{self.first_name}, {self.last_name}"

    def save(self, *args, **kwargs):
        state_code = self.retailer.state_code
        lga_code = self.retailer.lga_code
        manager_id = self.id
        business_name = self.retailer.business_name.replace(' ', '').upper()
        self.manager_code = f"{state_code}-{lga_code}-{manager_id}"
        super().save(*args, **kwargs) 

    class Meta:
        ordering = ('-date_created',)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    retailer = models.ForeignKey('Retailers', on_delete=models.CASCADE, related_name='staffs')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(max_length=10, choices=gender_choices)
    #dob = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    def get_full_name(self):
        """ Return the staff's full name """
        return f"{self.first_name}, {self.last_name}" 



    # @property
    # def manager_code(self):
    #     """ Generate and return the manager's code """
    #     state_code = self.retailer.state_code
    #     lga_code = self.retailer.lga_code
    #     business_name = self.retailer.business_name.replace(' ', '').upper()
    #     return f"{state_code}-{lga_code}-{business_name}"



CYLINDER_STATUS = (("PRE-FILLED", "PRE-FILLED"), ("EMPTY", "EMPTY"))

CYLINDER_LOCATION = (
    ("IN-STORE", "IN-STORE"),
    ("ISSUED", "ISSUED"),
    ("RETURNED", "RETURNED"),
    ("WITH-LPG", "WITH-LPG"),
)

ISSUING_LPG_STORE = (
    ("IYANA-IPAJA", "IYANA-IPAJA"),
    ("YABA", "YABA"),
    ("LAGOS", "LAGOS"),
)

RETURN_DESTINATION = (
    ("TRANSIT-OUT", "TRANSIT-OUT"),
    ("TRANSIT-IN", "TRANSIT-IN"),
    ("STORE_ONE", "STORE_ONE"),
    ("STORE_TWO", "STORE_TWO"),
)

'''
class RetailerStock(models.Model):
    issuer = models.CharField(
        max_length=30, choices=ISSUING_LPG_STORE, default="IYANA-IPAJA"
    )
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE)

    lpg_stock_received_by = models.CharField(max_length=200, null=True, blank=True)
    date_of_receipt_from_lpg = models.DateTimeField(
        auto_now=True, null=True, blank=True
    )

    tare_weight = models.CharField(max_length=30, null=True, blank=True)
    current_weight = models.CharField(max_length=30, null=True, blank=True)
    cylinder_capacity = models.CharField(max_length=30, null=True, blank=True)

    weight = models.CharField(max_length=10, default="0.0")

    # issue_to_delivery_guy = models.ForeignKey(
    #     Delivery,
    #     on_delete=models.CASCADE,
    #     related_name="receiving_delivery_guy",
    #     null=True,
    #     blank=True,
    # )
    issue_to_delivery_guy = models.CharField(max_length=10, null=True, blank=True)
    date_of_issue_to_delivery_guy = models.DateTimeField(
        auto_now=True, null=True, blank=True
    )

    receive_from_delivery_guy = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name="returning_delivery_guy",
        null=True,
        blank=True,
    )
    date_of_receipt_from_delivery_guy = models.DateTimeField(
        auto_now=True, null=True, blank=True
    )

    cylinder_location = models.CharField(
        max_length=40, choices=CYLINDER_LOCATION, default="IN-STORE"
    )
    cylinder_status = models.CharField(
        max_length=40, choices=CYLINDER_STATUS, default="PRE-FILLED"
    )

    lpg_staff_receive_stock = models.CharField(max_length=200, null=True, blank=True)
    return_destination = models.CharField(
        max_length=30, choices=RETURN_DESTINATION, default="TRANSIT-OUT"
    )
    date_of_return_to_lpg = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.cylinder)

    class Meta:
        ordering = ["-id"]


# class CylinderWeightTrack(models.Model):
#     cylinder_id = models.CharField(max_length=30)
#     current_weight = models.CharField(max_length=30, null=True, blank=True)
#     cylinder_capacity = models.CharField(max_length=30, null=True, blank=True)
#     tare_weight = models.CharField(max_length=30, null=True, blank=True)
#     filled_gas_weight = models.CharField(max_length=30, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.cylinder_id)

#     class Meta:
#         ordering = ["-id"]


# class UpdateCylinderWeight(models.Model):
#     cylinder_id = models.CharField(max_length=30)
#     new_current_weight = models.CharField(max_length=30, null=True, blank=True)
#     previous_weight = models.CharField(max_length=30, null=True, blank=True)
#     filled_gas_weight = models.CharField(max_length=30, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.cylinder_id)

#     class Meta:
#         ordering = ["-id"]

'''