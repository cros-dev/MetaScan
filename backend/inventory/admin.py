from django.contrib import admin
from .models import SlotHistory, CavaleteHistory

@admin.register(SlotHistory)
class SlotHistoryAdmin(admin.ModelAdmin):
    list_display = ['slot', 'user', 'timestamp', 'product_code', 'quantity', 'action']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['slot__cavalete__name', 'product_code', 'product_description']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

@admin.register(CavaleteHistory)
class CavaleteHistoryAdmin(admin.ModelAdmin):
    list_display = ['cavalete', 'user', 'timestamp', 'action']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['cavalete__name']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
