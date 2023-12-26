from rest_framework.serializers import ModelSerializer
from catalog.models import Nomenclature, Category
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NomenclatureSerializer(ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Nomenclature
        fields = ['name', 'cost', 'weight_or_piece',
                  'barcode', 'slug', 'user', 'country_made', 'category']
