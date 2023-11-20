from rest_framework.serializers import ModelSerializer
from catalog.models import Nomenclature

class NomenclatureSerializer(ModelSerializer):
    class Meta:
        model = Nomenclature
        fields = '__all__'
        