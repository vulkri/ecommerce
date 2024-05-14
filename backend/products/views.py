from rest_framework import filters, permissions, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from elasticsearch_dsl import Q

from users.permissions import IsManager

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .documents import CategoryDocument, ProductDocument



# extend category schema by better descriptions
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='ordering', description='Order by: name (reverse: "-").'),
            OpenApiParameter(name='search', description='Search in: name.'),
        ]
    )
)
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    
    # require Manager permissions for non-safe methods
    def get_permissions(self):
            self.permission_classes = [permissions.AllowAny]
            if self.request.method not in permissions.SAFE_METHODS:
                self.permission_classes = [IsManager]
            return super(CategoryViewSet, self).get_permissions()
    
    # override queryset - es fulltext search
    def get_queryset(self):
        qs = super().get_queryset()
        if 'search' in self.request.query_params.keys():
            query =  self.request.query_params['search']
            q = Q(
                'multi_match',
                query=query,
                fields=['name'],
                fuzziness='AUTO'
            )
            # return 30 items at max
            search = CategoryDocument.search().query(q)[:30]
            qs = search.to_queryset()
        return qs



# extend product schema by better descriptions
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='category', description='Filter by: category_id.', type=int),
            OpenApiParameter(name='price__gte', description='Price greater or equal.', type=float),
            OpenApiParameter(name='price__lte', description='Price less or equal.', type=float),
            OpenApiParameter(name='ordering', description='Order by: category.name, name, price (reverse: "-").'),
            OpenApiParameter(name='search', description='Search in: name, category.name, description.'),
            OpenApiParameter(name='photo', description='Photo file', type=OpenApiTypes.BYTE),
        ]
    )
)

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
         'category':['exact'], 
         'price':['gte', 'lte'],
    }
    ordering_fields = ['category__name', 'name', 'price']

    # require Manager permissions for non-safe methods
    def get_permissions(self):
            self.permission_classes = [permissions.AllowAny]
            if self.request.method not in permissions.SAFE_METHODS:
                self.permission_classes = [IsManager]
            return super(ProductViewSet, self).get_permissions()
    
    # override queryset - es fulltext search
    def get_queryset(self):
        qs = super().get_queryset()
        if 'search' in self.request.query_params.keys():
            query =  self.request.query_params['search']
            q = Q(
                'multi_match',
                query=query,
                fields=[
                     'name',
                     'description',
                     'category.name'
                ],
                fuzziness='AUTO'
            )
            # return 30 items at max
            search = ProductDocument.search().query(q)[:30]
            qs = search.to_queryset()
        return qs

    def destroy(self, request, *args, **kwargs):
         product = self.get_object()
         # do not allow product deletion if it's already sold
         if product.orderdata_set.all().count() > 0:
              raise serializers.ValidationError({"error": "product already sold"})
         product.delete()
         return Response()