from django.urls import include, path
from rest_framework.routers import SimpleRouter
from store_api import views

router = SimpleRouter()

router.register(r'nomenclature', views.NomenclatureViewSet)

urlpatterns = [
     path('', include('social_django.urls', namespace='social')),
     path('auth/', views.auth, name='auth')
]

urlpatterns += router.urls