from django.contrib import admin
from conference.models import Conference, CallEvent, Call

admin.site.register(Conference)
admin.site.register(CallEvent)
admin.site.register(Call)
