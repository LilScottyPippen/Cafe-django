from django.db import models


class Coupon(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    code = models.IntegerField(unique=True, verbose_name="Код")
    uses = models.IntegerField(verbose_name="Количество использований")
    used = models.IntegerField(default=0, verbose_name="Количество использовано")
    discount = models.IntegerField(verbose_name="Скидка (%)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"
