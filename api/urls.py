from django.urls import path
from .views import (
    HelloView,
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    TokenRefreshView,
    CurrentUserView,
    UpdateUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ChangePasswordView,
)

# URL patterns for the API application
# Organized into sections for better maintainability
urlpatterns = [
    # ============================================================
    # GENERAL ENDPOINTS
    # ============================================================
    path("hello/", HelloView.as_view(), name="hello"),
    
    # ============================================================
    # AUTHENTICATION ENDPOINTS
    # ============================================================
    # User registration and login
    path("auth/register/", UserRegistrationView.as_view(), name="auth-register"),
    path("auth/login/", UserLoginView.as_view(), name="auth-login"),
    path("auth/logout/", UserLogoutView.as_view(), name="auth-logout"),
    
    # Token management
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    
    # Current user profile
    path("auth/me/", CurrentUserView.as_view(), name="auth-current-user"),
    path("auth/me/", UpdateUserView.as_view(), name="auth-update-user"),
    
    # Password management
    path("auth/password/reset/", PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path("auth/password/reset/confirm/", PasswordResetConfirmView.as_view(), name="auth-password-reset-confirm"),
    path("auth/password/change/", ChangePasswordView.as_view(), name="auth-password-change"),
    
    # ============================================================
    # FUTURE ENDPOINTS
    # ============================================================
    # Add new endpoint groups here as the application grows
    # Examples:
    # - User management (admin only)
    # - Role management (admin only)
    # - Additional business logic endpoints
]
