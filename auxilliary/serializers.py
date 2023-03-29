from rest_framework import serializers
from .models import Auxiliary #RetailerAuxiliary


class AuxiliarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Auxiliary
        fields = ["customer", "first_name", "last_name", "phone_number", "date_created"]


class AuxiliarySerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = Auxiliary
        fields = ["first_name", "last_name", "phone_number"]


# class RetailerAuxiliarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RetailerAuxiliary
#         # fields = "__all__"
#         exclude = ("customer",)
