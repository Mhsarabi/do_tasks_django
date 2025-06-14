from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import View,ListView,DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

# Create your views here.
    
class Template(TemplateView):
    template_name='task/task.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super().dispatch(request,*args,**kwargs)