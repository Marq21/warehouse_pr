from django.contrib import admin
from .models import Category, Nomenclature


@admin.register(Nomenclature)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight_or_piece',
                    'cost', 'barcode', 'slug', 'user',)
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
