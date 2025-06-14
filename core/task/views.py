from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import View,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

# Create your views here.
class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task/task.html'
    context_object_name = 'tasks'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super().dispatch(request,*args,**kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskCreateView(LoginRequiredMixin,View):
    model=Task
    success_url=reverse_lazy('task:task_list')
    def dispatch(self, request, *args, **kwargs):
          if not request.user.is_authenticated:
           return redirect('account:login')
          return super().dispatch(request,*args,**kwargs)
    
    def post(self,request, *args, **kwargs):
         data = json.loads(request.body)
         text = data.get('task', '').strip()
         if text:
                task = Task.objects.create(user=request.user, task=text)
                return JsonResponse({'success': True, 'task_id': task.id})
         else:
                return JsonResponse({'success': False, 'error': 'Empty task'})

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model=Task
    success_url=reverse_lazy('task:task_list')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super().dispatch(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object=self.get_object()

        if self.object.user != request.user:
             return JsonResponse({'success': False, 'error': '.دسترسی ندارید'})
        
        self.object.delete()
        return JsonResponse({'success': True})
    
class ToggleDoneView(LoginRequiredMixin,View):
    model=Task
    success_url=reverse_lazy('task:task_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request,id):
        task=get_object_or_404(Task,id=id,user=self.request.user)
        task.done=not task.done
        task.save()
        return JsonResponse({'success':True,'done':task.done})
    
class TaskEditView(LoginRequiredMixin,View):
    model=Task
    success_url=reverse_lazy('task:task_list')
    
    def post(self,request,id):
         task=get_object_or_404(Task,id=id,user=request.user)
         data=json.loads(request.body)
         new_text=data.get('task','').strip()
         if new_text:
             task.task=new_text
             task.save()
             return JsonResponse({'success':True})
         return JsonResponse({'success':False,'error':'.متن نمی تواند خالی باشد'})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super().dispatch(request,*args,**kwargs)