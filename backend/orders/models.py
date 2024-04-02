import datetime
from django.db import models
from django.db.models import F, Sum, Value
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(User, on_delete=models.PROTECT)
    shipment_address = models.TextField() # text field for simplicity - i'd opt for django-address
    payment_deadline = models.GeneratedField(
        expression=F('created_at') + datetime.timedelta(days=5),
        output_field=models.DateTimeField(),
        db_persist=True
    )
    remainder_sent = models.BooleanField(default=False)
    remainder_force = models.BooleanField(default=False)


    @property
    def order_total(self) -> float:
        ot = (self.order_data
              .values('product_price','quantity')
              .aggregate(order_total=Sum(F('product_price') * F('quantity'))))
        return ot['order_total']
    



class OrderData(models.Model):
    order = models.ForeignKey(Order, related_name='order_data', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    product_price = models.DecimalField(max_digits=9, decimal_places=2)