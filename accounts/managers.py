from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model. The email_id is the unique identifier. 
    This user has admin priviledges.
    """
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        if not password:
            raise ValueError(_("The password must be set"))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_sme_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        if not password:
            raise ValueError(_("The password must be set"))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('role', 2)

        if extra_fields.get('role') != 2:
            raise ValueError('Superuser must have role of Global Admin!')
        return self.create_user(phone_number, password, **extra_fields)
