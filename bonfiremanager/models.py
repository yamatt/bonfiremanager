from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(max_length=1024)
    
    def __str__(self):
        return self.name
    
class TimeSlot(models.Model):
    event = models.ForeignKey(Event)
    bookable = models.BooleanField(default=True)
    end = models.DateTimeField()
    name = models.CharField(max_length=1024)
    start = models.DateTimeField()
    
    def __str__(self):
        return "{0} ({1})".format(self.name, self.event)

class Room(models.Model):
    event = models.ForeignKey(Event)
    directions = models.TextField()
    name = models.CharField(max_length=1024)
    
    def __str__(self):
        return "{0} ({1})".format(self.name, self.event)

class Talk(models.Model):
    room = models.ForeignKey(Room, null=True, blank=True)
    timeslot = models.ForeignKey(TimeSlot, null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=1024)
    title = models.CharField(max_length=1024, unique=True)
    
    def __str__(self):
        return "{0} in {1}".format(self.title, self.room)
