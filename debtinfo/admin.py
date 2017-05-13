from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('debtor', 'creditor')

class DebtorAdmin(admin.ModelAdmin):
	list_display = ('debtor', 'id_number')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Debtor, DebtorAdmin)
