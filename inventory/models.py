from datetime import datetime
from django.db import models
from django.urls import reverse
from catalog.utils import slugify
from catalog.models import Nomenclature


class NomenclatureRemain(models.Model):
    name = models.CharField(max_length=200, blank=True)
    nomenclature = models.OneToOneField(
        'catalog.Nomenclature',
        on_delete=models.CASCADE,
        related_name='nomenclature_remain',
    )
    quantity = models.IntegerField(default=0, blank=True)
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


class InventoryTask(models.Model):

    class InventoryStatus(models.TextChoices):
        FORMED = 'F', 'Формиурется'
        IN_PROGRESS = 'IP', 'В работе'
        DONE = 'D', 'Завершено'

    name = models.CharField(max_length=200)
    created = models.DateTimeField(
        auto_now_add=True,)
    category = models.ForeignKey(
        'catalog.Category',
        on_delete=models.CASCADE,
        related_name='inventory_task',
        null=True)
    status = models.CharField(
        max_length=2,
        choices=InventoryStatus.choices,
        blank=True,
        default=InventoryStatus.FORMED,
        help_text='Статус инвентаризации',
        verbose_name='InventoryStatus')

    class Meta:
        ordering = ["name"]
        verbose_name = "InventoryTask"
        verbose_name_plural = "InventoryTasks"

    def get_absolute_url(self):
        return reverse('inventory-task-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'


class InventoryItem(models.Model):
    name = models.CharField(max_length=200, blank=True)
    nomenclature = models.OneToOneField(
        'catalog.Nomenclature',
        on_delete=models.CASCADE,
        related_name='inventory_item',
    )
    current_quantity = models.FloatField(
        default=0, blank=True, verbose_name='Количество', help_text='Введите количество товара')
    inventory_task = models.ForeignKey(
        'InventoryTask',
        on_delete=models.CASCADE,
        related_name='inventory_item',
        null=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "InventoryItem"
        verbose_name_plural = "InventoryItems"

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.name = f'{Nomenclature.objects.get(id=self.nomenclature.id).name}-{datetime.now()}-{self.inventory_task.pk}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory-item-update', kwargs={"pk": self.pk})
