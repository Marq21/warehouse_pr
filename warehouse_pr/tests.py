from django.test import TestCase
from django.contrib.auth.models import User
from actions.utils import create_action
from catalog.models import Category, Country, GoodsProvider, Nomenclature


class TestBasedModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        number_of_cats = 13

        Country.objects.create(
            name='Test_Country')

        for category_num in range(number_of_cats):
            parse_int = int('00000000000') + category_num
            place_for_number = len(str(parse_int))
            result = ['0' for _ in range(11)]
            result[-place_for_number:] = str(parse_int)
            n_barcode = ''.join(result)
            GoodsProvider.objects.create(
                name='Test_Provider_%s' % category_num,
            )
            cat = Category.objects.create(name='Category %s' % category_num)
            country = Country.objects.create(name='Country %s' % category_num)
            nom = Nomenclature.objects.create(name='Nomenclature %s' % category_num,
                                              cost=10 + category_num,
                                              barcode=n_barcode,)

            create_action(cls.user, 'Добавление номенклатуры', nom)
            create_action(cls.user, 'Добавление категории', cat)
            create_action(cls.user, 'Добавление страны', country)
