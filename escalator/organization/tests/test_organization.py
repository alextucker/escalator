from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from organization.models import Organization
from organization.utils import assign_admin_perms


class CreateOrganizationTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('api_create_organization')

    def test_create_organization(self):
        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.client.login(username='foo', password='password')
        data = {
            "name": "Foo Organization"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        instance = Organization.objects.get(id=response.data['id'])
        self.assertEquals(len(instance.user_set.all()), 1)
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.has_perm('edit_organization', instance))
        self.assertTrue(user.has_perm('view_organization', instance))
        self.assertTrue(user.has_perm('create_organization_group', instance))
        self.assertTrue(user.has_perm('invite_organization_user', instance))


class ViewOrganizationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo', email='foo@foo.com', password='password')
        self.client.login(username='foo', password='password')
        self.organization = Organization(name='Foo Org')
        self.organization.save()
        assign_admin_perms(self.organization, self.user)
        self.url = reverse('api_retrieve_organization', args=(self.organization.id,))

    def test_view_organization(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.organization.id)
        self.assertEqual(response.data['name'], self.organization.name)
        self.assertEqual(len(response.data['user_set']), len(self.organization.user_set.all()))

