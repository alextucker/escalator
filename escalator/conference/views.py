from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from twilio import twiml
from twilio.rest import TwilioRestClient

from organization.models import Organization
from conference.models import Conference, CallEvent, Call
from conference.service import ConferenceCallService
from conference.serializers import ConferenceSerializer


class CreateConfernceAPIView(generics.CreateAPIView):

    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()

    def pre_save(self, obj):
        obj.organization = Organization.objects.get(id=self.kwargs['pk'])
        obj.twilio_name = get_random_string(length=20, allowed_chars='ABCDEFGHJKMNPQRST23456789')


    def post_save(self, obj, created):
        if not created:
            return

        twilio_client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
        call_service = ConferenceCallService(twilio_client, settings.TWILIO_OUTGOING)
        for user in obj.user_set.all():
            call_service.initiate_conference_call(obj, user)


class ConferenceRetrieveAPIView(generics.RetrieveAPIView):

    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()


class ConferenceResponseView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ConferenceResponseView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        call = Call.objects.get(twilio_sid=self.request.POST['CallSid'])


        calls_connected = Call.objects.filter(conference=call.conference, call_state=Call.IN_CALL)

        call_event = CallEvent(call=call, event_type=CallEvent.JOIN)
        call_event.save()


        r = twiml.Response()
        r.say('We are now connecting you')
        if calls_connected.exists():
            twilio_client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
            r.pause(length=1)
            r.say('The following people are already on the call')
            for c in calls_connected:
                name = "{} {}".format(c.user.first_name, c.user.last_name)
                r.say(name)
                r.pause(length=1)
                url = reverse('conference_announce', args=(call.conference.id, call.user.id,))
                twilio_client.calls.update(c.twilio_sid, method="POST", url=settings.BASE_URL+url)
        with r.dial() as d:
            d.conference(name=str(call.conference.twilio_name), eventCallbackUrl=settings.BASE_URL + reverse('voice_conference_status'), record="record-from-start")

        call.call_state = Call.IN_CALL
        call.save()

        return HttpResponse(r.toxml())


class ConferenceAnnounceView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ConferenceAnnounceView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        call = Call.objects.get(twilio_sid=self.request.POST['CallSid'])
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        r = twiml.Response()
        announce = "{} {} is joining the call".format(user.first_name, user.last_name)
        r.say(announce)
        with r.dial() as d:
            d.conference(name=str(call.conference.twilio_name), eventCallbackUrl=settings.BASE_URL + reverse('voice_conference_status'))

        return HttpResponse(r.toxml())


class CallStatusView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CallStatusView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        DONE_STATUS = ['canceled', 'completed', 'failed', 'busy', 'no-answer']
        call = Call.objects.get(twilio_sid=self.request.POST['CallSid'])
        status = self.request.POST['CallStatus']

        if status in DONE_STATUS:
            call.call_state = Call.DONE
            call.save()
            call_event = CallEvent(call=call, event_type=CallEvent.LEAVE)
            call_event.save()

        return HttpResponse("")


class ConferenceStatusView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ConferenceStatusView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        return HttpResponse("")
