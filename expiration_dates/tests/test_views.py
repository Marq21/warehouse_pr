from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from catalog.models import Nomenclature
from expiration_dates.models import ExpirationDateEntity
from inventory.models import NomenclatureRemain


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
            reverse('expiraion_date_list'), {'quantity_list': ExpirationDateEntity.objects.all()})
        self.assertEqual(resp.status_code, 200)
