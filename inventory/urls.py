from django.urls import path
from . import views


urlpatterns = [
    path('inventory_item/<int:pk>', views.InventoryItemUpdateView.as_view(),
         name='inventory-item-update'),
    path('inventory_task_detail/<int:pk>', views.inventory_task_detail,
         name='inventory-task-detail'),
    path('inventory_task_detail/<int:pk>/delete/', views.DeleteInventoryTaskView.as_view(),
         name='inventory-task-delete'),
    path('list_of_quantity/', views.show_list_of_quantity, name='list_of_quantity'),
    path('create_inventory_task/', views.CreateInventoryTask.as_view(),
         name='create-inventory-task'),
    path('list_inventory_task/', views.InventoryTaskListView.as_view(),
         name='list-inventory-task'),
    path('accept_task/confirm/<int:pk>', views.inventory_task_confirm,
         name='accept_task_confirm'),
    path('accept_task/done/<int:pk>',
         views.inventory_task_done, name='inventory_task_done')
]
