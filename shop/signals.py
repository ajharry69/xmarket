from django.db.models.signals import post_save

from .models import LocationAddress


def on_location_address_post_save(sender, instance, created, **kwargs):
    """
    retrieve and update geographical coordinates on created
    """
    if created:
        pass


post_save.connect(on_location_address_post_save, LocationAddress, dispatch_uid='location_address01')
