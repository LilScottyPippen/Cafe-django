from django.contrib import admin
from .models import *


admin.site.register(Catalog)
admin.site.register(Coupon)


@admin.register(Dish)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('title', 'catalog', 'price')
    list_editable = ('price',)
