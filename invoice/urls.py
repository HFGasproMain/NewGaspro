from django.urls import path
from .views import InvoiceListView

urlpatterns = [
	path('all/', InvoiceListView.as_view(), name='invoice-list'),
	path('user/<int:user_id>/', InvoiceListView.as_view(), name='invoice-list-by-user'),
]