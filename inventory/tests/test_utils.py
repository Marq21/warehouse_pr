from datetime import date
from django.test import TestCase

from inventory.models import InventoryItem, InventoryTask, NomenclatureRemain
from catalog.models import Category, Nomenclature
from inventory.utils import get_inventory_item_list, get_nomenclature_remain_list, reorganize_dates, update_remains
from expiration_dates.models import ExpirationDateEntity
from inventory import utils


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


class ReorganizeExpirationDatesTest(TestCase):

    def setUp(self) -> None:

        self.cat = Category.objects.create(
            name="CategoryTest",
        )

        self.inventory_task = InventoryTask.objects.create(
            name='TestTask1',
            category=self.cat,
        )

        self.inventory_item_list = list()
        self.nom_remain_list = list()

        for i in range(10):
            nomenclature = Nomenclature.objects.create(
                name=f'Nomenclature{i}',
                cost=10.1,
            )
            self.inventory_item_list.append(
                InventoryItem.objects.create(
                    name=f'InventoryItem{i}',
                    nomenclature=nomenclature,
                    inventory_task=self.inventory_task,
                    current_quantity=i+1,
                )
            )
            self.nom_remain_list.append(
                NomenclatureRemain.objects.create(
                    nomenclature=nomenclature,
                    quantity=i
                )
            )

        self.nom_remain = NomenclatureRemain.objects.last()

        for i in range(20):
            ExpirationDateEntity.objects.create(nomenclature_remain=self.nom_remain,
                                                quantity=i+1,
                                                date_of_manufacture=date(
                                                    1111, 11, 11),
                                                date_of_expiration=date(1111, 11, 11))

        return super().setUp()

    def test_reorganize_expiration_dates_equals_of_sum_quantities(self):
        update_remains(self.inventory_item_list, self.nom_remain_list)
        exp_date_quantities = sum(
            [exp_date.quantity for exp_date in ExpirationDateEntity.objects.all()])
        nom_remain_quantities = sum(
            [nom_remain.quantity for nom_remain in NomenclatureRemain.objects.all()])
        self.assertEqual(exp_date_quantities, nom_remain_quantities)

    def test_reorganize_expiration_dates_empty_list(self):
        nom_remain = self.nom_remain
        reorganize_dates(nom_remain, list(), 4)
        exp_date_quantities = sum(
            [exp_date.quantity for exp_date in ExpirationDateEntity.objects.all()])
        nom_remain_quantities = sum(
            [nom_remain.quantity for nom_remain in NomenclatureRemain.objects.all()])
        self.assertNotEqual(exp_date_quantities, nom_remain_quantities)

    def test_reorganize_expiration_dates_exp_date__quantity_more_quantity_diff(self):
        ExpirationDateEntity.objects.create(nomenclature_remain=self.nom_remain,
                                            quantity=100,
                                            date_of_manufacture=date(
                                                1000, 10, 10),
                                            date_of_expiration=date(
                                                1100, 10, 10)
                                            )
        update_remains(self.inventory_item_list, self.nom_remain_list)
        exp_date_quantities = sum(
            [exp_date.quantity for exp_date in ExpirationDateEntity.objects.all()])
        nom_remain_quantities = sum(
            [nom_remain.quantity for nom_remain in NomenclatureRemain.objects.all()])
        self.assertEqual(exp_date_quantities, nom_remain_quantities)

    def test_reorganize_expiration_dates_count_of_elements(self):
        count_of_elements = ExpirationDateEntity.objects.all().count()
        update_remains(self.inventory_item_list, self.nom_remain_list)
        self.assertNotEqual(
            ExpirationDateEntity.objects.all().count(), count_of_elements)
