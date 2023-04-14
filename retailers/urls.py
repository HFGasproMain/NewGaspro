from django.urls import path
from .views import RetailersCreateView, RetailersListView, RetailersDetailView

urlpatterns = [
	path('create-retailer/', RetailersCreateView.as_view(), name='retailers-create'),
	path('all-outlets/', RetailersListView.as_view(), name='retailers-list'),
	path('<str:pk>/', RetailersDetailView.as_view(), name='retailer-detail')
]