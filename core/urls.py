from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

urlpatterns = [
    # Django admin url
    path('admin/', admin.site.urls),
    # DRF login url
    path('api-auth/', include('rest_framework.urls')),
    # API urls
    path('api/', include('api.urls')),
    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    path('auth/email-verify/', views.VerifyEmailView.as_view(), name='auth-email-verify'),
    path('auth/email-verify-resend/', views.ResendEmailConfirmationView.as_view(), name='auth-email-verify-resend'),
    path('auth/change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth-change-password'),
]
