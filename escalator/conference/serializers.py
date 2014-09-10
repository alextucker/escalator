from django.contrib.auth.models import User
from rest_framework import serializers

from conference.models import Conference, Call
from organization.serializers import OrganizationSerializer, UserDetailSerializer


class ConferenceSerializer(serializers.ModelSerializer):
    user_set = serializers.PrimaryKeyRelatedField(many=True)
    has_active_calls = serializers.SerializerMethodField('get_has_active_calls')
    users_on_call = serializers.SerializerMethodField('get_users_on_call')
    users_incoming = serializers.SerializerMethodField('get_users_incoming')
    users_not_in_call = serializers.SerializerMethodField('get_users_not_in_call')

    class Meta:
        model = Conference
        fields = ('id', 'user_set', 'organization', 'name', 'has_active_calls', 'users_on_call', 'users_incoming', 'users_not_in_call', 'twilio_name',)
        read_only_fields = ('organization', 'twilio_name', 'name',)

    def get_has_active_calls(self, obj):
        return obj.call_set.filter(call_state__in=[Call.INCOMING, Call.IN_CALL]).exists()

    def get_users_on_call(self, obj):
        users = []
        active_calls = obj.call_set.filter(call_state=Call.IN_CALL)
        for call in active_calls:
            users.append(call.user)

        return UserDetailSerializer(users, many=True).data

    def get_users_incoming(self, obj):
        users = []
        incoming_calls = obj.call_set.filter(call_state=Call.INCOMING)
        for call in incoming_calls:
            users.append(call.user)

        return UserDetailSerializer(users, many=True).data

    def get_users_not_in_call(self, obj):
        users = []
        not_in_call = obj.call_set.filter(call_state__in=[Call.DONE, Call.UNREACHABLE])
        for call in not_in_call:
            users.append(call.user)

        return UserDetailSerializer(users, many=True).data

