from django import forms
from index.models import Dish
from utils.constants import ERROR_MESSAGES


class BaseDishForm(forms.Form):
    """
    Базовая форма блюда корзины.
    """
    product_id = forms.CharField()

    def clean(self):
        """
        Валидация полей формы.
        """
        cleaned_data = super().clean()
        product_id = cleaned_data.get('product_id')

        try:
            Dish.objects.get(pk=product_id)
        except (Dish.DoesNotExist, ValueError):
            raise forms.ValidationError(ERROR_MESSAGES['error_adding_item'])

        return cleaned_data
