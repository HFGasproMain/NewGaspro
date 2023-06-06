from django.db import models
from retailers.models import Retailers

# Create your models here.
class DeliveryOfficer(models.Model):
    ro = models.ForeignKey(Retailers, on_delete=models.CASCADE, related_name='delivery_officers')
    unique_code = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    # Other fields for DO
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate the unique code based on RO's business_state and business_lga
            state_code = str(self.ro.business_state)[-2:]  # Take the last two digits of business_state
            lga_code = str(self.ro.business_lga)[-2:]  # Take the last two digits of business_lga
            do_count = DeliveryOfficer.objects.filter(ro=self.ro).count() + 1  # Count existing DOs + 1
            unique_code = f"{state_code}/{lga_code}/{do_count:02d}"  # Format the unique code
            
            # Assign the generated unique code
            self.unique_code = unique_code
        
        super().save(*args, **kwargs)

    def __str__(self):
    	return self.unique_code

