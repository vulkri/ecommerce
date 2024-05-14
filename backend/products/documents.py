from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Category, Product


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Category
        fields = [
            'id',
            'name'
        ]

# TODO: update Product.Category.name on Category.name change
@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
            "name": fields.TextField()
        })
    
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Product
        fields = [
            'id',
            'name',
            'description'
        ]