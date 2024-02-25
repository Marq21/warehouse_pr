
from django.test import TestCase
from django.urls import reverse
from actions.utils import create_action
from django.contrib.auth.models import User

from catalog.models import Category, Country, Nomenclature
from warehouse_pr.tests import TestBasedModel


class ActionViewTest(TestBasedModel):

    def test_show_actions_ok_status(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(reverse('show-actions'))
        self.assertEqual(resp.status_code, 200)
