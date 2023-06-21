from django.shortcuts import render
from django.utils.timezone import make_aware
import datetime
from datetime import datetime as dt
#from datetime import timedelta
from .models import OnboardingOrder, RefillOrder, RefillOrderAssignDeliveryOfficer
from asset.models import ResidentialAssignCylinder
from accounts.models import User
from delivery.models import DeliveryOfficer
from billing.models import OrderOnboardBilling
from .serializers import OnboardingOrderSerializer, OnboardedOrderListSerializer, RefillOrderSerializer, RefillOrderDetailSerializer, \
    RefillOrderAcceptSerializer, RefillOrderDeliveryAssignSerializer, RefillOrderDeliveryAcceptSerializer

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .pagination import LargeResultsSetPagination
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
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



class RefillOrderCustomerAcceptAPIView(generics.UpdateAPIView):
    """API to allow a customer to accept or reschedule a refill order"""
    queryset = RefillOrder.objects.all()
    serializer_class = RefillOrderAcceptSerializer

    def put(self, request, *args, **kwargs):
        refill_order = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            action = serializer.validated_data.get('action')
            action_date = serializer.validated_data.get('action_date')

            if action == 'accept':
                refill_order.status = 'approved'
                refill_order.action = action
                refill_order.action_date = action_date
                refill_order.save()
                print(f'date & action {action_date}, {action}')
                return Response({'status': 'success',  'message': 'Refill order accepted successfully!.', "data":serializer.data}, 
                    status=status.HTTP_200_OK)
            elif action == 'reschedule':
                refill_order.status = 'rescheduled'
                refill_order.action = action
                refill_order.action_date = action_date
                refill_order.save()
                print(f'date & action {action_date}, {action}')
                return Response({'status': 'success', 'message': 'Refill order rescheduled successfully!.',"data":serializer.data}, 
                    status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Invalid action!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RefillOrderDeliveryAssignAPIView(generics.UpdateAPIView):
    """API to assign a delivery officer to a refill order"""
    queryset = RefillOrder.objects.all()
    serializer_class = RefillOrderDeliveryAssignSerializer

    def put(self, request, *args, **kwargs):
        refill_order = self.get_object()
        serializer = self.get_serializer(refill_order, data=request.data, partial=True)
        print(f'refill_order => {refill_order}, {refill_order.user.lga}')

        if serializer.is_valid():
            assigned_delivery_officer = serializer.validated_data.get('delivery_officer')
            # manager = request.user.manager  # Assuming the manager is authenticated
            ro_lga = assigned_delivery_officer.manager.business_lga
            print(f'ro_lga : {ro_lga}')

            # Check if the manager's LGA matches the refill_order user's LGA
            if refill_order.user.lga == ro_lga and refill_order.status == 'approved':
                refill_order.status = 'assigned'
                refill_order.delivery_officer = assigned_delivery_officer
                refill_order.save()
                return Response({'status': 'success', 'message': 'Delivery officer assigned.'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': "No available delivery officer for this order's lga!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RefillOrderDeliveryAcceptAPIView(generics.UpdateAPIView):
    """API for delivery officer to accept/reject assigned refill order"""
    queryset = RefillOrder.objects.all()
    serializer_class = RefillOrderDeliveryAcceptSerializer

    def put(self, request, *args, **kwargs):
        refill_order = self.get_object()
        print(f'refill_order => {refill_order}, {refill_order.user.lga}')
        serializer = self.get_serializer(refill_order, data=request.data, partial=True)

        if serializer.is_valid():
            action = serializer.validated_data.get('action')
            print(f'action taken by do => {action}')
    
            # Check if the manager's LGA matches the refill_order user's LGA
            if action == 'accept':
                refill_order.status = 'in progress'
                refill_order.save()
                
                # Send email to the user
                subject = 'Refill Order Accepted'
                message = f'Hi {refill_order.user.first_name}, Your refill order {refill_order.order_id} has been accepted.\n' \
                          f'Delivery officer: {refill_order.delivery_officer.get_full_name()} is already on the way.\n' \
                          f'Phone number: {refill_order.delivery_officer.do_phone_number}\n' \
                          f'Access code: {refill_order.access_code} \n\n\n' \
                          f'Love & Energy \n' \
                          f'Homefort'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = refill_order.user.email
                send_mail(subject, message, from_email, [to_email])

                return Response({'status': 'success', 'message': f'Delivery officer accepted order {refill_order} successfully!'},
                 status=status.HTTP_200_OK)
            elif action == 'reject':
                refill_order.status == 'approved'
                refill_order.save()
                return Response({'status': 'success', 'message': f'Delivery officer rejected the order {refill_order} successfully!'},
                 status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'No action was taken or an error occured!'}, status=status.HTTP_400_BAD_REQUEST)


class RefillOrderDeliveredAPIView(generics.UpdateAPIView):
    """API for delivery officer to deliver refill order"""
    queryset = RefillOrder.objects.all()
    serializer_class = RefillOrderDeliveryAcceptSerializer

    def put(self, request, *args, **kwargs):
        refill_order = self.get_object()
        print(f'refill_order => {refill_order}, {refill_order.user.lga}')
        serializer = self.get_serializer(refill_order, data=request.data, partial=True)

        if serializer.is_valid():
            action = serializer.validated_data.get('action')
            print(f'action taken by do => {action}')
            #assigned_delivery_officer = serializer.validated_data.get('delivery_officer')
            #manager = request.user.manager  # Assuming the manager is authenticated
            #ro_lga = assigned_delivery_officer.manager.business_lga

            # Check if the manager's LGA matches the refill_order user's LGA
            if action == 'accept':
                refill_order.status = 'in progress'
                refill_order.save()
                return Response({'status': 'success', 'message': f'Delivery officer accepted order {refill_order} successfully!'},
                 status=status.HTTP_200_OK)
            elif action == 'reject':
                refill_order.status == 'approved'
                refill_order.save()
                return Response({'status': 'success', 'message': f'Delivery officer rejected the order {refill_order} successfully!'},
                 status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'No action was taken or an error occured!'}, status=status.HTTP_400_BAD_REQUEST)
        



class RefillOrderSearchAPIView(generics.ListAPIView):
    serializer_class = RefillOrderSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('query')
        queryset = RefillOrder.objects.all()

        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__phone_number__icontains=query) |
                Q(smart_box__box_id__icontains=query)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)



