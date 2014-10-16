from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from datetime import datetime

class Event(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(max_length=1024)
    
    def get_unassigned_talks(self):
        """Gets all talks grouped by timeslot
        """
        times = []
        for timeslot in self.timeslot_set.all():
            times.append(timeslot.talk_set.filter(room__isnull=True))
        return times

    def get_talk_grid(self):
        """Get the talk grid

        Recommend that you do a prefetch_related("room", "timeslot", "room__talk") to
        reduce fetch-time. You can also annotate "room_count" on too :)"""
        if hasattr(self, "_grid"):
            return self._grid
        else:
            rooms = []

            # create the first row
            times = [None]
            times.extend(self.timeslot_set.all())
            rooms.append(times)

            # add a grid of None
            rooms.extend([[None for i in xrange(0, len(rooms[0]))] for i in xrange(0, self.get_room_count())])

            # replace grid cells with talks
            for room_index, room in enumerate(self.room_set.all().distinct()):
                rooms[room_index+1][0] = room
                for talk in room.talk_set.all():
                    column_index = rooms[0].index(talk.timeslot)
                    rooms[room_index+1][column_index] = talk

            # store grid locally and return
            self._grid = rooms
            return rooms

    def get_room_count(self):
        if hasattr(self, "room_count"):
            return self.room_count
        else:
            return self.room_set.count()

    def __str__(self):
        return self.name
    
class TimeSlot(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=1024)
    bookable = models.BooleanField(default=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def started(self):
        return self.start < datetime.utcnow()
    
    def ended(self):
        return self.end < datetime.utcnow()
    
    def __str__(self):
        return "{0} ({1})".format(self.name, self.event)

class Room(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=1024)
    directions = models.TextField(blank=True)
    
    def __str__(self):
        return "{0} ({1})".format(self.name, self.event)

class Talk(models.Model):
    room = models.ForeignKey(Room, null=True, blank=True)
    timeslot = models.ForeignKey(TimeSlot)
    title = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(max_length=1024)
    description = models.TextField()
    score = models.IntegerField(default=0)
    
    def save(self):
        """Over-riding to add talk slug so can be added from template
        """
        if hasattr(self, "slug") and not self.slug:
            self.slug = slugify(self.title)
        return super(Talk, self).save()

    def __str__(self):
        return "{0} in {1} at {2}".format(self.title, self.room if self.room else "no room", self.timeslot)
