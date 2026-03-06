from django.db import models
from api1.models.products import Products

from user.models import User

class Order(models.Model):

    status_choice = [
        ('pending', 'pending'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name="order_product",null=True,blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    payment_method = models.CharField( max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=status_choice, default='pending')
    quantity = models.PositiveIntegerField(default=1)
    variant = models.CharField(max_length=300,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     variant = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot price

#     def __str__(self):
#         return f"{self.variant} - Qty: {self.quantity}"

