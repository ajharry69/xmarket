import os
from hashlib import md5

from django.conf import settings
from django.db import models
from django.utils.datetime_safe import datetime


def user_receipt_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    owner_id = instance.owner.id
    encoded_id = f"{owner_id}".encode(encoding='utf8', errors='replace')
    encoded_timestamped_id = f"{owner_id}{datetime.utcnow().timestamp()}".encode(encoding='utf8', errors='replace')
    hashed_id = md5(encoded_id).hexdigest()
    hashed_timestamped_id = md5(encoded_timestamped_id).hexdigest()
    return os.path.join(f'receipts/{hashed_id}/', f"{hashed_timestamped_id}.{ext}")


class Receipt(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    receipt = models.ImageField(upload_to=user_receipt_upload_path)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-uploaded_on', '-updated_on',)
