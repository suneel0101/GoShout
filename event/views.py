import datetime
import simplejson as json

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.serializers import serialize

from django.views.generic.base import TemplateView, View
from event.models import Event, ReShout, make_16_key
from event.forms import CreateEventForm

class DashboardView(TemplateView):
    template_name = 'mobile/oldindex.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.process(request.user.account)
        return HttpResponseRedirect(reverse('dashboard'))


    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['events'] = Event.objects.filter(is_expired=False).order_by('-end_date')
        context['form'] = CreateEventForm()
        context['token'] = make_16_key()
        return context


class CreateEventView(View):

    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.process(request.user.account)
        return HttpResponseRedirect(reverse('dashboard'))


class CreateFormView(TemplateView):
    template_name = 'mobile/shout.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.process(request.user.account)
        return HttpResponseRedirect(reverse('dashboard'))


class MobileCreateEventView(View):
    def post(self, request, *args, **kwargs):
        time = request.POST.get('time')
        components = time.split(':')
        day = int(components[0])
        hour = int(components[1])
        minute = int(components[2])
        now = datetime.datetime.now()
        start_date = datetime.datetime(now.year, now.month, day, hour, minute)
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
        if request.user.is_authenticated():
            events = Event.objects.filter(is_active=True, is_expired=False)
            response_data = []
            for event in events:
                event_data = {
                    'name': event.name,
                    'location': event.location,
                    'year': event.start_date.year,
                    'month': event.start_date.month - 1,
                    'day': event.start_date.day,
                    'hour': event.start_date.hour,
                    'minute': event.start_date.minute,
                    'host': event.host.handle,
                    'reshout_count': event.reshout_count
                }
                response_data.append(event_data)
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        else:
            print 'Unauthorized ping to API!!!'
            return HttpResponse('{}', mimetype="application/json")
