from django.urls import path
from .views import SendNotifications, send_notification

urlpatterns = [
	path('messages/', SendNotifications.as_view(), name='create-messages'),
	#path('messages/', send_notification, name='messages')
	#path('messages/', NotificationsListView.as_view(), name='messages')
]