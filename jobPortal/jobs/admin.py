from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Job)
admin.site.register(JobTitle)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(JobPortalProfile)
admin.site.register(Location)