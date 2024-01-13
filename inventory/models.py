from datetime import datetime
from django.db import models
from django.urls import reverse
from catalog.utils import slugify
from catalog.models import Nomenclature


class NomenclatureRemain(models.Model):
    name = models.CharField(max_length=200)
    nomenclature = models.OneToOneField(
        'catalog.Nomenclature',
        on_delete=models.CASCADE,
        related_name='nomenclature_remain',
    )
    quantity = models.IntegerField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "NomenclatureRemain"
        verbose_name_plural = "NomenclatureRemains"

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.name = f'{Nomenclature.objects.get(id=self.nomenclature.id).name} {datetime.now()}'
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
