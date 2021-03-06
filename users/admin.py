from django.contrib import admin, auth

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass
    # list_display = ("id", "email", "get_full_name", "is_superuser", "is_active")


admin.site.unregister(auth.models.Group)
