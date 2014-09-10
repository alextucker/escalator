from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.utils.crypto import get_random_string
from django.http import Http404
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, get_objects_for_user

from organization.serializers import OrganizationSerializer, OrganizationInviteSerializer, OrganizationDetailSerializer, UserDetailSerializer
from organization.models import Organization
from organization.utils import assign_admin_perms


class HomeView(TemplateView):

    template_name = 'home.html'


class OrganizationCreateView(generics.CreateAPIView):

    serializer_class = OrganizationSerializer

    def post_save(self, obj, created):
        if created:
            assign_admin_perms(obj, self.request.user)


class OrganizationInviteCreateView(generics.CreateAPIView):

    serializer_class = OrganizationInviteSerializer

    def pre_save(self, obj):
        organization = Organization.objects.get(id=self.kwargs['pk'])
        obj.organization = organization
        obj.token = get_random_string(length=20, allowed_chars='ABCDEFGHJKMNPQRST23456789')
        obj.user = self.request.user

    def post_save(self, obj, created):
        if created:
            message = "You have been invited to join Escalator!\n {}{}"
            url = reverse('start_invite', args=(obj.id, obj.token,))
            message = message.format(settings.BASE_URL, url)
            send_mail('You have been invited to Escalator', message, 'hello@escalator.io', [obj.email])


class MeRetrieveView(APIView):

    def get(self, request, format=None):
        user = self.request.user
        orgs = get_objects_for_user(self.request.user, 'view_organization', klass=Organization)
        serializer = UserDetailSerializer(user)
        data = serializer.data
        data['organization_id'] = orgs[0].id

        return Response(data)


class OrganizationRetrieveView(generics.RetrieveAPIView):

    serializer_class = OrganizationDetailSerializer
    queryset = Organization.objects.all()
