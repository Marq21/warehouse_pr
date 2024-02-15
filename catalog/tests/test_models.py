from decimal import Decimal
from django.test import TestCase

from catalog.models import Nomenclature, get_barcode, get_new_barcode


class NomenclatureModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Nomenclature.objects.create(
            name='Test_Nom', cost='10.0', barcode='00000000001')

    def test_name_label(self):
        nom = Nomenclature.objects.get(pk=1)
        field_label = nom._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_positive_cost_of_nom(self):
        nom = Nomenclature.objects.get(pk=1)
        field_label = nom.cost
        self.assertTrue(field_label > 0)

    def test_weight_or_piece_default_weight_type(self):
        nom = Nomenclature.objects.get(pk=1)
        field_label = nom.weight_or_piece
        self.assertEqual(field_label, 'PC')

    def test_slugify_method_in_save_model_function(self):
        nom = Nomenclature.objects.get(pk=1)
        nom.name = 'New name 1'
        nom.save()
        self.assertEqual(nom.slug, 'new-name-1')

    def test_get_barcode(self):
        nom = Nomenclature.objects.get(pk=1)
        print(nom)
        nom.barcode = '00000000002'
        nom.save()
        new_barcode = get_barcode(nom.barcode)
        self.assertEqual(new_barcode, '00000000003')

    def test_get_new_barcode(self):
        new_barcode = get_new_barcode()
        self.assertEqual(new_barcode, '00000000002')
