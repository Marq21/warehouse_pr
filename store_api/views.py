from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from catalog.models import Nomenclature
from .serializers import NomenclatureSerializer


class NomenclatureViewSet(ModelViewSet):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['weight_or_piece', 'category', 'user']
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'barcode', 'slug']
    ordering_fields = ['name', 'cost']


def auth(request):
    return render(request, 'oauth.html')
