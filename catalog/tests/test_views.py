from django.test import RequestFactory
from catalog.forms import AddCategoryForm, AddNomenclatureForm
from catalog.models import Category, Country, Nomenclature
from catalog.views import AddNomenclature, EditNomenclature, NomenclatureHome
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages

from warehouse_pr.tests import TestBasedModel


class NomenclatureViewTest(TestBasedModel):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.cat = Category.objects.last()
        self.country = Country.objects.last()
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        return super().setUp()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('nomenclature-list-view'))
        self.assertEqual(resp.status_code, 200)

    def test_view_nom_list_template_used(self):
        resp = self.client.get(reverse('nomenclature-list-view'))
        self.assertTemplateUsed(resp, 'catalog/nomenclature-list.html')

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
        self.assertQuerySetEqual(
            nomenclature_list, context["nomenclature_list"])

    def test_call_view_fail_blank(self):
        response = self.client.post(
            reverse('add-nomenclature'), {})
        self.assertFormError(response, 'form', 'name',
                             'Это поле обязательно для заполнения.')

    def test_create_view_POST_success_form_valid(self):

        data = {
            'name': 'nome_CreateView_test',
            'weight_or_piece': Nomenclature.NomsType.PIECE,
            'barcode': '00000100000',
            'cost': 10.0,
            'category': self.cat,
            'country_made_id': self.country,
        }

        form = AddNomenclatureForm(data)
        request = self.factory.post('/catalog/add_nomenclature/', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        view = AddNomenclature()
        view.setup(request)
        self.assertTrue(view.form_valid(form=form))
        self.assertTrue(Nomenclature.objects.get(name='nome_CreateView_test'))

    def test_update_view_POST_success_form_valid(self):
        nom = Nomenclature.objects.last()
        name_for_compare_in_assert = nom.name
        data = {
            'name': "New_Nom_Name",
            'weight_or_piece': nom.weight_or_piece,
            'barcode': nom.barcode,
            'cost': 13,
            'category': self.cat,
            'country_made_id': self.country,
            'user': self.user,
        }

        form = AddNomenclatureForm(data)
        request = self.factory.post(
            f'/catalog/edit_nomenclature/{nom.id}', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        view = EditNomenclature()
        view.setup(request)
        self.assertTrue(view.form_valid(form=form))
        self.assertFalse(Nomenclature.objects.get(
            name='New_Nom_Name') == name_for_compare_in_assert)


class CategoryViewTest(TestBasedModel):

    def setUp(self) -> None:
        self.client.login(username='john', password='johnpassword')
        return super().setUp()

    def test_category_list(self):
        resp = self.client.get(reverse('list-category'))
        self.assertEqual(resp.status_code, 200)

    def test_add_category_by_status_code(self):
        form_data = {
            'name': 'Cat_Test3',
        }
        form = AddCategoryForm(form_data)

        resp = self.client.post(
            '/catalog/add_category/',
            {'form': form, })
        self.assertEqual(resp.status_code, 200)

    def test_show_category_list(self):
        resp = self.client.get(
            '/catalog/list-category/', {'category_list': Category.objects.all()})
        self.assertEqual(resp.status_code, 200)

    def test_category_detail(self):
        self.client.login(username='john', password='johnpassword')
        cat_slug = Category.objects.last().slug
        resp = self.client.get(
            f'/catalog/category/{cat_slug}')
        self.assertEqual(resp.status_code, 200)


class CountryViewTest(TestBasedModel):

    def test_country_list(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/catalog/country_list/')
        self.assertEqual(resp.status_code, 200)

    def test_add_country_by_status_code(self):
        resp = self.client.post(
            '/catalog/add_country/',
            {'name': 'Country_Test3', })
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
