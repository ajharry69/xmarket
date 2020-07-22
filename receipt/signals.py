import pytesseract
from django.db.models.signals import post_save

from .models import Receipt


def on_receipt_post_save(sender, instance, created, **kwargs):
    """
    extract shop and product details
    """
    pytesseract.pytesseract.tesseract_cmd = r''
    if created and isinstance(instance, Receipt):
        pass


post_save.connect(on_receipt_post_save, Receipt, dispatch_uid='reciept01')
