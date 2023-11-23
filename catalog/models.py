from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify as django_slugify


def slugify(s):

    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
                'я': 'ya'}

    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


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
        indexes = [models.Index(fields=["-cost"]), ]
        verbose_name_plural = "Nomenclatures"

    def __str__(self):
        return f"{self.name} ({self.barcode})"

    def get_absolute_url(self):
        return reverse('noms-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
