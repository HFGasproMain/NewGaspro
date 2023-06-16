from django.urls import path
from .views import OnboardingOrderCreateView, OnboardedOrderListView, RefillOrderList, RefillOrderDetailView, \
	RefillOrderSearchAPIView

urlpatterns = [
	path('onboard-order/', OnboardingOrderCreateView.as_view(), name='onboard-order'),
	path('onboarded-orders/', OnboardedOrderListView.as_view(), name='list-onboard-order'),

	# refill orders
	path('refill-orders/', RefillOrderList.as_view(), name='refill_order_list'),
	path('refill-order/<str:refill_order_id>/', RefillOrderDetailView.as_view(), name='order-detail'),
	path('refill-order-search/', RefillOrderSearchAPIView.as_view(), name='refill-order-search'),
]