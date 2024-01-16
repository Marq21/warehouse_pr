from django.contrib import admin
from .models import InventoryItem, InventoryTask, NomenclatureRemain


@admin.register(NomenclatureRemain)
class NomenclatureRemainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity',
                    'slug', )
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name', 'quantity', 'id', 'slug')
    ordering = ['name', 'quantity']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'current_quantity',)
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ( 'id', 'name', 'quantity',)
    ordering = ['name', 'current_quantity']


@admin.register(InventoryTask)
class InventoryTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created',)
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ( 'id', 'name', 'created',)
    ordering = ['name', 'created']