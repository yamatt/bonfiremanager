from django.conf.urls import url
from django.db import transaction
from django.db.models import F

from tastypie import fields
from tastypie import http
from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from bonfiremanager import models

class TalkResource(ModelResource):
    @transaction.atomic
    def make_vote(self, request, **kwargs):
        """Voting endpoint"""
        self.method_check(request, allowed=["post"])
        self.throttle_check(request)
        raise Exception(kwargs)
        # we don't know whether we're going to use PKs or slugs
        # so grab the detail_uri_name setting from Meta
        filters = {self._meta.detail_uri_name: kwargs[self._meta.detail_uri_name]}
        models.Talk.objects.filter(**filters).update(score=F("score")+1)

        self.log_throttled_access(request)

        return http.HttpNoContent()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<%s>.*?)/vote%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('make_vote'), name="api_talk_vote"),
            ]

    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Talk.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class TimeSlotResource(ModelResource):
    talks = fields.ToManyField(TalkResource, "talk_set")

    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.TimeSlot.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class RoomResource(ModelResource):
    talks = fields.ToManyField(TalkResource, "talk_set")

    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Room.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class EventResource(ModelResource):
    timeslots = fields.ToManyField(TimeSlotResource, "timeslot_set", full=True, full_list=False)
    rooms = fields.ToManyField(RoomResource, "room_set", full=True, full_list=False)

    # collect talks too
    talks = fields.ToManyField(
                TalkResource,
                lambda bundle: models.Talk.objects.filter(timeslot__event__pk=bundle.obj.pk),
                full=True,
                full_list=False,
                )

    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Event.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        detail_uri_name = "slug" # use slug field instead of PK
        excludes = ["id"]
