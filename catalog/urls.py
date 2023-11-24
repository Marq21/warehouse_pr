from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', views.NomenclatureHome.as_view(), name='home'),
    path('nomenclature/<slug:slug>/',
         views.NomenclatureDetailView.as_view(), name='noms-detail'),
    path('category/<int:pk>/',
         views.CategoryDetailView.as_view(), name='category-detail'),
    path('nomenclature_list/', views.NomenclatureListView.as_view(),
         name='nomenclature-list-view'),
    path('category/<slug:cat_slug>', views.show_category, name='category'),
    path('add_nomenclature/', views.AddNomenclature.as_view(),
         name='add-nomenclature'),
    path('add_category/', views.AddCategory.as_view(), name='add-category'),
    path('edit_nomenclature/<int:pk>',
         views.EditNomenclature.as_view(), name='edit-nomenclature'),
    path('edit_category/<int:pk>',
         views.EditCategory.as_view(), name='edit-category'),     
    path('<int:nom_id>/share/',
         views.nom_share, name='nom_share'),
    path('list-category/', views.CategoryListView.as_view(), name='list-category'),
    path('search/', views.nom_search, name='nom-search'),
]
