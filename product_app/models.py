from django.db import models
from enum import Enum

class ProductCategory(Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    GROCERY = "Grocery"
    FURNITURE = "Furniture"
    TOYS = "Toys"

    @classmethod
    def choices(cls):
        return [(category.value, category.value) for category in cls]

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(
        max_length=50,
        choices=ProductCategory.choices(),
        default=ProductCategory.ELECTRONICS.value
    )
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller_id = models.IntegerField()
    product_quantity = models.IntegerField()
    product_description = models.TextField(blank=True)
    product_image = models.URLField(blank=True, default="https://img-b.udemycdn.com/course/750x422/6072899_3371_18.jpg")

    def __str__(self):
        return self.product_name
