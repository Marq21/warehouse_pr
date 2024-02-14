from catalog.models import Category, Nomenclature
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store_api.serializers import NomenclatureSerializer


class NomenclatureTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create(username='user1')
        cat1 = Category.objects.create(name='cat1')
        cat2 = Category.objects.create(name='cat2')
        self.nom1 = Nomenclature.objects.create(
            name='Nom1', cost=10, weight_or_piece='PC', barcode='00000000001', category=cat1, user=user)
        self.nom2 = Nomenclature.objects.create(
            name='Nom2', cost=11, weight_or_piece='PC', barcode='00000000002', category=cat2, user=user)

    def test_get(self):
        url = reverse('nomenclature-list-view')
        print(url)
        response = self.client.get(url)
        print(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
