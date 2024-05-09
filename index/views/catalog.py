from django.http import Http404
from django.views.generic import TemplateView
from cart.views import CartView
from ..models import Catalog, Dish


class CatalogView(TemplateView):
    template_name = 'catalog/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Catalog.objects.all()
        return context


class DishView(TemplateView):
    template_name = 'catalog/dishes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = Dish.objects.filter(catalog__slug=self.kwargs['slug'])

        try:
            context['title'] = Catalog.objects.get(slug=self.kwargs['slug']).title
        except Catalog.DoesNotExist:
            raise Http404()

        items_in_cart = []
        for item_id in CartView().get_cart(self.request).cart.keys():
            items_in_cart.append(int(item_id))

        context['catalog'] = dish
        context['cart_ids'] = items_in_cart
        return context
