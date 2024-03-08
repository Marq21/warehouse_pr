from .models import InventoryItem, InventoryTask, NomenclatureRemain


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
        nomenclature_remain_list[i].quantity = inventory_item_list[i].current_quantity
        nomenclature_remain_list[i].save()
