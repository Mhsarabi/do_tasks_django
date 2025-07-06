from django.urls import include,path,reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views

app_name='account'

urlpatterns=[
    path('register/',views.Register.as_view(),name='register'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='/account/login'),name='logout'),
    path('change_password/',views.ChangePassword.as_view(),name='change_password'),
    path('Reset_password/',views.ResetPassword.as_view(),name='Reset_password'),
    path('send-email/',views.SendEmail.as_view(),name='send_email'),
    path('api/v1/',include(('account.api.v1.urls', 'api_v1'), namespace='api_v1'))
]