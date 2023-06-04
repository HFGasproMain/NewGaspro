from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.forms import ModelChoiceField
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .models import Cylinder, SMEAssignCylinder, SmartBox, SmartScale, ResidentialAssignCylinder, GasPrice, OtherBillableAssets



# Cylinders Serilizers
class CylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        #fields = '__all__'
        fields = ['cylinder_serial_number', 'cylinder_capacity', 'cylinder_gas_content', 'cylinder_tare_weight', 'manufacturer',
        'manufactured_date', 'current_actor', 'location']
        read_only_fields = ['cylinder_total_weight']


        def to_representation(self, instance):
            representation = super().to_representation(instance)
            actor = representation.get('current_actor')

            if actor == 'HQ':
                representation['location'] = self.fields['location'].to_representation(instance.location)
            else:
                representation.pop('location', None)

            return representation

        # def validate(self, data):
        #     actor = data.get('current_actor')
        #     location = data.get('location')

        #     if actor != 'HQ' and location:
        #         raise serializers.ValidationError("Location should not be provided for non-HQ actors.")

        #     return data


class CylinderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = '__all__'


class CylinderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = ["cylinder_serial_number", "cylinder_capacity", "cylinder_gas_content", "cylinder_tare_weight", \
            "cylinder_total_weight", "manufacturer", "manufactured_date", "maintenance_date", "current_actor", \
              "expiry_status", "gas_content_type", "location"]


class UnassignedCylindersChoiceField(ModelChoiceField):
    def queryset(self, queryset):
        if self.required:
            return queryset.filter(Q(cylinder_status='unassigned'))
        else:
            return queryset.filter(Q(cylinder_status='unassigned') | Q(pk=self.value()))

class SMEAssignCylinderSerializer(serializers.ModelSerializer):
    cylinder = serializers.PrimaryKeyRelatedField(queryset=Cylinder.objects.filter(cylinder_status='unassigned'))
    smart_box = serializers.PrimaryKeyRelatedField(queryset=SmartBox.objects.filter(smartbox_status='unassigned'))
    smart_scale = serializers.PrimaryKeyRelatedField(queryset=SmartScale.objects.filter(smartscale_status='unassigned'))

    class Meta:
        model = SMEAssignCylinder
        fields = ['user', 'cylinder', 'smart_scale', 'smart_box']

    

class ResidentialAssignCylinderSerializer(serializers.ModelSerializer):
    cylinder = serializers.PrimaryKeyRelatedField(queryset=Cylinder.objects.filter(cylinder_status='unassigned'))
    smart_box = serializers.PrimaryKeyRelatedField(queryset=SmartBox.objects.filter(smartbox_status='unassigned'))
    print('SmartBox[[]]', smart_box)

    class Meta:
        model = ResidentialAssignCylinder
        fields = ['user', 'cylinder', 'smart_box', 'assigned_date']


class SmartScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartScale
        fields = '__all__'


class SmartBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBox
        fields = ['box_id', 'manufacturer']
        #fields = '__all__'


# othe assets
class GasPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasPrice
        fields = '__all__'


class OtherBillableAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherBillableAssets
        fields = '__all__'
        

"""
# class QuestionnaireSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Questionnaire
#         fields = '__all__'


class ReassignCylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReassignCylinder
        fields = '__all__'


class AssignableCylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = "__all__"


class AssignableUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UnassignableUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CylinderWeightTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderWeightTrack
        fields = "__all__"


class ExtraCylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraCylinder
        fields = ("user", "cylinder", "date_modified" )


class UpdateCylinderWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateCylinderWeight
        fields = "__all__"


class BoxMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxMonitor
        fields = "__all__"


class CylinderMovementTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovementTracker
        fields = "__all__"


class CylinderMovementTrackerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovementTracker
        fields = ('cylinder', 'move_from', 'transit', 'pickup_staff')


class CylinderMovementTrackerDropOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovementTracker
        fields = ('cylinder', 'move_to', 'arrival', 'receipt_staff')


class CylinderMovementDropOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovementDropOff
        fields = "__all__"


class CylinderMovementIISerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovementDropOff
        fields = ('cylinder',)


class CylinderMovementTrackerSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovementTracker
        fields = ('person_one', 'person_two')


class CreateUpdateCylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateCylinderWeight
        fields = ("cylinder_id", "new_current_weight")


class CylinderResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderResolution
        fields = "__all__"


class CylinderMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderMovement
        fields = "__all__"


class OperationsAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationsAssignment
        fields = "__all__"


class OperationsAssignmentOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationsAssignment
        fields = ("cylinder", "asset_location")


class OperationsAssignmentOperatorAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationsAssignment
        fields = ("cylinder", "operations", "pickup_location", "capacity", "current_weight", "tare_weight")


class OperationsAssignmentUserAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationsAssignment
        fields = ("cylinder", "user")


class ApproveOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproveOperator
        fields = '__all__'
"""
