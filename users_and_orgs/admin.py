from django.contrib import admin

from users_and_orgs.models import CustomUser, Organization

admin.site.register(CustomUser)
admin.site.register(Organization)
