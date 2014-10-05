from django.db import models

class TimeSlot(models.Model):
    event = models.ForeignKey(Event)
    bookable = models.BooleanField(default=True)
    end = models.DateTimeField()
    name = models.CharField(max_length=1024)
    start = models.DateTimeField()

class Event(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(max_length=1024)

class Room(models.Model):
    event = models.ForeignKey(Event)
    directions = models.TextField()
    name = models.CharField(max_length=1024)

class Talk(models.Model):
    room = models.ForeignKey(Room, null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=1024)
    timeslot = models.IntegerField(default=0)
    title = models.CharField(max_length=1024, unique=True)
