from django.contrib import admin

from .models import APIKey, Weather

admin.register(APIKey)(admin.ModelAdmin)
admin.register(Weather)(admin.ModelAdmin)