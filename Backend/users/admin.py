from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# pyrefly: ignore [missing-import]
from .models import User

admin.site.register(User, UserAdmin)




