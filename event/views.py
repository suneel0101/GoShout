import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.serializers import serialize

from django.views.generic.base import TemplateView, View
from event.models import Event, Account, ReShout
from event.forms import CreateEventForm


class DashboardView(TemplateView):
    template_name = 'event/dashboard.html'

    def get(self, request, *args, **kwargs):
        self.events = Event.objects.filter(is_expired=False).order_by('start_date')
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
            form.process(request.user.account)
        return HttpResponseRedirect(reverse('dashboard'))


class ReShoutView(View):

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(id=event_id)
        account = request.user.account
        timestamp = datetime.datetime.now()
        reshout = ReShout(
            event=event,
            account=account,
            timestamp=timestamp
        )
        reshout.save()
        return HttpResponseRedirect(reverse('dashboard'))


class EventListView(View):

    def get(self, request, *args, **kwargs):
        key = request.session.get('key')
        try:
            Account.objects.get(key=key)
        except Account.DoesNotExist:
            print 'Unauthorized ping to API!!!'
            return HttpResponse('{}', mimetype="application/json")
        else:
            events = Event.objects.filter(is_active=True, is_expired=False)
            json = serialize('json', events)
            return HttpResponse(json, mimetype="application/json")
