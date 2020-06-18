from django.apps import AppConfig


class ReceiptConfig(AppConfig):
    name = 'receipt'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from receipt import signals
