from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings
from django.conf.urls.static import static
from signup.views import LandingView
from event.views import DashboardView, CreateEventView, ReShoutView, EventListView, MobileCreateEventView, CreateFormView
admin.autodiscover()

#urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',

    url(r'^logout/$', 'signup.views.logout', name='logout'),
    url(r'^login/$', LandingView.as_view(), name='login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'create_event/', CreateEventView.as_view(), name='create_event'),
    url(r'reshout/(?P<event_id>[\d]+)/', ReShoutView.as_view(), name='reshout'),
    url(r'^events/', EventListView.as_view(), name='event_api'),
    url(r'^create/', MobileCreateEventView.as_view(), name='mobile_create'),
    url(r'^create_form/', CreateFormView.as_view(), name='create_shout'),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)



