from django.conf import settings
from django.db import models


def user_receipt_upload_path(instance, filename):
    return f'receipts/{instance.owner.id}/{filename}'


class Receipt(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    receipt = models.ImageField(upload_to=user_receipt_upload_path)
