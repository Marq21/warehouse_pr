from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', views.NomenclatureHome.as_view(), name='home'),
    path('nomenclature/<slug:slug>/',
         views.NomenclatureDetailView.as_view(), name='noms-detail'),
    path('nomenclature_list/', views.NomenclatureListView.as_view(),
         name='nomenclature-list-view'),
    path('category/<slug:cat_slug>', views.show_category, name='category'),
    path('add_nomenclature/', views.AddNomenclature.as_view(), name='add-nomenclature'),
    path('edit_nomenclature/<int:pk>',
         views.EditPage.as_view(), name='edit-nomenclature'),
    path('add_category/', views.AddCategory.as_view(), name='add-category'),
    path('<int:nom_id>/share/',
         views.nom_share, name='nom_share'),
    path('list-category/', views.CategoryListView.as_view(), name='list-category'),
    path('search/', views.nom_search, name='nom-search'),
]
