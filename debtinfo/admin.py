from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    """Customise the Profile content displayed on the admin site."""

    list_display = ('debtor', 'creditor')


class DebtorAdmin(admin.ModelAdmin):
    """Customise the Debtor content displayed on the admin site."""

    list_display = ('debtor', 'id_number')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Debtor, DebtorAdmin)
