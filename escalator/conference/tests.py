from mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from organization.models import Organization, PhoneNumber, UserProfile
from conference.models import Conference, Call, CallEvent
from conference.service import ConferenceCallService


class CreateConferenceTestCase(APITestCase):

    def setUp(self):
        self.organization = Organization(name='Foo Org')
        self.organization.save()

        self.phone_number = PhoneNumber(organization=self.organization, twilio_sid='xxx', phone_number='+15550009999')
        self.phone_number.save()

        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.user.userprofile.phone_number = "5556667777"
        self.user.userprofile.save()

        self.client.login(usernam='foo', password='password')

        self.url = reverse('api_create_conference', args=(self.organization.id,))

    @patch.object(ConferenceCallService, '_make_call')
    def test_create_conference_with_no_participants(self, mock_method):
        mock_method.return_value = '123'
        data = {
            "name": "Lonely Conference",
            "phone_number": self.phone_number.id,
            "users": []
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Conference.objects.filter(name=data["name"]).exists())
        self.assertFalse(mock_method.called)

    @patch.object(ConferenceCallService, '_make_call')
    def test_create_conference_with_self_participants(self, mock_method):
        mock_method.return_value = '123'
        data = {
            "name": "Lonely Conference",
            "user_set": [
                self.user.id
            ]
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Conference.objects.filter(name=data["name"]).exists())
        conf = Conference.objects.get(id=response.data['id'])
        self.assertEquals(conf.organization, self.organization)
        self.assertEquals(len(conf.user_set.all()), 1)
        self.assertEquals(conf.user_set.all()[0], self.user)
        self.assertTrue(mock_method.called)

    @patch.object(ConferenceCallService, '_make_call')
    def test_create_conference_with_multiple_participants(self, mock_method):
        mock_method.return_value = '123'
        new_user = User.objects.create_user(username='bar', email='bar@foo.com', password='password')
        new_user.userprofile.phone_number = "5556667777"
        new_user.userprofile.save()


        data = {
            "name": "Party Conference",
            "phone_number": self.phone_number.id,
            "user_set": [
                self.user.id,
                new_user.id
            ]
        }

        response = self.client.post(self.url, data, format='json')
        conf = Conference.objects.get(id=response.data['id'])
        self.assertEquals(len(conf.user_set.all()), 2)


class ConferenceResponseViewTestCase(TestCase):

    def setUp(self):
        self.organization = Organization(name='Foo Org')
        self.organization.save()

        self.phone_number = PhoneNumber(organization=self.organization, twilio_sid='xxx', phone_number='+15550009999')
        self.phone_number.save()

        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.user.userprofile.phone_number = "5556667777"
        self.user.userprofile.save()

        self.conference = Conference(organization=self.organization, name='My Conf', phone_number=self.phone_number)
        self.conference.save()

    def test_incoming_call(self):
        self.conference.user_set.add(self.user)
        call = Call(conference=self.conference, user=self.user, twilio_sid='888')
        call.save()
        self.assertEquals(call.call_state, call.INCOMING)

        url = reverse('conference_response', args=(self.conference.id,))
        resp = self.client.post(url, {'CallSid':call.twilio_sid})
        #self.assertContains(resp.content, self.conference.name)
        call_result = Call.objects.get(id=call.id)
        self.assertEquals(call_result.call_state, Call.IN_CALL)
        self.assertTrue(CallEvent.objects.filter(call=call, event_type=CallEvent.JOIN).exists())
