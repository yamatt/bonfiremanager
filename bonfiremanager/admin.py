from django.contrib import admin

from bonfiremanager import models

admin.site.register(models.Event)
admin.site.register(models.Room)
admin.site.register(models.Talk)
admin.site.register(models.TimeSlots)
