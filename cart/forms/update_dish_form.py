from django import forms
from index.models import Dish
from utils.constants import ERROR_MESSAGES


class UpdateDishForm(forms.Form):
    """
    Форма обновления количества блюда в корзине.
    """
    product_id = forms.CharField()
    quantity = forms.IntegerField()

    def clean(self):
        """
        Валидация полей формы.
        """
        cleaned_data = super().clean()
        product_id = cleaned_data.get('product_id')
        quantity = cleaned_data.get('quantity')

        try:
            Dish.objects.get(pk=product_id)
        except (Dish.DoesNotExist, ValueError):
            raise forms.ValidationError(ERROR_MESSAGES['error_adding_item'])

        try:
            if 1 > quantity or quantity > 100:
                raise forms.ValidationError(ERROR_MESSAGES['error_adding_item'])
        except TypeError:
            raise forms.ValidationError(ERROR_MESSAGES['error_adding_item'])

        return cleaned_data
