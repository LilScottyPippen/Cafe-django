from django.db import models
from utils.media_paths import dish_path
from .catalog import Catalog


class Dish(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='Каталог')
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to=dish_path, verbose_name='Изображение')
    description = models.CharField(max_length=256, verbose_name='Описание')
    weight = models.IntegerField(verbose_name='Вес (граммы)')
    price = models.IntegerField(verbose_name='Стоимость (BYN)')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блюд'
        verbose_name_plural = 'Блюда'
