from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# Create your models here.
class Item(models.Model):
    STATUS = (
        ("In cart", "In cart"),
        ("Order received", "Order received"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField(max_length=5)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default="In cart")
    img_url = models.CharField(max_length=2083)
