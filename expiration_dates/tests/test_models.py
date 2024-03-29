from datetime import datetime
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from expiration_dates.models import ExpirationDateEntity
from inventory.models import NomenclatureRemain
from catalog.models import Nomenclature


class ExpirationDateEntityModelTest(TestCase):

    def setUp(self) -> None:
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now().strftime("%Y-%m-%d"),
            date_of_expiration=datetime.now().strftime("%Y-%m-%d"),
        )
        return super().setUp()

    def test_str(self):
        name = f'{self.nom_remain} ({self.exp_date_entity.date_of_expiration})'
        date_entity = ExpirationDateEntity.objects.get(name=name)
        self.assertEqual(str(date_entity), name)

    def test_save_method(self):
        true_name = f'{self.nom_remain} ({self.exp_date_entity.date_of_expiration})'
        # Trying to give random name
        self.exp_date_entity.name = 'jafsjasfj'
        # save method overwrite name
        self.exp_date_entity.save()
        self.assertEqual(str(self.exp_date_entity), true_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.exp_date_entity.get_absolute_url(), reverse(
            'exp_date_details', kwargs={'pk': self.exp_date_entity.pk}))

    def test_get_absolute_url_without_pk(self):
        with self.assertRaises(NoReverseMatch):
            reverse(
                'exp_date_details')
