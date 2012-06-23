from django.contrib import admin
from event.models import Event, Account, ReShout

class ReShoutAdmin(admin.ModelAdmin):
    list_display = ('event', 'account', 'timestamp',)
    search_fields = ['event__name', 'account__handle']
    ordering = ('-timestamp',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'host','is_active', 'is_expired', 'location',)
    ordering = ('-start_date',)
    list_filter = ('is_active', 'is_expired')

admin.site.register(Event, EventAdmin)
admin.site.register(Account)
admin.site.register(ReShout, ReShoutAdmin)
