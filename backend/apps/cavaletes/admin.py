from django.contrib import admin
from .models import Cavalete, Slot


class SlotInline(admin.TabularInline):
    """
    Permite editar slots diretamente na tela do Cavalete.
    """

    model = Slot
    extra = 0
    fields = ["side", "number", "product_code", "quantity", "status"]
    readonly_fields = ["updated_at"]
    ordering = ["side", "number"]


@admin.register(Cavalete)
class CavaleteAdmin(admin.ModelAdmin):
    """
    Admin para gestão de Cavaletes.
    """

    list_display = ["code", "name", "status", "user", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["code", "name", "user__username", "user__first_name"]
    autocomplete_fields = ["user"]
    inlines = [SlotInline]

    fieldsets = (
        (None, {"fields": ("code", "name", "status")}),
        ("Responsável", {"fields": ("user",)}),
    )


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    """
    Admin para visualização de Slots (geralmente acessado via Cavalete).
    """

    list_display = [
        "cavalete",
        "side",
        "number",
        "product_code",
        "quantity",
        "status",
    ]
    list_filter = ["status", "side", "cavalete__status"]
    search_fields = ["cavalete__code", "product_code", "product_description"]
    ordering = ["cavalete", "side", "number"]
