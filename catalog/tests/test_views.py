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
        resp = self.client.get(reverse('nomenclature-list-view'))
        self.assertEqual(resp.status_code, 200)
