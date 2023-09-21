from django.contrib import admin
from .models import Organization, OrganizationLunchWallet, OrganizationInvites

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationLunchWallet)
admin.site.register(OrganizationInvites)
