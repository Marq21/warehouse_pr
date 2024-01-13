from django.shortcuts import render
from .models import NomenclatureRemain


def show_list_of_quantity(request):
    quantity = NomenclatureRemain.objects.all()
    data = {
        'quantity_list': quantity
    }
    return render(request, 'inventory/list_of_remaining_quantities.html', data)
