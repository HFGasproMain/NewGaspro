from django.urls import path
from .views import CardCreateView, CardListView, CardDetailView, UserCardDetailView, UserCardListView

urlpatterns = [
    path('add-card/', CardCreateView.as_view(), name='card-create'),
    path('list/', CardListView.as_view(), name='card-list'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('uses/<int:user_id>/', UserCardDetailView.as_view(), name='card-detail-by-user-id'),
    path('user/<int:user_id>/', UserCardListView.as_view(), name='card-list-by-user-id'),
]
