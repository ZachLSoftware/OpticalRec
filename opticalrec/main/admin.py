from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CreateUser
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form=CreateUser
    model=User
    list_display = ['username',]

admin.site.register(User, CustomUserAdmin)

# Register your models here.
