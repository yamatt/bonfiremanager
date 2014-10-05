from django.contrib import admin

from bonfiremanager import models

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class TalkAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Room)
admin.site.register(models.Talk, TalkAdmin)
admin.site.register(models.TimeSlot)
