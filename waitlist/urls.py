from django.urls import path
from .views import WaitlistCreateView, WaitlistListView


urlpatterns = [
	path('create/', WaitlistCreateView.as_view(), name='create-waitlist'),
	path('users/', WaitlistListView.as_view(), name='user-waitlist')
]