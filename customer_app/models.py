from django.db import models

from django.db import models
class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=200)
    customer_address=models.CharField(max_length=250)
    customer_phoneNo=models.CharField(max_length=100)
    customer_password=models.CharField(max_length=100,unique=True)
    customer_username=models.CharField(max_length=200,unique=True)
    
    def __str__(self):
        return self.customer_name



class CartItem(models.Model):
    # ForeignKey to the Product model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 

    quantity = models.PositiveIntegerField(default=1)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Discounted price if any


    def total_price(self):
        """Calculate the total price for the item (quantity * price or discount price)."""
        return self.quantity * (self.discount_price if self.discount_price else self.price)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in cart for {self.customer.customer_username}"

    
    
    




