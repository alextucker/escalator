from django.db import models
from django.contrib.auth.models import Group, User


class Conference(models.Model):

    organization = models.ForeignKey('organization.Organization')
    phone_number = models.ForeignKey('organization.PhoneNumber', null=True, blank=True)
    user_set = models.ManyToManyField(User)

    twilio_name = models.CharField(max_length=127)
    name = models.CharField(max_length=127, default='')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{} -- {}".format(self.name, self.organization.name)


class Call(models.Model):
    INCOMING = 'INCOMING'
    IN_CALL = 'IN_CALL'
    DONE = 'DONE'
    UNREACHABLE = 'UNREACHABLE'

    CALL_STATE_CHOICES = (
        (INCOMING, 'Call is being initiated'),
        (IN_CALL, 'User is actively in call'),
        (DONE, 'User has hang up'),
        (UNREACHABLE, 'User was unreachable'),
    )

    conference = models.ForeignKey('conference.Conference')
    user = models.ForeignKey(User)
    twilio_sid = models.CharField(max_length=40, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    call_state = models.CharField(choices=CALL_STATE_CHOICES, default=INCOMING, max_length=20)

    def __unicode__(self):
        return "{} - {} {}".format(
            self.conference.name,
            self.user.first_name,
            self.user.last_name)


class CallEvent(models.Model):
    CALL = 'CALL'
    JOIN= 'JOIN'
    LEAVE= 'LEAVE'

    CONFERENCE_EVENT_CHOICES = (
        (CALL, 'User is Called'),
        (JOIN, 'User Joins Call'),
        (LEAVE, 'User Leaves Call'),
    )

    call = models.ForeignKey('conference.Call')
    event_datetime = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=16, choices=CONFERENCE_EVENT_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} {}, {}, {}".format(
            self.call.user.first_name,
            self.call.user.last_name,
            self.event_type,
            str(self.event_datetime))

