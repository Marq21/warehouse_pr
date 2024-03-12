from django.urls import path
from . import views


urlpatterns = [
    path('exp_dates_list/', views.ExpirationDatesEntityListView.as_view(),
         name='expiraion_date_list'),
    path('exp_date_details/<int:pk>/',
         views.ExpirationDatesEntityDetailView.as_view(), name='exp_date_details'),
    path('exp_date_create/',
         views.AddExpirationDatesEntityView.as_view(), name='exp_date_create'),
]
