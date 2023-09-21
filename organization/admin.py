from django.contrib import admin


from .models import Invitation

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lunch_price', 'currency', 'created_at', 'updated_at')

    # You can customize the display and behavior of the Organization admin here.


@admin.register(OrganizationLunchWallet)
class OrganizationLunchWalletAdmin(admin.ModelAdmin):
    list_display = ('org_id', 'balance', 'created_at', 'updated_at')
    list_filter = ('org_id', 'created_at', 'updated_at')
    search_fields = ('org_id__name',)



@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'organization', 'email', 'token', 'ttl')
    list_filter = ('organization', 'ttl')
    search_fields = ('sender__username', 'receiver__username', 'organization__name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'receiver', 'organization')


from .models import Organization, OrganizationInvites, OrganizationLunchWallet

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationLunchWallet)
admin.site.register(OrganizationInvites)

