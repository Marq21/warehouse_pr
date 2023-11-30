from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_actions, name='show-actions'),
]