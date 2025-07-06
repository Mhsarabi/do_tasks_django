from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from .models import *
from .forms import *

# Create your views here.
class Register(CreateView):
    model=User
    form_class=RegisterUserForm
    template_name='account/register.html'
    success_url=reverse_lazy('account:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task:task-list')
        return super().dispatch(request,*args,**kwargs)

class Login(LoginView):
    form_class=LoginForm
    template_name='account/login.html'
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return '/task'
    
class ChangePassword(TemplateView):
    template_name='account/change_password.html'

class SendEmail(TemplateView):
    template_name='account/send_email.html'
    
class ResetPassword(TemplateView):
    template_name='account/reset_password.html'
    



