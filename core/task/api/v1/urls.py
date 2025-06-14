from django.urls import path,include
from . import views

app_name='api_v1'

urlpatterns=[
    path('task',views.TaskListPostApiView.as_view(),name='task-list'),
    path('task/<int:pk>',views.TaskGetUpdateDelete.as_view(),name='task-single')
]