from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Skill)
admin.site.register(Hobby)
admin.site.register(Interest)
admin.site.register(UserImages)
admin.site.register(UserHobby)
admin.site.register(UserInterest)