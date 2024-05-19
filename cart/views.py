import json
import math
import os
from json import JSONDecodeError
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework.views import APIView
from index.models import Dish, Coupon
from utils.response import success_response, error_response
from .cart import Cart
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES
from .forms import BaseDishForm, UpdateDishForm, CouponForm


class CartTemplateView(TemplateView):
    """
    Класс шаблона корзины.
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        Инициализация шаблона.
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

        context.update(self.get_discount(cart_amount))

        return context

    def get_cart_products(self) -> dict:
        """
        Возвращяет список товаров корзины.
        """
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

    def get_discount(self, cart_amount: int) -> dict:
        """
        Расчитывает скидку и возвращяет словарь с данными о скидке.
        """
        try:
            coupon_discount = Coupon.objects.get(code=self.request.session.get('coupon')).discount
        except Coupon.DoesNotExist:
            coupon_discount = None

        context = {}

        delivery_cost = self.get_delivery_cost()

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

    def get(self, request: WSGIRequest) -> JsonResponse:
        """
        Возвращяет содержимое корзины.
        """
        cart = self.get_cart(request)
        items = cart.cart.items()
        return success_response(None, items=list(items))

    @staticmethod
    @api_view(('GET',))
    @renderer_classes((JSONRenderer,))
    def get_amount(request: WSGIRequest):
        """
        Возвращяет сумму корзины.
        """
        cart = CartView().get_cart(request)
        amount = cart.get_total_amount()

        return success_response(None, amount=amount)

    @staticmethod
    @api_view(('POST',))
    @renderer_classes((JSONRenderer,))
    def add(request: WSGIRequest) -> JsonResponse:
        """
        Вызывает метод добавления товара в корзину.
        """
        try:
            data = json.loads(json.dumps(request.data))
        except JSONDecodeError:
            return error_response(ERROR_MESSAGES['invalid_request'])

        add_dish_form = BaseDishForm(data)

        if add_dish_form.is_valid():
            product_id = str(data.get('product_id'))
            quantity = data.get('quantity')

            cart = CartView().get_cart(request)

            if quantity:
                update_dish_form = UpdateDishForm(data)

                if update_dish_form.is_valid():
                    result = cart.add(product_id, quantity)
                    message = SUCCESS_MESSAGES['success_updating_item']
                else:
                    return error_response(ERROR_MESSAGES['invalid_request'])
            else:
                message = SUCCESS_MESSAGES['success_adding_item']
                result = cart.add(product_id)

            if result is True:
                items = cart.cart.items()
                return success_response(message, items=list(items))
            else:
                return error_response(ERROR_MESSAGES['error_adding_item'])
        else:
            for field, error in add_dish_form.errors.items():
                if error:
                    return error_response(error[0])

    @staticmethod
    @api_view(('POST',))
    @renderer_classes((JSONRenderer,))
    def delete(request: WSGIRequest) -> JsonResponse:
        """
        Вызывает метод удаления товара из корзины.
        """
        try:
            data = json.loads(json.dumps(request.data))
        except JSONDecodeError:
            return error_response(ERROR_MESSAGES['invalid_request'])

        delete_dish_form = BaseDishForm(data)

        if delete_dish_form.is_valid():
            product_id = str(data.get('product_id'))
            cart = CartView().get_cart(request)

            result = cart.remove(product_id)

            if result is not True:
                return error_response(ERROR_MESSAGES['error_deleting_item'])

            items = cart.cart.items()
            return success_response(SUCCESS_MESSAGES['success_deleting_item'], items=list(items))
        return error_response(ERROR_MESSAGES['error_deleting_item'])

    @staticmethod
    @api_view(('POST',))
    @renderer_classes((JSONRenderer,))
    def coupon(request: WSGIRequest) -> JsonResponse:
        """
        Применяет купон.
        """
        try:
            data = json.loads(json.dumps(request.data))
        except JSONDecodeError:
            return error_response(ERROR_MESSAGES['invalid_request'])

        coupon_form = CouponForm(data)

        if coupon_form.is_valid():
            coupon = data.get('code')

            coupon = Coupon.objects.get(code=coupon)
            session_coupon = request.session.get('coupon')

            if not session_coupon or session_coupon != coupon.code:
                request.session['coupon'] = coupon.code

                coupon.used += 1
                coupon.save()

                discount = coupon.discount
                return success_response(SUCCESS_MESSAGES['success_apply_coupon'], discount=discount)
            else:
                if session_coupon == coupon.code:
                    return error_response(ERROR_MESSAGES['error_apply_coupon'])
        return error_response(ERROR_MESSAGES['error_dont_exist_coupon'])
