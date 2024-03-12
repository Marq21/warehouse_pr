from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from expiration_dates.models import ExpirationDateEntity


class ExpirationDatesEntityView(generic.ListView):
    model = ExpirationDateEntity
    queryset = ExpirationDateEntity.objects.all()
    context_object_name = 'exp_date_entity_list'
    template_name = 'expiration_dates/exp-date-entity-list.html'


class NomenclatureDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExpirationDateEntity
    context_object_name = 'expiration_date_entity'
    template_name = 'expiration_dates/exp_date_entity_detail.html'
