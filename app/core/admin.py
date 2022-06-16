from django.contrib import admin # noqa
# noqa tells the flake8 to not lookinto that line of code
# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translationStub
# language translation

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin page"""
    ordering = ["id"]
    #ordering comes with the django useradmin
    list_display = ["email","name","follower","memberType"]
    fieldsets = (
        ('ThisIsTheTitle', {'fields': ('email','password')}),
        #(title, )
        (
            translationStub('Permission'),
            {
                'fields' : (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'follower',
                    'memberType',
                )
            }
        ),
        (
            translationStub('Important dates'),
            {
                'fields': ('last_login',)
            }
        ),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        ("Add_One_User",{
            'classes':('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                'follower',
                'memberType',
            ),
        }),
    )

admin.site.register(models.User, UserAdmin)
#if without UserAdmin will basic CRUD operation in models.user