from django.shortcuts import render
from .models import OnboardingOrder, RefillOrder
from accounts.models import User
from billing.models import OrderOnboardBilling
from .serializers import OnboardingOrderSerializer, OnboardedOrderListSerializer, RefillOrderSerializer

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .pagination import LargeResultsSetPagination

import time

# Create your views here.
class OnboardingOrderCreateView(generics.CreateAPIView):
	""" API For Registered Users Who Want To Subscribe """
	queryset = OnboardingOrder
	serializer_class = OnboardingOrderSerializer
	permission_classes = (AllowAny,)

	def post(self, request):
		serializer = OnboardingOrderSerializer(data=request.data)
		if serializer.is_valid():
			cy_type = request.data.get('cylinder_type')
			customer = request.data.get('customer')
			print('customer here--', customer)
			transaction_id = int(round(time.time() * 1000))
			serializer.save(order_transaction_id=transaction_id)
			order_id = serializer.data['id']
			this_order=OnboardingOrder.objects.get(id=order_id)
			this_customer = User.objects.get(id=customer)
			print('onboard-order data:', this_order.id)
			
			# create transaction bill for new cylinders
			# if cy_type == 'new_cylinder':
			# 	OrderOnboardBilling.objects.create(order=this_order, customer=this_customer)
			# # create transaction bill for existing cylinders
			# elif cy_type == 'existing_cylinder':
			# 	OrderOnboardBilling.objects.create(order=order_id, cylinder_cost='', gas_cost='')

			return Response(data=serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnboardedOrderListView(generics.ListAPIView):
	""" API To List All Onboarded User Orders """
	queryset = OnboardingOrder.objects.all()
	serializer_class = OnboardedOrderListSerializer
	pagination_class = LargeResultsSetPagination
			


class RefillOrderList(APIView):
    def get(self, request):
        refill_orders = RefillOrder.objects.all()
        serializer = RefillOrderSerializer(refill_orders, many=True)
        return Response(serializer.data)