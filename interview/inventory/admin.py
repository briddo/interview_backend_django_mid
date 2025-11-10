from django.contrib import admin

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)


@admin.register(InventoryTag)
class InventoryTagAdmin(admin.ModelAdmin):
    """Admin configuration for InventoryTag model."""
    
    list_display = ["name", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name"]
    list_editable = ["is_active"]
    ordering = ["name"]


@admin.register(InventoryLanguage)
class InventoryLanguageAdmin(admin.ModelAdmin):
    """Admin configuration for InventoryLanguage model."""
    
    list_display = ["name", "created_at", "updated_at"]
    list_filter = ["created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(InventoryType)
class InventoryTypeAdmin(admin.ModelAdmin):
    """Admin configuration for InventoryType model."""
    
    list_display = ["name", "created_at", "updated_at"]
    list_filter = ["created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Admin configuration for Inventory model."""
    
    list_display = ["name", "type", "language", "created_at", "updated_at"]
    list_filter = ["type", "language", "created_at", "tags"]
    search_fields = ["name"]
    filter_horizontal = ["tags"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "type", "language")
        }),
        ("Tags", {
            "fields": ("tags",)
        }),
        ("Metadata", {
            "fields": ("metadata",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
