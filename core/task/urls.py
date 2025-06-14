from django.urls import path,include
from . import views

app_name='task'
urlpatterns=[
    path('', views.TaskListView.as_view(), name='task-list'),
    path('add-task', views.TaskCreateView.as_view(), name='add-task'),
    path('delete/<int:pk>', views.TaskDeleteView.as_view(), name='delete-task'),
    path('toggle_done/<int:id>', views.ToggleDoneView.as_view(), name='toggle-done'),
    path('edit/<int:id>', views.TaskEditView.as_view(), name='edit-task'),
]
