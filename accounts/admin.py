from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Customise the CustomUser content displayed on the admin site."""

    list_display = ('username', 'email', 'is_staff')
    readonly_fields = ('username', 'last_login', 'date_joined', 'email', 'first_name', 'last_name')
    exclude = ('password',)

admin.site.register(User, UserAdmin)
