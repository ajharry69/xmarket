from django.db import models

from shop.models import Shop

PRODUCT_NAME_LENGTH = 255


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=PRODUCT_NAME_LENGTH, )
    unit_price = models.DecimalField(decimal_places=2, max_digits=20, )
    added_on = models.DateTimeField(auto_now_add=True, )
    updated_on = models.DateTimeField(auto_now=True, )

    class Meta:
        ordering = ('name', 'added_on', 'updated_on',)

    def __str__(self):
        return f'{self.name} @ {self.unit_price}/='


class Measurement(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, )
    quantity = models.FloatField(default=1, )
    unit = models.CharField(max_length=50, )

    def __str__(self):
        return f'{self.quantity}{self.unit}'
