from django.contrib import admin
from .models import Cavalete, Slot

@admin.register(Cavalete)
class CavaleteAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'status', 'user']
    list_filter = ['status', 'user']
    search_fields = ['code', 'name']
    readonly_fields = ['code', 'name']
    ordering = ['code']

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['cavalete', 'side', 'number', 'product_code', 'quantity', 'status']
    list_filter = ['cavalete', 'side', 'status']
    search_fields = ['product_code', 'product_description']
    ordering = ['cavalete', 'side', 'number']
