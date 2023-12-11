from registration_app import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('auth/', views.auth, name='auth'),
    path('', include('social_django.urls', namespace='social')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)