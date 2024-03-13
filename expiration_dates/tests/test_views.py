from datetime import datetime
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from catalog.models import Nomenclature
from expiration_dates.models import ExpirationDateEntity
from inventory.models import NomenclatureRemain
from expiration_dates.forms import AddExpirationDatesEntityForm
from expiration_dates.views import AddExpirationDatesEntityView, EditExpirationDatesEntityView


class ExpirationDateListViewTest(TestCase):

    def setUp(self) -> None:
        User.objects.create(username='john', password='johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now().strftime("%Y-%m-%d"),
            date_of_expiration=datetime.now().strftime("%Y-%m-%d"),
        )
        return super().setUp()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('expiraion_date_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_nom_list_template_used(self):
        resp = self.client.get(reverse('expiraion_date_list'))
        self.assertTemplateUsed(
            resp, 'expiration_dates/exp-date-entity-list.html')

    def test_home_view(self):
        resp = self.client.get(
            reverse('expiration_date_list'), {'quantity_list': ExpirationDateEntity.objects.all()})
        self.assertEqual(resp.status_code, 200)


class ExpirationDateDetailViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.get(username='john')
        self.client.login(username='john', password='johnpassword')
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now().strftime("%Y-%m-%d"),
            date_of_expiration=datetime.now().strftime("%Y-%m-%d"),
        )
        return super().setUp()

    def test_exp_date_detail(self):
        resp = self.client.get(
            reverse('exp_date_details', kwargs={'pk': self.exp_date_entity.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_exp_date_detail_template_used(self):
        resp = self.client.get(
            reverse('exp_date_details', kwargs={'pk': self.exp_date_entity.pk}))
        self.assertTemplateUsed(
            resp, 'expiration_dates/exp_date_entity_detail.html')


class ExpirationDateCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.get(username='john')
        self.client.login(username='john', password='johnpassword')
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now().strftime("%Y-%m-%d"),
            date_of_expiration=datetime.now().strftime("%Y-%m-%d"),
        )
        return super().setUp()

    def test_call_view_fail_blank(self):
        response = self.client.post(
            reverse('exp_date_create'), {})
        self.assertFormError(response, 'form', 'date_of_manufacture',
                             'Это поле обязательно для заполнения.')

    def test_create_view_POST_success_form_valid(self):
        date_of_manufacture = datetime(2000, 10, 13).strftime("%Y-%m-%d")
        date_of_expiration = datetime(2001, 10, 13).strftime("%Y-%m-%d")
        data = {
            'nomenclature_remain': self.nom_remain,
            'quantity': 1,
            'date_of_manufacture': date_of_manufacture,
            'date_of_expiration': date_of_expiration,
        }

        form = AddExpirationDatesEntityForm(data)
        request = self.factory.post(reverse('exp_date_create'), data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        add_view = AddExpirationDatesEntityView()
        add_view.setup(request)
        self.assertTrue(add_view.form_valid(form=form))
        self.assertTrue(ExpirationDateEntity.objects.get(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=date_of_manufacture,
            date_of_expiration=date_of_expiration
        ))


class TestEditExpirationDatesEntityView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.get(username='john')
        self.client.login(username='john', password='johnpassword')
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now().strftime("%Y-%m-%d"),
            date_of_expiration=datetime.now().strftime("%Y-%m-%d"),
        )
        return super().setUp()

    def test_update_view_POST_form_invalid(self):
        data = {
            'nomenclature_remain': self.nom_remain,
            'quantity': 1,
            'date_of_manufacture': 'date_of_manufacture',
            'date_of_expiration': 'date_of_expiration',
        }

        form = AddExpirationDatesEntityForm(data)
        request = self.factory.post(
            reverse('edit_exp_date', kwargs={'pk': self.exp_date_entity.pk}), data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        edit_view = EditExpirationDatesEntityView(object=self.exp_date_entity)
        edit_view.setup(request)
        self.assertTrue(edit_view.form_invalid(form=form))

    def test_update_view_POST_success_form_valid(self):
        quantity_for_compare_in_assert = self.exp_date_entity.name
        date_of_manufacture = datetime(2000, 10, 13).strftime("%Y-%m-%d")
        date_of_expiration = datetime(2001, 10, 13).strftime("%Y-%m-%d")
        data = {
            'nomenclature_remain': self.nom_remain,
            'quantity': 10,
            'date_of_manufacture': date_of_manufacture,
            'date_of_expiration': date_of_expiration,
        }

        form = AddExpirationDatesEntityForm(data)
        request = self.factory.post(
            reverse('edit_exp_date', kwargs={'pk': self.exp_date_entity.pk}), data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        view = EditExpirationDatesEntityView(object=self.exp_date_entity)
        view.setup(request)
        self.assertTrue(view.form_valid(form=form))
        self.assertFalse(self.exp_date_entity.quantity ==
                         quantity_for_compare_in_assert)


class TestDeleteExpirationDatesEntityView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.get(username='john')
        self.client.login(username='john', password='johnpassword')
        self.nomenclature = Nomenclature.objects.create(
            name='Test_Nomenclature',
            cost='10',
        )
        self.nom_remain = NomenclatureRemain.objects.create(
            nomenclature=self.nomenclature,
        )
        self.exp_date_entity = ExpirationDateEntity.objects.create(
            nomenclature_remain=self.nom_remain,
            date_of_manufacture=datetime.now().strftime("%Y-%m-%d"),
            date_of_expiration=datetime.now().strftime("%Y-%m-%d"),
        )
        return super().setUp()

    def test_delete_exp_date_by_status_code(self):
        resp = self.client.post(
            reverse('delete_exp_date', kwargs={'pk': self.exp_date_entity.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_delete_view_get_context(self):
        resp = self.client.get(reverse('delete_exp_date', kwargs={
                               'pk': self.exp_date_entity.pk}))
        resp.user = self.user
        self.assertIsInstance(resp.context_data, dict)
        self.assertEqual(
            resp.context_data['title'], "Удалить срок годности")
        self.assertFalse(
            resp.context_data['title'], "")
