from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'shop'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from shop import signals
