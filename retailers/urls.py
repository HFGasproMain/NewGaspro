from django.urls import path
from .views import RetailersCreateView, RetailersListView, RetailersDetailView, CreateManagerAPIView, ROManagerListView

urlpatterns = [
	path('create-retailer/', RetailersCreateView.as_view(), name='retailers-create'),
	path('outlets/', RetailersListView.as_view(), name='retailers-list'),
	path('<str:pk>/', RetailersDetailView.as_view(), name='retailer-detail'),

	# Staff
	path('ro/create-manager/', CreateManagerAPIView.as_view(), name='create_manager'),
	path('ro/managers/', ROManagerListView.as_view(), name='managers'),
]