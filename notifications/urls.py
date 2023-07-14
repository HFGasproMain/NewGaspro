from django.urls import path
from .views import SendNotifications, send_notification, NotificationListView

urlpatterns = [
	path('messages/', SendNotifications.as_view(), name='create-messages'),
	path('user/<int:user_id>/', NotificationListView.as_view(), name='user-notifications'),
	#path('messages/', send_notification, name='messages')
	#path('messages/', NotificationsListView.as_view(), name='messages')
]