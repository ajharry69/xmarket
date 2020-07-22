import pycountry
from django.db import models
from rest_framework.reverse import reverse


class Shop(models.Model):
    name = models.CharField(blank=False, null=False, max_length=150, )
    tax_pin = models.CharField(max_length=50, )
    phone = models.CharField(blank=True, null=True, max_length=20, )
    email = models.CharField(max_length=200, blank=True, null=True, )
    added_on = models.DateTimeField(auto_now_add=True, )
    updated_on = models.DateTimeField(auto_now=True, )

    class Meta:
        ordering = ('name', 'added_on', 'updated_on',)

    def __str__(self):
        return self.name

    def get_products_url(self):
        return reverse('product-list', kwargs={'shop_id': self.id})


class PostalAddress(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, primary_key=True, )
    box = models.CharField(null=True, blank=True, max_length=20, )
    code = models.CharField(null=True, blank=True, max_length=20, )

    def __str__(self):
        return f'{self.box} - {self.code}'


class Location(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, primary_key=True, )

    class Meta:
        abstract = True


class PhysicalAddress(Location):
    __DEFAULT_COUNTRY = pycountry.countries.get(alpha_2='KE').name
    __COUNTRIES = [(c.name, c.name) for c in list(pycountry.countries)]
    country = models.CharField(
        choices=__COUNTRIES, default=__DEFAULT_COUNTRY,
        blank=True, null=True, max_length=100,
    )
    major_town = models.CharField(blank=True, null=True, max_length=100, )
    specific_town = models.CharField(blank=True, null=True, max_length=100, )
    street = models.CharField(blank=True, null=True, max_length=250, )

    def __str__(self):
        return f'{self.specific_town}, {self.major_town}, {self.country}'


class Coordinates(Location):
    latitude = models.FloatField(default=-1.288457, )
    longitude = models.FloatField(default=36.823103, )
    altitude = models.FloatField(default=0.0, )

    def __str__(self):
        return f'{self.latitude},{self.longitude}'
