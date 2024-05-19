from django.db import models
from index.models import Dish, Coupon


class Order(models.Model):
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    client_phone = models.CharField(max_length=100, verbose_name='Номер телефона клиента')
    client_mail = models.EmailField(verbose_name='Электронная почта клиента')
    client_address = models.CharField(max_length=100, verbose_name='Адрес клиента')
    status = models.BooleanField(default=False, verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Заказ')
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
