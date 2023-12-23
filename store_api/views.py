from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from catalog.models import Nomenclature, Category
from .serializers import NomenclatureSerializer, CategorySerializer


class NomenclatureViewSet(ModelViewSet):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['weight_or_piece', 'category', 'user']
    # permission_classes = [IsAuthenticated]
    search_fields = ['name', 'barcode', 'slug']
    ordering_fields = ['name', 'cost']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']

