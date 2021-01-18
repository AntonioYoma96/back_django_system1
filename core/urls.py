from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from api import views

urlpatterns = [
    # Django admin url
    path('admin/', admin.site.urls),
    # DRF login url
    path('api-auth/', include('rest_framework.urls')),
    # API urls
    path('api/', include('api.urls')),
    # JWT Auth
    # path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    path('auth/full-register/', views.FullRegisterView.as_view(), name='auth-full-register'),
    path('auth/email-verify/', views.VerifyEmailView.as_view(), name='auth-email-verify'),
    path('auth/email-verify-resend/', views.ResendEmailConfirmationView.as_view(), name='auth-email-verify-resend'),
    path('auth/change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth-change-password'),
    path('auth/request-reset-password/', views.ResetPasswordRequestView.as_view(), name='auth-request-reset-password'),
    path('auth/reset-password/<str:uidb64>/<str:token>/', views.ResetPasswordView.as_view(), name='auth-reset-password')
]

# Swagger implementation
schema_view = get_schema_view(
    openapi.Info(
        title='SmartPeople API',
        default_version='0.1.1',
        description='API de la nueva versión de SmartPeople',
        contact=openapi.Contact(email='felipe.maldonado@sistemasexpertos.cl'),
        license=openapi.License(name='Software privado')
    ),
    public=True,
    permission_classes=(AllowAny,),
)
urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
