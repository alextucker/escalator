from django.db import models
from django.contrib.auth.models import Group, User


class OrganizationInvite(models.Model):

    email = models.EmailField()
    token = models.CharField(max_length=50, default='')
    organization = models.ForeignKey('organization.Organization')
    is_used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="invitee")
    invited = models.ForeignKey(User, null=True, blank=True)


class BetaInvite(models.Model):

    email = models.EmailField()
    token = models.CharField(max_length=50, default='')
    is_used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    invited = models.ForeignKey(User, null=True, blank=True)
