from django.db import models
from django.db.models import F
from thumbnails.fields import ImageField



class Category(models.Model):
    name = models.CharField(max_length=30)
    

class Product(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    photo = ImageField(upload_to='products/photos', pregenerated_sizes=["small"])
