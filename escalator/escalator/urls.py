from django.conf.urls import patterns, include, url
from django.contrib import admin

from conference.views import ConferenceResponseView, CreateConfernceAPIView, ConferenceAnnounceView, ConferenceRetrieveAPIView, CallStatusView, ConferenceStatusView
from organization.views import HomeView, OrganizationCreateView, OrganizationInviteCreateView, OrganizationRetrieveView, MeRetrieveView
from invite.views import InviteView, UseInviteView, OrganizationOnboardingView, InviteOnboardingView
from dashboard.views import DashboardView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'escalator.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^dashboard/?$', DashboardView.as_view(), name='dashboard'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^invite/(?P<id>\d+)/(?P<token>[\w-]+)/?$', InviteView.as_view(), name='start_invite'),
    url(r'^start/?$', UseInviteView.as_view(), name='use_invite'),
    url(r'^start/organization/?$', OrganizationOnboardingView.as_view(), name='onboard_organization'),
    url(r'^start/invite/?$', InviteOnboardingView.as_view(), name='onboard_invite'),

    url(r'^conf/(?P<conf_id>\d+)/?$', ConferenceResponseView.as_view(), name='conference_response'),
    url(r'^conf/(?P<conf_id>\d+)/announce/(?P<user_id>\d+)/?$', ConferenceAnnounceView.as_view(), name='conference_announce'),
    url(r'^voice/call/status/?$', CallStatusView.as_view(), name='voice_call_status'),
    url(r'^voice/conference/status/?$', ConferenceStatusView.as_view(), name='voice_conference_status'),

    url(r'^api/v1/me/?$', MeRetrieveView.as_view(), name='api_me'),
    url(r'^api/v1/organizations/(?P<pk>\d+)/conferences/?$', CreateConfernceAPIView.as_view(), name='api_create_conference'),
    url(r'^api/v1/organizations/(?P<pk>\d+)/invites/?$', OrganizationInviteCreateView.as_view(), name='api_invite_user'),
    url(r'^api/v1/organizations/?$', OrganizationCreateView.as_view(), name='api_create_organization'),
    url(r'^api/v1/organizations/(?P<pk>\d+)/?$', OrganizationRetrieveView.as_view(), name='api_retrieve_organization'),
    url(r'^api/v1/conferences/(?P<pk>\d+)/?$', ConferenceRetrieveAPIView.as_view(), name='api_retrieve_conference'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'},name='logout'),
)
