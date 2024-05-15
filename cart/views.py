import math
import os
from typing import Union
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from index.models import Dish, Coupon
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

        cart_products = self.get_cart_products()

        cart = CartView().get_cart(self.request)
        cart_amount = cart.get_total_amount()

        delivery_cost = self.get_delivery_cost()

        context['products'] = cart_products
        context['cart_amount'] = cart_amount
        context['delivery_cost'] = delivery_cost
        context['cart_total'] = cart_amount + delivery_cost

        context.update(self.get_discount(cart_amount, delivery_cost))

        return context

    def get_cart_products(self) -> dict:
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
        return cart_products

    def get_delivery_cost(self) -> int:
        """
        Возвращяет стоимость доставки.
        """
        try:
            return int(os.getenv('DELIVERY_COST'))
        except ValueError:
            return 0

    def get_discount(self, cart_amount: int, delivery_cost: int) -> dict:
        """
        Расчитывает скидку и возвращяет словарь.
        """
        try:
            coupon_discount = Coupon.objects.get(code=self.request.session.get('coupon')).discount
        except Coupon.DoesNotExist:
            coupon_discount = None

        context = {}

        if coupon_discount:
            discount = math.ceil(cart_amount / 100 * coupon_discount)

            context['discount'] = coupon_discount
            context['cart_total'] = (cart_amount - discount) + delivery_cost

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

    @staticmethod
    @api_view(('POST',))
    @renderer_classes((JSONRenderer,))
    def coupon(request: WSGIRequest, coupon: str) -> Response:
        try:
            coupon_obj = Coupon.objects.get(code=coupon)
        except Coupon.DoesNotExist:
            coupon_obj = False

        response_data = {
            'status': STATUS_TYPES['error'],
            'message': ERROR_MESSAGES['error_dont_exist_coupon']
        }

        if coupon_obj is not False and coupon_obj.used < coupon_obj.uses:
            session_coupon = request.session.get('coupon')

            if not session_coupon or session_coupon != coupon:
                request.session['coupon'] = coupon
                coupon_obj.used += 1
                coupon_obj.save()

                response_data['status'] = STATUS_TYPES['success']
                response_data['message'] = SUCCESS_MESSAGES['success_apply_coupon']
                response_data['discount'] = coupon_obj.discount
            else:
                if session_coupon == coupon:
                    response_data['status'] = STATUS_TYPES['error']
                    response_data['message'] = ERROR_MESSAGES['error_apply_coupon']
        return Response(response_data)
