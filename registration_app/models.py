from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):

    class Positions(models.TextChoices):
        DIRECTOR = 'DIR', 'director'
        ADMINISTRATOR = 'ADM', 'administrator'
        SELLER = 'SEL', 'seller'

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, region="RU")
    position = models.CharField(
        max_length=3,
        choices=Positions.choices,
        blank=True,
        default=Positions.SELLER,
        help_text='Position',
        verbose_name='Должность')
    photo = models.ImageField(upload_to='uploads',
                              blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_start_working = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
