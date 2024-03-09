from catalog.models import Country, Nomenclature, get_barcode, get_new_barcode
from warehouse_pr.tests import TestBasedModel


class NomenclatureModelTest(TestBasedModel):

    def test_name_label(self):
        nom = Nomenclature.objects.last()
        field_label = nom._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_positive_cost_of_nom(self):
        nom = Nomenclature.objects.last()
        field_label = nom.cost
        self.assertTrue(field_label > 0)

    def test_weight_or_piece_default_weight_type(self):
        nom = Nomenclature.objects.last()
        field_label = nom.weight_or_piece
        self.assertEqual(field_label, 'PC')

    def test_slugify_method_in_save_model_function(self):
        nom = Nomenclature.objects.last()
        nom.name = 'New name 1'
        nom.save()
        self.assertEqual(nom.slug, 'new-name-1')

    def test_get_barcode(self):
        nom = Nomenclature.objects.last()
        nom.barcode = '00000000002'
        nom.save()
        new_barcode = get_barcode(nom.barcode)
        self.assertEqual(new_barcode, '00000000003')

    def test_get_barcode_lt_eleven_digits(self):
        nom = Nomenclature.objects.last()
        nom.barcode = '2'
        nom.save()
        new_barcode = get_barcode(nom.barcode)
        self.assertEqual(new_barcode, '00000000003')

    def test_get_new_barcode_gt(self):
        last_barcode = Nomenclature.objects.latest('barcode').barcode
        new_barcode = get_new_barcode()
        self.assertTrue(int(new_barcode) > int(last_barcode))

    def test_get_new_barcode_len_equals(self):
        last_barcode = Nomenclature.objects.latest('barcode').barcode
        new_barcode = get_new_barcode()
        self.assertEqual(len(new_barcode), len(last_barcode))

    def test_get_new_barcode_difference_by_one(self):
        last_barcode = Nomenclature.objects.latest('barcode').barcode
        new_barcode = get_new_barcode()
        result_one = int(new_barcode) - int(last_barcode)
        self.assertEqual(result_one, 1)


class CountryModelTest(TestBasedModel):

    def test_str(self):
        name = 'Test_Country'
        country = Country.objects.get(name=name)
        self.assertEqual(str(country), 'Test_Country')
