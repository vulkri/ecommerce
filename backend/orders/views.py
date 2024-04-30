from typing import List
import dateutil.parser

from django.db.models import F, Sum
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, extend_schema_field
from rest_framework.schemas.openapi import AutoSchema

from .models import Order, OrderData
from .serializers import ForceRemainder, OrderSerializer, TopSellers

from products.models import Product
from users.permissions import IsClient, IsManager

class CreateOrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsClient]



# extend product schema by better descriptions
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='products_max', description='Maximum number of products to return', type=int),
            OpenApiParameter(name='date_min', description='Order created at minimum date.'),
            OpenApiParameter(name='date_max', description='Order created at maximum date.'),
        ]
    )
)
# I'd rather store orders in elastic stack for easier data exploration and visualizations
class TopSellersListAPIView(generics.ListAPIView):
    serializer_class = TopSellers
    permission_classes = [IsManager]
    queryset = Product.objects.none()

    def get_queryset(self):
        products_max = self.request.GET.get('products_max', None)
        date_min = self.request.GET.get('date_min', None)
        date_max = self.request.GET.get('date_max', None)
        if not (products_max and date_min and date_max):
            raise APIException('Provide required arguments: products_max (int), date_min, date_max.')
        date_max = dateutil.parser.parse(date_max)
        date_min = dateutil.parser.parse(date_min)
        if not products_max.isdigit():
            raise APIException('Provide required arguments: products_max (int).')
        orders = Order.objects.filter(created_at__date__gte=date_min, created_at__date__lte=date_max)
        qs = OrderData.objects.filter(order__in=orders).values('product','product__name').annotate(sold=Sum('quantity'))
        qs = qs.order_by('-sold')[:int(products_max)]
        return qs
    
# Force sending the payment remainder email - DEMO
class ForceRemainderAPIView(generics.GenericAPIView):
    serializer_class = ForceRemainder
    permission_classes = [IsManager]

    
    def patch(self, request, *args, **kwargs):
        qs = Order.objects.none()
        if 'order_id' in self.request.data:
            order_id = self.request.data['order_id']
            qs = Order.objects.filter(id=order_id)
            qs.update(remainder_force=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

