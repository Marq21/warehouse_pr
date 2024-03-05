from datetime import datetime

from django.urls import NoReverseMatch, reverse
from inventory.models import InventoryItem, InventoryTask, NomenclatureRemain
from catalog.models import Category, Nomenclature
from warehouse_pr.tests import TestBasedModel


class NomenclatureRemainModelTest(TestBasedModel):

    def setUp(self) -> None:
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=Nomenclature.objects.last(),
            quantity=10.0,
        )
        return super().setUp()

    def test_str(self):
        str_object_name = f'{self.nom_remain.nomenclature.name} {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
        self.assertEqual(str(self.nom_remain), str_object_name)


class InventoryTaskModelTest(TestBasedModel):

    def setUp(self) -> None:
        cat = Category.objects.last()
        self.inv_task = InventoryTask.objects.create(
            name='TestTask1',
            category=cat,
        )
        return super().setUp()

    def test_get_absoulte_url(self):
        self.assertEqual(self.inv_task.get_absolute_url(), reverse(
            'inventory-task-detail', kwargs={'pk': self.inv_task.pk}))

    def test_get_absoulte_url_failed(self):
        with self.assertRaises(NoReverseMatch):
            reverse(
                'inventory-task-detail', kwargs={'failed_args': 'FailedArgsFOrTest'})

    def test_str(self):
        self.assertEqual(str(self.inv_task), self.inv_task.name)

    def test_str_failed(self):
        self.assertNotEqual(str(self.inv_task), 'failed_str')


class InventoryItemTest(TestBasedModel):
    def setUp(self) -> None:
        cat = Category.objects.last()
        self.nom = Nomenclature.objects.last()
        self.inventory_task = InventoryTask.objects.create(
            name='TestTask1',
            category=cat,
        )
        self.inv_item = InventoryItem.objects.create(
            name='TestItem1',
            nomenclature=self.nom,
            inventory_task=self.inventory_task,
        )
        return super().setUp()

    def test_str(self):
        self.assertEqual(str(self.inv_item), self.inv_item.name)

    def test_str_failed(self):
        self.assertNotEqual(str(self.inv_item), 'TestItem1')

    def test_save(self):
        tested_item = InventoryItem(
            nomenclature=self.nom,
            inventory_task=self.inventory_task,
        )
        tested_item.save()
        self.assertTrue(InventoryItem.objects.contains(tested_item))

    def test_save_failed(self):
        with self.assertRaises(AttributeError):
            tested_item = InventoryItem(
                nomenclature=self.nom,
            )
            tested_item.save()

    def test_get_absoulte_url(self):
        self.assertEqual(self.inv_item.get_absolute_url(), reverse(
            'inventory-item-update', kwargs={"pk": self.inv_item.pk}))

    def test_get_absoulte_url_failed(self):
        with self.assertRaises(NoReverseMatch):
            reverse(
                'inventory-item-update', kwargs={'failed_args': 'FailedArgsFOrTest'})
