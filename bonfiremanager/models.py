from django.db import models

class TimeSlot(models.Model):
    pass

class Event(models.Model):
    timeslots = models.ManyToManyField(TimeSlot)

class Room(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=1024)
    directions = models.TextField()

class Talk(models.Model):
    room = models.ForeignKey(Room, null=True, blank=True)
    event = models.ForeignKey(Event)
    timeslot = models.IntegerField(default=0)
    title = models.CharField(max_length=1024)
    description = models.TextField()
