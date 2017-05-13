from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'is_staff')
	readonly_fields = ('username', 'last_login', 'date_joined', 'email')
	exclude = ('password',)

admin.site.register(User, UserAdmin)
