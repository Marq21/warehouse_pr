from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, )
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Nomenclature(models.Model):

    class NomsType(models.TextChoices):
        WEIGHT = 'WT', 'weight'
        PIECE = 'PC', 'pieces'

    name = models.CharField(
        max_length=80,
        help_text='Enter the name of nomenclature',
        verbose_name='Название')
    cost = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name='Цена')
    weight_or_piece = models.CharField(
        max_length=2,
        choices=NomsType.choices,
        blank=True,
        default=NomsType.PIECE,
        help_text='Nomenclature type',
        verbose_name='Тип товара (вес. или штуч.)')
    barcode = models.CharField(
        max_length=11,
        blank=True,
        help_text='Enter the barcode')
    slug = models.SlugField(max_length=250, unique=True,
                            db_index=True, verbose_name='URL')
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='nomenclatures',
        null=True,
        blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='nomenclatures',
        null=True,
        verbose_name='Категория'
    )
    country_made = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Страна изготовления',
        help_text='Enter the country')

    class Meta:
        ordering = ["name", "-cost"]
        indexes = [models.Index(fields=["-cost"]), models.Index(fields=["barcode"]), ]
        verbose_name_plural = "Nomenclatures"

    def __str__(self):
        return f"{self.name} ({self.barcode})"

    def get_absolute_url(self):
        return reverse('noms-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def format_new_barcode(barcode, format_length):
    parse_int = int(barcode) + 1
    place_for_number = format_length - len(str(parse_int))
    result = ''
    for _ in range(place_for_number):
        result += '0'
    result += str(parse_int) 
    return result 

def get_new_barcode():
    barcode = Nomenclature.objects.latest('barcode').barcode
    return format_new_barcode(barcode, len(barcode))