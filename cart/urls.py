from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', CartTemplateView.as_view(), name='cart'),
    path('get', CartView.as_view(), name='cart_get'),
    path('get-amount', CartView.get_amount, name='cart_get_amount'),
    path('add/<str:product_id>', CartView.add, name='cart_add'),
    path('add/<str:product_id>/<int:quantity>', CartView.add, name='cart_add_quantity'),
    path('delete/<str:product_id>', CartView.delete, name='cart_delete'),
    path('coupon/<str:coupon>', CartView.coupon)
]