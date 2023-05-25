from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (
    SMEUserRegistrationView, AdminUserRegistrationView, DeliveryUserRegistrationView, OperationsUserRegistrationView, 
    UserLoginView, UserListView, get_user_profile, AdminLoginView, get_ops_and_delivery, SMEUserListView, ResidentUserRegistrationView,
    AdminUserListView, DeliveryUserListView, UpdateUserProfileView, delete_user, OpsDeliveryListView, PasswordChangeView, 
    ResidentialUsersListView, PasswordResetView, PasswordResetConfirmView
)

urlpatterns =[
	# Registration
	path('sme/register/', SMEUserRegistrationView.as_view(), name='sme-register'),
    path('residential/register/', ResidentUserRegistrationView.as_view(), name='retail-register'),
    path('admin-register/', AdminUserRegistrationView.as_view(), name='admin-register'),
    path('delivery-register/', DeliveryUserRegistrationView.as_view(), name='delivery-register'),
    path('operations-register/', OperationsUserRegistrationView.as_view(), name='ops-register'),

    # Login
    path('login/', UserLoginView.as_view(), name='login'),
    path('admin/login', AdminLoginView.as_view(), name='admin-login'),

    # Password change
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    # Password reset
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # Users
    path('users/', UserListView.as_view(), name='users'),
    path('sme/clients/', SMEUserListView.as_view(), name='sme-users'),
    path('residential/users/', ResidentialUsersListView.as_view(), name='residential-users'),
    path('admin-users/', AdminUserListView.as_view(), name='users'),
    path('delivery-users/', DeliveryUserListView.as_view(), name='users'),
    #path('ops-delivery/', get_ops_and_delivery, name='ops-delivery'),
    path('ops-delivery/', OpsDeliveryListView.as_view(), name='ops-delivery'),
    
    # Single User
    path("user-profile/<str:user_id>/", get_user_profile, name='user-profile'),
    path("update-profile/<str:user_id>", UpdateUserProfileView.as_view(), name='update-user'),
    path('delete-user/<str:user_id>', delete_user, name='delete-user'),

    # jwt
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
]
