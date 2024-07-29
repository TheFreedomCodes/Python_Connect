from django.contrib import admin
from .models import *
admin.site.register(NGO)
admin.site.register(Profile)
class NGOAdmin(admin.ModelAdmin):
    list_display=('name','location','email')