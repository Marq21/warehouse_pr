from registration_app import views
from django.urls import path


urlpatterns = [
    path('', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
