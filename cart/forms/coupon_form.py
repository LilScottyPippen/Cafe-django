from django import forms
from index.models import Coupon
from utils.constants import ERROR_MESSAGES


class CouponForm(forms.Form):
    """
    Форма купона корзины.
    """
    code = forms.CharField()

    def clean(self):
        """
        Валидация полей формы.
        """
        cleaned_data = super().clean()
        coupon = cleaned_data.get('code')

        try:
            coupon = Coupon.objects.get(code=coupon)
        except (Coupon.DoesNotExist, ValueError):
            raise forms.ValidationError(ERROR_MESSAGES['error_dont_exist_coupon'])

        if coupon.used >= coupon.uses:
            raise forms.ValidationError(ERROR_MESSAGES['error_dont_exist_coupon'])

        return cleaned_data
