from django.db import models

# Create your models here.
class Product(models.Model):
    prodname = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=2083)