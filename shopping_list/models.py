from django.conf import settings
from django.db import models

from products.models import PRODUCT_NAME_LENGTH


class ShoppingList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=PRODUCT_NAME_LENGTH)
    created_on = models.DateTimeField(auto_now_add=True, )
    updated_on = models.DateTimeField(auto_now=True, )

    class Meta:
        ordering = ('item_name', 'created_on', 'updated_on',)


class Measurement(models.Model):
    quantity = models.FloatField(default=1, )
    unit = models.CharField(max_length=50, )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.quantity}{self.unit}'


class ProductMeasurement(Measurement):
    shopping_list = models.OneToOneField(ShoppingList, on_delete=models.CASCADE, )


class PurchaseMeasurement(Measurement):
    shopping_list = models.OneToOneField(ShoppingList, on_delete=models.CASCADE, )
