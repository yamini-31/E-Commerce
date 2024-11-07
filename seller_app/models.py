from django.db import models
from customer_app.models import Customer
from product_app.models import Product

class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)  
    email = models.EmailField(unique=True)  
    shop_address = models.CharField(max_length=255)  
    phone_number = models.CharField(max_length=15, unique=True)  
    username = models.CharField(max_length=50, unique=True)  
    password = models.CharField(max_length=128)  # Lengthy to store hashed passwords

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_bill = models.FloatField()

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()} - Customer {self.cust_id} - Product {self.product_id}"



