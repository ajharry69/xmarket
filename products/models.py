from django.db import models

from shop.models import Shop


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, )
    unit_price = models.DecimalField(decimal_places=2, max_digits=20, )


class Measurement(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1, )
    unit = models.CharField(max_length=50, )
