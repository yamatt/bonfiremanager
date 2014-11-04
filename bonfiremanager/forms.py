from django import forms
from django.db.models import F

from bonfiremanager import models

class TalkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.fields["timeslot"].queryset = models.TimeSlot.objects.filter(event=kwargs["initial"]["event"], bookable=True)

    class Meta:
        model = models.Talk
        fields = ["title", "description", "timeslot"]

class VoteForm(forms.Form):
    """Empty form for "vote" button"""
    def __init__(self, instance=None, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.object = instance
        if not isinstance(self.object, models.Talk):
            raise Exception("wtf mate")

    def save(self):
        models.Talk.objects.filter(pk=self.object.pk).update(score=F("score")+1)
        return self.object
