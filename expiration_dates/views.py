from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from expiration_dates.models import ExpirationDateEntity
from actions.utils import create_action
from expiration_dates.forms import AddExpirationDatesEntityForm


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
    template_name = 'expiration_dates/add_expiration_dates_enitity.html'
    success_url = reverse_lazy('expiraion_date_list')
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
