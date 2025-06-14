from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from task.models import Task

class TaskListPostApiView(ListCreateAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=TaskSerializer
     
     def get_queryset(self):
          return Task.objects.filter(user=self.request.user)

class TaskGetUpdateDelete(RetrieveUpdateDestroyAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=TaskSerializer
     
     def get_queryset(self):
          return Task.objects.filter(user=self.request.user)