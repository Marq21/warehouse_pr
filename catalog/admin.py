from django.contrib import admin
from .models import Category, Country, GoodsProvider, Nomenclature


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight_or_piece',
                    'cost', 'barcode', 'country_made_id', 'goods_provider', 'slug', 'user',)
    list_display_links = ('id', 'name',)
    list_filter = ('weight_or_piece',)
    search_fields = ('name', 'cost', 'category__name')
    ordering = ['name', 'cost']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'slug',)
    ordering = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ['name']


@admin.register(GoodsProvider)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mail',
                    'providers_phone', 'contact_name', 'contact_name_phone', 'address', 'country',)
    list_display_links = ('id', 'name',)
    list_filter = ('contact_name_phone', 'country')
    search_fields = ('name', 'contact_name', 'country')
    ordering = ['name', 'country']
