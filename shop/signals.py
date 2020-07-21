from django.db.models.signals import post_save

from .models import Coordinates, PhysicalAddress


def on_physical_address_post_save(sender, instance, created, **kwargs):
    """
    retrieve and update geographical coordinates on created
    """
    if created:
        pass


def on_coordinates_post_save(sender, instance, created, **kwargs):
    """
    retrieve and update geographical coordinates on created
    """
    if created:
        pass


post_save.connect(on_physical_address_post_save, PhysicalAddress, dispatch_uid='physical_address01')
post_save.connect(on_coordinates_post_save, Coordinates, dispatch_uid='location_coordinates01')
