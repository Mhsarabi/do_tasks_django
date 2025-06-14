from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display=["email","is_superuser","is_active"]
    list_filter=["email","is_superuser","is_active"]
    search_fields=("email",)
    ordering=('email',)
    add_form = RegisterUserForm
    fieldsets=(
        ("personal_data",{
            "fields":(
                "email","password"
            )
        }),
        ("group_permission",{
            "fields":(
                "groups","user_permissions"
            )
        }),
        ("important_date",{
            "fields":(
                "last_login",
            )
        }),
        ("permission",{
            "fields":(
                'is_staff','is_active',"is_superuser"
            )
        })  
    )
    add_fieldsets=(
        ("personal_date",{
            "fields":(
                "email","password1","password2","is_staff","is_active","is_superuser"
            )
        }),
    )
admin.site.register(User,CustomUserAdmin)
admin.site.site_header="To Do List"