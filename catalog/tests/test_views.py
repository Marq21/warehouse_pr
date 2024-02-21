from django.test import TestCase
from django.contrib.auth.models import User

from catalog.models import Category, Country, Nomenclature
from django.urls import reverse

from catalog.views import NomenclatureHome


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
                                        barcode=n_barcode,)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('nomenclature-list-view'))
        self.assertEqual(resp.status_code, 200)

    def test_home_view(self):
        resp = self.client.get(
            "/", {'nomenclature_list': Nomenclature.objects.all()})
        self.assertEqual(resp.status_code, 200)

    def test_home_view_get_context(self):
        nomenclature_list = Nomenclature.objects.all()
        resp = self.client.get("/")
        view = NomenclatureHome()
        view.setup(resp)

        context = view.get_context_data()
        self.assertQuerySetEqual(nomenclature_list, context["nomenclature_list"])

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


class CategoryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_cats = 13
        for category_num in range(number_of_cats):
            Category.objects.create(name='Category %s' % category_num)

    def test_category_list(self):
        resp = self.client.get(reverse('list-category'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_category_by_status_code(self):
        category = Category.objects.last()
        resp = self.client.post(
            f'/catalog/edit_category/{category.pk}',
            {'name': 'Cat_Test2'})
        self.assertEqual(resp.status_code, 302)

    def test_add_category_by_status_code(self):
        resp = self.client.post(
            '/catalog/add_category/',
            {'name': 'Cat_Test3',
             'cost': 10, })
        self.assertEqual(resp.status_code, 302)

    def test_show_category_list(self):
        resp = self.client.get(
            '/catalog/list-category/', {'category_list': Category.objects.all()})
        self.assertEqual(resp.status_code, 200)


class CountryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        number_of_countries = 13
        for country in range(number_of_countries):
            Country.objects.create(name='Country %s' % country)

    def test_country_list(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/catalog/country_list/')  
        self.assertEqual(resp.status_code, 200)

    def test_add_category_by_status_code(self):
        resp = self.client.post(
            '/catalog/add_country/',
            {'name': 'Country_Test3',})
        self.assertEqual(resp.status_code, 302)

    def test_country_detail_by_status_code(self):
        self.client.login(username='john', password='johnpassword')
        country = Country.objects.last()
        resp = self.client.get(f'/catalog/country_detail/{country.pk}')
        self.assertEqual(resp.status_code, 200)

    def test_edit_country_by_status_code(self):
        country = Country.objects.last()
        resp = self.client.post(
            f'/catalog/edit_country/{country.pk}',
            {'name': 'Country_Test2'})
        self.assertEqual(resp.status_code, 302)

    def test_delete_country_by_status_code(self):
        country = Country.objects.last()
        resp = self.client.post(
            f'/catalog/delete_country/{country.id}',)
        self.assertEqual(resp.status_code, 302)