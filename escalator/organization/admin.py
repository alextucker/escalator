from django.contrib import admin
from organization.models import Organization, PhoneNumber, UserProfile

admin.site.register(Organization)
admin.site.register(PhoneNumber)
admin.site.register(UserProfile)

