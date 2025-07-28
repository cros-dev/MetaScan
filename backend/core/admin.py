from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cavalete, Slot, SlotHistory, CavaleteHistory

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role', 'sankhya_password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

@admin.register(Cavalete)
class CavaleteAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'user', 'status')
    list_filter = ('status',)
    search_fields = ('code', 'name', 'user__email')

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('cavalete', 'side', 'number', 'product_code', 'quantity', 'status')
    list_filter = ('side', 'status', 'cavalete')
    search_fields = ('cavalete__name', 'product_code', 'product_description')

@admin.register(SlotHistory)
class SlotHistoryAdmin(admin.ModelAdmin):
    list_display = ('slot', 'user', 'timestamp', 'product_code', 'quantity', 'action')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('slot__cavalete__name', 'product_code', 'product_description')

@admin.register(CavaleteHistory)
class CavaleteHistoryAdmin(admin.ModelAdmin):
    list_display = ('cavalete', 'user', 'timestamp', 'action')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('cavalete__name',)
