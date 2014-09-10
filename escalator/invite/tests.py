from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.test import APITestCase

from organization.models import Organization
from invite.models import OrganizationInvite
from organization.utils import assign_admin_perms


class CreateInviteTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.client.login(username='foo', password='password')


    def test_create_invite(self):
        self.org = Organization(name='Foo Org')
        self.org.save()
        assign_admin_perms(self.org, self.user)
        url = reverse('api_invite_user', args=(self.org.id,))
        data = {
            "email": "foo@bar.com"
        }
        resp = self.client.post(url, data, format='json')
        self.assertEquals(20, len(resp.data['token']))
        self.assertEquals(resp.data['user']['id'], self.user.id)


class StartInviteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.org = Organization(name='Foo Org')
        self.org.save()
        assign_admin_perms(self.org, self.user)
        self.invite = OrganizationInvite(email='foo@bar.com', organization=self.org, user=self.user)
        self.invite.token = get_random_string(length=20, allowed_chars='ABCDEFGHJKMNPQRST23456789')
        self.invite.save()

    def test_receive_invite(self):
        url = reverse('start_invite', args=(self.invite.id, self.invite.token,))
        resp = self.client.get(url)
        self.assertEquals(self.client.session['invite'], self.invite.id)
        self.assertEquals(resp.context['invite_user'], self.user)
        self.assertEquals(resp.context['organization'], self.org)
        self.assertEquals(resp.status_code, 200)

    def test_receive_invite_used(self):
        url = reverse('start_invite', args=(self.invite.id, self.invite.token,))
        self.invite.is_used = True
        self.invite.save()
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)

    def test_receive_invite_does_not_exist(self):
        url = reverse('start_invite', args=(999, 'fake',))
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)


class UseInviteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.org = Organization(name='Foo Org')
        self.org.save()
        assign_admin_perms(self.org, self.user)
        self.invite = OrganizationInvite(email='foo@bar.com', organization=self.org, user=self.user)
        self.invite.token = get_random_string(length=20, allowed_chars='ABCDEFGHJKMNPQRST23456789')
        self.invite.save()

    def test_use_invite(self):
        url = reverse('use_invite')
        self.client.login(username='foo', password='password')
        session = self.client.session
        session['invite'] = self.invite.id
        session.save()
        resp = self.client.get(url)
        invite = OrganizationInvite.objects.get(id=self.invite.id)
        self.assertTrue(invite.is_used)
        self.assertEquals(resp.status_code, 302)

    def test_no_invite(self):
        url = reverse('use_invite')
        self.client.login(username='foo', password='password')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 302)
