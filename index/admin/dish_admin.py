from django.contrib import admin

from index.models import Dish


@admin.register(Dish)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('title', 'catalog', 'price')
    list_editable = ('price',)
