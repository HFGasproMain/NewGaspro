from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.forms import ModelChoiceField
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .models import Cylinder, SMEAssignCylinder, SmartBox, SmartScale, RetailAssignCylinder



# Cylinders Serilizers
class CylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = '__all__'
        #exclude = ('cylinder_status',)

class CylinderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = '__all__'
        

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

    

class RetailAssignCylinderSerializer(serializers.ModelSerializer):
    cylinder = serializers.PrimaryKeyRelatedField(queryset=Cylinder.objects.filter(cylinder_status='unassigned'))
    smart_box = serializers.PrimaryKeyRelatedField(queryset=SmartBox.objects.filter(smartbox_status='unassigned'))
    print('SmartBox[[]]', smart_box)

    class Meta:
        model = RetailAssignCylinder
        fields = ['user', 'cylinder', 'smart_box', 'assigned_date']


class SmartScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartScale
        fields = '__all__'


class SmartBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBox
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
