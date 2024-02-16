from django.test import TestCase
from django.test import Client

from catalog.models import Category, Nomenclature
from django.urls import reverse


class NomenclatureViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_noms = 13
        for nomenclature_num in range(number_of_noms):
            parse_int = int('00000000000') + nomenclature_num
            place_for_number = len(str(parse_int))
            result = ['0' for _ in range(11)]
            result[-place_for_number:] = str(parse_int)
            n_barcode = ''.join(result)
            Nomenclature.objects.create(name='Nomenclature %s' % nomenclature_num,
                                        cost=10 + nomenclature_num,
                                        barcode=n_barcode)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('nomenclature-list-view'))
        self.assertEqual(resp.status_code, 200)

    def test_home_view(self):
        resp = self.client.get(
            "/", {'nomenclature_list': Nomenclature.objects.all()})
        self.assertEqual(resp.status_code, 200)

    def test_add_nomenclature_by_status_code(self):
        resp = self.client.post(
            '/catalog/add_nomenclature/',
            {'name': 'Nom_Test2',
             'cost': 10, })
        self.assertEqual(resp.status_code, 302)

    def test_edit_nomenclature_by_status_code(self):
        nomenclature = Nomenclature.objects.last()
        resp = self.client.post(
            f'/catalog/edit_nomenclature/{nomenclature.pk}',
            {'name': 'Nom_Test2',
             'cost': 10, })
        self.assertEqual(resp.status_code, 302)


class CategoryListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_cats = 13
        for category_num in range(number_of_cats):
            Category.objects.create(name='Category %s' % category_num)

    def test_category_list(self):
        resp = self.client.get(reverse('list-category'))
        self.assertEqual(resp.status_code, 200)
