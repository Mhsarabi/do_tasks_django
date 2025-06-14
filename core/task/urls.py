from django.urls import path,include
from . import views

app_name='task'
urlpatterns=[
    path('',views.Template.as_view(),name='task'),
    path('api/v1/',include('task.api.v1.urls'))
]
