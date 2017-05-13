from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    """Customizes the Profile content displayed on the admin site."""

    list_display = ('debtor', 'creditor')


class DebtorAdmin(admin.ModelAdmin):
    """Customizes the Debtor content displayed on the admin site."""

    list_display = ('debtor', 'id_number')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Debtor, DebtorAdmin)
