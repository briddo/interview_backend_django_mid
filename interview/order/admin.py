from django.contrib import admin

from interview.order.models import Order, OrderTag


@admin.register(OrderTag)
class OrderTagAdmin(admin.ModelAdmin):
    """Admin configuration for OrderTag model."""
    
    list_display = ["name", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name"]
    list_editable = ["is_active"]
    ordering = ["name"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    
    list_display = ["inventory", "start_date", "embargo_date", "is_active", "created_at"]
    list_filter = ["is_active", "start_date", "embargo_date", "created_at", "tags"]
    search_fields = ["inventory__name"]
    filter_horizontal = ["tags"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "start_date"
    
    fieldsets = (
        ("Order Information", {
            "fields": ("inventory", "start_date", "embargo_date")
        }),
        ("Tags", {
            "fields": ("tags",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
