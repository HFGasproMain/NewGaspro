from rest_framework import serializers
from .models import Range, SmartBoxReadings, CollectGasReading, ActivatedSmartBoxReading, GasMeterStatus
from asset.models import Cylinder, SmartScale, SmartBox
from asset.models import ResidentialAssignCylinder


class SmartBoxReadingsSerializer(serializers.ModelSerializer):
    ''' API to Show Gas Readings from User Smart Box  '''
    class Meta:
        model = SmartBoxReadings
        fields = '__all__'
        #fields = ("smart_box_id", "quantity_used", "battery_remaining", "longitude", "latitude" )


class CollectGasReadingsSerializer(serializers.ModelSerializer):
    ''' API to Save Live Gas Readings from User Smart Box  '''
    last_push = serializers.DateTimeField(read_only=True)
    class Meta:
        model = CollectGasReading
        #fields = '__all__'
        fields = ("smart_box_id", "quantity_used", "battery_remaining", "longitude", "latitude", "last_push" )


class GasMeterStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasMeterStatus
        fields = "__all__"


class UserGasReadingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = CollectGasReading
        fields = ['smart_box_id', 'quantity_remaining', 'user']

    def get_user(self, obj):
        return {
            'id': obj.residential_assign_meter.user.id,
            'first_name': obj.residential_assign_meter.user.first_name,
            'last_name': obj.residential_assign_meter.user.last_name,
            # Include any other user information you want
        }



class ResidentialCustomersGasReadingsSerializer(serializers.ModelSerializer):
    ''' API to Save Live Gas Readings from User Smart Box  '''
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()

    class Meta:
        model = CollectGasReading
        #fields = '__all__'
        #fields = ("smart_box_id", "quantity_used", "battery_remaining", "longitude", "latitude" )
        fields = ['smart_box_id','user_first_name', 'user_last_name', 'quantity_used', 'quantity_remaining', 'last_push']

    def get_meter_user_first_name(self, obj):
        if obj.residential_assign_meter and obj.residential_assign_meter.user:
            return obj.residential_assign_meter.user.first_name
        return None

    def get_meter_user_last_name(self, obj):
        if obj.residential_assign_meter and obj.residential_assign_meter.user:
            return obj.residential_assign_meter.user.last_name
        return None


class AssignedSmartBoxReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialAssignCylinder
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
 