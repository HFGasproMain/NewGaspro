from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from datetime import datetime

from .models import DeliveryOfficer
from orders.models import RefillOrder
from .serializers import DeliveryOfficerSerializer




class DeliveryOfficerCreateAPIView(generics.CreateAPIView):
	""" API to Create a Delivery Officer """
	queryset = DeliveryOfficer.objects.all()
	serializer_class = DeliveryOfficerSerializer


class DeliveryOfficerListAPIView(generics.ListAPIView):
	""" API to List all Delivery Officers """
	queryset = DeliveryOfficer.objects.all()
	serializer_class = DeliveryOfficerSerializer


class DeliveryOfficerOrdersListAPIView(generics.RetrieveAPIView):
	""" API to List all Delivery Officer Assigned Orders """
	queryset = DeliveryOfficer.objects.all()
	serializer_class = DeliveryOfficerSerializer

	def retrieve(self, *args, **kwargs):
		delivery_officer = self.get_object()
		print(f'delivery-officer: {delivery_officer}')

		try:
			refill_order = RefillOrder.objects.get(delivery_officer=delivery_officer)
			print(f'all orders for this do => {refill_order}')
			#delivery_officer_orders = 
		except RefillOrder.DoesNotExist:
			return Response({'error': 'Refill order not found.'}, status=404)

		serializer = self.get_serializer(refill_order)
		return Response(serializer.data)




