from django.db import models

from accounts.models import User
#from cylinder.models import Cylinder
#from delivery.models import Delivery


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


class Retailers(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="retailer")
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    business_name = models.CharField(max_length=100, unique=True)
    business_address = models.TextField(null=True)
    business_lga = models.CharField(max_length=60, choices=lagos_lga)
    business_state = models.CharField(max_length=100, null=True)
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