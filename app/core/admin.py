from django.contrib import admin # noqa
# noqa tells the flake8 to not lookinto that line of code
# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin page"""
    ordering = ["id"]
    #ordering comes with the django useradmin
    list_display = ["email","name"]

admin.site.register(models.User, UserAdmin)
#if without UserAdmin will basic CRUD operation in models.user