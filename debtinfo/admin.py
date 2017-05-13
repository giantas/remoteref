from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    """Customise the Profile content displayed on the admin site."""

    list_display = ('debtor', 'creditor')

admin.site.register(Profile, ProfileAdmin)
