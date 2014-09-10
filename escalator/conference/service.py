from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from twilio import twiml
from twilio.rest import TwilioRestClient

from conference.models import Conference, CallEvent, Call


class ConferenceCallService(object):

    def __init__(self, client, calling_number):
        self.client = client
        self.calling_number = calling_number

    def initiate_conference_call(self, conference, user):
        path = reverse('conference_response', args=(conference.id,))
        url = "{}{}".format(
            settings.BASE_URL,
            path)
        sid = self._make_call(user.userprofile.phone_number, self.calling_number, url)

        call = Call(conference=conference, user=user, twilio_sid=sid)
        call.save()

        call_event = CallEvent(call=call, event_type=CallEvent.CALL)
        call_event.save()

    def _make_call(self, to_number, from_number, callback_url):
        call = self.client.calls.create(
            to=to_number,
            from_=from_number,
            url=callback_url,
            status_callback=settings.BASE_URL + reverse('voice_call_status'),
            status_method='POST',
            if_machine='Hangup')

        return call.sid

