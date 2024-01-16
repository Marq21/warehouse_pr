from django.shortcuts import get_object_or_404, render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views import generic

from inventory.forms import CreateInventoryTaskForm
from .models import InventoryTask, NomenclatureRemain
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
        form.save()
        create_action(self.request.user, 'Задание на пересчёт', inventory_task)
        messages.success(self.request, 'Задание на пересчёт создано успешно')
        return super(CreateInventoryTask, self).form_valid(form)


class InventoryTaskListView(generic.ListView):
    model = InventoryTask
    queryset = InventoryTask.objects.all()
    context_object_name = 'inventory_task_list'
    template_name = 'inventory/list_inventory_task.html'
