from django import forms
import datetime

from event.models import Event
from django.contrib.auth.models import User


class CreateEventForm(forms.Form):
    name = forms.CharField(max_length=300)
    start_date = forms.DateTimeField(initial=datetime.datetime.now())
    location = forms.CharField(max_length=300)

    def process(self, account):
        event = Event(
            name=self.cleaned_data['name'],
            start_date=self.cleaned_data['start_date'],
            location=self.cleaned_data['location'],
            host=account
        )
        event.save()
