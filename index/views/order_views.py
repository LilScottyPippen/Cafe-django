import json
from json import JSONDecodeError
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.views import APIView
from index.forms import OrderForm, OrderItemForm
from index.models import Dish
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES
from utils.response import success_response, error_response
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


@method_decorator(ratelimit(key='ip', rate='1/m'), name='dispatch')
class OrderAPIView(APIView):
    """
    Класс API для работы с заказом.
    """
    def post(self, request: WSGIRequest) -> JsonResponse:
        """
        Форматирует и записывает заказ в БД.
        """
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return error_response(ERROR_MESSAGES['invalid_request'])

        client_data = data.get("client_data")
        dish_data = data.get("dish_data")

        order_form = OrderForm(data=client_data)

        if order_form.is_valid():
            order = order_form.save()

            try:
                order_items = dish_data.items()
            except AttributeError:
                return error_response(ERROR_MESSAGES['invalid_request'])

            if len(order_items) > 0:
                for dish_id, quantity in order_items:
                    dish = Dish.objects.get(id=dish_id)
                    order_item_dict = self.get_formated_order_item_dict(dish, quantity)

                    order_item_form = OrderItemForm(order_item_dict)

                    if order_item_form.is_valid():
                        order_item = order_item_form.save(commit=False)
                        order_item.order_id = order
                        order_item.save()
                        return success_response(SUCCESS_MESSAGES['success_order'])
                    else:
                        return error_response(ERROR_MESSAGES['invalid_request'])
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
