from django.db import models
from django.utils import timezone

from players.models import Player


class Country(models.Model):
    """The model has info about country"""

    name = models.CharField(max_length=255, default='Беларусь', unique=True, verbose_name='Страна')

    class Meta:
        verbose_name_plural = 'Страны'
        verbose_name = 'Страна'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    """The model has info about city"""

    name = models.CharField(max_length=255, default='Минск', verbose_name='Город')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='city_country', verbose_name='Страна')

    class Meta:
        unique_together = ('name', 'country')
        verbose_name_plural = 'Города'
        verbose_name = 'Город'

    def __str__(self):
        return f"{self.name}"
