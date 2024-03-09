from django.contrib import admin

from expiration_dates.models import ExpirationDateEntity


@admin.register(ExpirationDateEntity)
class ExpirationDateEntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nomenclature_remain', 'quantity',
                    'date_of_manufacture', 'date_of_expiration',)
    list_display_links = ('id', 'name',)
    list_filter = ('name', 'nomenclature_remain',)
    search_fields = ('name', 'nomenclature_remain',
                     'date_of_manufacture', 'date_of_expiration',)
    ordering = ['name', 'date_of_manufacture', 'quantity']
