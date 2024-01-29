from django.urls import path
from . import views


urlpatterns = [
    path('inventory_item/<int:pk>', views.InventoryItemUpdateView.as_view(),
         name='inventory-item-update'),
    path('inventory_task_detail/<int:pk>', views.inventory_task_detail,
         name='inventory-task-detail'),
    path('list_of_quantity/', views.show_list_of_quantity, name='list_of_quantity'),
    path('create_inventory_task/', views.CreateInventoryTask.as_view(),
         name='create-inventory-task'),
    path('list_inventory_task/', views.InventoryTaskListView.as_view(),
         name='list-inventory-task'),
]
