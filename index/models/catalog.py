from django.db import models
from utils.media_paths import catalog_path


class Catalog(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to=catalog_path, verbose_name='Изображение')
    slug = models.CharField(max_length=256, unique=True, verbose_name='Псевдоним')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Каталоги'
        verbose_name_plural = 'Каталог'
