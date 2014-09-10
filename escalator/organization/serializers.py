from django.contrib.auth.models import User

from rest_framework import serializers

from organization.models import Organization, UserProfile, PhoneNumber
from invite.models import OrganizationInvite


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('name', 'id',)
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('phone_number',)


class UserDetailSerializer(serializers.ModelSerializer):

    #userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id',)
        read_only_fields = ('first_name', 'last_name', 'id',)


class OrganizationDetailSerializer(serializers.ModelSerializer):

    user_set = UserDetailSerializer(many=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'user_set', 'phonenumber_set',)


class OrganizationInviteSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = OrganizationInvite
        fields = ('id', 'email', 'token', 'is_used', 'created', 'modified', 'user',)
        read_only_fields = ('id', 'token', 'is_used', 'created', 'modified', )
        depth = 1
