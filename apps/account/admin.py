from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'phone', 'is_admin', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)
    filter_horizontal = ()