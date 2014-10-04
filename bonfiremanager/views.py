from django.views import generic

from bonfiremanager import forms, models

class IndexView(generic.ListView):
    model = models.Room
    template_name = "grid.dj.html"
    event = None
    context_object_name = "rooms"

    def get_event_timeslots(self):
        return models.TimeSlot.objects.filter(event__id=self.event)

    def get_context_data(self, **kwargs):
        kwargs.setdefault("event_timeslots", self.get_event_timeslots)

        return super(IndexView, self).get_context_data(**kwargs)

class AddTalkView(generic.CreateView):
    model = models.Talk
    form_class = forms.TalkForm
    template_name = "talk_form.dj.html"
