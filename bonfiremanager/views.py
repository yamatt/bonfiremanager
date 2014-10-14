from django.db.models import Count
from django.views import generic
from django.core.urlresolvers import reverse

from bonfiremanager import forms, models

class EventSlugMixin(object):
    """Mixin that puts the event slug into the template context"""
    def get_context_data(self, **kwargs):
        kwargs.setdefault("event_slug", self.kwargs["event_slug"])
        return super(EventSlugMixin, self).get_context_data(**kwargs)

class IndexView(generic.ListView):
    model = models.Event
    template_name = "event_list.dj.html"
    context_object_name = "events"

class EventView(EventSlugMixin, generic.DetailView):
    model = models.Event
    template_name = "grid.dj.html"
    context_object_name = "event"
    slug_url_kwarg = "event_slug"

    def get_queryset(self):
        qs = super(EventView, self).get_queryset().annotate(room_count=Count("room__id"))
        return qs.prefetch_related("room_set", "timeslot_set", "timeslot_set__talk_set", "room_set__talk_set")

class AddTalkView(EventSlugMixin, generic.CreateView):
    model = models.Talk
    form_class = forms.TalkForm
    template_name = "talk_form.dj.html"

    def get_initial(self):
        return {"event": models.Event.objects.get(slug=self.kwargs["event_slug"])}

    def get_success_url(self):
        return reverse("talk", kwargs={"event_slug": self.kwargs["event_slug"], "talk_slug": self.object.slug})
        
class TalkView(EventSlugMixin, generic.DetailView):
    model = models.Talk
    template_name = "talk.dj.html"
    context_object_name = "talk"
    slug_url_kwarg = "talk_slug"

class RoomView(EventSlugMixin, generic.DetailView):
    model = models.Room
    template_name = "room.dj.html"
    context_object_name = "room"
