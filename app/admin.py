from django.contrib import admin
from .models import CustomUser, Password
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'username','email','hash_key')
        }),
    )



admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Password)