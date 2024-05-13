import os
from typing import Union
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from index.models import Dish
from .cart import Cart
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES, STATUS_TYPES


class CartTemplateView(TemplateView):
    """
    Класс шаблона корзины.
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        Инициализация шаблона корзины.
        """
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        cart_items = dict(cart.cart.items())
        cart_items_ids = cart_items.keys()
        products = Dish.objects.filter(id__in=cart_items_ids)

        cart_products = {}

        for product in products:
            cart_products[product.id] = {
                'id': product.id,
                'title': product.title,
                'image': product.image,
                'price': product.price,
                'quantity': cart_items[str(product.id)]['quantity']
            }

        cart = CartView().get_cart(self.request)
        cart_amount = cart.get_total_amount()

        try:
            delivery_cost = int(os.getenv('DELIVERY_COST'))
        except ValueError:
            delivery_cost = 0

        context['products'] = cart_products
        context['cart_amount'] = cart_amount
        context['cart_total'] = cart_amount + delivery_cost
        context['delivery_cost'] = delivery_cost
        return context


class CartView(APIView):
    """
    Класс API для работы с корзиной.
    """
    def get_cart(self, request: WSGIRequest) -> Cart:
        """
        Возвращяет экземляр корзины.
        """
        cart = Cart(request)
        return cart

    def get(self, request: WSGIRequest) -> Union[HttpResponse, Response]:
        """
        Возвращяет содержимое корзины.
        """

        cart = self.get_cart(request)

        response_data = {
            'status': STATUS_TYPES['success'],
            'items': cart.cart.items(),
        }
        return Response(response_data)

    @staticmethod
    @api_view(('GET',))
    @renderer_classes((JSONRenderer,))
    def get_amount(request):
        """
        Возвращяет сумму корзины.
        """
        cart = CartView().get_cart(request)

        response_data = {
            'status': STATUS_TYPES['success'],
            'amount': cart.get_total_amount()
        }
        return Response(response_data)

    @staticmethod
    @api_view(('POST',))
    @renderer_classes((JSONRenderer,))
    def add(request: WSGIRequest, product_id: str, quantity=1) -> Response:
        """
        Вызывает метод добавления товара в коризну.
        """
        cart = CartView().get_cart(request)
        isNewItem = True

        response_data = {
            'status': STATUS_TYPES['error'],
            'message': ERROR_MESSAGES['error_adding_item']
        }

        if product_id in cart.cart.keys():
            isNewItem = False

        result = cart.add(product_id, quantity)

        if result is True:
            if isNewItem is True:
                response_data['message'] = SUCCESS_MESSAGES['success_adding_item']
            else:
                response_data['message'] = SUCCESS_MESSAGES['success_updating_item']

            response_data['status'] = STATUS_TYPES['success']
            response_data['items'] = cart.cart.items()

        return Response(response_data)

    @staticmethod
    @api_view(('POST',))
    @renderer_classes((JSONRenderer,))
    def delete(request: WSGIRequest, product_id: str) -> Response:
        """
        Вызывает метод удаления товара из коризны.
        """
        cart = CartView().get_cart(request)

        response_data = {
            'status': STATUS_TYPES['error'],
            'message': ERROR_MESSAGES['error_deleting_item']
        }

        try:
            result = cart.remove(product_id)

            if result is not True:
                return Response(response_data)

        except ValueError:
            return Response(response_data)

        response_data = {
            'status': STATUS_TYPES['success'],
            'message': SUCCESS_MESSAGES['success_deleting_item'],
            'items': cart.cart.items(),
        }
        return Response(response_data)
