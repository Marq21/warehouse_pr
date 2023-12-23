from rest_framework.serializers import ModelSerializer
from catalog.models import Nomenclature, Category

class NomenclatureSerializer(ModelSerializer):
    class Meta:
        model = Nomenclature
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        