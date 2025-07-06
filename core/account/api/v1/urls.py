from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name='api_v1'

urlpatterns=[
    # token and jwt
    path('register',views.RegistrationApiView.as_view(),name='registration-token'),

    # token
    path('login',views.CustomObtainAuthToken.as_view(),name='login'),
    path('logout',views.CustomDiscardAuthToken.as_view(),name='logout'),

    # jwt
    path('jwt/create',views.CustomTokenObtainPairView.as_view(),name='jwt-create'),
    path('jwt/refresh',TokenRefreshView.as_view(),name='jwt-refresh'),

    # verified
    path('activation/confirm/<str:token>',views.ActivationApiView.as_view(),name='activation'),

    # change password
    path('change-password',views.ChangePasswordApiView.as_view(),name='change_password'),

    # reset password
    path('password-reset', views.PasswordResetRequestApiView.as_view(), name='password-reset'),
    path('password-reset-confirm', views.PasswordResetConfirmApiView.as_view(), name='password-reset-confirm'),
]