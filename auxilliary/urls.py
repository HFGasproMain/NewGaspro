from django.urls import path
from .views import (
    AuxiliaryDetailByUserView,
    AuxiliaryListView,
    AuxiliaryCreateView,
    AuxiliaryDetailView,
    AuxiliaryDeleteView,
    AuxiliaryUpdateView,
    # RetailerAuxiliaryCreateView,
    # RetailerAuxiliaryListView,
    # RetailerAuxiliaryDetailView,
    # retailer_auxiliary_by_retailer,
)

urlpatterns = [
    # Auxiliary endpoints
    path("aux-create/", AuxiliaryCreateView.as_view(), name='aux-create'),
    path("auxlist/", AuxiliaryListView.as_view(), name='aux-list'),
    path("aux/<int:pk>/", AuxiliaryDetailView.as_view(), name='aux-detail'),
    path("aux-delete/<int:pk>/", AuxiliaryDeleteView.as_view(), name='aux-delete'),
    path("aux-update/<int:pk>/", AuxiliaryUpdateView.as_view(), name='aux-update'),
    path("useraux/<int:customer>/", AuxiliaryDetailByUserView.as_view(), name='aux-user-detail'),

    # path("create-retailer-aux/", RetailerAuxiliaryCreateView.as_view()),
    # path("all-retailer-aux/", RetailerAuxiliaryListView.as_view()),
    # path("retailer-aux/<int:pk>/", RetailerAuxiliaryDetailView.as_view()),
    # path("retailer-aux-list/<str:retailer_id>/", retailer_auxiliary_by_retailer),
]