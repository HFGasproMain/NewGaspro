from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Notifications
from accounts.models import User
from meter_readings.models import GasMeterStatus
from orders.models import RefillOrder

from .serializers import NotificationsSerializer
from orders.utils import generate_transaction_id

# Create your views here.

class SendNotifications(APIView):
	""" API to Send User Gas Quantiy Notifications """
	def get(self, request):
		meter_readings = GasMeterStatus.objects.all()
		notification_messages = []

		print(f'meter readings => {meter_readings}')

		for gl in meter_readings:
			quantity_remaining = gl.quantity_gas_left
			owner = gl.user_id
			user = get_object_or_404(User, id=int(owner))
			print(f'user id = {user.id}')
			# Retrieve the SmartBox instance
			smart_box = SmartBox.objects.get(box_id=gl.smart_box)
			# Retrieve the Cylinder instance
			cylinder = Cylinder.objects.get(serial_number=gl.cylinder_serial_number)

			if user:
				time = gl.last_push
				
				print(f'Quantity of gas left for {user} as at {time} is {quantity_remaining}kg.')

				if quantity_remaining >= 11.50 and quantity_remaining < 12.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 0.5kg of gas.")
				elif quantity_remaining >= 11.00 and quantity_remaining < 11.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 1.0kg of gas.")
				elif quantity_remaining >= 10.5 and quantity_remaining < 11.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 1.5kg of gas.")
				elif quantity_remaining >= 10.0 and quantity_remaining < 10.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 2kg of gas.")
				elif quantity_remaining >= 9.5 and quantity_remaining < 10.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 2.5kg of gas.")
				elif quantity_remaining >= 9.0 and quantity_remaining < 9.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 3.0kg of gas.")
				elif quantity_remaining >= 8.5 and quantity_remaining < 9.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 3.5kg of gas.")
				elif quantity_remaining >= 8.0 and quantity_remaining < 8.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 4.0kg of gas.")
				elif quantity_remaining >= 7.5 and quantity_remaining < 8.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 4.5kg of gas.")
				elif quantity_remaining >= 7.0 and quantity_remaining < 7.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 5.0kg of gas.")
				elif quantity_remaining >= 6.5 and quantity_remaining < 7.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 5.5kg of gas.")
				elif quantity_remaining >= 6.0 and quantity_remaining < 6.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 6.0kg of gas")
				elif quantity_remaining >= 5.5 and quantity_remaining < 6.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 6.5kg of gas.")
				elif quantity_remaining >= 5.0 and quantity_remaining < 5.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 7.0kg of gas.")
				elif quantity_remaining >= 4.5 and quantity_remaining < 5.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 7.5kg of gas.")
				elif quantity_remaining >= 4.0 and quantity_remaining < 4.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 8.0kg of gas.")
				elif quantity_remaining >= 3.5 and quantity_remaining < 4.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 8.5kg of gas.")
				elif quantity_remaining >= 3.0 and quantity_remaining < 3.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 9.0kg of gas.")
				elif quantity_remaining >= 2.5 and quantity_remaining < 3.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have used 9.5kg of gas.")
					print(f'quantiy_remaining => {quantity_remaining}')
					# Generate or retrieve the transaction_id
					transaction_id = generate_transaction_id()
					print(f'transaction_id => {transaction_id}')
					# Create a RefillOrder instance
					refill_order = RefillOrder.objects.create(user=user,
                                              smart_box=smart_box,
                                              cylinder=cylinder,
                                              quantity_remaining=quantity_remaining,
                                              status='pending',
                                              transaction_id=transaction_id
                                              )
					refill_order.save()
					print(f'refill status => {refill_order}')
				elif quantity_remaining >= 2.0 and quantity_remaining < 2.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have 2kg of gas left. Open your app to schedule gas delivery.")
					

				elif quantity_remaining >= 1.5 and quantity_remaining < 2.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have 1.50kg of gas left. Open your app to schedule gas delivery.")
				elif quantity_remaining >= 1.0 and quantity_remaining < 1.5:
					notification = Notifications.objects.create(user=user, 
	            		message="You have 1.0kg of gas left. Open your app to schedule gas delivery.")
				elif quantity_remaining >= 0.5 and quantity_remaining < 1.0:
					notification = Notifications.objects.create(user=user, 
	            		message="You have 0.50kg of gas left. Open your app to schedule gas delivery.")
				else:
					notification = Notifications.objects.create(user=user, 
	            		message="Your gas is on extra life. It would finish anytime. Call 08095567851 to order immediately!!!")


				notification_messages.append(notification) 
				#notification = Notification.objects.create(user=user, time=time, message=message)
			else:
				print('User does not exist for the meter reading')
				return Response({'message':'User for this meter not found!'}, status=status.HTTP_400_BAD_REQUEST)
		serializer = NotificationsSerializer(notification_messages, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


# class NotificationsListView(generics.ListAPIView):
# 	""" API For Residential Gas Usage Notification """
# 	queryset = Notifications.objects.all()
# 	serializer_class = NotificationsSerializer

# 	def get(self, request):
# 		meter_readings = GasMeterStatus.objects.all()
# 		response_data = []

# 		for gl in meter_readings:
# 			quantity_remaining = gl.quantity_gas_left
#             owner = gl.user_id
#             user = get_object_or_404(User, id=int(owner))
#             print(f'user id = {user.id}')
#             time = gl.last_push
#             print(f'Quantity of gas left for {user} as at {time} is {quantity_remaining}kg.')

#             if quantity_remaining >= 11.50 and quantity_remaining < 12.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 0.5kg of gas.")
#             elif quantity_remaining >= 11.00 and quantity_remaining < 11.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 1.0kg of gas.")
#             elif quantity_remaining >= 10.5 and quantity_remaining < 11.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 1.5kg of gas.")
#             elif quantity_remaining >= 10.0 and quantity_remaining < 10.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 2kg of gas.")
#             elif quantity_remaining >= 9.5 and quantity_remaining < 10.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 2.5kg of gas.")
#             elif quantity_remaining >= 9.0 and quantity_remaining < 9.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 3.0kg of gas.")
#             elif quantity_remaining >= 8.5 and quantity_remaining < 9.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 3.5kg of gas.")
#             elif quantity_remaining >= 8.0 and quantity_remaining < 8.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 4.0kg of gas.")
#             elif quantity_remaining >= 7.5 and quantity_remaining < 8.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 4.5kg of gas.")
#             elif quantity_remaining >= 7.0 and quantity_remaining < 7.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 5.0kg of gas.")
#             elif quantity_remaining >= 6.5 and quantity_remaining < 7.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 5.5kg of gas.")
#             elif quantity_remaining >= 6.0 and quantity_remaining < 6.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 6.0kg of gas")
#             elif quantity_remaining >= 5.5 and quantity_remaining < 6.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 6.5kg of gas.")
#             elif quantity_remaining >= 5.0 and quantity_remaining < 5.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 7.0kg of gas.")
#             elif quantity_remaining >= 4.5 and quantity_remaining < 5.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 7.5kg of gas.")
#             elif quantity_remaining >= 4.0 and quantity_remaining < 4.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 8.0kg of gas.")
#             elif quantity_remaining >= 3.5 and quantity_remaining < 4.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 8.5kg of gas.")
#             elif quantity_remaining >= 3.0 and quantity_remaining < 3.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 9.0kg of gas.")
#             elif quantity_remaining >= 2.5 and quantity_remaining < 3.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have used 9.5kg of gas.")
#             elif quantity_remaining >= 2.0 and quantity_remaining < 2.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have 2kg of gas left. Open your app to schedule gas delivery.")
#             elif quantity_remaining >= 1.5 and quantity_remaining < 2.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have 1.50kg of gas left. Open your app to schedule gas delivery.")
#             elif quantity_remaining >= 1.0 and quantity_remaining < 1.5:
#             	Notifications.objects.create(user=user, 
#             		message="You have 1.0kg of gas left. Open your app to schedule gas delivery.")
#             elif quantity_remaining >= 0.5 and quantity_remaining < 1.0:
#             	Notifications.objects.create(user=user, 
#             		message="You have 0.50kg of gas left. Open your app to schedule gas delivery.")
#             else:
#             	Notifications.objects.create(user=user, 
#             		message="Your gas is on extra life. It would finish anytime. Call 08095567851 to order immediately!!!")

#             # Call the base class implementation to get the default behavior
#             response = super().get(request, *args, **kwargs)

#         # Modify the response or perform additional operations

#         return response


def send_notification(request):
	#collect_gas_reading = get_object_or_404(GasMeterStatus, smart_box=smart_box_id)
	meter_readings = GasMeterStatus.objects.all()

	for gl in meter_readings:
		quantity_remaining = gl.quantity_gas_left
		owner = gl.user_id
		user = get_object_or_404(User, id=int(owner))
		time = gl.last_push
		print(f'Quantityss of gas left for {user} as at {time} is {quantity_remaining}kg.')
	
	return JsonResponse({"message": "success", "data": quantity_remaining}, status=status.HTTP_200_OK)


