from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings

from guardian.shortcuts import get_objects_for_user
from organization.models import Organization


class DashboardView(TemplateView):

    template_name = 'dashboard.html'

