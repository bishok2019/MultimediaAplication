from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    
    path('activate/<token>', views.VerifyEmailView.as_view(), name='verify-email'),
    
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # path('profile/image/', views.ProfileImageView.as_view(), name='profile-image'),
    
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
]