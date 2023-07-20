from django.urls import path
from .views import CardCreateView, CardListView, CardDetailView, UserCardDetailView

urlpatterns = [
    path('add-card/', CardCreateView.as_view(), name='card-create'),
    #path('list/', CardListView.as_view(), name='card-list'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('user/<int:user_id>/', UserCardDetailView.as_view(), name='card-list-by-user-id'),
    path('user-cards/<int:user_id>/', CardListView.as_view(), name='card-list'),
]
