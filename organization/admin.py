from django.contrib import admin
from .models import Organization, OrganizationInvites, OrganizationLunchWallet

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationLunchWallet)
admin.site.register(OrganizationInvites)
