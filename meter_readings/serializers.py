from rest_framework import serializers
from .models import Range, SmartBoxReadings, CollectGasReading, ActivatedSmartBoxReading
from asset.models import Cylinder, SmartScale, SmartBox
from asset.models import RetailAssignCylinder


class SmartBoxReadingsSerializer(serializers.ModelSerializer):
    ''' API to Show Gas Readings from User Smart Box  '''
    class Meta:
        model = SmartBoxReadings
        # fields = '__all__'
        fields = ("smart_box_id", "quantity_used", "battery_remaining", "longitude", "latitude" )


class CollectGasReadingsSerializer(serializers.ModelSerializer):
    ''' API to Save Live Gas Readings from User Smart Box  '''
    class Meta:
        model = CollectGasReading
        #fields = '__all__'
        fields = ("smart_box_id", "quantity_used", "battery_remaining", "longitude", "latitude" )


class AssignedSmartBoxReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailAssignCylinder
        cylinder = serializers.PrimaryKeyRelatedField(queryset=Cylinder.objects.filter(cylinder_status='unassigned'))
        fields = '__all__'
        #fields = ("smart_box", "quantity_supplied", "quantity_used", "quantity_remaining", "battery_remaining")


class ActivatedSmartboxReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivatedSmartBoxReading
        smart_box = serializers.PrimaryKeyRelatedField(queryset=SmartBox.objects.filter(smartbox_status='assigned'))
        cylinder = serializers.PrimaryKeyRelatedField(queryset=Cylinder.objects.filter(cylinder_status='assigned'))
        #get_user = serializers.PrimaryKeyRelatedField(queryset=RetailAssignCylinder.objects.filter(user=''))

        fields = ("smart_box", "quantity_used", "battery_remaining", "longitude", "latitude" )



class ReadingOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBoxReadings
        fields = (
            "smart_box",
            "quantity_supplied",
            "total_quantity_used",
            "quantity_remaining",
            "battery_remaining",
            "longitude",
            "latitude",
            "min_value",
            "max_value",
            "last_push",
        )


# The only thing that changes upon reset are the qty_remanining, qty_supplied, and cylinder
# Payments;
# onboarding_order (1ce a year), gas_order
# when customer wants new cylinder; subscription fee (10k), gas fee (9.6k) & cylinder fee (18k).

class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Range
        fields = "__all__"
 