from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser,Address,Hobby,Interest,UserActivity,UserQualifications

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["email", "username","id"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(Hobby)
admin.site.register(Interest)
admin.site.register(UserActivity)
admin.site.register(UserQualifications)