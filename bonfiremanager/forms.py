from django import forms

from bonfiremanager import models

class TalkForm(forms.ModelForm):
    class Meta:
        model = models.Talk
        fields = ["title", "description", "timeslot"]
