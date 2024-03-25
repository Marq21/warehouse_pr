from datetime import date, datetime, timedelta
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from expiration_dates.models import ExpirationDateEntity
from actions.utils import create_action
from expiration_dates.forms import AddExpirationDatesEntityForm, ExpiredGoodsForm, LimitToExpirationDateForm
from expiration_dates.utils import validate_dates


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
        result_validation = validate_dates(exp_date_enitity)
        form.save()
        create_action(self.request.user,
                      'Добавление срока годности', exp_date_enitity)
        if result_validation:
            result_message = f"""Срок годности не может быть меньше даты производства.
                                Установлены параметры по умолчанию: \n
                                Дата производства: {exp_date_enitity.date_of_manufacture}\n 
                                Срок годности: {exp_date_enitity.date_of_expiration}
                            """
            messages.success(self.request, result_message)
        else:
            messages.success(
                self.request, 'Добавление срока годности: успешно')
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
        result_validation = validate_dates(exp_date)
        form.save()
        if result_validation:
            result_message = f"""Срок годности не может быть меньше даты производства.
                                Установлены параметры по умолчанию: \n
                                Дата производства: {exp_date.date_of_manufacture}\n 
                                Срок годности: {exp_date.date_of_expiration}
                            """
            messages.success(self.request, result_message)
        else:
            messages.success(
                self.request, 'Изменение срока годности: успешно')
        create_action(self.request.user, 'Изменение сроков годности', exp_date)
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
    # List of boolean values that less than five days to expiration
    is_nearest_expiration_value = []

    if request.method == 'POST':
        form = LimitToExpirationDateForm(request.POST)

        if form.is_valid():
            exp_date_nearest_entity_list = ExpirationDateEntity.objects.filter(
                date_of_expiration__gt=datetime.now() + timedelta(days=1),
                date_of_expiration__lte=(
                    datetime.now() + timedelta(
                        days=form.cleaned_data['days_to_expiration']
                    ))).order_by('date_of_expiration')

            for exp_date in exp_date_nearest_entity_list:
                if exp_date.date_of_expiration <= (date.today() + timedelta(days=5)):
                    is_nearest_expiration_value.append((exp_date, True))
                else:
                    is_nearest_expiration_value.append((exp_date, False))

    else:
        form = LimitToExpirationDateForm()

    context = {
        'is_nearest_expiration_value': is_nearest_expiration_value,
        'form': form,
    }

    return render(request, 'expiration_dates/exp-date-nearest-entity-list.html', context)


def get_expired_goods(request):

    expired_goods_list = []

    if request.method == 'POST':
        form = ExpiredGoodsForm(request.POST)
        expired_goods_list = ExpirationDateEntity.objects.filter(
            date_of_expiration__lte=(
                datetime.now()
            )).order_by('date_of_expiration')
    else:
        form = ExpiredGoodsForm()

    context = {
        'expired_goods_list': expired_goods_list,
        'form': form,
    }

    return render(request, 'expiration_dates/expired_goods.html', context)
