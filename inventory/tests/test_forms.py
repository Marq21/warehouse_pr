from django import forms
from inventory.forms import InputBarcodeForm
from catalog.models import Nomenclature
from warehouse_pr.tests import TestBasedModel


class TestFormValidInputBarcodeForm(TestBasedModel):

    def setUp(self):
        self.nom = Nomenclature.objects.last()
        self.form_data = {
            'barcode_input': self.nom.barcode,
        }

    def test_form_cleaned_data(self):
        nom_barcode = self.nom.barcode
        form = InputBarcodeForm(data=self.form_data)
        form.is_valid
        self.assertEqual(form.clean_barcode_input(), nom_barcode)

    def test_form_cleaned_data_validation_error(self):
        failed_barcode = {
            'barcode_input': '0',
        }
        form = InputBarcodeForm(data=failed_barcode)
        with self.assertRaises(forms.ValidationError):
            print(form.errors)
            print(form.non_field_errors())
            print(form.has_error('barcode_input', "Штрих-код отсутствует в базе данных"))
            form.is_valid()
            form.clean_barcode_input()
