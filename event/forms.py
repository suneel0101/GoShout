from django import forms
import datetime

from event.models import Event
from django.contrib.auth.models import User


class CreateEventForm(forms.Form):
    name = forms.CharField(max_length=300)
    time = forms.CharField(max_length=100)
    location = forms.CharField(max_length=300)

    def process(self, account):

        components = self.cleaned_data['time'].split(':')
        day = int(components[0])
        hour = int(components[1])
        minute = int(components[2])
        now = datetime.datetime.now()
        start_date = datetime.datetime(now.year, now.month, day, hour, minute)

        event = Event(
            name=self.cleaned_data['name'],
            start_date=start_date,
            location=self.cleaned_data['location'],
            host=account
        )
        event.save()
