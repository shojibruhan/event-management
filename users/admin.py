from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model= CustomUser
    fieldsets= (
        (None, {'fields': ('username', 'password')}),
        ("Personal Info", {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_image', 'mobile')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Importants Dates", {"fields": ('last_login', 'date_joined')})
    )

    add_fieldsets= (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'email', 'mobile', 'bio', 'profile_image')
        })
    )

    list_display= ('username', 'first_name', 'last_name', 'email', 'mobile', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'mobile')
    
    
