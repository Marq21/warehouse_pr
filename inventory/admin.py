from django.contrib import admin
from .models import NomenclatureRemain


@admin.register(NomenclatureRemain)
class NomenclatureRemainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity',
                    'slug', )
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name', 'quantity', 'id', 'slug')
    ordering = ['name', 'quantity']
    prepopulated_fields = {'slug': ('name',)}
