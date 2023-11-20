from decimal import Decimal
from django.test import TestCase

from catalog.models import Nomenclature


class NomenclatureModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Nomenclature.objects.create(name='Test_Nom', cost='10.0')

    def test_name_label(self):
        nom = Nomenclature.objects.get(pk=1)
        field_label = nom._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_positive_cost_of_nom(self):
        nom = Nomenclature.objects.get(pk=1)
        field_label = nom.cost
        print(field_label)
        self.assertTrue(field_label > 0)

    def test_weight_or_piece_defaukt_weight_type(self):
        nom = Nomenclature.objects.get(pk=1)
        field_label = nom.weight_or_piece
        print(field_label)
        self.assertEquals(field_label, 'PC')
