import datetime

from django.db import models
from django.contrib.auth.models import User

# creates Mobile API Key
def make_16_key():
    return User.objects.make_random_password(length=16)

class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    host = models.ForeignKey('event.Account')
    location = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False, blank=True)
    is_expired = models.BooleanField(default=False, blank=True) 

    def __unicode__(self):
        return u"{} ({}) @ {}, starting {}".format(self.name, self.host.handle, self.location, self.start_date)

    @property
    def reshout_count(self):
        return ReShout.objects.filter(event=self).count()

    def save(self):
        # sets is_active based on if the event is already happening
        if datetime.datetime.now() < self.start_date:
            self.is_active = False
        else:
            self.is_active = True

        # sets the end_date to thirty minutes after the start_date
        # only if it upon event creation
        if not self.end_date:
            self.end_date = self.start_date + datetime.timedelta(minutes=30)

        # automatically set is_expired based on now and end_date
        self.is_expired = datetime.datetime.now() > self.end_date
        super(Event, self).save()


class ReShout(models.Model):
    event = models.ForeignKey('event.Event')
    account = models.ForeignKey('event.Account')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{} RS {}".format(self.event.name, self.account)

    def save(self):
        super(ReShout, self).save()
        self.event.end_date = self.timestamp + datetime.timedelta(minutes=30)
        self.event.save()


class Account(models.Model):
    handle = models.CharField(unique=True, max_length=20)
    user = models.ForeignKey('auth.User')
    key = models.CharField(max_length=16, unique=True, blank=True)

    def __unicode__(self):
        return self.handle

    def save(self):
        self.key = make_16_key()
        super(Account, self).save()
