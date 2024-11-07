from django.db import models

from product_app.models import Product
class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=200)
    customer_address=models.CharField(max_length=250)
    customer_phoneNo=models.CharField(max_length=100)
    customer_password=models.CharField(max_length=100)
    customer_username=models.CharField(max_length=200)
    
    def __str__(self):
        return self.customer_name



class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 

    quantity = models.PositiveIntegerField(default=1)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in cart for {self.customer.customer_username}"
