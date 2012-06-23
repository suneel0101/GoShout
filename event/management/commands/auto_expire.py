from django.core.management.base import BaseCommand
from event.models import Event

import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        events = Event.objects.filter(is_expired=False, end_date__lt=now).update(is_expired=True, is_active=False)
