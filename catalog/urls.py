from django.urls import path
from . import views


urlpatterns = [
    path('', views.NomenclatureHome.as_view(), name='home'),

    path('nomenclature/<slug:slug>/',
         views.NomenclatureDetailView.as_view(), name='noms-detail'),
    path('nomenclature_list/', views.NomenclatureListView.as_view(),
         name='nomenclature-list-view'),
    path('add_nomenclature/', views.AddNomenclature.as_view(),
         name='add-nomenclature'),
    path('edit_nomenclature/<int:pk>',
         views.EditNomenclature.as_view(), name='edit-nomenclature'),
    path('delete_nomenclature/<slug:slug>', views.DeleteNomenclatureView.as_view(),
         name='delete_nomenclature'),

    path('category_details/<slug:slug>/',
         views.CategoryDetailView.as_view(), name='category-details'),
    path('add_category/', views.AddCategory.as_view(), name='add-category'),
    path('edit_category/<int:pk>',
         views.EditCategory.as_view(), name='edit-category'),
    path('list-category/', views.CategoryListView.as_view(), name='list-category'),
    path('delete_category/<int:pk>', views.DeleteCategoryView.as_view(),
         name='delete_category'),

    path('country_list/', views.CountryListView.as_view(), name='country-list'),
    path('country_detail/<int:pk>',
         views.CountryDetailView.as_view(), name='country-detail'),
    path('add_country/', views.AddCountry.as_view(),
         name='add-country'),
    path('edit_country/<int:pk>',
         views.EditCountry.as_view(), name='edit-country'),
    path('delete_country/<int:pk>',
         views.DeleteCountry.as_view(), name='delete-country'),

    path('providers_list/', views.ProvidersListView.as_view(), name='providers_list'),
    path('provider_detail/<int:pk>',
         views.ProviderDetailView.as_view(), name='provider_detail'),
    path('add_provider/', views.AddProvider.as_view(),
         name='add_provider'),
    path('edit_provider/<int:pk>',
         views.EditProvider.as_view(), name='edit_provider'),
    path('delete_provider/<int:pk>',
         views.DeleteProvider.as_view(), name='delete_provider'),

    path('search/', views.nom_search, name='nom-search'),
    path('<int:nom_id>/share/',
         views.nom_share, name='nom_share'),
]
