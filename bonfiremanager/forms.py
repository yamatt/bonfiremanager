from django import forms

from bonfiremanager import models

class TalkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.fields["timeslot"].queryset = models.TimeSlot.objects.filter(event=kwargs["initial"]["event"], bookable=True)

    class Meta:
        model = models.Talk
        fields = ["title", "description", "timeslot"]
