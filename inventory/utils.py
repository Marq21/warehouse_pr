from datetime import date
from expiration_dates.models import ExpirationDateEntity
from .models import InventoryItem, InventoryTask, NomenclatureRemain
from django.contrib import messages


def get_nomenclature_remain_list(inventory_item_list: list):

    confirm_task_list = []

    for item in inventory_item_list:
        if NomenclatureRemain.objects.filter(
                nomenclature=item.nomenclature).exists():
            confirm_task_list.append(NomenclatureRemain.objects.get(
                nomenclature=item.nomenclature))

        else:
            confirm_task_list.append(NomenclatureRemain.objects.create(
                nomenclature=item.nomenclature))

    return confirm_task_list


def get_inventory_item_list(inventory_task: InventoryTask):
    inventory_item_list = InventoryItem.objects.filter(
        inventory_task=inventory_task)
    return list(inventory_item_list)


def update_remains(inventory_item_list: list, nomenclature_remain_list: list):
    for i in range(len(inventory_item_list)):
        if nomenclature_remain_list[i].quantity != inventory_item_list[i].current_quantity:
            reorganize_expiration_dates(inventory_item_list)
        nomenclature_remain_list[i].quantity = inventory_item_list[i].current_quantity
        nomenclature_remain_list[i].save()


def reorganize_expiration_dates(inventory_item_list: list) -> None:

    for nom_item in inventory_item_list:
        exp_date_list = list(
            __get_expiration_dates_by_nomenclature_remain(nom_item))

        exp_date_quantity_sum = sum(
            [exp_date.quantity for exp_date in exp_date_list])
        remain_list_quantity = nom_item.current_quantity

        quantities_diff = exp_date_quantity_sum - remain_list_quantity

        __reorgonize_dates((NomenclatureRemain.objects.get(
            nomenclature=nom_item.nomenclature)), exp_date_list, quantities_diff)


def __reorgonize_dates(nom_item: NomenclatureRemain, exp_date_list: list, quantities_diff: int):
    if quantities_diff < 0:
        ExpirationDateEntity.objects.create(nomenclature_remain=nom_item,
                                            quantity=abs(
                                                quantities_diff),
                                            date_of_manufacture=date(
                                                1111, 11, 11),
                                            date_of_expiration=date(1111, 11, 11))
    else:
        while (quantities_diff > 0):
            if not exp_date_list:
                continue
            exp_date_entity = exp_date_list.pop()
            if exp_date_entity.quantity > quantities_diff:
                exp_date_entity.quantity -= quantities_diff
                exp_date_entity.save()
                quantities_diff -= exp_date_entity.quantity
            else:
                quantities_diff -= exp_date_entity.quantity
                exp_date_entity.delete()


def __get_expiration_dates_by_nomenclature_remain(inventory_item: InventoryItem) -> list:
    return list(ExpirationDateEntity.objects.filter
                (nomenclature_remain__nomenclature=inventory_item.nomenclature).order_by('date_of_expiration'))
