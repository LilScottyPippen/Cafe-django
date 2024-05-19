from django.contrib import admin
from index.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'uses', 'used')
