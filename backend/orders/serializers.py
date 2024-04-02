from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, extend_schema_serializer, OpenApiExample

from .models import Order, OrderData
from .tasks import send_order_confirmation_mail

from products.models import Product

class OrderDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderData
        fields = ['product', 'quantity', 'product_price']
        read_only_fields = ['product_price',]

class OrderSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(source ='client.email', read_only = True)
    client_first_name = serializers.CharField(source = 'client.first_name', read_only = True)
    client_last_name = serializers.CharField(source = 'client.last_name', read_only = True)
    order_data = OrderDataSerializer(many=True)
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id',
            'created_at',
            'client',
            'client_email',
            'client_first_name',
            'client_last_name',
            'shipment_address',
            'payment_deadline',
            'order_total',
            'order_data',
        ]
        read_only_fields = [
            'created_at',
            'payment_deadline',
            'order_total',
        ]


    # creating OrderData related objects (product, price, quantity)
    def create(self, validated_data):
        order_items = validated_data.pop('order_data')
        order = Order.objects.create(**validated_data)
        for item in order_items:
            OrderData.objects.create(order=order, product_price=item['product'].price, **item)
        send_order_confirmation_mail.delay(order.client.email, order.created_at)
        return order



class TopSellers(serializers.ModelSerializer):

    product__name = serializers.CharField()
    sold = serializers.IntegerField()


    class Meta:
        model = OrderData
        fields = ('product__name', 'sold')


class ForceRemainder(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ('id', 'remainder_force', 'order_id')
        read_only_fields = ('id', 'remainder_force')