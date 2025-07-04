from django.urls import include,path,reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views

app_name='account'

urlpatterns=[
    path('register/',views.Register.as_view(),name='register'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='/account/login'),name='logout'),
    path('api/v1/',include('account.api.v1.urls'))
]