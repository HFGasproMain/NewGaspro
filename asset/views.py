import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .models import Cylinder, SmartScale, SmartBox, SMEAssignCylinder, RetailAssignCylinder, OtherBillableAssets, GasPrice
from meter_readings.models import SmartBoxMonitor, SmartScaleMonitor, SmartBoxReadings

from .serializers import CylinderSerializer, CylinderListSerializer, SMEAssignCylinderSerializer, \
	SmartScaleSerializer, SmartBoxSerializer, ResidentialAssignCylinderSerializer, OtherBillableAssetsSerializer, \
	GasPriceSerializer, CylinderDetailSerializer


"""
All Assets Related Views
"""

# Unassigned Cylinder Views.
class CylinderCreateView(generics.CreateAPIView):
	""" API to Register a New Cylinder """
	queryset = Cylinder.objects.all()
	serializer_class = CylinderSerializer
	permission_classes = (AllowAny,)

	def post(self, request, *args, **kwargs):
		actor = request.data.get('current_actor')
		location = request.data.get('location')
		serializer = CylinderSerializer(data=request.data)

		# validate to ensure field enforcement
		if actor != 'HQ' and location:
			return Response({"message": "Location should not be provided for non-HQ actors."}, 
				status=status.HTTP_400_BAD_REQUEST)

		if serializer.is_valid():
			serializer.save()
			return Response({"message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CylinderListView(generics.ListAPIView):
	""" All Cylinders """
	queryset = Cylinder.objects.all()
	serializer_class = CylinderListSerializer
	permission_classes = (AllowAny,)


class CylinderDetailView(generics.RetrieveAPIView):
	""" API for a Single Cylinder """
	queryset = Cylinder.objects.all()
	serializer_class = CylinderSerializer
	lookup_field = 'cylinder_serial_number'
	permission_classes = (AllowAny,)


# Cylinder Detail View
@api_view(['GET'])
@permission_classes((AllowAny,))
def cylinder_detail_view(self, cylinder):
    """ API for Cylinder Detail by Cyinder_Serial_Number """
    try:
        cylinder = Cylinder.objects.get(cylinder_serial_number=cylinder)
        cylinder_serializer = CylinderDetailSerializer(cylinder)
        return Response({"message": "success", "data": cylinder_serializer.data}, status=status.HTTP_200_OK)
    except Cylinder.DoesNotExist:
        return Response({"message": "Cylinder not found!"},
            status=status.HTTP_400_BAD_REQUEST)


class CylinderDeleteView(generics.RetrieveDestroyAPIView):
	""" DELETE API for the Unassigned Cylinder """
	queryset = Cylinder.objects.all()
	serializer_class = CylinderSerializer
	permission_classes = (AllowAny,)

class CylinderUpdateView(generics.UpdateAPIView):
	""" Update API for the Unassigned Cylinder """
	queryset = Cylinder.objects.all()
	serializer_class = CylinderSerializer
	permission_classes = (AllowAny,)

# Assigned Cylinder
# class AssignCylinderCreateView(generics.CreateAPIView):
#     queryset = AssignCylinder.objects.all()
#     serializer_class = AssignCylinderSerializer
#     permission_classes = (AllowAny,)

class SMEAssignCylinderCreateView(generics.CreateAPIView):
    """ Onboard A Cylinder To A SME User """
    serializer_class = SMEAssignCylinderSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
    	serializer = SMEAssignCylinderSerializer(data=request.data)
    	if serializer.is_valid():
    		# Change status of onboarded assets to assigned
    		get_smartbox = request.data.get('smart_box')
    		sb = SmartBox.objects.get(box_id=get_smartbox)
    		sb.smartbox_status = 'assigned'
    		sb.save()
    		print('SmartBox now ==>', get_smartbox, sb)
    		get_smartscale = request.data.get('smart_scale')
    		sc = SmartScale.objects.get(scale_id=get_smartscale)
    		sc.smartbox_status = 'assigned'
    		sc.save()
    		print('SmartScale now ==>',get_smartscale, sc)
    		get_cylinder = request.data.get('cylinder')
    		g_cylinder = get_cylinder
    		print('g_cylinder=', g_cylinder)
    		c = Cylinder.objects.get(cylinder_serial_number=get_cylinder)
    		c.cylinder_status = 'assigned'
    		c.save()
    		print('Cylinder now ==>;', get_cylinder, c) 	
    		serializer.save()
    		return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResidentialAssignCylinderCreateView(generics.CreateAPIView):
    """ Onboard A HF Cylinder To A Residential User """
    serializer_class = ResidentialAssignCylinderSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
    	serializer = ResidentialAssignCylinderSerializer(data=request.data)
    	
    	if serializer.is_valid():  
	   		# Change status of onboarded assets to assigned
	   		get_cylinder = request.data.get('cylinder')
	   		print('This is the fetched cylinder=>', get_cylinder)
	   		c = Cylinder.objects.get(cylinder_serial_number=get_cylinder)
	   		c.cylinder_status = 'assigned'
	   		get_smartbox = request.data.get('smart_box')
	   		print('This is the fetched sb=>', get_smartbox)
	   		sb = SmartBox.objects.get(box_id=get_smartbox)
	   		sb.smartbox_status = 'assigned'
	   		sb.save()
	   		c.save()
	   		print('SmartBox now ==>', get_smartbox, sb)
	   		print('Cylinder now ==>;', get_cylinder, c) 	
	   		serializer.save()
	   		return Response({"message": f"Cylinder {get_cylinder} onboarded successfully!", "data": serializer.data}, 
    			status=status.HTTP_201_CREATED)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResidentialAssignedCylinderListView(generics.ListAPIView):
	""" All Residential Users Assigned Assets (Cylinders & SmartBoxes) """
	queryset = RetailAssignCylinder.objects.all()
	serializer_class = ResidentialAssignCylinderSerializer
	permission_classes = (AllowAny,)



class SMEAssignedCylinderListView(generics.ListAPIView):
	""" All SME Assigned Cylinders """
	queryset = SMEAssignCylinder.objects.all()
	serializer_class = SMEAssignCylinderSerializer
	permission_classes = (AllowAny,)



# SME Cylinder History
class SMEUserAssignedCylinderHistory(generics.ListAPIView):
	queryset = SMEAssignCylinder.objects.all()
	serializer_class = SMEAssignCylinderSerializer
	permission_classes = (AllowAny,)

	def get_queryset(self):
		sme = get_object_or_404(User, id=self.kwargs.get('sme_id'))
		print('this is the sme;', sme.business_name)
		return AssignCylinder.objects.filter(user=sme).order_by('-date_assigned')

# Assigned Cylinder History
class AssignedCylinderHistory(generics.ListAPIView):
	"""
        This view should return a history for
        the given assigned cyinder of the URL.
    """
	queryset = SMEAssignCylinder.objects.all()
	serializer_class = SMEAssignCylinderSerializer
	permission_classes = (AllowAny,)

	def get_queryset(self):
		a_cylinder = self.kwargs['cy_tag_id']
		return SMEAssignCylinder.objects.filter(cylinder__cylinder_serial_number=a_cylinder).order_by('-date_assigned')
		
		
# Smart Scales Views
class SmartScaleCreateView(generics.CreateAPIView):
	""" Smart Scale Create View """
	queryset = SmartScale.objects.all()
	serializer_class = SmartScaleSerializer
	permission_classes = (AllowAny,)

	def post(self, request, *args, **kwargs):
		ser = self.get_serializer(data=request.data)
		if not ser.is_valid(raise_exception=True):
			return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

		scale_id = request.data.get('scale_id')
		date_time_created = datetime.datetime.now()

		if ser.is_valid():
			ser.save()
		return Response({"message": f"Smart scale {scale_id} successfully created!"}, status=status.HTTP_201_CREATED)


class SmartScaleListView(generics.ListAPIView):
	""" Smart Scale List View """
	queryset = SmartScale.objects.all()
	serializer_class = SmartScaleSerializer
	permission_classes = (AllowAny,)


class SmartScaleDeleteView(generics.RetrieveDestroyAPIView):
	""" Delete Smart Scale View """
	queryset = SmartScale.objects.all()
	serializer_class = SmartScaleSerializer
	permission_classes = (AllowAny,)


class SmartScaleUpdateView(generics.UpdateAPIView):
	""" Update Smart Scale View """
	queryset = SmartScale.objects.all()
	serializer_class = SmartScaleSerializer
	permission_classes = (AllowAny,)


""" Smart Box Views """

# SmartBox Create View
class SmartBoxCreateView(generics.CreateAPIView):
    queryset = SmartBox.objects.all()
    serializer_class = SmartBoxSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        box_id = request.data.get('box_id')
        date_time_created = datetime.datetime.now()
        quantity_supplied = request.data.get('quantity_supplied')

        if quantity_supplied == 0 or quantity_supplied is None:
            quantity_supplied = 12
        else:
            quantity_supplied = request.data.get('quantity_supplied')

        if not SmartBox.objects.filter(box_id=box_id).exists():
            payload = {
                "smart_box": box_id,
                "quantity_supplied": quantity_supplied,
                "quantity_used": 0.0,
                "quantity_remaining": quantity_supplied,
                "battery_remaining": 100.0,
                "last_push": str(date_time_created),
                "min_transmit_time": 4,
                "max_transmit_time":25,
                "transmit_type":"flow",
                "min_value":2,
                "max_value":12
            }
            SmartBoxReadings.objects.create(**payload)

            monitor_payload = {
                "smart_box": box_id,
                "value": 0
            }

            SmartBoxMonitor.objects.create(**monitor_payload)

        if serializer.is_valid():
            serializer.save()

        return Response({"message": f"Smart box {box_id} successfully created!"}, status=status.HTTP_201_CREATED)




class SmartBoxListView(generics.ListAPIView):
	""" Smart Box List View """
	queryset = SmartBox.objects.all()
	serializer_class = SmartBoxSerializer
	permission_classes = (AllowAny,)


class SmartBoxDeleteView(generics.RetrieveDestroyAPIView):
	""" Delete Smart Box View """
	queryset = SmartBox.objects.all()
	serializer_class = SmartBoxSerializer
	permission_classes = (AllowAny,)


class SmartBoxUpdateView(generics.UpdateAPIView):
	""" Update Smart Box View """
	queryset = SmartBox.objects.all()
	serializer_class = SmartBoxSerializer
	permission_classes = (AllowAny,)

   

class OtherBillableAssetsCreateView(generics.CreateAPIView):
	""" API to Set Other Assets Price """
	queryset = OtherBillableAssets.objects.all()
	serializer_class = OtherBillableAssetsSerializer
	#permission_classes = (AllowAny)

class OtherBillableAssetsListView(generics.ListAPIView):
	""" API to List Other Billable Assets """
	queryset = OtherBillableAssets.objects.all()
	serializer_class = OtherBillableAssetsSerializer
	permission_classes = (AllowAny,)


class OtherBillableAssetsUpdateView(generics.UpdateAPIView):
	""" API to Update Current Gas Price """
	queryset = OtherBillableAssets.objects.all()
	serializer_class = OtherBillableAssetsSerializer
	permission_classes = (AllowAny,)


class GasPriceCreateView(generics.CreateAPIView):
	""" API to Set Current Gas Price """
	queryset = GasPrice.objects.all()
	serializer_class = GasPriceSerializer
	#permission_classes = (AllowAny)


class GasPriceListView(generics.ListAPIView):
	""" API to List Current Gas Price """
	queryset = GasPrice.objects.all()
	serializer_class = GasPriceSerializer
	permission_classes = (AllowAny,)


class GasPriceUpdateView(generics.UpdateAPIView):
	""" API to Update Current Gas Price """
	queryset = GasPrice.objects.all()
	serializer_class = GasPriceSerializer
	permission_classes = (AllowAny,)