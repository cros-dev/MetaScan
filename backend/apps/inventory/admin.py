from django.contrib import admin
from .models import CavaleteHistory, SlotHistory


@admin.register(CavaleteHistory)
class CavaleteHistoryAdmin(admin.ModelAdmin):
    list_display = ["cavalete", "action", "user", "timestamp"]
    list_filter = ["action", "timestamp", "user"]
    search_fields = ["cavalete__code", "user__username", "description"]
    readonly_fields = [
        "cavalete",
        "user",
        "action",
        "timestamp",
        "description",
    ]
    ordering = ["-timestamp"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SlotHistory)
class SlotHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "slot",
        "action",
        "user",
        "timestamp",
        "old_quantity",
        "new_quantity",
    ]
    list_filter = ["action", "timestamp", "user"]
    search_fields = [
        "slot__cavalete__code",
        "user__username",
        "description",
        "new_product_code",
    ]
    readonly_fields = [
        "slot",
        "user",
        "action",
        "timestamp",
        "old_product_code",
        "new_product_code",
        "old_quantity",
        "new_quantity",
        "description",
    ]
    ordering = ["-timestamp"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