class RefillOrderByStatusAPIView(generics.ListAPIView):
    serializer_class = RefillOrderSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        status = self.kwargs.get('status')
        return RefillOrder.objects.filter(status=status)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)



class RefillOrderByDateAPIView(generics.ListAPIView):
    """API view to filter refill orders by date_created"""
    serializer_class = RefillOrderSerializer
    pagination_class = LargeResultsSetPagination 

    def get_queryset(self):
        date = self.kwargs['date']
        start_date = make_aware(dt.strptime(date, "%Y-%m-%d"))
        end_date = start_date + datetime.timedelta(days=1)
        queryset = RefillOrder.objects.filter(date_created__gte=start_date, date_created__lt=end_date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()

        if not queryset.exists():
            return Response({"message": "No refill orders found for this date!"}, status=status.HTTP_404_NOT_FOUND)

        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)





class RefillOrderAssignDeliveryOfficerCreateView(generics.CreateAPIView):
    """ API to allow RO manager assign a delivery officer to a refill order """
    queryset = RefillOrder.objects.all()
    serializer_class = RefillOrderSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RefillOrderSerializer(data=request.data)
        
        if serializer.is_valid():  
            # Change status of refill order to assigned
            refill_order = request.data.get('transaction_id')
            print('This is the fetched order =>', refill_order)
            manager = request.user.manager # Assuming the manager is authenticated
            manager_lga = manager.retailer.business_lga # Get RO lga
            print(f'manager lga is {manager_lga}')

            if refill_order.user.lga == lga:
                # Retrieve a delivery officer managed by the manager
                delivery_officer = DeliveryOfficer.objects.filter(manager=manager).first()

                if delivery_officer:
                    refill_order.status = 'assigned' # Update the refill order status
                    refill_order.delivery_officer = delivery_officer
                    refill_order.save()
                    serializer.save()
                    return Response({'status': 'success', 'message': 'Delivery officer assigned.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'No available delivery officer.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'error', 'message': 'Refill order is not in your LGA.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    

