from django.test import TestCase

from catalog.models import Nomenclature
from django.urls import reverse


class NomenclatureListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_noms = 13
        for nomenclature_num in range(number_of_noms):
            Nomenclature.objects.create(name='Nomenclature %s' % nomenclature_num,
                                        cost=10 + nomenclature_num,)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('catalog/nomenclature_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('nomenclature'))
        self.assertEqual(resp.status_code, 200)
