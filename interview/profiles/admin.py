from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from interview.profiles.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(BaseUserAdmin):
    """Admin configuration for UserProfile model."""
    
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active", "date_joined"]
    list_filter = ["is_staff", "is_superuser", "is_admin", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_admin", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

