from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import Subscription

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = (
        'id', 'email', 'username',
        'first_name', 'last_name', 'is_staff',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = (
        'email', 'username', 'first_name', 'last_name',
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Личная информация'), {
            'fields': (
                'username', 'first_name',
                'last_name', 'avatar',
            )
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            )
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name',
                'last_name', 'avatar',
                'password1', 'password2',
            ),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user__username', 'author__username')
