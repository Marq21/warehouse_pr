from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views import generic

from .forms import CreateInventoryTaskForm, InputBarcode, UpdateStatus
from catalog.models import Nomenclature
from .models import InventoryItem, InventoryTask, NomenclatureRemain
from actions.utils import create_action


def show_list_of_quantity(request):

    quantity = NomenclatureRemain.objects.all()
    data = {
        'quantity_list': quantity
    }
    return render(request, 'inventory/list_of_remaining_quantities.html', data)


class CreateInventoryTask(LoginRequiredMixin, FormView):

    form_class = CreateInventoryTaskForm
    template_name = 'inventory/create_inventory_task.html'
    success_url = reverse_lazy('list-inventory-task')
    extra_context = {
        'title': 'Задание на пересчёт'
    }

    def form_valid(self, form):

        form.instance.user = self.request.user
        inventory_task = form.save(commit=False)
        category = inventory_task.category
        nomenclature_list = Nomenclature.objects.filter(category=category)
        inventory_item_list = []
        inventory_task.save()

        for nom in nomenclature_list:
            inventory_item_list.append(InventoryItem(
                name=f'{nom.name}--{inventory_task.id}', nomenclature=nom, inventory_task=inventory_task))
            
        InventoryItem.objects.bulk_create(inventory_item_list)
        form.save()
        create_action(self.request.user, 'Задание на пересчёт', inventory_task)
        messages.success(self.request, 'Задание на пересчёт создано успешно')

        return super(CreateInventoryTask, self).form_valid(form)


class InventoryTaskListView(generic.ListView):

    model = InventoryTask
    queryset = InventoryTask.objects.all()
    context_object_name = 'inventory_task_list'
    template_name = 'inventory/list_inventory_task.html'


def inventory_task_detail(request, id: int):

    inventory_task = InventoryTask.objects.get(pk=id)
    inventory_item_list = InventoryItem.objects.filter(
        inventory_task=inventory_task)

    if inventory_task.status == 'F' and request.method == 'POST':
        update_form = UpdateStatus(request.POST)
        form = update_form

        if update_form.is_valid():
            updating_task = InventoryTask.objects.get(id=inventory_task.id)
            updating_task.status = 'IP'
            updating_task.save()

    elif inventory_task.status == 'IP' and request.method == 'POST':
        input_barcode_form = InputBarcode(request.POST)
        form = input_barcode_form

        if form.is_valid():
            barcode = request.POST.get('barcode_input')
            print(barcode)           


    elif inventory_task.status == 'F':
        update_form = UpdateStatus()
        form = update_form

    elif inventory_task.status == 'IP':
        input_barcode_form = InputBarcode()
        form = input_barcode_form

    data = {
        'title': f'Задание на пересчёт: {inventory_task} №{inventory_task.id} ',
        'inventory_item_list': inventory_item_list,
        'task': inventory_task,
        'form': form,
    }

    return render(request, 'inventory/inventory_task_detail.html', data)
