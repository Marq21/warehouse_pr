from django.test import TestCase

from inventory.models import InventoryItem, InventoryTask, NomenclatureRemain
from catalog.models import Category, Nomenclature
from inventory.utils import get_inventory_item_list, get_nomenclature_remain_list, update_remains


class GetNomenclatureRemainList(TestCase):

    def setUp(self) -> None:

        self.cat = Category.objects.create(
            name="CategoryTest",
        )

        self.inventory_task = InventoryTask.objects.create(
            name='TestTask1',
            category=self.cat,
        )

        self.inventory_item_list = list()

        for i in range(10):
            self.inventory_item_list.append(
                InventoryItem.objects.create(
                    name=f'InventoryItem{i}',
                    nomenclature=Nomenclature.objects.create(
                        name=f'Nomenclature{i}',
                        cost=10.1,
                    ),
                    inventory_task=self.inventory_task,
                )
            )

        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=Nomenclature.objects.last(),
        )
        return super().setUp()

    def test_get_nomenclature_remain_list_equals_lists_len(self):
        self.assertEqual(len(get_nomenclature_remain_list(
            self.inventory_item_list)), 10)

    def test_get_nomenclature_remain_list_equals_lists(self):
        self.assertIsInstance(get_nomenclature_remain_list(
            self.inventory_item_list), list)

    def test_get_inventory_item_list(self):
        self.assertListEqual(self.inventory_item_list,
                             get_inventory_item_list(self.inventory_task.pk))

    def test_update_remains(self):
        inventory_remain_list = get_nomenclature_remain_list(
            self.inventory_item_list)
        sum_of_quantities = sum(i.quantity for i in inventory_remain_list)
        update_remains(self.inventory_item_list, inventory_remain_list)
        self.assertNotEquals(sum_of_quantities, inventory_remain_list)
