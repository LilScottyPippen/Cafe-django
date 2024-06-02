import math
import os
from typing import Union
from django.core.handlers.wsgi import WSGIRequest
from cafe import settings
from index.models import Dish, Coupon


class Cart(object):
    def __init__(self, request: WSGIRequest) -> None:
        """
        Инициализирует экземпляр корзины, получая сессию из запроса.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product_id: str, quantity=1) -> bool:
        """
        Добавляет продукт в корзину или обновляет его количество.
        """
        try:
            product = Dish.objects.get(id=product_id)
        except Dish.DoesNotExist:
            return False

        self.cart[product_id] = {
            'quantity': quantity,
            'price': product.price,
            'total_sum': product.price * quantity,
        }

        self.save()
        return True

    def remove(self, product_id: str) -> bool:
        """
        Удаляет товар из корзины.
        """
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            return True
        return False

    def save(self) -> None:
        """
        Сохранение корзины в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self.cart

    def get_amount(self) -> int:
        """
        Расчитывает сумму корзины.
        """
        amount = 0

        for product_id, item in self.cart.items():
            try:
                product = Dish.objects.get(id=product_id)
            except Dish.DoesNotExist:
                return False
            amount += product.price * int(item['quantity'])
        return amount

    def get_total_amount(self) -> Union[int, bool]:
        """
        Расчитывает итоговую сумму корзины.
        """
        amount = self.get_amount()

        discount = self.get_discount()

        delivery_cost = int(os.getenv('DELIVERY_COST'))

        if discount:
            discount = math.ceil(amount / 100 * discount)

        return (amount - discount) + delivery_cost

    def get_discount(self) -> Union[int, bool]:
        coupon = self.session.get(settings.COUPON_SESSION_ID)

        if coupon:
            try:
                coupon_discount = Coupon.objects.get(code=coupon).discount
            except Coupon.DoesNotExist:
                coupon_discount = None

            if coupon_discount:
                return coupon_discount
        return False
