from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# pyrefly: ignore [missing-import]
from .models import User
class CustomUserAdmin(UserAdmin):
    model = User

    # Used when creating a new user via the admin "Add user" button
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    # Used when editing an existing user
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar_color")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("email", "username", "is_staff", "is_active")
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)


