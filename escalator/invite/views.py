from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.utils.crypto import get_random_string
from django.http import Http404
from django.core.urlresolvers import reverse
from django import forms
from django.views.generic.edit import FormView

from rest_framework import generics
from guardian.shortcuts import assign_perm

from organization.serializers import OrganizationSerializer, OrganizationInviteSerializer, OrganizationDetailSerializer
from organization.models import Organization, UserProfile
from invite.models import OrganizationInvite
from organization.utils import assign_admin_perms


class InviteView(TemplateView):

    template_name = 'invite.html'

    def get_context_data(self, id, token):
        context = {}
        invite = get_object_or_404(OrganizationInvite, id=self.kwargs['id'])

        if not invite.is_used and invite.token == self.kwargs['token']:
            context['invite_user'] = invite.user
            context['organization'] = invite.organization
            self.request.session['invite'] = invite.id
        else:
            raise Http404

        return context


class UseInviteView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'dashboard'

    def get_redirect_url(self, *args, **kwargs):

        try:
            invite = OrganizationInvite.objects.get(id=self.request.session['invite'])
            invite.is_used = True
            invite.save()

            invite.organization.user_set.add(self.request.user)
            assign_perm('view_organization', self.request.user, invite.organization)
            assign_perm('create_organization_group', self.request.user, invite.organization)
            return reverse('onboard_invite')
        except:
            return reverse('onboard_organization')

        return super(UseInviteView, self).get_redirect_url(*args, **kwargs)


class OrganizationOnboardingForm(forms.Form):

    name = forms.CharField()
    phone_number = forms.CharField()


class InviteOnboardingForm(forms.Form):

    phone_number = forms.CharField()


class OrganizationOnboardingView(FormView):

    template_name = 'orgOnboarding.html'
    form_class = OrganizationOnboardingForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        org = Organization(name=form.cleaned_data['name'])
        org.save()
        self.request.user.userprofile.phone_number = form.cleaned_data['phone_number']
        self.request.user.userprofile.save()

        assign_admin_perms(org, self.request.user)
        return super(OrganizationOnboardingView, self).form_valid(form)


class InviteOnboardingView(FormView):

    template_name = 'inviteOnboarding.html'
    form_class = InviteOnboardingForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        self.request.user.userprofile.phone_number = form.cleaned_data['phone_number']
        self.request.user.userprofile.save()

        return super(InviteOnboardingView, self).form_valid(form)
