from django.urls import path
from . import views


urlpatterns = [
    path('exp_dates_list/', views.ExpirationDatesEntityView.as_view(),
         name='expiraion_date_list'),
    path('exp_date_details/<int:pk>/',
         views.NomenclatureDetailView.as_view(), name='exp_date_details'),
]
