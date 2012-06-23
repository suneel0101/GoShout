import datetime

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.base import TemplateView, View
from event.models import Event, Account, ReShout
from event.forms import CreateEventForm

class DashboardView(TemplateView):
    template_name = 'event/dashboard.html'


    def get(self, request, *args, **kwargs):
        self.events = Event.objects.filter(is_expired=False)
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['events'] = self.events
        context['form'] = CreateEventForm()
        return context


class CreateEventView(View):

    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.process(Account.objects.get(user=request.user))
        return HttpResponseRedirect(reverse('dashboard'))

class ReshoutView(View):

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(id=event_id)
        account = Account.objects.get(user=request.user)
        timestamp = datetime.datetime.now()
        reshout = ReShout(
            event = event,
            account = account,
            timestamp = timestamp
        )
        reshout.save()
        return HttpResponseRedirect(reverse('dashboard'))

        pass