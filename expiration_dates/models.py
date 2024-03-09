from django.db import models
from django.urls import reverse

from inventory.models import NomenclatureRemain


class ExpirationDateEntity(models.Model):
    name = models.CharField(max_length=255, db_index=True, blank=True,)
    nomenclature_remain = models.ForeignKey(
        NomenclatureRemain,
        on_delete=models.DO_NOTHING,
        related_name='exp_date_entity',
        null=True,
    )
    quantity = models.FloatField(
        default=0, blank=True, verbose_name='Количество', help_text='Введите количество товара')
    date_of_manufacture = models.DateField(
        null=True,
        verbose_name='Дата изготовления',
        help_text='Введите дату изготовления товара',
    )
    date_of_expiration = models.DateField(
        null=True,
        verbose_name='Дата окончания',
        help_text='Введите дату окончания срока годности товара',
    )

    class Meta:
        ordering = ["date_of_manufacture", "name"]
        indexes = [models.Index(fields=["name"])]
        verbose_name_plural = "ExpirationDateEntities"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('date_entity_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name = f'{self.nomenclature_remain} ({self.date_of_expiration})'
        super().save(*args, **kwargs)
