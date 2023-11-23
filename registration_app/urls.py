from registration_app import views
from django.urls import include, path


urlpatterns = [
    path('', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('auth/', views.auth, name='auth'),
    path('', include('social_django.urls', namespace='social')),
]
