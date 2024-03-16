from datetime import datetime, timedelta
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from expiration_dates.models import ExpirationDateEntity
from actions.utils import create_action
from expiration_dates.forms import AddExpirationDatesEntityForm, LimitToExpirationDateForm


class ExpirationDatesEntityListView(generic.ListView):
    model = ExpirationDateEntity
    queryset = ExpirationDateEntity.objects.all()
    context_object_name = 'exp_date_entity_list'
    template_name = 'expiration_dates/exp-date-entity-list.html'


class ExpirationDatesEntityDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExpirationDateEntity
    context_object_name = 'expiration_date_entity'
    template_name = 'expiration_dates/exp_date_entity_detail.html'


class AddExpirationDatesEntityView(LoginRequiredMixin, generic.CreateView):
    form_class = AddExpirationDatesEntityForm
    template_name = 'expiration_dates/add_expiration_dates_entity.html'
    success_url = reverse_lazy('expiration_date_list')
    extra_context = {
        'title': 'Добавление срока годности для партии',
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        exp_date_enitity = form.save(commit=False)
        form.save()
        create_action(self.request.user,
                      'Добавление срока годности', exp_date_enitity)
        messages.success(self.request, 'Добавление срока годности: успешно')
        return super(AddExpirationDatesEntityView, self).form_valid(form)


class EditExpirationDatesEntityView(LoginRequiredMixin,  generic.UpdateView):
    model = ExpirationDateEntity
    form_class = AddExpirationDatesEntityForm
    template_name = 'expiration_dates/add_expiration_dates_entity.html'
    extra_context = {
        'title': 'Изменение сроков годности'
    }

    def get_success_url(self, **kwargs):
        return reverse_lazy('exp_date_details', args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.user = self.request.user
        exp_date = form.save(commit=False)
        form.save()
        create_action(self.request.user, 'Изменение сроков годности', exp_date)
        messages.success(self.request, 'Изменение сроков годности: успешно')
        return super(EditExpirationDatesEntityView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Page update failed')
        return super(EditExpirationDatesEntityView, self).form_invalid(form)


class DeleteExpirationDatesEntityView(LoginRequiredMixin, generic.DeleteView):
    model = ExpirationDateEntity
    success_url = reverse_lazy('expiration_date_list')
    template_name = "expiration_dates/delete_expiration_date.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Удалить срок годности"
        return context


def get_nearest_expiration_dates(request):

    exp_date_nearest_entity_list = []
    context = {}

    if request.method == 'POST':
        form = LimitToExpirationDateForm(request.POST)

        if form.is_valid():
            exp_date_nearest_entity_list = ExpirationDateEntity.objects.filter(
                date_of_expiration__gt=datetime.now() + timedelta(days=2),
                date_of_expiration__lte=(
                    datetime.now() + timedelta(
                        days=form.cleaned_data['days_to_expiration']
                    )))
    else:
        form = LimitToExpirationDateForm()

    context = {
        'exp_date_nearest_entity_list': exp_date_nearest_entity_list,
        'form': form,
    }

    return render(request, 'expiration_dates/exp-date-nearest-entity-list.html', context)
