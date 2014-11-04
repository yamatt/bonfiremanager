from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import F
from django.middleware.csrf import _sanitize_token, constant_time_compare

from tastypie import fields
from tastypie import http
from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from bonfiremanager import models

class CsrfAuthentication(object):
    """Make sure CSRF header is there and valid

    We don't have users per se, but we need to do something to prevent
    CSRF abuse.
    """
    def is_authenticated(self, request, **kwargs):
        """Check for valid CSRF token"""
        # Cargo-culted from TastyPie (which itself was cargo-culted from Django)
        # However, we only want CSRF, all our anons are anon.
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return True

        csrf_token = _sanitize_token(request.COOKIES.get(settings.CSRF_COOKIE_NAME, ''))

        if request.is_secure():
            referer = request.META.get('HTTP_REFERER')

            if referer is None:
                return False

            good_referer = 'https://%s/' % request.get_host()

            if not same_origin(referer, good_referer):
                return False

        request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

        return constant_time_compare(request_csrf_token, csrf_token)

    def get_identifier(self, request):
        return "nouser"

    def check_active(self, user):
        return True

class CreateAndReadAuthorization(ReadOnlyAuthorization):
    """Create And Read, but you can't Update"""
    def create_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return object_list

##
# Resources
##

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
    event = fields.ToOneField(EventResource, "event")

    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.TimeSlot.objects.all().select_related("event")
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class RoomResource(ModelResource):
    event = fields.ToOneField(EventResource, "event")

    class Meta:
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        queryset = models.Room.objects.all().select_related("event")
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        detail_uri_name = "slug" # use slug field instead of PK
        excludes = ["id"]

class TalkResource(ModelResource):
    vote_uri = fields.CharField(readonly=True)
    room = fields.ToOneField(RoomResource, "room", readonly=True, null=True)
    timeslot = fields.ToOneField(TimeSlotResource, "timeslot")

    @transaction.atomic
    def make_vote(self, request, **kwargs):
        """Voting endpoint

        Expects no data and returns HTTP 204 to the client
        """
        self.method_check(request, allowed=["post"])
        self.throttle_check(request)

        # so grab the detail_uri_name setting from Meta
        filters = {self._meta.detail_uri_name: kwargs[self._meta.detail_uri_name]}
        models.Talk.objects.filter(**filters).update(score=F("score")+1)

        self.log_throttled_access(request)

        return http.HttpNoContent()

    def dehydrate_vote_uri(self, bundle):
        """Build the URL for voting"""
        # our voting url takes the same kwargs as 'resource_uri'
        return reverse("api_talk_vote", kwargs=self.resource_uri_kwargs(bundle))

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<%s>.*?)/vote%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('make_vote'), name="api_talk_vote"),
            ]

    class Meta:
        detail_allowed_methods = ["get", "post"]
        list_allowed_methods = ["get", "post"]
        queryset = models.Talk.objects.all().select_related("timeslot", "room")
        authentication = CsrfAuthentication()
        authorization = CreateAndReadAuthorization()
        detail_uri_name = "slug" # use slug field instead of PK
        excludes = ["id"]
