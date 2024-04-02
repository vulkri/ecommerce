from django.contrib import admin

from .models import Order, OrderData

class OrderAdmin(admin.ModelAdmin):
    list_display = (
                'created_at',
                'client',
                'remainder_sent',
                'remainder_force',
                'order_total'
            )
    

class OrderDataAdmin(admin.ModelAdmin):
    list_display = (
                'order',
                'product',
                'quantity',
                'product_price'
            )

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderData, OrderDataAdmin)