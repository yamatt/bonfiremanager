from django.contrib import admin

from bonfiremanager import models

class EventAdmin(admin.ModelAdmin):
    pass

class TalkAdmin(admin.ModelAdmin):
    list_display = ("title", "room", "timeslot")
    list_filter = ("room__event",)

class TimeSlotAdmin(admin.ModelAdmin):
    list_filter = ("event",)

class RoomAdmin(admin.ModelAdmin):
    list_filter = ("event",)

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Talk, TalkAdmin)
admin.site.register(models.TimeSlot, TimeSlotAdmin)
