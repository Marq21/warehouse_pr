from django.urls import include, path
from rest_framework.routers import SimpleRouter
from store_api import views

router = SimpleRouter()

router.register(r'nomenclature', views.NomenclatureViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = []

urlpatterns += router.urls