import pycountry
from django.db import models


class Shop(models.Model):
    name = models.CharField(blank=False, null=False, max_length=150, )
    tax_pin = models.CharField(max_length=50, )
    phone = models.CharField(blank=True, null=True, max_length=20, )
    email = models.CharField(max_length=200, blank=True, null=True, )


class PostalAddress(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    box = models.IntegerField(default=-1)
    code = models.IntegerField(default=-1)


class Location(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)

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


class Coordinates(Location):
    latitude = models.CharField(blank=True, null=True, max_length=50, )
    longitude = models.CharField(blank=True, null=True, max_length=50, )
    altitude = models.CharField(blank=True, null=True, max_length=50, )
