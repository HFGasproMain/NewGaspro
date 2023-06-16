from django.shortcuts import render
from .models import OnboardingOrder, RefillOrder
from asset.models import ResidentialAssignCylinder
from accounts.models import User
from billing.models import OrderOnboardBilling
from .serializers import OnboardingOrderSerializer, OnboardedOrderListSerializer, RefillOrderSerializer, RefillOrderDetailSerializer

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
	""" API to See Bottle Swap Orders """
	pagination_class = LargeResultsSetPagination
	def get(self, request):
		refill_orders = RefillOrder.objects.all()

		# Create an instance of the pagination class
		paginator = self.pagination_class()

		# Paginate the queryset
		paginated_refill_orders = paginator.paginate_queryset(refill_orders, request)

		# Serialize the paginated results
		serializer = RefillOrderSerializer(paginated_refill_orders, many=True)

		# Return the paginated response
		return paginator.get_paginated_response(serializer.data)



class RefillOrdersDetailView(APIView):
    """ API For Residential User Detail """
    def get(self, request, user_id):
        # try:
        #     user = User.objects.get(id=user_id)
        # except User.DoesNotExist:
        #     return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
        	order = RefillOrder.objects.get(id=user_id)
        except RefillOrder.DoesNotExist:
        	return Response({'error':'Refill Order not found!'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming you have a UserProfile model that extends the User model
        #phone_number = user.phone_number
        customer = order.user
        cylinder = order.cylinder
        smart_box_id = order.smart_box

        # Get the SmartBox object for the user
        #smart_box = ResidentialAssignCylinder.objects.filter(user=user).first()
        #refill_order = RefillOrder.objects.filter(user=user).first()
        #smart_box_id = smart_box.smart_box_id if smart_box else None

        # Get the onboarding order for the user
        #onboarding_order = OnboardingOrder.objects.filter(customer=user).first()
        #date_of_onboarding = onboarding_order.date_created if onboarding_order else None

        data = {
            #'full_name': user.get_full_name(),
            #'address': user.get_full_address(),
            #'phone_number': phone_number,
            'smart_box_id': smart_box_id,
            'refill_order': order
        }

        return Response(data)



class RefillOrderDetailView(generics.RetrieveAPIView):
    """ API to Get Refill Order Details by ID """

    queryset = RefillOrder.objects.all()
    serializer_class = RefillOrderDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        refill_order_id = self.kwargs['refill_order_id']
        try:
            refill_order = RefillOrder.objects.get(id=refill_order_id)
        except RefillOrder.DoesNotExist:
            return Response({'error': 'Refill order not found.'}, status=404)

        serializer = self.get_serializer(refill_order)
        return Response(serializer.data)

		