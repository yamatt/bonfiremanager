from django.views import generic

from bonfiremanager import forms, models

class EventSlugMixin(object):
    """Mixin that puts the event slug into the template context"""
    def get_context_data(self, **kwargs):
        kwargs.setdefault("event_slug", self.kwargs["event_slug"])
        return super(EventSlugMixin, self).get_context_data(**kwargs)

class IndexView(generic.ListView):
    model = models.Event

class EventView(EventSlugMixin, generic.ListView):
    model = models.Room
    template_name = "grid.dj.html"
    context_object_name = "rooms"

    def get_queryset(self):
        qs = super(EventView, self).get_queryset().filter(event__slug=self.kwargs["event_slug"])
        return qs

    def get_event_timeslots(self):
        return models.TimeSlot.objects.get(event__slug=self.kwargs["event_slug"])

    def get_context_data(self, **kwargs):
        kwargs.setdefault("event_timeslots", self.get_event_timeslots)

        return super(EventView, self).get_context_data(**kwargs)

class AddTalkView(EventSlugMixin, generic.CreateView):
    model = models.Talk
    form_class = forms.TalkForm
    template_name = "talk_form.dj.html"

    def get_initial(self):
        return {"event": models.Event.objects.get(slug=self.kwargs["event_slug"])}
