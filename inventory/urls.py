from django.urls import path
from . import views


urlpatterns = [
    path('list_of_quantity/', views.show_list_of_quantity, name='list_of_quantity'),
]