from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(max_length=1024)

    def get_talk_grid(self):
        """Get the talk grid

        Recommend that you do a prefetch_related("room", "timeslot", "room__talk") to
        reduce fetch-time. You can also annotate "room_count" on too :)"""
        rows = []
        times = [None]
        times.extend(self.timeslot_set.all())
        rows.append(times)
        rows.extend([[None]*len(rows[0])] * self.get_room_count())
        for row_index, room in enumerate(self.room_set.all()):
            rows[row_index+1][0] = room
            for talk in room.talk_set.all():
                column_index = rows[0].index(talk.timeslot)
                rows[row_index+1][column_index] = talk

        return rows

    def get_room_count(self):
        if hasattr(self, "room_count"):
            return self.room_count
        else:
            return self.room_set.count()

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
        return "{0} in {1} at {2}".format(self.title, self.room, self.timeslot)
