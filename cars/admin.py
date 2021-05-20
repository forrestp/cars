from django.contrib import admin

from .models import Car, Make, Model, Trim

admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Trim)
admin.site.register(Car)
