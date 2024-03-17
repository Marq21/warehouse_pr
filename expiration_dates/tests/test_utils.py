from datetime import date, datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User

from catalog.models import Nomenclature
from inventory.models import NomenclatureRemain
from expiration_dates.models import ExpirationDateEntity
from expiration_dates.utils import validate_dates


class ValidateDateTest(TestCase):

    def setUp(self) -> None:
        User.objects.create(username='john', password='johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity1 = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now(),
            date_of_expiration=datetime.now() - timedelta(days=20),
        )
        self.exp_date_entity2 = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now(),
            date_of_expiration=datetime.now() + timedelta(days=20),
        )
        return super().setUp()

    def test_date_of_expiration_lte(self):
        self.assertTrue(validate_dates(self.exp_date_entity1))

    def test_date_of_expiration_gt(self):
        self.assertFalse(validate_dates(self.exp_date_entity2))
