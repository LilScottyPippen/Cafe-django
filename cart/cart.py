from typing import Union
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from index.models import Dish


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

    def get_total_amount(self) -> Union[int, bool]:
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

    def save(self) -> None:
        """
        Сохранение корзины в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
