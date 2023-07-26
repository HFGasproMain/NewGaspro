from django.urls import path
from .views import OnboardingOrderCreateView, OnboardedOrderListView, RefillOrderList, RefillOrderDetailView, \
	RefillOrderSearchAPIView, RefillOrderByStatusAPIView, RefillOrderByDateAPIView, RefillOrderCustomerAcceptAPIView, \
	RefillOrderDeliveryAssignAPIView, RefillOrderDeliveryAcceptAPIView, RefillOrderSwapAPIView, DeliveryHistoryByUserIdAPIView, \
	TransactionByUserIdAPIView


urlpatterns = [
	path('onboard-order/', OnboardingOrderCreateView.as_view(), name='onboard-order'),
	path('onboarded-orders/', OnboardedOrderListView.as_view(), name='list-onboard-order'),

	# refill orders
	path('refill-orders/', RefillOrderList.as_view(), name='refill_order_list'),
	path('refill-order/<str:refill_order_id>/', RefillOrderDetailView.as_view(), name='order-detail'),
	path('refill-order-search/', RefillOrderSearchAPIView.as_view(), name='refill-order-search'),
	path('refill-orders/status/<str:status>/', RefillOrderByStatusAPIView.as_view(), name='refill-orders-by-status'),
	path('refill-orders/date/<str:date>/', RefillOrderByDateAPIView.as_view(), name='refill-orders-by-date'),

	# refill-order-cycle
	path('refill-order/<int:pk>/customer-accept/', RefillOrderCustomerAcceptAPIView.as_view(), name='refill-order-accept'),
	path('refill-order/<int:pk>/assign-delivery-officer/', RefillOrderDeliveryAssignAPIView.as_view(), name='assign-delivery-officer'),
	path('refill-order/<int:pk>/delivery-officer-accept/', RefillOrderDeliveryAcceptAPIView.as_view(), name='delivery-officer-accept'),
	path('refill-order/<int:pk>/swap/', RefillOrderSwapAPIView.as_view(), name='refill-order-swap'),

	# Delivery history
	path('delivery-history/<int:user_id>/', DeliveryHistoryByUserIdAPIView.as_view(), name='delivery-history-by-user-id'),
	path('transactions/user/<int:user_id>/', TransactionByUserIdAPIView.as_view(), name='transaction-by-user'),

]
