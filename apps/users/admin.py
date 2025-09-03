from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdminInterface(UserAdmin):
    
    """
        modification in admin interface for our custom user
    """
    
    ordering = ('-created_at',)
    search_fields = ('email',)
    list_display = ('email','username','is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password'),
        }),
    )

admin.site.register(User,CustomUserAdminInterface)