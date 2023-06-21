from django.db import models
from retailers.models import Retailers
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r"^[0]\d{10}$", message="must be a valid phone number")

# Create your models here.
class DeliveryOfficer(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    nok_choices = (
        ('Brother', 'Brother'),
        ('Sister','Sister'),
        ('Father', 'Father'),
        ('Mother','Mother'),
        ('Husband', 'Husband'),
        ('Wife', 'Wife')
    )
    manager = models.ForeignKey(Retailers, on_delete=models.CASCADE, related_name='retail_outlet')
    unique_code = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    do_phone_number = models.CharField(unique=True, null=True, validators=[phone_regex], max_length=11, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    nok_first_name = models.CharField(max_length=30, blank=True, null=True)
    nok_last_name = models.CharField(max_length=30, blank=True, null=True)
    nok_phone_number = models.CharField(unique=True, null=True, validators=[phone_regex], max_length=11, blank=True)
    nok_relationship = models.CharField(max_length=30, choices=nok_choices, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # Other fields for DO
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate the unique code based on RO's business_state and business_lga
            state_code = str(self.manager.business_state)[-2:]  # Take the last two digits of business_state
            lga_code = str(self.manager.business_lga)[-2:]  # Take the last two digits of business_lga
            do_count = DeliveryOfficer.objects.filter(manager=self.manager).count() + 1  # Count existing DOs + 1
            unique_code = f"{state_code}/{lga_code}/{do_count:02d}"  # Format the unique code
            
            # Assign the generated unique code
            self.unique_code = unique_code
        
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
    	return '{},{}'.format(self.get_full_name(), self.manager.business_lga)

    class Meta:
        ordering = ['-date_created']

