from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    stock = models.IntegerField()
    img_upload = models.ImageField(null=True, blank=False, upload_to="images/")
