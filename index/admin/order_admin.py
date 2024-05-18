from django.contrib import admin

from index.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client_name', 'client_phone', 'client_mail', 'client_address', 'status', 'created_at')

    list_editable = ('client_name', 'client_phone', 'client_mail', 'client_address')

    inlines = [OrderItemInline]
