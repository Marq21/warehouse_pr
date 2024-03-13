from django.http import HttpResponseNotFound
from django.test import RequestFactory
from catalog.forms import AddCategoryForm, AddCountryForm, AddNomenclatureForm, EmailNomenclatureForm
from catalog.models import Category, Country, Nomenclature
from catalog.views import AddCategory, AddCountry, AddNomenclature, DeleteCountry, EditCategory, EditCountry, EditNomenclature, NomenclatureHome, nom_share
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
        add_view = AddNomenclature()
        add_view.setup(request)
        self.assertTrue(add_view.form_valid(form=form))
        self.assertTrue(Nomenclature.objects.get(name='nome_CreateView_test'))

    def test_update_view_POST_form_invalid(self):
        nom = Nomenclature.objects.last()
        data = {
            'name': 'nome_CreateView_test',
            'weight_or_piece': Nomenclature.NomsType.PIECE,
            'barcode': '00000100000',
            'cost': 10.0,
            'category': self.cat,
            'country_made_id': 'keks', }

        form = AddNomenclatureForm(data)
        request = self.factory.post(
            f'/catalog/edit_nomenclature/{nom.id}', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        edit_view = EditNomenclature(object=nom)
        edit_view.setup(request)
        self.assertTrue(edit_view.form_invalid(form=form))

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
        self.factory = RequestFactory()
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
            reverse('category-details', kwargs={'slug': cat_slug}))
        self.assertEqual(resp.status_code, 200)

    def test_create_view_POST_success_form_valid(self):

        data = {
            'name': 'nome_category_view_test',
        }

        form = AddCategoryForm(data)
        request = self.factory.post('/catalog/add_category/', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        add_view = AddCategory()
        add_view.setup(request)
        self.assertTrue(add_view.form_valid(form=form))
        self.assertTrue(Category.objects.get(name='nome_category_view_test'))

    def test_update_view_POST_success_form_valid(self):
        cat = Category.objects.last()
        name_for_compare_in_assert = cat.name
        data = {
            'name': 'new_category_name',
        }

        form = AddCategoryForm(data)
        request = self.factory.post(
            f'/catalog/edit_category/{cat.id}', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        view = EditCategory()
        view.setup(request)
        self.assertTrue(view.form_valid(form=form))
        self.assertFalse(Category.objects.get(
            name='new_category_name') == name_for_compare_in_assert)

    def test_update_view_POST_form_invalid(self):
        cat = Category.objects.last()
        data = {'name': ''}
        form = AddCategoryForm(data)
        request = self.factory.post(
            f'/catalog/edit_category/{cat.id}', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        edit_view = EditCategory(object=cat)
        edit_view.setup(request)
        self.assertTrue(edit_view.form_invalid(form=form))


class CountryViewTest(TestBasedModel):

    def setUp(self) -> None:
        self.client.login(username='john', password='johnpassword')
        self.factory = RequestFactory()
        return super().setUp()

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

    def test_create_view_POST_success_form_valid(self):
        data = {
            'name': 'country_view_test',
        }
        form = AddCountryForm(data)
        request = self.factory.post('/catalog/add_country/', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        add_view = AddCountry()
        add_view.setup(request)
        self.assertTrue(add_view.form_valid(form=form))
        self.assertTrue(Country.objects.get(name='country_view_test'))

    def test_update_view_POST_form_invalid(self):
        country = Country.objects.last()
        data = {'name': ''}
        form = AddCountryForm(data)
        request = self.factory.post(
            f'/catalog/edit_country/{country.id}', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        edit_view = EditCountry(object=country)
        edit_view.setup(request)
        self.assertTrue(edit_view.form_invalid(form=form))

    def test_delete_view_get_context(self):
        country = Country.objects.last()
        resp = self.client.get(f"/catalog/delete_country/{country.pk}")
        resp.user = self.user
        self.assertIsInstance(resp.context_data, dict)
        self.assertEqual(
            resp.context_data['title'], "Удалить страну изготовления")


class TestPageNotFound(TestBasedModel):

    def test_not_found(self):
        resp = self.client.get("/kkkk/")
        self.assertIsInstance(resp, HttpResponseNotFound)

    def test_not_found_message(self):
        resp = self.client.get("/kkkk/")
        self.assertEqual(resp.content.decode(),
                         "<h1> Страница не найдена! </h1>")


class TestNomSearch(TestBasedModel):

    def setUp(self) -> None:
        self.client.login(username='john', password='johnpassword')
        self.factory = RequestFactory()
        return super().setUp()

    def test_nom_search_status_code(self):
        resp = self.client.get("/catalog/search/")
        self.assertEqual(resp.status_code, 200)


class NomShareTest(TestBasedModel):

    def setUp(self) -> None:
        self.nom = Nomenclature.objects.last()
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        self.factory = RequestFactory()
        return super().setUp()

    def test_nom_share_get_status_code(self):

        resp = self.client.get(f"/catalog/{self.nom.pk}/share/")
        self.assertEqual(resp.status_code, 200)

    def test_nom_share_post_status_code(self):

        resp = self.client.post(f"/catalog/{self.nom.pk}/share/")
        self.assertEqual(resp.status_code, 200)

    def test_nom_share_is_valid(self):

        data = {
            'name': 'test1',
            'email': 'muqqyjmuqq@gmail.com',
            'to': 'muqqyjmuqq@gmail.com',
            'comments': 'some test comments'
        }
        request = self.factory.post(
            f"/catalog/{self.nom.pk}/share/", data=data)
        form = EmailNomenclatureForm(data)

        request.user = self.user
        share_view = nom_share(request, nom_id=self.nom.pk)

        self.assertTrue(form.is_valid())
        self.assertTrue(share_view.status_code, 200)
