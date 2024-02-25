from django.test import TestCase
from django.contrib.auth.models import User

from catalog.models import Category, Country, Nomenclature
from actions.utils import create_action
from warehouse_pr.tests import TestBasedModel


class TestCreateAction(TestBasedModel):

    def test_create_action_nom(self):
        user = User.objects.get(username='john')
        nom = Nomenclature.objects.create(
            name='Test_Nom', cost='10.0', barcode='00000000001')
        result = create_action(user, 'Добавление номенклатуры', nom)
        self.assertTrue(result)

    def test_create_action_nom_false_case(self):
        user = User.objects.get(username='john')
        nom = Nomenclature.objects.create(
            name='Test_Nom', cost='10.0', barcode='00000000001')
        create_action(user, 'Добавление номенклатуры', nom)
        similar_action_result = create_action(
            user, 'Добавление номенклатуры', nom)
        self.assertFalse(similar_action_result)
