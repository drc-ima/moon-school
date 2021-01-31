from django.contrib import admin

# Register your models here.
# Register your models here.
"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'slug')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'account_id', 'profile', 'school_id')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type',
                                       'groups', 'user_permissions', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
        # (_('Security Details'), {'fields': ('security_questions', 'answers', 'longitude', 'latitude', 'current_address')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('account_id', 'username', 'first_name', 'last_name', 'is_active', 'user_type', 'school_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
