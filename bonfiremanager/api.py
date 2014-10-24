from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource

from bonfiremanager import models

class EventResource(ModelResource):
    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Event.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        detail_uri_name = "slug" # use slug field instead of PK
        excludes = ["id"]

class TimeSlotResource(ModelResource):
    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.TimeSlot.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class RoomResource(ModelResource):
    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Room.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class TalkResource(ModelResource):
    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Talk.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

