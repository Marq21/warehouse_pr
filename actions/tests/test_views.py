
from django.test import TestCase
from django.urls import reverse
from actions.utils import create_action
from django.contrib.auth.models import User

from catalog.models import Category, Country, Nomenclature


class ActionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        number_of_cats = 13

        for category_num in range(number_of_cats):            
            parse_int = int('00000000000') + category_num
            place_for_number = len(str(parse_int))
            result = ['0' for _ in range(11)]
            result[-place_for_number:] = str(parse_int)
            n_barcode = ''.join(result)

            cat = Category.objects.create(name='Category %s' % category_num)
            country = Country.objects.create(name='Country %s' % category_num)
            nom = Nomenclature.objects.create(name='Nomenclature %s' % category_num,
                                        cost=10 + category_num,
                                        barcode=n_barcode,)
            
            create_action(cls.user, 'Добавление номенклатуры', nom)
            create_action(cls.user, 'Добавление категории', cat)
            create_action(cls.user, 'Добавление страны', country)

    def test_show_actions_ok_status(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(reverse('show-actions'))
        self.assertEqual(resp.status_code, 200)
