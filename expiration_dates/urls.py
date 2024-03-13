from django.urls import path
from . import views


urlpatterns = [
    path('exp_dates_list/', views.ExpirationDatesEntityListView.as_view(),
         name='expiration_date_list'),
    path('exp_date_details/<int:pk>/',
         views.ExpirationDatesEntityDetailView.as_view(), name='exp_date_details'),
    path('exp_date_create/',
         views.AddExpirationDatesEntityView.as_view(), name='exp_date_create'),
    path('edit_expiration_date/<int:pk>/',
         views.EditExpirationDatesEntityView.as_view(), name='edit_exp_date'),
    path('delete_expiration_date/<int:pk>',
         views.DeleteExpirationDatesEntityView.as_view(), name='delete_exp_date'),
]
