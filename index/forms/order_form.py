from django import forms
from index.models import Order, OrderItem
from utils.constants import ERROR_MESSAGES
from utils.is_valid_value import is_valid_phone, is_valid_name


class OrderForm(forms.ModelForm):
    """
    Форма модели Order.
    """
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        """
        Валидация полей формы.
        """
        cleaned_data = super().clean()
        client_name = cleaned_data.get('client_name')
        client_phone = cleaned_data.get('client_phone')

        if not is_valid_name(client_name):
            raise forms.ValidationError(ERROR_MESSAGES['invalid_name'])

        if not is_valid_phone(client_phone):
            raise forms.ValidationError(ERROR_MESSAGES['invalid_phone'])


class OrderItemForm(forms.ModelForm):
    """
    Форма модели OrderItem.
    """
    class Meta:
        model = OrderItem
        fields = '__all__'
