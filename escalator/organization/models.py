from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class BaseModel(models.Model):

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Organization(BaseModel):

    name = models.CharField(max_length=127, default='')
    user_set = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('edit_organization', 'Edit Organization'),
            ('view_organization', 'View Organization'),
            ('create_organization_group', 'Create Organization Group'),
            ('invite_organization_user', 'Invite User to Organization'),
        )


class PhoneNumber(models.Model):

    twilio_sid = models.CharField(max_length=34, default='')
    phone_number = models.CharField(max_length=20)
    organization = models.ForeignKey('organization.Organization')

    def __unicode__(self):
        return "{} ({})".format(self.phone_number, self.organization.name)


class UserProfile(models.Model):

    phone_number = models.CharField(max_length=20, default='')
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "{} {} - {}".format(self.user.first_name, self.user.last_name, self.phone_number)


## Create Auth Tokens
@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
