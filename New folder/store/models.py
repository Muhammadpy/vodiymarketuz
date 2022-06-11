from difflib import unified_diff
from distutils.command.upload import upload
from statistics import mode
from unicodedata import category
from django.db import models
from pandas import describe_option
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            =models.SlugField(max_length=200, unique=True)
    describtion     =models.TextField(max_length=500, blank=True)
    Price           =models.IntegerField()
    image           =models.ImageField(upload_to='photos/products')
    stock           =models.IntegerField()
    is_available    =models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   =models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_name

