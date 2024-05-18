from django.urls import path
from .views import *

app_name = 'index'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('catalog/<str:slug>', DishView.as_view(), name='dishes'),
    path('create-order', OrderAPIView.as_view(), name='create_order'),
]
