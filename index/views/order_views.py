import json
from json import JSONDecodeError
import stripe
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from rest_framework.views import APIView
from cafe import settings
from cart.views import CartView
from index.forms import OrderForm, OrderItemForm
from index.models import Dish
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES
from utils.response import success_response, error_response
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


@method_decorator(ratelimit(key='ip', rate='2/m'), name='dispatch')
class OrderAPIView(APIView):
    """
    Класс API для работы с заказом.
    """
    def post(self, request: WSGIRequest) -> JsonResponse:
        """
        Форматирует и записывает заказ в БД.
        """
        try:
            data = json.loads(json.dumps(request.data))
        except JSONDecodeError:
            return error_response(ERROR_MESSAGES['invalid_request'])

        client_data = data.get('client_data')

        order_form = OrderForm(data=client_data)

        if order_form.is_valid():
            order = order_form.save()
            request.session[settings.ORDER_ID_SESSION_ID] = order.pk

            order_items = CartView().get_cart(request).cart

            if len(order_items) > 0:
                for dish_id, value in order_items.items():
                    dish = Dish.objects.get(id=dish_id)
                    order_item_dict = self.get_formated_order_item_dict(dish, value['quantity'])

                    order_item_form = OrderItemForm(order_item_dict)

                    if order_item_form.is_valid():
                        order_item = order_item_form.save(commit=False)
                        order_item.order_id = order
                        order_item.save()
                    else:
                        return error_response(ERROR_MESSAGES['invalid_request'])

                payment_link = self.get_payment_link(request)

                return success_response(SUCCESS_MESSAGES['success_order'], payment_url=payment_link)

            else:
                return error_response(ERROR_MESSAGES['error_cart_is_empty'])
        else:
            for field, errors in order_form.errors.items():
                if errors:
                    return error_response(errors[0])
        return error_response(ERROR_MESSAGES['invalid_request'])

    def get_formated_order_item_dict(self, dish: Dish, quantity: int) -> dict:
        """
        Возвращяет форматированный словарь блюда из корзины.
        """
        dish_price = round(dish.price * quantity)

        return {
            'dish_id': dish.pk,
            'quantity': quantity,
            'price': dish_price,
        }

    def get_payment_link(self, request: WSGIRequest) -> str:
        """
        Создает и возвращяет ссылку на оплату.
        """
        redirect_url = request.build_absolute_uri(reverse('cart:cart'))

        cart = CartView().get_cart(request)
        cart_amount = cart.get_total_amount() * 100

        stripe_request = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': settings.CURRENCY,
                    'unit_amount': cart_amount,
                    'product_data': {
                        'name': settings.TRANSACTION_NAME
                    }
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=redirect_url
        )

        request.session[settings.STRIPE_SESSION_ID] = stripe_request['id']

        return stripe_request['url']
