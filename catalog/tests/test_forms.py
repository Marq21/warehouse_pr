from catalog.forms import AddNomenclatureForm
from warehouse_pr.tests import TestBasedModel


class TestFormValidAddNomenclatureForm(TestBasedModel):

    def setUp(self):
        self.form_data = {
            'user': self.user,
            'name': 'Лаваш 180 гр.',
            'weight_or_piece': 'PC',
            'barcode': '00000000000',
            'cost': '10.00',
            'category': '30',
            'country_made_id': '30',
        }

    def test_new_patient_form_is_valid(self):
        form = AddNomenclatureForm(data=self.form_data)
        print(form)
        self.assertTrue(form.is_valid())