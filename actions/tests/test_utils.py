from django.test import TestCase
from django.contrib.auth.models import User

from catalog.models import Category, Country, Nomenclature
from actions.utils import create_action


class TestCreateAction(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        number_of_cats = 13

        for category_num in range(number_of_cats):
            Category.objects.create(name='Category %s' % category_num)
            Country.objects.create(name='Country %s' % category_num)
            parse_int = int('00000000000') + category_num
            place_for_number = len(str(parse_int))
            result = ['0' for _ in range(11)]
            result[-place_for_number:] = str(parse_int)
            n_barcode = ''.join(result)
            Nomenclature.objects.create(name='Nomenclature %s' % category_num,
                                        cost=10 + category_num,
                                        barcode=n_barcode,)

    def test_create_action_nom(self):
        user = User.objects.get(username='john')
        nom = Nomenclature.objects.create(
            name='Test_Nom', cost='10.0', barcode='00000000001')
        result = create_action(user, 'Добавление номенклатуры', nom)
        self.assertTrue(result)

    def test_crea_action_nom_false_case(self):
        user = User.objects.get(username='john')
        nom = Nomenclature.objects.create(
            name='Test_Nom', cost='10.0', barcode='00000000001')
        create_action(user, 'Добавление номенклатуры', nom)
        similar_action_result = create_action(
            user, 'Добавление номенклатуры', nom)
        self.assertFalse(similar_action_result)
